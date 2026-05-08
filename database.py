from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:root@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Error:", e)