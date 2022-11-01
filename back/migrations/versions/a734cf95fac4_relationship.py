"""relationship

Revision ID: a734cf95fac4
Revises: 
Create Date: 2022-10-28 17:24:36.821663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a734cf95fac4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'companies', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    # ### end Alembic commands ###
