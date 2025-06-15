from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from database import init_db

from api import router
# from seeders.templates import seed_prompt_templates


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup code (equivalent to on_event("startup"))

    init_db()
    # seed_prompt_templates()
    yield
    # Shutdown code would go here if needed (equivalent to on_event("shutdown"))

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173",  # React Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
