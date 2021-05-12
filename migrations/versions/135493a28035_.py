"""empty message

Revision ID: 135493a28035
Revises: 724c5f362b88
Create Date: 2021-05-11 21:01:47.834567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135493a28035'
down_revision = '724c5f362b88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.drop_constraint('task_connected_goal_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    op.drop_column('task', 'connected_goal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('connected_goal', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_connected_goal_fkey', 'task', 'goal', ['connected_goal'], ['goal_id'])
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
