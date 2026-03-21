import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class SectionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSES = "EXPENSES"
    SPECIAL_EXPENSES = "SPECIAL_EXPENSES"
    RENTAL = "RENTAL"
    BUSINESS = "BUSINESS"
    EXTRAORDINARY_BURDENS = "EXTRAORDINARY_BURDENS"
    HOUSEHOLD_SERVICES = "HOUSEHOLD_SERVICES"
    RETIREMENT = "RETIREMENT"


class SectionStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaxSection(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tax_sections"

    tax_return_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_returns.id"), nullable=False
    )
    section_type: Mapped[SectionType] = mapped_column(Enum(SectionType), nullable=False)
    status: Mapped[SectionStatus] = mapped_column(
        Enum(SectionStatus), nullable=False, default=SectionStatus.NOT_STARTED
    )
    data: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    tax_return = relationship("TaxReturn", back_populates="sections")
    documents = relationship("Document", back_populates="tax_section")
    advisor_notes = relationship("AdvisorNote", back_populates="tax_section")
