"""add job title

Revision ID: 334ec19730af
Revises: ef2e21bc31e1
Create Date: 2025-04-16 20:42:47.643124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '334ec19730af'
down_revision = 'ef2e21bc31e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_title', sa.String(length=300), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_column('job_title')

    # ### end Alembic commands ###
