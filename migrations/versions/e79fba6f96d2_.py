"""empty message

Revision ID: e79fba6f96d2
Revises: 046923de7835
Create Date: 2022-06-03 02:08:49.709769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e79fba6f96d2'
down_revision = '046923de7835'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('shows_artist_id_fkey', 'shows', type_='foreignkey')
    op.drop_constraint('shows_venue_id_fkey', 'shows', type_='foreignkey')
    op.create_foreign_key(None, 'shows', 'venue', ['venue_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'shows', 'artist', ['artist_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.create_foreign_key('shows_venue_id_fkey', 'shows', 'venue', ['venue_id'], ['id'])
    op.create_foreign_key('shows_artist_id_fkey', 'shows', 'artist', ['artist_id'], ['id'])
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('shows', 'start_time')
    op.drop_column('shows', 'id')
    # ### end Alembic commands ###