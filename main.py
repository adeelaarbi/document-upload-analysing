from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db

from api import router
from seeders.templates import seed_prompt_templates


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup code (equivalent to on_event("startup"))

    init_db()
    # seed_prompt_templates()
    yield
    # Shutdown code would go here if needed (equivalent to on_event("shutdown"))

app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
