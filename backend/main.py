from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import SessionLocal, engine
from backend import models
from backend.routers import auth, categories, transactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    #Creation of tables
    models.Base.metadata.create_all(bind=engine)

    #Then seed data
    db = SessionLocal()
    try:
        #Only seed if categories table is empty
        if db.query(models.Category).count() == 0:
            categories = [
                models.Category(name = "Food"),
                models.Category(name = "Transport"),
                models.Category(name = "Shopping"),
                models.Category(name = "Entertainment"),
                models.Category(name = "Bills"),
                models.Category(name = "Other")
            ]
            db.add_all(categories)
            db.commit()
            #print("Default categories seeded in successfully")
        if db.query(models.Transactions).count() == 0:
            transactions = [
                models.Transactions(amt = 25.50, ),
                models.Transactions(),
                models.Transactions(),
                models.Transactions(),
                
            ]
    
    except Exception as e:
        print(f"Error seeding data {e}")
        db.rollback()
    finally:
        db.close()
    yield


#Creation of FastAPI app instance
app = FastAPI(lifespan = lifespan)
    
#Including of routers with prefixes and corresponding tags
app.include_router(auth.router, prefix="/auth", tags = ["Authentication"])
app.include_router(transactions.router, prefix = "/transactions", tags = ["Transactions"])
app.include_router(categories.router, prefix = "/categories", tags = ["Categories"])

#Root endpoint
@app.get("/")
async def check():
    return "Hello! Trackleh is running!"

