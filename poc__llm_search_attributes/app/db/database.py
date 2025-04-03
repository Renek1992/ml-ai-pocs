"""
database client.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from langchain_community.utilities.sql_database import SQLDatabase 


DATABASE_URI = os.environ.get('DATABASE_URI')


def get_db():
    db = SQLDatabase.from_uri(database_uri=DATABASE_URI)
    return db

