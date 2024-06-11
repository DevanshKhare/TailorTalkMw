from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from scraper import web_loader, document_loader
import Constants
scraper = APIRouter(prefix="/api/scraper")

class URLSCRAPERMODEL(BaseModel):
    url: str
    deep_scrap: bool

@scraper.get(Constants.HEALTH_CHECK, tags=["scraper"])
def healthcheck():
    return {"message": "Up and running!", "success": True}

@scraper.post(Constants.SCRAPER["web"], tags=["scraper"])
def load(body: URLSCRAPERMODEL):
    response = web_loader.load(body)
    return response

@scraper.post(Constants.SCRAPER["document"], tags=["scraper"])
async def load_document(file: UploadFile = File(...)):
    response = await document_loader.load_document(file)
    return response