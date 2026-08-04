from datetime import date
from decimal import Decimal

from missioncloud_value_hub.domain.models import (
    Money,
    OpportunityCategory,
    OpportunityStatus,
    OptimizationOpportunity,
    ValueSummary,
)


def get_demo_value_summary() -> ValueSummary:
    return ValueSummary(
        period_start=date(2026, 7, 1),
        period_end=date(2026, 7, 31),
        total_cloud_spend=Money(amount=Decimal("184250.00")),
        budget_variance_percent=Decimal("3.8"),
        identified_annual_savings=Money(amount=Decimal("428400.00")),
        realized_monthly_savings=Money(amount=Decimal("27650.00")),
        optimization_coverage_percent=Decimal("81.4"),
        allocation_coverage_percent=Decimal("94.7"),
        policy_compliance_percent=Decimal("91.2"),
        open_opportunities=18,
    )


def get_demo_opportunities() -> list[OptimizationOpportunity]:
    return [
        OptimizationOpportunity(
            id="opp-001",
            title="Rightsize analytics compute pool",
            category=OpportunityCategory.RIGHTSIZING,
            owner_team="Data Platform",
            service="Azure Virtual Machines",
            account_name="prod-data-platform",
            estimated_monthly_savings=Money(amount=Decimal("12400.00")),
            confidence_percent=94,
            effort="medium",
            risk="low",
            status=OpportunityStatus.APPROVED,
            rationale=(
                "Thirty-day CPU and memory utilization remain below the selected SKU baseline."
            ),
        ),
        OptimizationOpportunity(
            id="opp-002",
            title="Purchase database reserved capacity",
            category=OpportunityCategory.COMMITMENT,
            owner_team="Commerce Platform",
            service="Azure SQL Database",
            account_name="prod-commerce",
            estimated_monthly_savings=Money(amount=Decimal("8700.00")),
            confidence_percent=89,
            effort="low",
            risk="medium",
            status=OpportunityStatus.VALIDATING,
            rationale=(
                "Stable twelve-month baseline supports a one-year commitment after growth review."
            ),
        ),
        OptimizationOpportunity(
            id="opp-003",
            title="Delete unattached managed disks",
            category=OpportunityCategory.IDLE_RESOURCE,
            owner_team="Cloud Operations",
            service="Azure Managed Disks",
            account_name="shared-services",
            estimated_monthly_savings=Money(amount=Decimal("4150.00")),
            confidence_percent=98,
            effort="low",
            risk="low",
            status=OpportunityStatus.NEW,
            rationale=(
                "Disks have been unattached for more than forty-five days "
                "and have no active exception."
            ),
        ),
        OptimizationOpportunity(
            id="opp-004",
            title="Apply lifecycle policy to diagnostic logs",
            category=OpportunityCategory.STORAGE,
            owner_team="Security Engineering",
            service="Azure Blob Storage",
            account_name="security-logging",
            estimated_monthly_savings=Money(amount=Decimal("2380.00")),
            confidence_percent=86,
            effort="medium",
            risk="low",
            status=OpportunityStatus.IN_PROGRESS,
            rationale="Retention exceeds policy requirements for low-access diagnostic data.",
        ),
    ]
