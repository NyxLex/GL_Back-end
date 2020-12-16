"""create account table

Revision ID: b70383ece7e4
Revises: 
Create Date: 2020-12-08 20:33:27.141896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70383ece7e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
    'user',
    sa.Column("user_id", sa.Integer, primary_key=True),
    sa.Column('username', sa.String, unique=True)
    )


    op.create_table(
    'wallets',
    sa.Column("user_id", sa.Integer, primary_key=True),
    sa.Column('username', sa.String, unique=True),
    sa.Column('owner_id', sa.Integer ),
    sa.Column('name',sa.String),
    sa.Column('uah',sa.Integer),
    )

def downgrade():
    op.drop_table('user')
    op.drop_table('wallets')