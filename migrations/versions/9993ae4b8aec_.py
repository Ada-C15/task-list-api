"""empty message

Revision ID: 9993ae4b8aec
Revises: 7d77b8a7ba69
Create Date: 2021-05-11 19:47:09.212696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9993ae4b8aec'
down_revision = '7d77b8a7ba69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
