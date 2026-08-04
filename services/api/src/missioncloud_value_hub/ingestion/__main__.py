import argparse
import json
from pathlib import Path

from missioncloud_value_hub.ingestion.pipeline import (
    run_azure_ingestion,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Ingest a fictional Azure cost export into raw, normalized, and curated layers."
        )
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to the Azure cost-export CSV.",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Root directory for materialized datasets.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=3,
    )
    return parser


def main() -> None:
    """Run the Azure ingestion command."""

    arguments = _parser().parse_args()

    result = run_azure_ingestion(
        source_path=arguments.source,
        output_root=arguments.output,
        max_attempts=arguments.max_attempts,
    )

    print(
        json.dumps(
            {
                "source_digest": result.source_digest,
                "status": result.status,
                "attempts": result.attempts,
                "balanced": result.reconciliation.balanced,
                "artifacts": [
                    {
                        "layer": artifact.layer,
                        "path": str(artifact.path),
                        "row_count": artifact.row_count,
                    }
                    for artifact in result.artifacts
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
