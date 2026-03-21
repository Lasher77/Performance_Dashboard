import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class ReferenceType(str, enum.Enum):
    FIELD = "FIELD"
    DOCUMENT = "DOCUMENT"
    GENERAL = "GENERAL"


class Message(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "messages"

    tax_return_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_returns.id"), nullable=False
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    reference_type: Mapped[ReferenceType] = mapped_column(
        Enum(ReferenceType), nullable=False, default=ReferenceType.GENERAL
    )
    reference_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    tax_return = relationship("TaxReturn", back_populates="messages")
    sender = relationship("User", back_populates="messages")
