import databases
import sqlalchemy
from config import settings

DATABASE_URL = f"postgresql://" \
               f"{settings.database_username}:{settings.database_password}@" \
               f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
#engine = sqlalchemy.create_engine(DATABASE_URL)


