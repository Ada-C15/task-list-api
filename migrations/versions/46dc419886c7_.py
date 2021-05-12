"""empty message

Revision ID: 46dc419886c7
Revises: 58519762887d
Create Date: 2021-05-07 12:13:52.689965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46dc419886c7'
down_revision = '58519762887d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_goal_id', sa.Integer(), nullable=True))
    op.drop_constraint('task_goal_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['task_goal_id'], ['goal_id'])
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_goal_id_fkey', 'task', 'goal', ['goal_id'], ['goal_id'])
    op.drop_column('task', 'task_goal_id')
    # ### end Alembic commands ###
