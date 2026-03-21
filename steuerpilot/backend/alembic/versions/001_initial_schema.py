"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enums
    userrole = postgresql.ENUM("MANDANT", "STEUERBERATER", "ADMIN", name="userrole", create_type=True)
    taxreturnstatus = postgresql.ENUM(
        "DRAFT", "SUBMITTED", "IN_REVIEW", "QUERY", "APPROVED", "EXPORTED",
        name="taxreturnstatus", create_type=True,
    )
    sectiontype = postgresql.ENUM(
        "INCOME", "EXPENSES", "SPECIAL_EXPENSES", "RENTAL", "BUSINESS",
        "EXTRAORDINARY_BURDENS", "HOUSEHOLD_SERVICES", "RETIREMENT",
        name="sectiontype", create_type=True,
    )
    sectionstatus = postgresql.ENUM(
        "NOT_STARTED", "IN_PROGRESS", "COMPLETED",
        name="sectionstatus", create_type=True,
    )
    documentcategory = postgresql.ENUM(
        "LOHNSTEUERBESCHEINIGUNG", "RENTENBESCHEINIGUNG", "VERSICHERUNG",
        "SPENDE", "HANDWERKER", "FAHRTKOSTEN", "MIETVERTRAG", "RECHNUNG", "SONSTIGES",
        name="documentcategory", create_type=True,
    )
    ocrstatus = postgresql.ENUM(
        "PENDING", "PROCESSING", "COMPLETED", "FAILED",
        name="ocrstatus", create_type=True,
    )
    referencetype = postgresql.ENUM(
        "FIELD", "DOCUMENT", "GENERAL",
        name="referencetype", create_type=True,
    )

    # Tenants
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("branding", postgresql.JSONB, server_default="{}"),
        sa.Column("settings", postgresql.JSONB, server_default="{}"),
        sa.Column("datev_config", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", userrole, nullable=False, server_default="MANDANT"),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("tax_id", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Tax Returns
    op.create_table(
        "tax_returns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("tax_year", sa.Integer, nullable=False),
        sa.Column("status", taxreturnstatus, nullable=False, server_default="DRAFT"),
        sa.Column("assigned_advisor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("scenarios", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("estimated_refund", sa.Numeric(12, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Tax Sections
    op.create_table(
        "tax_sections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tax_return_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_returns.id"), nullable=False),
        sa.Column("section_type", sectiontype, nullable=False),
        sa.Column("status", sectionstatus, nullable=False, server_default="NOT_STARTED"),
        sa.Column("data", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Documents
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tax_return_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_returns.id"), nullable=False),
        sa.Column("tax_section_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_sections.id"), nullable=True),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("file_type", sa.String(50), nullable=False),
        sa.Column("category", documentcategory, nullable=True),
        sa.Column("ocr_text", sa.Text, nullable=True),
        sa.Column("ocr_data", postgresql.JSONB, nullable=True),
        sa.Column("ocr_status", ocrstatus, nullable=False, server_default="PENDING"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Messages
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tax_return_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_returns.id"), nullable=False),
        sa.Column("sender_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("reference_type", referencetype, nullable=False, server_default="GENERAL"),
        sa.Column("reference_id", sa.String(255), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Calculations
    op.create_table(
        "calculations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tax_return_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_returns.id"), nullable=False),
        sa.Column("input_data", postgresql.JSONB, server_default="{}"),
        sa.Column("result_data", postgresql.JSONB, server_default="{}"),
        sa.Column("estimated_refund", sa.Numeric(12, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Advisor Notes
    op.create_table(
        "advisor_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tax_return_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_returns.id"), nullable=False),
        sa.Column("tax_section_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tax_sections.id"), nullable=True),
        sa.Column("field_key", sa.String(255), nullable=True),
        sa.Column("note", sa.Text, nullable=False),
        sa.Column("correction_value", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("advisor_notes")
    op.drop_table("calculations")
    op.drop_table("messages")
    op.drop_table("documents")
    op.drop_table("tax_sections")
    op.drop_table("tax_returns")
    op.drop_table("users")
    op.drop_table("tenants")

    for enum_name in [
        "referencetype", "ocrstatus", "documentcategory",
        "sectionstatus", "sectiontype", "taxreturnstatus", "userrole",
    ]:
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
