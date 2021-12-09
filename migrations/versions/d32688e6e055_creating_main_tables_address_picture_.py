""" Creating main tables: address, picture, republic, state, user

Revision ID: d32688e6e055
Revises: 
Create Date: 2021-12-09 15:05:14.731246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd32688e6e055'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uf', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=False),
    sa.Column('street_number', sa.String(length=5), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('uf_id', sa.Integer(), nullable=True),
    sa.Column('zip_code', sa.String(length=8), nullable=True),
    sa.ForeignKeyConstraint(['uf_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('college', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.PrimaryKeyConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('republics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('vacancies_qty', sa.Integer(), nullable=False),
    sa.Column('max_occupancy', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_cpf', sa.String(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['user_cpf'], ['users.cpf'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('picture_url', sa.String(), nullable=False),
    sa.Column('rep_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rep_id'], ['republics.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pictures')
    op.drop_table('republics')
    op.drop_table('users')
    op.drop_table('addresses')
    op.drop_table('states')
    # ### end Alembic commands ###