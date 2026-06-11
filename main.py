from fastapi import FastAPI
import uvicorn
import models
import os
from database import engine
from routers import user

os.makedirs("data", exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliothicc")

app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Besuche /docs für die Swagger UI"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)