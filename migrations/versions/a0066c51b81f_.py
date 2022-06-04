"""empty message

Revision ID: a0066c51b81f
Revises: e79fba6f96d2
Create Date: 2022-06-03 20:20:54.643644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0066c51b81f'
down_revision = 'e79fba6f96d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###