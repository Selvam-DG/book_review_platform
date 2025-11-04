import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def make_db_uri() -> str:
    host = os.environ.get("POSTGRES_HOST", "postgres")
    db   = os.environ.get("POSTGRES_DB", "bookdb")
    user = os.environ.get("POSTGRES_USER", "bookuser")
    pwd  = os.environ.get("POSTGRES_PASSWORD", "bookpass")
    port = os.environ.get("POSTGRES_PORT", "5432")
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"

engine = create_engine(make_db_uri(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
