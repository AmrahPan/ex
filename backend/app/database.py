from sqlmodel import create_engine, Session, select, SQLModel
from .models import GlobalSettings, Kitchen

engine = create_engine('sqlite:///db.sqlite3', echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        gs = session.get(GlobalSettings, 1)
        if not gs:
            gs = GlobalSettings()
            session.add(gs)
        if not session.exec(select(Kitchen)).first():
            session.add_all([
                Kitchen(name='Kitchen A', orders_day=6),
                Kitchen(name='Kitchen B', orders_day=40),
                Kitchen(name='Kitchen C', orders_day=15),
            ])
        session.commit()

