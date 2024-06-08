from config.database import Base, Session, engine
from sqlalchemy import Column, Integer, String, Float
from models.Movies import Movie
import uuid

class Movie_db(Base):
    __tablename__ = "movies"

    id       = Column(String, primary_key = True, default=lambda: str(uuid.uuid4()))
    title    = Column(String)
    year     = Column(Integer)
    director = Column(String)
    duration = Column(Float)
    poster   = Column(String)
    genre    = Column(String)
    rate     = Column(Float)

    def save (self):
        Base.metadata.create_all(bind = engine)
        db = Session()
        db.add(self)
        db.commit()
        db.close()
        return True