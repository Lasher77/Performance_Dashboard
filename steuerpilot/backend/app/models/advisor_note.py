import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class AdvisorNote(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "advisor_notes"

    tax_return_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_returns.id"), nullable=False
    )
    tax_section_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_sections.id"), nullable=True
    )
    field_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    correction_value: Mapped[str | None] = mapped_column(Text, nullable=True)

    tax_return = relationship("TaxReturn", back_populates="advisor_notes")
    tax_section = relationship("TaxSection", back_populates="advisor_notes")
