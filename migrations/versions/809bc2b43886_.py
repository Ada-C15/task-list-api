"""empty message

Revision ID: 809bc2b43886
Revises: 29b07fd9e8c8
Create Date: 2021-05-06 12:05:03.516853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '809bc2b43886'
down_revision = '29b07fd9e8c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
