from fastapi import APIRouter, Depends
from pymongo.database import Database
from ....services.mongo_services import create_collection_if_not_exists, insert_document, update_document, delete_document
from ....utils.dependency import get_mongo_database

router = APIRouter()


@router.post('/create_collection')
async def create_new_collection(collection_name: str,db: Database = Depends(get_mongo_database)):
        collection = await create_collection_if_not_exists(collection_name, db=db)
        return {
            "message": f"Collection '{collection_name}' is ready.",
            "collection": collection.name
        }

@router.post("/create_document")
async def insert_data(collection_name: str, document: dict, db: Database = Depends(get_mongo_database)):
    return await insert_document(collection_name, document, db)

@router.put("/update_document")
async def update_data(collection_name: str, filter: dict, update_data: dict, db: Database = Depends(get_mongo_database)):
    return await update_document(collection_name, filter, update_data, db)

@router.delete("/delete_document")
async def delete_data(collection_name: str, filter: dict, db: Database = Depends(get_mongo_database)):
    return await delete_document(collection_name, filter, db)
