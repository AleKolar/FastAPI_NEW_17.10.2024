from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declared_attr, DeclarativeBase
from config import settings


DATABASE_URL = ( f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}' )

engine = create_async_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


    # @declared_attr
    # def __tablename__(cls):
    #     return f"{cls.__name__.lower()}s"

class Base(DeclarativeBase):
    pass


