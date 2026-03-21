from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class Tenant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    branding: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    settings: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    datev_config: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    users = relationship("User", back_populates="tenant")
    tax_returns = relationship("TaxReturn", back_populates="tenant")
