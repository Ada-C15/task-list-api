"""empty message

Revision ID: 383407853bb9
Revises: eb6d977d3596
Create Date: 2021-05-11 15:57:45.778915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '383407853bb9'
down_revision = 'eb6d977d3596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
