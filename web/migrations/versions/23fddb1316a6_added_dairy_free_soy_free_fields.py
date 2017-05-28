"""Added dairy-free and soy-free fields to Recipe

Revision ID: 23fddb1316a6
Revises: 56b6764ae94a
Create Date: 2017-05-27 22:46:39.020832

"""

# revision identifiers, used by Alembic.
revision = '23fddb1316a6'
down_revision = '56b6764ae94a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('recipes', sa.Column('dairy_free_recipes', sa.Boolean(), nullable=True))
    op.add_column('recipes', sa.Column('soy_free_recipe', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('recipes', 'dairy_free_recipes')
    op.drop_column('recipes', 'soy_free_recipe')
