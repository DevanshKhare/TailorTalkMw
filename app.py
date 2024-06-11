"""
File: app.py
Author: Devansh Khare
Date: 2024-05-18
Description: This file is the entry point of the FastAPI application. 
It includes the routers for the different endpoints of the application. 
It also includes the scheduler that runs every 30 minutes to store the data in the Neo4j database. 
The scheduler is run in a separate thread to avoid blocking the main thread. The app is run using the uvicorn server.
"""
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import api.scraper as scraper
import api.scheduler as scheduler
import uvicorn
import Constants
import os
from dotenv import load_dotenv
import schedule
import time
import threading
import requests
from services import neo4j_data_trainer
import api.retriever as retreiver
load_dotenv()

app = FastAPI()

def call_scheduler():
    neo4j_data_trainer.store_to_neo4j()
    print("Scheduler called", flush=True)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(30).minutes.do(call_scheduler)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(scraper.scraper)
app.include_router(scheduler.scheduler)
app.include_router(retreiver.retriever)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", reload=True)