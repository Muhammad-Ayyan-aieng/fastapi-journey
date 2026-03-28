from typing import Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, PydanticObjectId
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from models.events import Event
from models.users import User

# Monkey patch to fix the append_metadata issue
def patch_motor_client():
    """Add append_metadata method to Motor client if it doesn't exist"""
    if not hasattr(AsyncIOMotorClient, 'append_metadata'):
        def append_metadata(self, metadata):
            if not hasattr(self, '_metadata'):
                self._metadata = []
            self._metadata.append(metadata)
        AsyncIOMotorClient.append_metadata = append_metadata

# Apply the patch
patch_motor_client()


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "planner"
    
    async def initialize_database(self):
        """Initialize database connection"""
        client = AsyncIOMotorClient(self.DATABASE_URL)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB")
        
        db = client[self.DATABASE_NAME]
        
        await init_beanie(
            database=db,
            document_models=[Event, User]
        )
        print("✅ Beanie initialized")
        return client

    class Config:
        env_file = ".env"
        extra = "ignore"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        """Insert a new document"""
        await document.create()

    async def get(self, id: PydanticObjectId) -> Any:
        """Retrieve one document by ID"""
        return await self.model.get(id)

    async def get_all(self) -> List[Any]:
        """Retrieve all documents"""
        return await self.model.find_all().to_list()

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        """Update a document by ID"""
        doc = await self.get(id)
        if doc:
            update_data = {k: v for k, v in body.dict().items() if v is not None}
            await doc.update({"$set": update_data})
        return await self.get(id)

    async def delete(self, id: PydanticObjectId) -> bool:
        """Delete a document by ID"""
        doc = await self.get(id)
        if doc:
            await doc.delete()
            return True
        return False