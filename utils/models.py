from utils.database import metadata
import sqlalchemy
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import registry

mapper_registry = registry()

#this table will be removed with first alembic migration run
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

#main table for this app
#I've removed the "old version" of this table from existing DB on 2nd alembic migration
#I've added this version with 3rd alembic migration:
users = sqlalchemy.Table(
    "users",
    #mapper_registry.metadata,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(60),nullable=False,unique=True),
    sqlalchemy.Column("email", sqlalchemy.String(60),nullable=False,unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(60),nullable=False),
    sqlalchemy.Column("register_date", TIMESTAMP(timezone=True),nullable=False, server_default=text('now()')),
)

# class Users:
#     pass
# mapper_registry.map_imperatively(Users, users)
