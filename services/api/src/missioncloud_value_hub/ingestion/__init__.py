"""Cloud-cost ingestion and normalization pipelines."""

from missioncloud_value_hub.ingestion.pipeline import run_azure_ingestion

__all__ = ["run_azure_ingestion"]
