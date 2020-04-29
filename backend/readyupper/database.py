import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Engine/session.
def database_url(USER, PASSWORD, HOST, NAME):
    return f"postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}"


DATABASE_SETTINGS = {
    "USER": os.environ["DB_USER"],
    "PASSWORD": os.environ["DB_PASSWORD"],
    "HOST": os.environ["DB_HOST"],
    "NAME": os.environ["DB_NAME"],
}
SQLALCHEMY_DATABASE_URL = database_url(**DATABASE_SETTINGS)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

# Base class our models inherit from.
Base = declarative_base()
