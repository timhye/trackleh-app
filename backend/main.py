from fastapi import FastAPI
from database import engine

app = FastAPI()


@app.on_event("startup")
async def create_tables():
    import models  # Import only when needed
    models.Base.metadata.create_all(bind=engine)

    
@app.get("/")
async def check():
    return "Hello! Trackleh is running!"

