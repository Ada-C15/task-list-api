"""empty message

Revision ID: a0f76245d37b
Revises: 3326cf095dba
Create Date: 2021-05-10 16:17:48.138544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0f76245d37b'
down_revision = '3326cf095dba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'goal', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'goal', type_='unique')
    # ### end Alembic commands ###
