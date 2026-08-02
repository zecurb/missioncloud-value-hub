from fastapi import APIRouter

from missioncloud_value_hub.domain.demo_data import (
    get_demo_opportunities,
    get_demo_value_summary,
)
from missioncloud_value_hub.domain.models import OptimizationOpportunity, ValueSummary

router = APIRouter(prefix="/value", tags=["value"])


@router.get("/summary", response_model=ValueSummary)
def value_summary() -> ValueSummary:
    """Return the executive FinOps value summary for the active reporting period."""
    return get_demo_value_summary()


@router.get("/opportunities", response_model=list[OptimizationOpportunity])
def optimization_opportunities() -> list[OptimizationOpportunity]:
    """Return ranked optimization opportunities for the demo tenant."""
    return get_demo_opportunities()
