"""#add language to posts

Revision ID: 8253cdaab72e
Revises: 12de9a7b0040
Create Date: 2019-10-09 16:31:01.777502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8253cdaab72e'
down_revision = '12de9a7b0040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###