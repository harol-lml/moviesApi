from fastapi import APIRouter
from typing import Union, List
from models.Movies import Movie
from fastapi import Query, Depends
from models.movies_db import Movie_db
from fastapi.responses import JSONResponse
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder

movie_router = APIRouter()

@movie_router.get('/movies', tags=['Movies'], response_model = List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])#, dependencies=[Depends(JWTBearer())]
def get_movies(id: Union[str, None] = None) -> List[Movie]:
    if id:
        moviesdb = Movie_db.getById(id)
    else:
        moviesdb = Movie_db.getAll()

    if not moviesdb:
            return JSONResponse(status_code=404, content =  {"message": "Error get movie"})

    return JSONResponse(status_code=200, content = jsonable_encoder(moviesdb))

@movie_router.get('/movies/', tags=['Movies'], response_model = List[Movie], status_code=200)
def get_movies_category(genre: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    moviesdb = Movie_db.getByGenre(genre)
    if not moviesdb:
            return JSONResponse(status_code=404, content =  {"message": "Error get movie"})

    return JSONResponse(status_code=200, content = jsonable_encoder(moviesdb))

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def add_movies(movie: Movie) -> dict:
    new_movie = Movie_db(**movie.model_dump())
    if new_movie.save():
        return JSONResponse(status_code=201, content = {"message": "Post Movie"})

    return JSONResponse(status_code=400, content = {"message": "Error post movie"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: str, mov: Movie) -> dict:
    moviesdb = Movie_db.update(id, mov)
    if moviesdb: return JSONResponse(status_code=200, content = {"messge": "Updated movie"})

    return JSONResponse(status_code=404, content = {"error": "Movie not found"})

    for movie in movies:
        if movie['id'] == id:
            movie['title']    = mov.title
            movie['year']     = mov.year
            movie['director'] = mov.director
            movie['duration'] = mov.duration
            movie['poster']   = mov.poster
            movie['genre']    = mov.genre
            movie['rate']     = mov.rate
            return JSONResponse(status_code=200, content = {"messge": "Updated movie"})
    return JSONResponse(status_code=404, content = {"error": "Movie not found"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: str) -> dict:
    moviesdb = Movie_db.delete(id)
    if moviesdb: return JSONResponse(status_code=200, content = {"messge": "Deleted movie"})

    return JSONResponse(status_code=404, content = {"error": "Movie not found"})
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(status_code = 200, content = {"message": "Deleted Movie"})
    return JSONResponse(status_code = 404, content = {"error": "Movie not found"})