from fastapi import APIRouter, UploadFile, File, Form, Depends,Request
from fastapi.exceptions import HTTPException
from ....constants import MAX_FILE_SIZE
from ....utils.helper import validate_file_type, validate_file_size
from ....services.process_documents import extract_details
from ....prompts.prompts_manager import PromptManager, get_prompt_manager
from ....utils.dependency import get_gemini_client
from ....core.logging import get_logger
from google import genai
from datetime import datetime
from ....services.mongo_services import insert_document
from ....utils.dependency import get_mongo_database
from pymongo.database import Database

router = APIRouter()
logger = get_logger()

current_datetime = datetime.now()

@router.post("/upload_file")
async def upload_file(collection_name : str = Form(...), 
                      file : UploadFile = File(...), 
                      prompt_manager: PromptManager = Depends(get_prompt_manager),
                      gemini_client :genai = Depends(get_gemini_client),
                      mongo_db : Database = Depends(get_mongo_database)
                      ):
        #Extracts the content from the file and dumps to the specified mongo collection name
        try:
            file_content = await file.read()
            file_size = len(file_content)
            
            if not validate_file_size(file_size):
                raise HTTPException(
                    status_code=413,
                    detail=f"File size ({file_size / (1024*1024):.2f}MB) exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
                )
            

            if not validate_file_type(file_content, file.filename):
                raise HTTPException(
                    status_code=415,
                    detail="Unsupported file type. Only PDF and JPEG files are allowed."
                )            

            if file.content_type == "application/pdf":
                try:                                                                                          
                    file_content = await extract_details(collection_name, file_content, prompt_manager, gemini_client)
                    
                    #data cleaning here for the file content
                    mongo_payload = {
                         "document" : file_content,
                         "Uploaded_date" : current_datetime
                    }

                    #dump to mongo
                    try:
                         inserted_id = await insert_document(collection_name, mongo_payload, mongo_db)
                    except Exception as e:
                         logger.error("Exception Occurred During insertion operation", e)

                except Exception as e:
                    logger.error("Exception Occured While Processing pdf")

            elif file.content_type in ['image/jpeg', 'image/jpg']:
                 await extract_details(collection_name, file)

            if inserted_id:
            # File validation passed - process the file here
                return {
                    "message": "File uploaded successfully",
                    "collection_name": collection_name,
                    "filename": file.filename,
                    "file_size": f"{file_size / (1024*1024):.2f}MB",
                    "content_type": file.content_type
                } 
            
            else: 
                 logger.error("Not able to insert documents")
        
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while processing the file: {str(e)}"
            )