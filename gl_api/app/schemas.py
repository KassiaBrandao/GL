from pydantic import BaseModel, Field
from typing import List, Optional, TypeVar, Generic
from datetime import date
from .models import Status

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None

class EpisodeBase(BaseModel):
    number: int
    title: Optional[str] = None
    rating: Optional[float] = None
    air_date: Optional[date] = None
    duration: Optional[int] = None


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeUpdate(EpisodeBase):
    pass


class Episode(EpisodeBase):
    id: int
    drama_id: int

    class Config:
        orm_mode = True


class DramaGLBase(BaseModel):
    title: str
    title_english: Optional[str] = None
    alternative_titles: Optional[List[str]] = []
    year: Optional[int] = None
    release_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Status] = None
    duration: Optional[int] = None
    country: Optional[str] = None
    original_network: Optional[str] = None
    genres: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    rating: Optional[float] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None
    synopsis: Optional[str] = None
    cast: Optional[List[str]] = []
    screenwriter: Optional[str] = None
    director: Optional[str] = None
    trailer_url: Optional[str] = None
    poster_url: Optional[str] = None


class DramaGLCreate(DramaGLBase):
    episodes: Optional[List[EpisodeCreate]] = []


class DramaGLUpdate(DramaGLBase):
    episodes: Optional[List[EpisodeUpdate]] = []


class DramaGL(DramaGLBase):
    id: int
    episodes: List[Episode] = []

    class Config:
        orm_mode = True
