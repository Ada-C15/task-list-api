"""empty message

Revision ID: 5214f35b4f96
Revises: 6a8fd5873a20
Create Date: 2021-05-12 21:35:26.456622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5214f35b4f96'
down_revision = '6a8fd5873a20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('match_goal_id', sa.Integer(), nullable=True))
    op.drop_constraint('task_goal_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['match_goal_id'], ['goal_id'])
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_goal_id_fkey', 'task', 'goal', ['goal_id'], ['goal_id'])
    op.drop_column('task', 'match_goal_id')
    # ### end Alembic commands ###
