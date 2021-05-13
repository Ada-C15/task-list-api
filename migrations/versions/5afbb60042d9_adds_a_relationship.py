"""adds a relationship

Revision ID: 5afbb60042d9
Revises: f1d0bb2163c1
Create Date: 2021-05-12 00:48:50.375942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5afbb60042d9'
down_revision = 'f1d0bb2163c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('goal')
    op.add_column('tasks', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'goals', ['goal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'goal_id')
    op.create_table('goal',
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.drop_table('goals')
    # ### end Alembic commands ###
