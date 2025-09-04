from sqlalchemy.orm import Session
from . import models, schemas


def get_drama(db: Session, drama_id: int):
    return db.query(models.DramaGL).filter(models.DramaGL.id == drama_id).first()


def get_dramas(db: Session, skip: int = 0, limit: int = 10, title: str = None, country: str = None, genre: str = None):
    query = db.query(models.DramaGL)
    if title:
        query = query.filter(models.DramaGL.title.contains(title))
    if country:
        query = query.filter(models.DramaGL.country.contains(country))
    if genre:
        query = query.filter(models.DramaGL.genres.contains(genre))
    return query.offset(skip).limit(limit).all()


def create_drama(db: Session, drama: schemas.DramaGLCreate):
    db_drama = models.DramaGL(**drama.dict(exclude={"episodes"}))
    db.add(db_drama)
    db.commit()
    db.refresh(db_drama)
    for episode_data in drama.episodes:
        db_episode = models.Episode(**episode_data.dict(), drama_id=db_drama.id)
        db.add(db_episode)
    db.commit()
    db.refresh(db_drama)
    return db_drama


def update_drama(db: Session, drama_id: int, drama: schemas.DramaGLUpdate):
    db_drama = get_drama(db, drama_id)
    if not db_drama:
        return None
    update_data = drama.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "episodes":
            continue
        setattr(db_drama, key, value)

    if "episodes" in update_data:
        for episode_data in update_data["episodes"]:
            episode_number = episode_data.get("number")
            db_episode = db.query(models.Episode).filter(models.Episode.drama_id == drama_id, models.Episode.number == episode_number).first()
            if db_episode:
                for e_key, e_value in episode_data.items():
                    setattr(db_episode, e_key, e_value)
            else:
                db_episode = models.Episode(**episode_data, drama_id=drama_id)
                db.add(db_episode)

    db.add(db_drama)
    db.commit()
    db.refresh(db_drama)
    return db_drama



def delete_drama(db: Session, drama_id: int):
    db_drama = get_drama(db, drama_id)
    if not db_drama:
        return None
    db.delete(db_drama)
    db.commit()
    return db_drama


def create_drama_episode(db: Session, episode: schemas.EpisodeCreate, drama_id: int):
    db_episode = models.Episode(**episode.dict(), drama_id=drama_id)
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode


def update_episode(db: Session, drama_id: int, episode_number: int, episode: schemas.EpisodeUpdate):
    db_episode = db.query(models.Episode).filter(models.Episode.drama_id == drama_id, models.Episode.number == episode_number).first()
    if not db_episode:
        return None
    update_data = episode.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_episode, key, value)
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode


def delete_episode(db: Session, drama_id: int, episode_number: int):
    db_episode = db.query(models.Episode).filter(models.Episode.drama_id == drama_id, models.Episode.number == episode_number).first()
    if not db_episode:
        return None
    db.delete(db_episode)
    db.commit()
    return db_episode
