import hashlib
import json
from pathlib import Path

import polars as pl
import pytest

from missioncloud_value_hub.ingestion.azure import (
    AzureExportError,
)
from missioncloud_value_hub.ingestion.contracts import (
    DatasetLayer,
    IngestionStatus,
)
from missioncloud_value_hub.ingestion.pipeline import (
    run_azure_ingestion,
)

FIXTURE = Path(__file__).parent / "fixtures" / "azure_cost_export.csv"


def test_azure_pipeline_materializes_and_skips_duplicate(
    tmp_path: Path,
) -> None:
    first = run_azure_ingestion(
        source_path=FIXTURE,
        output_root=tmp_path,
    )
    second = run_azure_ingestion(
        source_path=FIXTURE,
        output_root=tmp_path,
    )

    assert first.status is IngestionStatus.SUCCEEDED
    assert first.attempts == 1
    assert second.status is IngestionStatus.SKIPPED
    assert second.attempts == 0
    assert first.source_digest == second.source_digest
    assert first.reconciliation.balanced is True

    artifacts = {artifact.layer: artifact for artifact in first.artifacts}

    assert artifacts[DatasetLayer.RAW].row_count == 5
    assert artifacts[DatasetLayer.NORMALIZED].row_count == 5
    assert artifacts[DatasetLayer.CURATED].row_count == 4

    normalized = pl.read_parquet(artifacts[DatasetLayer.NORMALIZED].path)
    curated = pl.read_parquet(artifacts[DatasetLayer.CURATED].path)

    assert normalized["cost_micros"].sum() == 6_500_000
    assert curated["cost_micros"].sum() == 6_500_000

    manifest = tmp_path / "manifests" / f"{first.source_digest}.json"

    assert manifest.is_file()


def test_invalid_export_retries_and_writes_failure_report(
    tmp_path: Path,
) -> None:
    invalid_export = tmp_path / "invalid.csv"
    invalid_export.write_text("UsageDate\n2026-07-01\n")

    output_root = tmp_path / "output"

    with pytest.raises(AzureExportError):
        run_azure_ingestion(
            source_path=invalid_export,
            output_root=output_root,
            max_attempts=2,
        )

    digest = hashlib.sha256(invalid_export.read_bytes()).hexdigest()

    failure_path = output_root / "failures" / f"{digest}.json"

    payload = json.loads(failure_path.read_text())

    assert payload["status"] == "failed"
    assert payload["attempts"] == 2
    assert payload["error_type"] == "AzureExportError"
