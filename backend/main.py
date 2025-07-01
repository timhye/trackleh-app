from fastapi import FastAPI
from database import engine
import models
from routers import auth, categories, transactions

#Creation of FastAPI app instance
app = FastAPI()


#Including of routers with prefixes and corresponding tags
app.include_router(auth.router, prefix="/auth", tags = ["Authentication"])
app.include_router(transactions.router, prefix = "/transactions", tags = ["Transactions"])
app.include_router(categories.router, prefix = "/categories", tags = ["Categories"])


#Startup event to automatically create tables
@app.on_event("startup")
async def create_tables():
    models.Base.metadata.create_all(bind=engine)

    
#Root endpoint
@app.get("/")
async def check():
    return "Hello! Trackleh is running!"

