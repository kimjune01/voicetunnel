"""empty message

Revision ID: d89b393fa672
Revises: e5d74bcbaba8
Create Date: 2017-11-19 16:04:40.876654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd89b393fa672'
down_revision = 'e5d74bcbaba8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('socketInstanceId', sa.String(length=60), nullable=True))
    pass


def downgrade():
    op.drop_column('users','socketInstanceId')
    pass
