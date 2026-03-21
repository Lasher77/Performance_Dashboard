import uuid

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class Calculation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "calculations"

    tax_return_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_returns.id"), nullable=False
    )
    input_data: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    result_data: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    estimated_refund: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    tax_return = relationship("TaxReturn", back_populates="calculations")
