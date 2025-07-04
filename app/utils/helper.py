import magic
import os
from ..constants import ALLOWED_MIMETYPES, MAX_FILE_SIZE
from ..core.logging import get_logger

logger = get_logger()

def validate_file_type(file_content: bytes, filename: str) -> bool:
    """
    Validate file type using actual mimetype
    """
    try:        
        mime = magic.from_buffer(file_content, mime=True)
        
        if mime not in ALLOWED_MIMETYPES:
            return False
            
        file_extension = os.path.splitext(filename)[1].lower()
        
        if mime == 'application/pdf' and file_extension not in ['.pdf']:
            return False
        elif mime in ['image/jpeg', 'image/jpg'] and file_extension not in ['.jpg', '.jpeg']:
            return False
            
        return True
        
    except Exception as e:
        logger.error("Error Processing file content")
        return False

def validate_file_size(file_size: int) -> bool:
    """
    Validate file size against maximum allowed size
    """
    return file_size <= MAX_FILE_SIZE