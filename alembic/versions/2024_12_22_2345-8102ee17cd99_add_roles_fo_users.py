"""add roles fo users

Revision ID: 8102ee17cd99
Revises: b313d5553b6e
Create Date: 2024-12-22 23:45:56.675711

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8102ee17cd99"
down_revision: Union[str, None] = "b313d5553b6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column("user", sa.Column("role_id", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column("user", "role_id")

    # ### end Alembic commands ###
