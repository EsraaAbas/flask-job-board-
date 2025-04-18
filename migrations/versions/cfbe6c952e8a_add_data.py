"""add data

Revision ID: cfbe6c952e8a
Revises: 334ec19730af
Create Date: 2025-04-16 21:18:56.787546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfbe6c952e8a'
down_revision = '334ec19730af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.alter_column('employees_count',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.alter_column('employees_count',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
