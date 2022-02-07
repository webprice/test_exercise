"""add tests table

Revision ID: 263e5abad228
Revises: 940d73d508c5
Create Date: 2022-02-07 19:48:28.088562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '263e5abad228'
down_revision = '940d73d508c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tests',
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("username", sa.String(60), nullable=False, unique=True),
                    sa.Column("email", sa.String(60), nullable=False, unique=True),
                    sa.Column("password", sa.String(60), nullable=False),
                    sa.Column("register_date", TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
                    )
    pass


def downgrade():
    op.drop_table('tests')
    pass
