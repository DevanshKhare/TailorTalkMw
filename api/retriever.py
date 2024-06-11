from fastapi import APIRouter
from pydantic import BaseModel
from services.retreival import get_matching_documents
import Constants
retriever = APIRouter(prefix="/api/retriever")

class Query(BaseModel):
    query: str

@retriever.get(Constants.HEALTH_CHECK, tags=["retriever"])
def healthcheck():
    return {"message": "Up and running!", "success": True}

@retriever.post("/query", tags=["retriever"])
def load(query: Query):
    response = get_matching_documents(query.query)
    return response