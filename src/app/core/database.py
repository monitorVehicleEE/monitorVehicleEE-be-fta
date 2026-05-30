from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:123@localhost:5432/movee"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("Connected successfully!")

        for row in result:
            print(row)

except Exception as e:
    print("Database connection failed!")
    print(e)