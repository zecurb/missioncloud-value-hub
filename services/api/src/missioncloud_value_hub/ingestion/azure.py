from decimal import Decimal, InvalidOperation
from pathlib import Path

import polars as pl
import pyarrow.parquet as parquet

REQUIRED_AZURE_COLUMNS = (
    "UsageDate",
    "BillingAccountId",
    "SubscriptionId",
    "ResourceGroup",
    "ResourceId",
    "ServiceName",
    "MeterCategory",
    "ResourceLocation",
    "BillingCurrencyCode",
    "CostInBillingCurrency",
)

_MICROS_PER_UNIT = Decimal("1000000")


class AzureExportError(ValueError):
    """Raised when a fictional Azure cost export is invalid."""


def _to_cost_micros(value: str) -> int:
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise AzureExportError(f"Invalid CostInBillingCurrency value: {value!r}") from error

    micros = amount * _MICROS_PER_UNIT

    if micros != micros.to_integral_value():
        raise AzureExportError(
            f"CostInBillingCurrency supports at most six decimal places: {value!r}"
        )

    return int(micros)


def read_azure_export(source_path: Path) -> pl.DataFrame:
    """Read and minimally validate a fictional Azure cost CSV export."""

    if not source_path.is_file():
        raise AzureExportError(f"Azure export does not exist: {source_path}")

    frame = pl.read_csv(
        source_path,
        schema_overrides={column: pl.String for column in REQUIRED_AZURE_COLUMNS},
    )

    missing = sorted(set(REQUIRED_AZURE_COLUMNS) - set(frame.columns))

    if missing:
        raise AzureExportError("Azure export is missing required columns: " + ", ".join(missing))

    return frame.with_row_index(
        name="source_row_number",
        offset=1,
    ).with_columns(
        pl.lit(source_path.name).alias("source_file"),
    )


def normalize_azure_costs(raw: pl.DataFrame) -> pl.DataFrame:
    """Transform Azure-specific columns into a provider-neutral schema."""

    return raw.select(
        pl.col("UsageDate").str.strptime(pl.Date, "%Y-%m-%d", strict=True).alias("usage_date"),
        pl.col("BillingAccountId").str.strip_chars().alias("billing_account_id"),
        pl.col("SubscriptionId").str.strip_chars().alias("cloud_account_id"),
        pl.col("ResourceGroup").fill_null("").str.strip_chars().alias("resource_group"),
        pl.col("ResourceId").str.strip_chars().alias("resource_id"),
        pl.col("ServiceName").str.strip_chars().alias("service_name"),
        pl.col("MeterCategory").str.strip_chars().alias("meter_category"),
        pl.col("ResourceLocation").fill_null("global").str.strip_chars().alias("region"),
        pl.col("BillingCurrencyCode").str.strip_chars().str.to_uppercase().alias("currency"),
        pl.col("CostInBillingCurrency")
        .map_elements(
            _to_cost_micros,
            return_dtype=pl.Int64,
        )
        .alias("cost_micros"),
        pl.lit("azure").alias("provider"),
        pl.col("source_file"),
        pl.col("source_row_number").cast(pl.UInt64),
    ).sort(
        ["usage_date", "source_row_number"],
    )


def curate_daily_service_costs(
    normalized: pl.DataFrame,
) -> pl.DataFrame:
    """Aggregate normalized line items by day, service, and currency."""

    return (
        normalized.group_by(
            [
                "usage_date",
                "service_name",
                "meter_category",
                "currency",
            ]
        )
        .agg(
            pl.sum("cost_micros").alias("cost_micros"),
            pl.len().alias("line_item_count"),
        )
        .sort(
            [
                "usage_date",
                "service_name",
                "meter_category",
                "currency",
            ]
        )
    )


def write_parquet(
    frame: pl.DataFrame,
    destination: Path,
) -> None:
    """Write a Polars frame through PyArrow using Zstandard compression."""

    destination.parent.mkdir(parents=True, exist_ok=True)

    parquet.write_table(
        frame.to_arrow(),
        destination,
        compression="zstd",
    )
