from decimal import Decimal
from pathlib import Path
from typing import cast

import duckdb

from missioncloud_value_hub.ingestion.contracts import (
    ReconciliationResult,
)


class ReconciliationError(RuntimeError):
    """Raised when materialized ingestion layers do not reconcile."""


def _quoted_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def reconcile_layers(
    raw_path: Path,
    normalized_path: Path,
    curated_path: Path,
) -> ReconciliationResult:
    """Reconcile row counts and monetary totals with DuckDB."""

    raw_sql = f"""
        SELECT
            COUNT(*) AS row_count,
            COALESCE(
                SUM(
                    CAST(
                        CostInBillingCurrency
                        AS DECIMAL(38, 6)
                    )
                ),
                0
            ) AS total_cost
        FROM read_csv_auto(
            '{_quoted_path(raw_path)}',
            header = true,
            all_varchar = true
        )
    """

    normalized_sql = f"""
        SELECT
            COUNT(*) AS row_count,
            COALESCE(SUM(cost_micros), 0) AS total_micros
        FROM read_parquet('{_quoted_path(normalized_path)}')
    """

    curated_sql = f"""
        SELECT
            COUNT(*) AS row_count,
            COALESCE(SUM(cost_micros), 0) AS total_micros
        FROM read_parquet('{_quoted_path(curated_path)}')
    """

    with duckdb.connect(":memory:") as connection:
        raw_row = cast(
            tuple[object, object] | None,
            connection.execute(raw_sql).fetchone(),
        )
        normalized_row = cast(
            tuple[object, object] | None,
            connection.execute(normalized_sql).fetchone(),
        )
        curated_row = cast(
            tuple[object, object] | None,
            connection.execute(curated_sql).fetchone(),
        )

    if raw_row is None:
        raise ReconciliationError("Raw reconciliation returned no result.")

    if normalized_row is None:
        raise ReconciliationError("Normalized reconciliation returned no result.")

    if curated_row is None:
        raise ReconciliationError("Curated reconciliation returned no result.")

    result = ReconciliationResult(
        raw_row_count=int(str(raw_row[0])),
        normalized_row_count=int(str(normalized_row[0])),
        curated_row_count=int(str(curated_row[0])),
        raw_total_micros=int(Decimal(str(raw_row[1])) * Decimal("1000000")),
        normalized_total_micros=int(str(normalized_row[1])),
        curated_total_micros=int(str(curated_row[1])),
    )

    if not result.balanced:
        raise ReconciliationError(
            "Ingestion reconciliation failed: "
            f"raw_rows={result.raw_row_count}, "
            f"normalized_rows={result.normalized_row_count}, "
            f"raw_total_micros={result.raw_total_micros}, "
            f"normalized_total_micros="
            f"{result.normalized_total_micros}, "
            f"curated_total_micros={result.curated_total_micros}"
        )

    return result
