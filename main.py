# main.py
from fastapi import FastAPI
from config import settings
from db import collection
from routers.home import router as home_router

app = FastAPI(title=settings.title)
app.include_router(home_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)