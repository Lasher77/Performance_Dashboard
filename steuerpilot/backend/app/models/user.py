import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class UserRole(str, enum.Enum):
    MANDANT = "MANDANT"
    STEUERBERATER = "STEUERBERATER"
    ADMIN = "ADMIN"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.MANDANT)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(20), nullable=True)

    tenant = relationship("Tenant", back_populates="users")
    tax_returns = relationship("TaxReturn", back_populates="user", foreign_keys="TaxReturn.user_id")
    assigned_returns = relationship(
        "TaxReturn", back_populates="assigned_advisor", foreign_keys="TaxReturn.assigned_advisor_id"
    )
    messages = relationship("Message", back_populates="sender")
