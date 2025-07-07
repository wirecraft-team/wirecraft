# type: ignore
"""init

Revision ID: 7f85f5c3aab9
Revises: 
Create Date: 2025-07-07 17:05:14.350171

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '7f85f5c3aab9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('levelstate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.Column('frozen_name', sa.Boolean(), nullable=False),
    sa.Column('deletable', sa.Boolean(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.Column('ip', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['level_id'], ['levelstate.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'level_id', name='uq_device_name_level_id')
    )
    op.create_table('cable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_id_1', sa.Integer(), nullable=False),
    sa.Column('port_1', sa.Integer(), nullable=False),
    sa.Column('device_id_2', sa.Integer(), nullable=False),
    sa.Column('port_2', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id_1'], ['device.id'], ),
    sa.ForeignKeyConstraint(['device_id_2'], ['device.id'], ),
    sa.ForeignKeyConstraint(['level_id'], ['levelstate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('cable')
    op.drop_table('device')
    op.drop_table('levelstate')
