"""add ai persistence tables

Revision ID: 0002_ai_persistence_tables
Revises: 0001_initial
Create Date: 2026-05-30
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_ai_persistence_tables"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "issue_analyses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("issue_draft_id", sa.String(), nullable=False),
        sa.Column("generated_title", sa.String(length=255), nullable=False),
        sa.Column("generated_description", sa.Text(), nullable=False),
        sa.Column("issue_type", sa.String(length=64), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("labels", sa.JSON(), nullable=False),
        sa.Column("acceptance_criteria", sa.JSON(), nullable=False),
        sa.Column("suggested_subtasks", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_draft_id"], ["issue_drafts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_issue_analyses_issue_draft_id"), "issue_analyses", ["issue_draft_id"], unique=False)

    op.create_table(
        "issue_quality_scores",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("issue_draft_id", sa.String(), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("clarity_score", sa.Integer(), nullable=False),
        sa.Column("completeness_score", sa.Integer(), nullable=False),
        sa.Column("testability_score", sa.Integer(), nullable=False),
        sa.Column("dependency_clarity_score", sa.Integer(), nullable=False),
        sa.Column("business_value_score", sa.Integer(), nullable=False),
        sa.Column("problems", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_draft_id"], ["issue_drafts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_issue_quality_scores_issue_draft_id"), "issue_quality_scores", ["issue_draft_id"], unique=False)

    op.create_table(
        "risk_predictions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("issue_draft_id", sa.String(), nullable=True),
        sa.Column("sprint_id", sa.String(length=128), nullable=True),
        sa.Column("risk_type", sa.String(length=64), nullable=False),
        sa.Column("risk_level", sa.String(length=32), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("main_risk_factors", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_draft_id"], ["issue_drafts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_risk_predictions_issue_draft_id"), "risk_predictions", ["issue_draft_id"], unique=False)
    op.create_index(op.f("ix_risk_predictions_sprint_id"), "risk_predictions", ["sprint_id"], unique=False)

    op.create_table(
        "business_impact_scores",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("issue_draft_id", sa.String(), nullable=False),
        sa.Column("impact_level", sa.String(length=32), nullable=False),
        sa.Column("impact_score", sa.Integer(), nullable=False),
        sa.Column("cost_of_delay", sa.String(length=32), nullable=False),
        sa.Column("customer_impact", sa.String(length=32), nullable=False),
        sa.Column("release_risk", sa.String(length=32), nullable=False),
        sa.Column("reasoning", sa.JSON(), nullable=False),
        sa.Column("recommended_action", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_draft_id"], ["issue_drafts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_business_impact_scores_issue_draft_id"), "business_impact_scores", ["issue_draft_id"], unique=False)

    op.create_table(
        "ai_recommendations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("issue_draft_id", sa.String(), nullable=False),
        sa.Column("recommendation_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_draft_id"], ["issue_drafts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_recommendations_issue_draft_id"), "ai_recommendations", ["issue_draft_id"], unique=False)

    op.create_table(
        "ai_request_logs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("route", sa.String(length=255), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_request_logs_user_id"), "ai_request_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_request_logs_user_id"), table_name="ai_request_logs")
    op.drop_table("ai_request_logs")

    op.drop_index(op.f("ix_ai_recommendations_issue_draft_id"), table_name="ai_recommendations")
    op.drop_table("ai_recommendations")

    op.drop_index(op.f("ix_business_impact_scores_issue_draft_id"), table_name="business_impact_scores")
    op.drop_table("business_impact_scores")

    op.drop_index(op.f("ix_risk_predictions_sprint_id"), table_name="risk_predictions")
    op.drop_index(op.f("ix_risk_predictions_issue_draft_id"), table_name="risk_predictions")
    op.drop_table("risk_predictions")

    op.drop_index(op.f("ix_issue_quality_scores_issue_draft_id"), table_name="issue_quality_scores")
    op.drop_table("issue_quality_scores")

    op.drop_index(op.f("ix_issue_analyses_issue_draft_id"), table_name="issue_analyses")
    op.drop_table("issue_analyses")
