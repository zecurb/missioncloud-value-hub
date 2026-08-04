import hashlib
import json
import os
import shutil
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import polars as pl

from missioncloud_value_hub.ingestion.azure import (
    curate_daily_service_costs,
    normalize_azure_costs,
    read_azure_export,
    write_parquet,
)
from missioncloud_value_hub.ingestion.contracts import (
    DatasetLayer,
    IngestionArtifact,
    IngestionResult,
    IngestionStatus,
    ReconciliationResult,
)
from missioncloud_value_hub.ingestion.reconciliation import (
    reconcile_layers,
)


@dataclass(frozen=True, slots=True)
class _OutputPaths:
    raw: Path
    normalized: Path
    curated: Path
    manifest: Path
    failure: Path


def _sha256_file(source_path: Path) -> str:
    digest = hashlib.sha256()

    with source_path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _output_paths(
    output_root: Path,
    source_digest: str,
) -> _OutputPaths:
    return _OutputPaths(
        raw=(output_root / DatasetLayer.RAW / source_digest / "azure_cost_export.csv"),
        normalized=(output_root / DatasetLayer.NORMALIZED / source_digest / "cost_records.parquet"),
        curated=(
            output_root / DatasetLayer.CURATED / source_digest / "daily_service_costs.parquet"
        ),
        manifest=output_root / "manifests" / f"{source_digest}.json",
        failure=output_root / "failures" / f"{source_digest}.json",
    )


def _artifact_row_count(path: Path) -> int:
    if path.suffix == ".csv":
        return int(pl.scan_csv(path).select(pl.len()).collect().item())

    return int(pl.scan_parquet(path).select(pl.len()).collect().item())


def _artifacts(paths: _OutputPaths) -> tuple[IngestionArtifact, ...]:
    return (
        IngestionArtifact(
            layer=DatasetLayer.RAW,
            path=paths.raw,
            row_count=_artifact_row_count(paths.raw),
        ),
        IngestionArtifact(
            layer=DatasetLayer.NORMALIZED,
            path=paths.normalized,
            row_count=_artifact_row_count(paths.normalized),
        ),
        IngestionArtifact(
            layer=DatasetLayer.CURATED,
            path=paths.curated,
            row_count=_artifact_row_count(paths.curated),
        ),
    )


def _write_json_atomically(
    destination: Path,
    payload: dict[str, object],
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")

    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, destination)


def _replace_directory(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        shutil.rmtree(destination)

    os.replace(source, destination)


def _manifest_payload(
    source_path: Path,
    source_digest: str,
    attempts: int,
    artifacts: tuple[IngestionArtifact, ...],
    reconciliation: ReconciliationResult,
) -> dict[str, object]:
    return {
        "source_file": source_path.name,
        "source_digest": source_digest,
        "status": IngestionStatus.SUCCEEDED,
        "attempts": attempts,
        "completed_at": datetime.now(UTC).isoformat(),
        "artifacts": [
            {
                "layer": artifact.layer,
                "path": str(artifact.path),
                "row_count": artifact.row_count,
            }
            for artifact in artifacts
        ],
        "reconciliation": {
            "raw_row_count": reconciliation.raw_row_count,
            "normalized_row_count": (reconciliation.normalized_row_count),
            "curated_row_count": reconciliation.curated_row_count,
            "raw_total_micros": reconciliation.raw_total_micros,
            "normalized_total_micros": (reconciliation.normalized_total_micros),
            "curated_total_micros": (reconciliation.curated_total_micros),
            "balanced": reconciliation.balanced,
        },
    }


def _failure_payload(
    source_path: Path,
    source_digest: str,
    attempts: int,
    error: Exception,
) -> dict[str, object]:
    return {
        "source_file": source_path.name,
        "source_digest": source_digest,
        "status": "failed",
        "attempts": attempts,
        "failed_at": datetime.now(UTC).isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
    }


def _completed_result(
    source_digest: str,
    paths: _OutputPaths,
) -> IngestionResult | None:
    required_paths = (
        paths.manifest,
        paths.raw,
        paths.normalized,
        paths.curated,
    )

    if not all(path.exists() for path in required_paths):
        return None

    reconciliation = reconcile_layers(
        paths.raw,
        paths.normalized,
        paths.curated,
    )

    return IngestionResult(
        source_digest=source_digest,
        status=IngestionStatus.SKIPPED,
        attempts=0,
        artifacts=_artifacts(paths),
        reconciliation=reconciliation,
    )


def _run_once(
    source_path: Path,
    output_root: Path,
    source_digest: str,
    paths: _OutputPaths,
    attempt: int,
) -> IngestionResult:
    staging_parent = output_root / ".staging"
    staging_parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(
        prefix=f"{source_digest}-",
        dir=staging_parent,
    ) as temporary_directory:
        staging_root = Path(temporary_directory)

        staged_raw = staging_root / DatasetLayer.RAW / "azure_cost_export.csv"
        staged_normalized = staging_root / DatasetLayer.NORMALIZED / "cost_records.parquet"
        staged_curated = staging_root / DatasetLayer.CURATED / "daily_service_costs.parquet"

        staged_raw.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, staged_raw)

        raw_frame = read_azure_export(staged_raw)
        normalized_frame = normalize_azure_costs(raw_frame)
        curated_frame = curate_daily_service_costs(normalized_frame)

        write_parquet(normalized_frame, staged_normalized)
        write_parquet(curated_frame, staged_curated)

        reconciliation = reconcile_layers(
            staged_raw,
            staged_normalized,
            staged_curated,
        )

        _replace_directory(
            staged_raw.parent,
            paths.raw.parent,
        )
        _replace_directory(
            staged_normalized.parent,
            paths.normalized.parent,
        )
        _replace_directory(
            staged_curated.parent,
            paths.curated.parent,
        )

    artifacts = _artifacts(paths)

    _write_json_atomically(
        paths.manifest,
        _manifest_payload(
            source_path=source_path,
            source_digest=source_digest,
            attempts=attempt,
            artifacts=artifacts,
            reconciliation=reconciliation,
        ),
    )

    paths.failure.unlink(missing_ok=True)

    return IngestionResult(
        source_digest=source_digest,
        status=IngestionStatus.SUCCEEDED,
        attempts=attempt,
        artifacts=artifacts,
        reconciliation=reconciliation,
    )


def run_azure_ingestion(
    source_path: Path,
    output_root: Path,
    *,
    max_attempts: int = 3,
    retry_delay_seconds: float = 0.0,
) -> IngestionResult:
    """Run an idempotent fictional Azure cost-ingestion job."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1.")

    source_path = source_path.resolve(strict=True)
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    source_digest = _sha256_file(source_path)
    paths = _output_paths(output_root, source_digest)

    completed = _completed_result(source_digest, paths)

    if completed is not None:
        return completed

    for attempt in range(1, max_attempts + 1):
        try:
            return _run_once(
                source_path=source_path,
                output_root=output_root,
                source_digest=source_digest,
                paths=paths,
                attempt=attempt,
            )
        except Exception as error:
            if attempt == max_attempts:
                _write_json_atomically(
                    paths.failure,
                    _failure_payload(
                        source_path=source_path,
                        source_digest=source_digest,
                        attempts=attempt,
                        error=error,
                    ),
                )
                raise

            if retry_delay_seconds > 0:
                time.sleep(retry_delay_seconds)

    raise AssertionError("Ingestion retry loop terminated unexpectedly.")
