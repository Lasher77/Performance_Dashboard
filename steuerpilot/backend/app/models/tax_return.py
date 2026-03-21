import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class TaxReturnStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    QUERY = "QUERY"
    APPROVED = "APPROVED"
    EXPORTED = "EXPORTED"


class TaxScenario(str, enum.Enum):
    EMPLOYED = "EMPLOYED"
    RETIREE = "RETIREE"
    LANDLORD = "LANDLORD"
    SELF_EMPLOYED = "SELF_EMPLOYED"


class TaxReturn(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tax_returns"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    tax_year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TaxReturnStatus] = mapped_column(
        Enum(TaxReturnStatus), nullable=False, default=TaxReturnStatus.DRAFT
    )
    assigned_advisor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    scenarios: Mapped[list[str] | None] = mapped_column(
        ARRAY(Enum(TaxScenario, create_constraint=False, native_enum=False)),
        nullable=True,
    )
    estimated_refund: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    tenant = relationship("Tenant", back_populates="tax_returns")
    user = relationship("User", back_populates="tax_returns", foreign_keys=[user_id])
    assigned_advisor = relationship(
        "User", back_populates="assigned_returns", foreign_keys=[assigned_advisor_id]
    )
    sections = relationship("TaxSection", back_populates="tax_return")
    documents = relationship("Document", back_populates="tax_return")
    messages = relationship("Message", back_populates="tax_return")
    calculations = relationship("Calculation", back_populates="tax_return")
    advisor_notes = relationship("AdvisorNote", back_populates="tax_return")
