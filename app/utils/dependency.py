from fastapi import Request
from pymongo.database import Database
from pymongo import AsyncMongoClient


def get_mongo_database(request: Request) -> Database:
    return request.app.state.mongo_db

def get_mongo_client(request: Request) -> AsyncMongoClient:
    return request.app.state.mongo_client

def get_gemini_client(request: Request):
    return request.app.state.gemini_client