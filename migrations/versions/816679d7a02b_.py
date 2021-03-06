"""empty message

Revision ID: 816679d7a02b
Revises: 
Create Date: 2022-01-14 13:59:22.941701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816679d7a02b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('videos', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'videos', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'videos', type_='foreignkey')
    op.drop_column('videos', 'author_id')
    op.drop_table('users')
    # ### end Alembic commands ###
