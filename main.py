from fastapi import FastAPI
from routes.main import api_router
from sqlmodel import Session, select
from fastapi import logger
from database import engine
import logging
from database import seed_naturaleza, seed_movimiento, seed_pokemon, seed_equipo
from sqlalchemy import Engine
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")
    seed_pokemon()
    seed_movimiento()
    seed_naturaleza()
    seed_equipo()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

main()
