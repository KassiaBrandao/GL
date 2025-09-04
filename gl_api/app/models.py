from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Enum,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from .database import Base
import enum


class Status(str, enum.Enum):
    on_air = "Em exibição"
    finished = "Finalizado"
    announced = "Anunciado"


class DramaGL(Base):
    __tablename__ = "dramas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    title_english = Column(String)
    alternative_titles = Column(JSON)
    year = Column(Integer)
    release_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(Status))
    duration = Column(Integer)
    country = Column(String)
    original_network = Column(String)
    genres = Column(JSON)
    tags = Column(JSON)
    rating = Column(Float)
    rank = Column(Integer)
    popularity = Column(Integer)
    synopsis = Column(String)
    cast = Column(JSON)
    screenwriter = Column(String)
    director = Column(String)
    trailer_url = Column(String)
    poster_url = Column(String)

    episodes = relationship("Episode", back_populates="drama", cascade="all, delete-orphan")


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    title = Column(String)
    rating = Column(Float)
    air_date = Column(Date)
    duration = Column(Integer)
    drama_id = Column(Integer, ForeignKey("dramas.id"))

    drama = relationship("DramaGL", back_populates="episodes")
