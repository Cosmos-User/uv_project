from pydantic import BaseModel
from typing import List,Dict,Any, Optional

class Ingestdata(BaseModel):
    collection_name: str
    documents: List[str] 
    metadata: List[Dict[str, Any]] 
    ids: Optional[List[int]] = None