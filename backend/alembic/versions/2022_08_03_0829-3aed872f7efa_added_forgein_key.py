"""Added forgein key

Revision ID: 3aed872f7efa
Revises: 6c97189ae672
Create Date: 2022-08-03 08:29:31.605120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aed872f7efa'
down_revision = '6c97189ae672'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('task_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'tasks', ['task_id'], ['task_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'task_id')
    # ### end Alembic commands ###