"""adds Goal model

Revision ID: 0572b382dd9e
Revises: 8b3a58fadaf6
Create Date: 2021-05-05 23:47:02.313925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0572b382dd9e'
down_revision = '8b3a58fadaf6'
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
