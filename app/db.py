from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import Base

engine = create_engine('sqlite:///app.db')
session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base.metadata.create_all(bind=engine)
Base.session = session.query_property()
