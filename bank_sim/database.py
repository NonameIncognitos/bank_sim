
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from bank_sim.config import DB_URL

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False))

class Base(DeclarativeBase):
    pass

def init_db():
    import bank_sim.models  # noqa
    Base.metadata.create_all(bind=engine)
