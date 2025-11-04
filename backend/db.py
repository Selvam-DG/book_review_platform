import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def make_db_uri() -> str:
    host = os.environ.get("POSTGRES_HOST", "localhost")
    db   = os.environ.get("POSTGRES_DB", "")
    user = os.environ.get("POSTGRES_USER", "")
    pwd  = os.environ.get("POSTGRES_PASSWORD", "")
    encoded_password = quote_plus(pwd)
    port = os.environ.get("POSTGRES_PORT", "5432")
    
    return f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{db}"

engine = create_engine(make_db_uri(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
