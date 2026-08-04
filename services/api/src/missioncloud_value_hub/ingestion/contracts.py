from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class DatasetLayer(StrEnum):
    """Dataset maturity layers produced by an ingestion run."""

    RAW = "raw"
    NORMALIZED = "normalized"
    CURATED = "curated"


class IngestionStatus(StrEnum):
    """Terminal status returned by an ingestion invocation."""

    SUCCEEDED = "succeeded"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class IngestionArtifact:
    """One materialized dataset produced by an ingestion run."""

    layer: DatasetLayer
    path: Path
    row_count: int


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    """Cross-layer row-count and monetary reconciliation results."""

    raw_row_count: int
    normalized_row_count: int
    curated_row_count: int
    raw_total_micros: int
    normalized_total_micros: int
    curated_total_micros: int

    @property
    def balanced(self) -> bool:
        """Return whether row counts and monetary totals reconcile."""

        return (
            self.raw_row_count == self.normalized_row_count
            and self.raw_total_micros == self.normalized_total_micros == self.curated_total_micros
        )


@dataclass(frozen=True, slots=True)
class IngestionResult:
    """Result returned after processing or skipping one source file."""

    source_digest: str
    status: IngestionStatus
    attempts: int
    artifacts: tuple[IngestionArtifact, ...]
    reconciliation: ReconciliationResult
