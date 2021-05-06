"""empty message

Revision ID: 1d08448e6c2b
Revises: f92a2eea5f0d
Create Date: 2021-05-04 22:45:56.813749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d08448e6c2b'
down_revision = 'f92a2eea5f0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    # ### end Alembic commands ###
