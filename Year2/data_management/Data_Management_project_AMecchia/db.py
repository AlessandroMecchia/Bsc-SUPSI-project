import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

class Model(DeclarativeBase):
    metadata = MetaData()

def create_connection():
    # Creates a engine using the database URL from the environment variables.
    # Get the database URL from the environment variables
    connection_string = os.environ.get('database_url')
    
    if not connection_string:
        raise ValueError("database_url environment variable not set.")
    
    # Create the engine
    engine = create_engine(connection_string)
    return engine

