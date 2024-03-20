from fastapi import FastAPI

from app.settings.db.connection import async_engine, Base

from app.api.routers import all_routers


app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello world!"}


for router in all_routers:
    app.include_router(router, prefix='/api/v1', tags=['Auth endpoints - API'])


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Сервер остановлен.")
