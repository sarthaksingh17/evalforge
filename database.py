from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine - connection to database
engine = create_async_engine(DATABASE_URL, echo=True)

# Base - foundation of all models
Base = declarative_base()

# Session - interaction with database
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency - used in routes via Depends()
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session