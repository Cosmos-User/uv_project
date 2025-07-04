from qdrant_client import models
import qdrant_client
from ..core.config import get_settings



async def initialise_qdrant():
    settings = get_settings()
    settings.qdrant_url
    client = qdrant_client.AsyncQdrantClient("localhost")

async def close_qdrant_connection():
    pass