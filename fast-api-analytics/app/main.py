from fastapi import FastAPI
from .routers import router as click_router
from .database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app = FastAPI(
    title="My API",
    description="This is a sample API using FastAPI",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "items",
            "description": "Operations with items."
        },
    ],
)


# Register routes
app.include_router(click_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener Analytics Service"}
