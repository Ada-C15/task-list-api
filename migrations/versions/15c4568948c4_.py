"""empty message

Revision ID: 15c4568948c4
Revises: 60033d6c6ef4
Create Date: 2021-05-10 19:32:03.030119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15c4568948c4'
down_revision = '60033d6c6ef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('assoc_goal', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['assoc_goal'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'assoc_goal')
    # ### end Alembic commands ###
