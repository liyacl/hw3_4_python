"""creation date

Revision ID: d470c2ebd2da
Revises: 9e623c258686
Create Date: 2025-03-26 14:39:16.870926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd470c2ebd2da'
down_revision = '9e623c258686'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('short_link', sa.Column('creation_date', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('short_link', 'creation_date')
    # ### end Alembic commands ###
