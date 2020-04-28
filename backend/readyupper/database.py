import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    os.environ["DB_USER"],
    os.environ["DB_PASSWORD"],
    os.environ["DB_HOST"],
    os.environ["DB_NAME"],
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

# Base class for models.
Base = declarative_base()
