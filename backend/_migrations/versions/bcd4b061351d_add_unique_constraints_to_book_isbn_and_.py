"""add unique constraints to book isbn and user email

Revision ID: bcd4b061351d
Revises: cda707af9b0c
Create Date: 2026-05-14 09:04:19.839769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcd4b061351d'
down_revision = 'cda707af9b0c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_book_isbn', ['isbn'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_users_email', ['email'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('uq_book_isbn', type_='unique')

    # ### end Alembic commands ###
