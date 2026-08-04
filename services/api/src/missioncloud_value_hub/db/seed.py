from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from missioncloud_value_hub.db.models import (
    AppUser,
    AuditEvent,
    BusinessUnit,
    CloudAccount,
    CloudService,
    Organization,
    Role,
    Team,
    UserRole,
)
from missioncloud_value_hub.db.session import session_factory

DEMO_ORGANIZATION_SLUG = "missioncloud-demo"


@dataclass(frozen=True, slots=True)
class SeedResult:
    """Result returned by the idempotent tenant seed operation."""

    organization_id: UUID
    created: bool


def seed_demo_tenant(session: Session) -> SeedResult:
    """Create the demonstration tenant unless it already exists."""

    with session.begin():
        existing = session.scalar(
            select(Organization).where(Organization.slug == DEMO_ORGANIZATION_SLUG)
        )

        if existing is not None:
            return SeedResult(
                organization_id=existing.id,
                created=False,
            )

        organization = Organization(
            slug=DEMO_ORGANIZATION_SLUG,
            name="MissionCloud Demo",
        )
        session.add(organization)
        session.flush()

        business_unit = BusinessUnit(
            organization_id=organization.id,
            slug="digital-platforms",
            name="Digital Platforms",
        )
        session.add(business_unit)
        session.flush()

        team = Team(
            organization_id=organization.id,
            business_unit_id=business_unit.id,
            slug="cloud-finops",
            name="Cloud FinOps",
        )

        cloud_account = CloudAccount(
            organization_id=organization.id,
            business_unit_id=business_unit.id,
            provider="aws",
            external_account_id="123456789012",
            name="MissionCloud Production",
        )

        session.add_all([team, cloud_account])
        session.flush()

        cloud_service = CloudService(
            organization_id=organization.id,
            team_id=team.id,
            slug="value-hub",
            name="MissionCloud Value Hub",
        )

        user = AppUser(
            organization_id=organization.id,
            email="finops.admin@missioncloud.example",
            display_name="FinOps Administrator",
        )

        role = Role(
            organization_id=organization.id,
            name="finops-admin",
            description="Full tenant-level FinOps administration access.",
        )

        session.add_all([cloud_service, user, role])
        session.flush()

        assignment = UserRole(
            user_id=user.id,
            role_id=role.id,
        )

        audit_event = AuditEvent(
            organization_id=organization.id,
            actor_user_id=user.id,
            action="tenant.seeded",
            entity_type="organization",
            entity_id=organization.id,
            details={
                "source": "development-seed",
                "organization_slug": organization.slug,
            },
        )

        session.add_all([assignment, audit_event])

    return SeedResult(
        organization_id=organization.id,
        created=True,
    )


def main() -> None:
    """Seed the configured database and print the operation result."""

    with session_factory() as session:
        result = seed_demo_tenant(session)

    status = "created" if result.created else "already exists"
    print(f"Demo tenant {status}: {DEMO_ORGANIZATION_SLUG} ({result.organization_id})")


if __name__ == "__main__":
    main()
