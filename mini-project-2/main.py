import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from database.connection import Settings
from routes.events import event_router
from routes.users import user_router

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await settings.initialize_database()
    print("✅ Database connected successfully")
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)