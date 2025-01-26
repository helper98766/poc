from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///example.db"  # Replace 'example.db' with your desired SQLite database name

# Create the SQLite engine
engine = create_engine(DATABASE_URL, echo=True)

# Configure the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    """
    Returns the SQLite engine for database connections.
    """
    return engine

def get_session():
    """
    Provides a database session for performing operations.
    """
    return SessionLocal()

def init_db(Base):
    """
    Initialize the database by creating all tables defined in the ORM.
    """
    Base.metadata.create_all(bind=engine)