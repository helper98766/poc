from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
DATABASE_URL = "sqlite:///dynamic_api_project.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Provide a session context."""
    from contextlib import contextmanager
    @contextmanager
    def session_scope():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    return session_scope()