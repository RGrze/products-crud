"""create initial tables

Revision ID: 9121818a2b6b
Revises: 
Create Date: 2024-05-25 00:11:18.533982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9121818a2b6b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'labels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('name', sa.String(64)),
    )

    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('name', sa.String(64)),
        sa.Column('description', sa.String(255)),
        sa.Column('stock', sa.Integer, nullable=False, default=0),
        sa.Column('price', sa.Integer),
    )

    op.create_table(
        'association',
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), primary_key=True),
        sa.Column('label_id', sa.Integer, sa.ForeignKey('labels.id'), primary_key=True),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('username', sa.String(30), unique=True, index=True),
        sa.Column('password_hash', sa.String),
    )

    op.create_table(
        'apikeys',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('key', sa.String(64), index=True, unique=True),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table('apikeys')
    op.drop_table('users')
    op.drop_table('association')
    op.drop_table('products')
    op.drop_table('labels')
