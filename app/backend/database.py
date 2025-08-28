from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import settings

engine = create_engine(url=settings.DATABASE_URL)

local_session = sessionmaker(bind=engine, autoflush=True, autocommit=True)

Base = declarative_base()


def get_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()
