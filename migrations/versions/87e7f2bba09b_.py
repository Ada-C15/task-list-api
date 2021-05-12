"""empty message

Revision ID: 87e7f2bba09b
Revises: 9a01612f7229
Create Date: 2021-05-11 14:19:09.372761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87e7f2bba09b'
down_revision = '9a01612f7229'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('goal', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    op.alter_column('goal', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
