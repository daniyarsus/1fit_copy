"""gpa to student

Revision ID: bb1e42ed224f
Revises: 2b725cfe47f5
Create Date: 2024-03-04 18:03:01.531604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb1e42ed224f'
down_revision: Union[str, None] = '2b725cfe47f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Student', sa.Column('gpa', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Student', 'gpa')
    # ### end Alembic commands ###
