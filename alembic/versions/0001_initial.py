"""Initial schema."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)

    op.create_table(
        "feed",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("handle", sa.String(), nullable=False),
        sa.Column("last_post_id", sa.String(), nullable=True),
    )
    op.create_index("ix_feed_handle", "feed", ["handle"], unique=True)

    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("feed_id", sa.Integer(), sa.ForeignKey("feed.id"), nullable=False),
        sa.Column("tweet_id", sa.String(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_post_tweet_id", "post", ["tweet_id"], unique=True)

    op.create_table(
        "flashcard",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("post.id"), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("ease_factor", sa.Float(), nullable=False, server_default="2.5"),
        sa.Column("interval", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("repetitions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_review", sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")),
    )


def downgrade() -> None:
    op.drop_table("flashcard")
    op.drop_index("ix_post_tweet_id", table_name="post")
    op.drop_table("post")
    op.drop_index("ix_feed_handle", table_name="feed")
    op.drop_table("feed")
    op.drop_index("ix_user_email", table_name="user")
    op.drop_table("user")

