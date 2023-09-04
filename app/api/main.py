from fastapi import FastAPI

from app.api.routes.train import router as train
from app.api.routes.recognize import router as recognize

app = FastAPI()

APP_PREFIX = '/v1'

app.include_router(train, prefix=APP_PREFIX)
app.include_router(recognize, prefix=APP_PREFIX)
