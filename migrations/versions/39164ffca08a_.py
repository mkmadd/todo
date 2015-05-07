"""empty message

Revision ID: 39164ffca08a
Revises: c3c21c020e7
Create Date: 2015-05-03 18:26:07.934617

"""

# revision identifiers, used by Alembic.
revision = '39164ffca08a'
down_revision = 'c3c21c020e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todo', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todo', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###