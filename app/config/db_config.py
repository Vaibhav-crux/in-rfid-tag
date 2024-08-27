import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the declarative models
Base = declarative_base()

# Dependency: get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize the database (create tables) and check the connection
def init_db():
    try:
        # Attempt to connect to the database
        connection = engine.connect()
        print("Database connection established successfully.")

        # Import models to create tables
        import app.model
        Base.metadata.create_all(bind=engine)
        
        # Close the connection after tables are created
        connection.close()
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")

# Function to close the database connection (optional, in case you want to manage sessions manually)
def close_db():
    engine.dispose()
