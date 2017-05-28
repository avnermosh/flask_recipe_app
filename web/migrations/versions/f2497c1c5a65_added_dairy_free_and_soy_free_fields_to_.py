"""Added dairy-free and soy-free fields to Recipe

Revision ID: f2497c1c5a65
Revises: 56b6764ae94a
Create Date: 2017-05-27 23:57:48.874816

"""

# revision identifiers, used by Alembic.
revision = 'f2497c1c5a65'
down_revision = '56b6764ae94a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('recipes', sa.Column('dairy_free_recipe', sa.Boolean(), nullable=True))
    op.add_column('recipes', sa.Column('soy_free_recipe', sa.Boolean(), nullable=True))
    op.add_column('recipes', sa.Column('date_created', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('recipes', 'dairy_free_recipe')
    op.drop_column('recipes', 'soy_free_recipe')
