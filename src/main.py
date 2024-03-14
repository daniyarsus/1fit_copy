from typing import List

import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.v1.db.database import Base, async_engine
from src.api.v1.auth.services.signup.handlers import router as register_router


app = FastAPI(
    title="Копия 1fit",
    description="API для копии 1fit",
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


app.include_router(register_router, prefix="/v1/registration", tags=["Registration API"])


@app.get(
    "/"
)
async def index():
    return JSONResponse(
        status_code=200,
        content={'details': 'Используйте /docs'}
    )


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Сервер остановлен.")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
