from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie_db(Base):
    __tablename__ = "movies"

    id       = Column(Integer, primary_key = True)
    titl     = Column(String)
    year     = Column(Integer)
    director = Column(String)
    duration = Column(Float)
    poster   = Column(String)
    genre    = Column(String)
    rate     = Column(Float)