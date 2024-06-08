from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[str] = None
    title: str      = Field(max_length = 20)
    year: int       = Field(ge = 1670, le = 2024)
    director: str   = Field(max_length = 20)
    duration: float
    poster: str
    genre: str
    rate: float     = Field(ge = 0.0, le = 10)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    # "id": "any_id",
                    "title": "Avatar",
                    "year": 2009,
                    "director": "James Cameron",
                    "duration": 162,
                    "poster": "https://i.etsystatic.com/35681979/r/il/dfe3ba/3957859451/il_fullxfull.3957859451_h27r.jpg",
                    # "genre": ["Action", "Adventure", "Fantasy"],
                    "genre": "Action",
                    "rate": 7.8
                    }
                ]
            }
        }