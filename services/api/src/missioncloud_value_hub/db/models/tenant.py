from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from missioncloud_value_hub.db.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Top-level customer or enterprise tenant."""

    __tablename__ = "organizations"

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class BusinessUnit(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Organizational cost and ownership boundary."""

    __tablename__ = "business_units"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "slug",
            name="uq_business_units_organization_slug",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Team(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Engineering or operational team responsible for cloud resources."""

    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "slug",
            name="uq_teams_organization_slug",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("business_units.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class CloudAccount(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Cloud-provider billing account, subscription, or project."""

    __tablename__ = "cloud_accounts"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "provider",
            "external_account_id",
            name="uq_cloud_accounts_org_provider_external",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("business_units.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    external_account_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )


class CloudService(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Business-facing service or workload consuming cloud resources."""

    __tablename__ = "cloud_services"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "slug",
            name="uq_cloud_services_organization_slug",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class AppUser(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tenant-scoped application user."""

    __tablename__ = "app_users"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "email",
            name="uq_app_users_organization_email",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )


class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tenant-scoped authorization role."""

    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "name",
            name="uq_roles_organization_name",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )


class UserRole(Base):
    """Assignment of a role to an application user."""

    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("app_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
