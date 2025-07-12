import uvicorn
from fastapi import FastAPI

from v1 import v1Router
from v1.settings import Settings


app = FastAPI()

# for v1 only
v1_router = v1Router
settings = Settings()
app.include_router(v1Router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.ip, port=settings.port)