"""empty message

Revision ID: 94477b487167
Revises: 854e56e7b946
Create Date: 2021-05-08 21:58:33.533043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94477b487167'
down_revision = '854e56e7b946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('goal', 'goal_id')
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['id'])
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'id')
    op.drop_column('task', 'goal_id')
    op.add_column('goal', sa.Column('goal_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'id')
    # ### end Alembic commands ###
