from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import models
import os
from database import engine
from routers import user, library, library_collection, media, category, category_per_media

os.makedirs("data", exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliothicc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(library.router)
app.include_router(library_collection.router)
app.include_router(media.router)
app.include_router(category.router)
app.include_router(category_per_media.router)

@app.get("/")
def root():
    return {"message": "Besuche /docs für die Swagger UI"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
