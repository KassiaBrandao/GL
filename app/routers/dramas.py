import logging
import json
import csv
from io import StringIO
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.SuccessResponse[schemas.DramaGL], status_code=201)
def create_drama(drama: schemas.DramaGLCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando novo drama: {drama.title}")
    db_drama = crud.create_drama(db=db, drama=drama)
    logger.info(f"Drama '{drama.title}' criado com sucesso.")
    return {"message": f"Drama '{db_drama.title}' criado com sucesso.", "data": db_drama}


@router.get("/", response_model=List[schemas.DramaGL])
def read_dramas(
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    country: Optional[str] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db),
):
    dramas = crud.get_dramas(
        db, skip=skip, limit=limit, title=title, country=country, genre=genre
    )
    return dramas


@router.get("/{drama_id}", response_model=schemas.DramaGL)
def read_drama(drama_id: int, db: Session = Depends(get_db)):
    db_drama = crud.get_drama(db, drama_id=drama_id)
    if db_drama is None:
        raise HTTPException(status_code=404, detail="Drama não encontrado")
    return db_drama


@router.put("/{drama_id}", response_model=schemas.SuccessResponse[schemas.DramaGL])
def update_drama(
    drama_id: int, drama: schemas.DramaGLUpdate, db: Session = Depends(get_db)
):
    logger.info(f"Atualizando drama com ID: {drama_id}")
    db_drama = crud.update_drama(db, drama_id=drama_id, drama=drama)
    if db_drama is None:
        raise HTTPException(status_code=404, detail="Drama não encontrado")
    logger.info(f"Drama com ID '{drama_id}' atualizado com sucesso.")
    return {"message": f"Drama com ID '{drama_id}' atualizado com sucesso.", "data": db_drama}


@router.delete("/{drama_id}", response_model=schemas.SuccessResponse[schemas.DramaGL])
def delete_drama(drama_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deletando drama com ID: {drama_id}")
    db_drama = crud.delete_drama(db, drama_id=drama_id)
    if db_drama is None:
        raise HTTPException(status_code=404, detail="Drama não encontrado")
    logger.info(f"Drama com ID '{drama_id}' deletado com sucesso.")
    return {"message": f"Drama com ID '{drama_id}' deletado com sucesso.", "data": db_drama}


@router.post("/{drama_id}/episodes", response_model=schemas.SuccessResponse[schemas.Episode])
def create_episode_for_drama(
    drama_id: int, episode: schemas.EpisodeCreate, db: Session = Depends(get_db)
):
    logger.info(f"Adicionando episódio ao drama com ID: {drama_id}")
    db_drama = crud.get_drama(db, drama_id=drama_id)
    if db_drama is None:
        raise HTTPException(status_code=404, detail="Drama não encontrado")
    db_episode = crud.create_drama_episode(db=db, episode=episode, drama_id=drama_id)
    logger.info(
        f"Episódio {db_episode.number} adicionado ao drama com ID '{drama_id}'."
    )
    return {"message": f"Episódio {db_episode.number} adicionado ao drama com ID '{drama_id}'.", "data": db_episode}


@router.put("/{drama_id}/episodes/{episode_number}", response_model=schemas.SuccessResponse[schemas.Episode])
def update_episode(
    drama_id: int,
    episode_number: int,
    episode: schemas.EpisodeUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"Atualizando episódio {episode_number} do drama com ID: {drama_id}")
    db_episode = crud.update_episode(
        db, drama_id=drama_id, episode_number=episode_number, episode=episode
    )
    if db_episode is None:
        raise HTTPException(status_code=404, detail="Episódio não encontrado")
    logger.info(
        f"Episódio {episode_number} do drama com ID '{drama_id}' atualizado com sucesso."
    )
    return {"message": f"Episódio {episode_number} do drama com ID '{drama_id}' atualizado com sucesso.", "data": db_episode}


@router.delete(
    "/{drama_id}/episodes/{episode_number}", response_model=schemas.SuccessResponse[schemas.Episode]
)
def delete_episode(drama_id: int, episode_number: int, db: Session = Depends(get_db)):
    logger.info(f"Deletando episódio {episode_number} do drama com ID: {drama_id}")
    db_episode = crud.delete_episode(
        db, drama_id=drama_id, episode_number=episode_number
    )
    if db_episode is None:
        raise HTTPException(status_code=404, detail="Episódio não encontrado")
    logger.info(
        f"Episódio {episode_number} do drama com ID '{drama_id}' deletado com sucesso."
    )
    return {"message": f"Episódio {episode_number} do drama com ID '{drama_id}' deletado com sucesso.", "data": db_episode}


@router.get("/export/json")
def export_dramas_to_json(db: Session = Depends(get_db)):
    dramas = crud.get_dramas(db, limit=1000)
    dramas_dict = [json.loads(schemas.DramaGL.from_orm(d).json()) for d in dramas]
    return Response(
        content=json.dumps(dramas_dict, indent=4, ensure_ascii=False),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=dramas.json"},
    )


@router.get("/export/csv")
def export_dramas_to_csv(db: Session = Depends(get_db)):
    dramas = crud.get_dramas(db, limit=1000)
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(schemas.DramaGL.__fields__.keys())

    for drama in dramas:
        drama_schema = schemas.DramaGL.from_orm(drama)
        writer.writerow(drama_schema.dict().values())

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dramas.csv"},
    )
