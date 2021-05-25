"""empty message

Revision ID: 157311429dcf
Revises: 7ff0a11c779f
Create Date: 2021-05-05 20:32:16.777761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157311429dcf'
down_revision = '7ff0a11c779f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'id')
    # ### end Alembic commands ###
