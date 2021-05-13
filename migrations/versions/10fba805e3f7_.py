"""empty message

Revision ID: 10fba805e3f7
Revises: 1bf482252e77
Create Date: 2021-05-12 20:53:38.453343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fba805e3f7'
down_revision = '1bf482252e77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.drop_constraint('task_goal_id_FK_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    op.drop_column('task', 'goal_id_FK')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id_FK', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_goal_id_FK_fkey', 'task', 'goal', ['goal_id_FK'], ['goal_id'])
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
