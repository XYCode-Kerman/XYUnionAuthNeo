from typing import Union

from fastapi import FastAPI

from routers import application_router, user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(application_router)
