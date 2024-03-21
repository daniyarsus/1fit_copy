from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.db.connection import async_engine, Base

from app.api.routers import all_routers


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Сервер остановлен.")


@app.get("/")
async def index():
    return {"message": "Хелоу :3"}


for router in all_routers:
    app.include_router(router, prefix='/api/v1', tags=['Auth endpoints - API'])
