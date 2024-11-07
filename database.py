from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr, DeclarativeBase
from config import settings


DATABASE_URL = ( f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}' )


Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


