"""empty message

Revision ID: d360204ff1aa
Revises: 
Create Date: 2019-05-07 00:53:06.123598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd360204ff1aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('excerpt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wpm', sa.Integer(), nullable=True),
    sa.Column('excerpt_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['excerpt_id'], ['excerpt.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    op.drop_table('excerpt')
    # ### end Alembic commands ###