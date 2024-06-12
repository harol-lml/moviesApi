from typing import Union, List
from fastapi import FastAPI, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from fastapi.security.http import HTTPAuthorizationCredentials
from models.Movies import Movie
from models.Users import User
from models.movies_db import Movie_db
from jwt_man import create_token, validate_token

app = FastAPI()
app.title = 'My API Movies'
app.version = '0.0.0'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        aunth = await super().__call__(request)
        data = validate_token(aunth.credentials)
        if data['email'] != "admin":
            raise HTTPException(status_code=403, detail="Invalid credentials")

movies = [
    {
        "id": "dcdd0fad-a94c-4810-8acc-5f108d3b18c3",
        "title": "The Shawshank Redemption",
        "year": 1994,
        "director": "Frank Darabont",
        "duration": 142,
        "poster": "https://i.ebayimg.com/images/g/4goAAOSwMyBe7hnQ/s-l1200.webp",
        "genre": ["Drama"],
        "rate": 9.3
    },
    {
        "id": "c8a7d63f-3b04-44d3-9d95-8782fd7dcfaf",
        "title": "The Dark Knight",
        "year": 2008,
        "director": "Christopher Nolan",
        "duration": 152,
        "poster": "https://i.ebayimg.com/images/g/yokAAOSw8w1YARbm/s-l1200.jpg",
        "genre": ["Action", "Crime", "Drama"],
        "rate": 9.0
    },
    {
        "id": "5ad1a235-0d9c-410a-b32b-220d91689a08",
        "title": "Inception",
        "year": 2010,
        "director": "Christopher Nolan",
        "duration": 148,
        "poster": "https://m.media-amazon.com/images/I/91Rc8cAmnAL._AC_UF1000,1000_QL80_.jpg",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "rate": 8.8
    },
    {
        "id": "241bf55d-b649-4109-af7c-0e6890ded3fc",
        "title": "Pulp Fiction",
        "year": 1994,
        "director": "Quentin Tarantino",
        "duration": 154,
        "poster": "https://www.themoviedb.org/t/p/original/vQWk5YBFWF4bZaofAbv0tShwBvQ.jpg",
        "genre": ["Crime", "Drama"],
        "rate": 8.9
    },
    {
        "id": "9e6106f0-848b-4810-a11a-3d832a5610f9",
        "title": "Forrest Gump",
        "year": 1994,
        "director": "Robert Zemeckis",
        "duration": 142,
        "poster": "https://i.ebayimg.com/images/g/qR8AAOSwkvRZzuMD/s-l1600.jpg",
        "genre": ["Drama", "Romance"],
        "rate": 8.8
    },
    {
        "id": "7e3fd5ab-60ff-4ae2-92b6-9597f0308d1",
        "title": "Gladiator",
        "year": 2000,
        "director": "Ridley Scott",
        "duration": 155,
        "poster": "https://img.fruugo.com/product/0/60/14417600_max.jpg",
        "genre": ["Action", "Adventure", "Drama"],
        "rate": 8.5
    },
    {
        "id": "c906673b-3948-4402-ac7f-73ac3a9e3105",
        "title": "The Matrix",
        "year": 1999,
        "director": "Lana Wachowski",
        "duration": 136,
        "poster": "https://i.ebayimg.com/images/g/QFQAAOSwAQpfjaA6/s-l1200.jpg",
        "genre": ["Action", "Sci-Fi"],
        "rate": 8.7
    },
    {
        "id": "b6e03689-cccd-478e-8565-d92f40813b13",
        "title": "Interstellar",
        "year": 2014,
        "director": "Christopher Nolan",
        "duration": 169,
        "poster": "https://m.media-amazon.com/images/I/91obuWzA3XL._AC_UF1000,1000_QL80_.jpg",
        "genre": ["Adventure", "Drama", "Sci-Fi"],
        "rate": 8.6
    },
    {
        "id": "aa391090-b938-42eb-b520-86ea0aa3917b",
        "title": "The Lord of the Rings: The Return of the King",
        "year": 2003,
        "director": "Peter Jackson",
        "duration": 201,
        "poster": "https://i.ebayimg.com/images/g/0hoAAOSwe7peaMLW/s-l1600.jpg",
        "genre": ["Action", "Adventure", "Drama"],
        "rate": 8.9
    },
    {
        "id": "2e6900e2-0b48-4fb6-ad48-09c7086e54fe",
        "title": "The Lion King",
        "year": 1994,
        "director": "Roger Allers, Rob Minkoff",
        "duration": 88,
        "poster": "https://m.media-amazon.com/images/I/81BMmrwSFOL._AC_UF1000,1000_QL80_.jpg",
        "genre": ["Animation", "Adventure", "Drama"],
        "rate": 8.5
    },
    {
        "id": "04986507-b3ed-442c-8ae7-4c5df804f896",
        "title": "The Avengers",
        "year": 2012,
        "director": "Joss Whedon",
        "duration": 143,
        "poster": "https://img.fruugo.com/product/7/41/14532417_max.jpg",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "rate": 8.0
    },
    {
        "id": "7d2832f8-c70a-410e-8963-4c93bf36cc9c",
        "title": "Jurassic Park",
        "year": 1993,
        "director": "Steven Spielberg",
        "duration": 127,
        "poster": "https://vice-press.com/cdn/shop/products/Jurassic-Park-Editions-poster-florey.jpg?v=1654518755&width=1024",
        "genre": ["Adventure", "Sci-Fi"],
        "rate": 8.1
    },
    {
        "id": "ccf36f2e-8566-47f7-912d-9f4647250bc7",
        "title": "Titanic",
        "year": 1997,
        "director": "James Cameron",
        "duration": 195,
        "poster": "https://i.pinimg.com/originals/42/42/65/4242658e6f1b0d6322a4a93e0383108b.png",
        "genre": ["Drama", "Romance"],
        "rate": 7.8
    },
    {
        "id": "8fb17ae1-bdfe-45e5-a871-4772d7e526b8",
        "title": "The Social Network",
        "year": 2010,
        "director": "David Fincher",
        "duration": 120,
        "poster": "https://i.pinimg.com/originals/7e/37/b9/7e37b994b613e94cba64f307b1983e39.jpg",
        "genre": ["Biography", "Drama"],
        "rate": 7.7
    },
    {
        "id": "6a360a18-c645-4b47-9a7b-2a71babbf3e0",
        "title": "Avatar",
        "year": 2009,
        "director": "James Cameron",
        "duration": 162,
        "poster": "https://i.etsystatic.com/35681979/r/il/dfe3ba/3957859451/il_fullxfull.3957859451_h27r.jpg",
        "genre": ["Action", "Adventure", "Fantasy"],
        "rate": 7.8
    }
]

@app.get('/movies', tags=['Movies'], response_model = List[Movie], status_code=200)#, dependencies=[Depends(JWTBearer())]
def get_movies(id: Union[str, None] = None) -> List[Movie]:
    if id:
        moviesdb = Movie_db.getById(id)
    else:
        moviesdb = Movie_db.getAll()

    if not moviesdb:
            return JSONResponse(status_code=404, content =  {"message": "Error get movie"})

    return JSONResponse(status_code=200, content = jsonable_encoder(moviesdb))

@app.get('/movies/', tags=['Movies'], response_model = List[Movie], status_code=200)
def get_movies_category(genre: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    moviesdb = Movie_db.getByGenre(genre)
    if not moviesdb:
            return JSONResponse(status_code=404, content =  {"message": "Error get movie"})

    return JSONResponse(status_code=200, content = jsonable_encoder(moviesdb))

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def add_movies(movie: Movie) -> dict:
    new_movie = Movie_db(**movie.model_dump())
    if new_movie.save():
        return JSONResponse(status_code=201, content = {"message": "Post Movie"})

    return JSONResponse(status_code=400, content = {"message": "Error post movie"})

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
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

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: str) -> dict:
    moviesdb = Movie_db.delete(id)
    if moviesdb: return JSONResponse(status_code=200, content = {"messge": "Deleted movie"})

    return JSONResponse(status_code=404, content = {"error": "Movie not found"})
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(status_code = 200, content = {"message": "Deleted Movie"})
    return JSONResponse(status_code = 404, content = {"error": "Movie not found"})

@app.post('/login', tags=['Aunth'])
def login(user: User):
    if user.email == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content = token)
    return user