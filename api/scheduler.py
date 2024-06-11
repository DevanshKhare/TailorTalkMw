from fastapi import APIRouter
from pydantic import BaseModel
from services import neo4j_data_trainer
import Constants
scheduler = APIRouter(prefix="/api/scheduler")

class URL(BaseModel):
    url: str

@scheduler.get(Constants.HEALTH_CHECK, tags=["scheduler"])
def healthcheck():
    return {"message": "Up and running!", "success": True}

@scheduler.get(Constants.TRAINER, tags=["scheduler"])
def traindata():
    print("Training data...")
    response = neo4j_data_trainer.store_to_neo4j()
    return response