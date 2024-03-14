"""year university

Revision ID: 2b725cfe47f5
Revises: be473f3ce189
Create Date: 2024-03-04 14:53:54.228102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b725cfe47f5'
down_revision: Union[str, None] = 'be473f3ce189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Student', sa.Column('year', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Student', 'year')
    # ### end Alembic commands ###
