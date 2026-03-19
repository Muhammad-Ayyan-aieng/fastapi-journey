from fastapi import FastAPI
from book import book_router
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Library API"}

app.include_router(book_router)