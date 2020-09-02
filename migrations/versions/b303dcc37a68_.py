"""empty message

Revision ID: b303dcc37a68
Revises: 
Create Date: 2020-09-02 17:41:00.743899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b303dcc37a68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('image_path', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('movie_rating', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('text_rank', sa.Float(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('movie_rating', sa.Integer(), nullable=False),
    sa.Column('emotion', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('comment')
    op.drop_table('movie')
    # ### end Alembic commands ###
