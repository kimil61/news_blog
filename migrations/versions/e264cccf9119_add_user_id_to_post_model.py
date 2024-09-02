"""Add user_id to Post model

Revision ID: e264cccf9119
Revises: 
Create Date: 2024-09-02 10:56:42.550000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e264cccf9119'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_post_user_id', 'user', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')