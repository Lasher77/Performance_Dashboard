import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class DocumentCategory(str, enum.Enum):
    LOHNSTEUERBESCHEINIGUNG = "LOHNSTEUERBESCHEINIGUNG"
    RENTENBESCHEINIGUNG = "RENTENBESCHEINIGUNG"
    VERSICHERUNG = "VERSICHERUNG"
    SPENDE = "SPENDE"
    HANDWERKER = "HANDWERKER"
    FAHRTKOSTEN = "FAHRTKOSTEN"
    MIETVERTRAG = "MIETVERTRAG"
    RECHNUNG = "RECHNUNG"
    SONSTIGES = "SONSTIGES"


class OCRStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Document(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "documents"

    tax_return_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_returns.id"), nullable=False
    )
    tax_section_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_sections.id"), nullable=True
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[DocumentCategory | None] = mapped_column(
        Enum(DocumentCategory), nullable=True
    )
    ocr_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocr_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ocr_status: Mapped[OCRStatus] = mapped_column(
        Enum(OCRStatus), nullable=False, default=OCRStatus.PENDING
    )

    tax_return = relationship("TaxReturn", back_populates="documents")
    tax_section = relationship("TaxSection", back_populates="documents")
