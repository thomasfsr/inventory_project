from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(getenv('DATABASE_URL'))

def get_session():
    with Session(engine) as session:
        yield session