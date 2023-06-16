"""empty message

Revision ID: ba8daeac2128
Revises: f96cc1e82979
Create Date: 2023-06-16 16:19:45.159919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8daeac2128'
down_revision = 'f96cc1e82979'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pengguna',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('nama', sa.String(), nullable=True),
    sa.Column('kontak', sa.String(), nullable=True),
    sa.Column('tipe', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pengguna')
    # ### end Alembic commands ###
