"""empty message

Revision ID: 739611644452
Revises: db785a2f0e05
Create Date: 2020-05-19 21:31:36.168149

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '739611644452'
down_revision = 'db785a2f0e05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('urls', 'short_url',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.create_index(op.f('ix_urls_user_id'), 'urls', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_urls_user_id'), table_name='urls')
    op.alter_column('urls', 'short_url',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    # ### end Alembic commands ###
