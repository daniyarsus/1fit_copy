import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.services.check.settings.db.database import Base, async_engine
from src.services.check.app.check.handlers import router as item_router


app = FastAPI(
    title="Копия 1fit",
    description="API авторизации для копии 1fit",
    version="1.0.0",
    docs_url="/docs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(item_router, prefix="/v1/item")


@app.get(
    "/"
)
async def index():
    return JSONResponse(
        status_code=200,
        content={'details': 'Салам :)'}
    )


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Сервер остановлен.")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port='8000')