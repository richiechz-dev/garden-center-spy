import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load.db_models import Base

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://usuario:contraseña@localhost:5432/nombre_db"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_session():
    return SessionLocal()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
