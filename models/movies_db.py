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

    def getAll():
        db = Session()
        movies = db.query(Movie_db).all()
        db.close()
        return movies

    def getById(id):
        db = Session()
        movie = db.query(Movie_db).filter(Movie_db.id == id).first()
        db.close()
        return movie

    def getByGenre(genre):
        db = Session()
        movie = db.query(Movie_db).filter(Movie_db.genre == genre).all()
        db.close()
        return movie

    def update(id, mv: Movie):
        db = Session()
        movie = db.query(Movie_db).filter(Movie_db.id == id).first()
        if not movie: return False

        movie.title = mv.title
        movie.year = mv.year
        movie.director = mv.director
        movie.duration = mv.duration
        movie.poster = mv.poster
        movie.genre = mv.genre
        movie.rate = mv.rate
        db.commit()
        db.close()
        return True

    def delete(id):
        db = Session()
        movie = db.query(Movie_db).filter(Movie_db.id == id).first()
        if not movie: return False
        db.delete(movie)
        db.commit()
        db.close()
        return True