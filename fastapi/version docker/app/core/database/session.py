from sqlalchemy.orm import sessionmaker, Session

from app.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()