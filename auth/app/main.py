from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.db.connection import async_engine, Base

from app.api.routers import all_routers


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print(f"Подключение к базе установлено для приложения {app.__class__.__name__}!")
    yield
    print(f"Подключение к базе остановлено для приложения {app.__class__.__name__}!")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Хелоу :3"}


for router in all_routers:
    app.include_router(router, prefix='/api/v1', tags=['Auth endpoints - API'])
