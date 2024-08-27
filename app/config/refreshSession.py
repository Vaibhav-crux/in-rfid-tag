from sqlalchemy.orm import sessionmaker
from app.config.db_config import engine

def create_session():
    session = sessionmaker(bind=engine)
    return session()