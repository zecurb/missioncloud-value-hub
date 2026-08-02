from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class OpportunityStatus(StrEnum):
    NEW = "new"
    VALIDATING = "validating"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    REALIZED = "realized"
    DISMISSED = "dismissed"


class OpportunityCategory(StrEnum):
    RIGHTSIZING = "rightsizing"
    COMMITMENT = "commitment"
    IDLE_RESOURCE = "idle_resource"
    STORAGE = "storage"
    SCHEDULING = "scheduling"
    ARCHITECTURE = "architecture"


class Money(BaseModel):
    model_config = ConfigDict(frozen=True)

    amount: Decimal = Field(ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class ValueSummary(BaseModel):
    period_start: date
    period_end: date
    total_cloud_spend: Money
    budget_variance_percent: Decimal
    identified_annual_savings: Money
    realized_monthly_savings: Money
    optimization_coverage_percent: Decimal = Field(ge=0, le=100)
    allocation_coverage_percent: Decimal = Field(ge=0, le=100)
    policy_compliance_percent: Decimal = Field(ge=0, le=100)
    open_opportunities: int = Field(ge=0)


class OptimizationOpportunity(BaseModel):
    id: str
    title: str
    category: OpportunityCategory
    owner_team: str
    service: str
    account_name: str
    estimated_monthly_savings: Money
    confidence_percent: int = Field(ge=0, le=100)
    effort: str
    risk: str
    status: OpportunityStatus
    rationale: str
