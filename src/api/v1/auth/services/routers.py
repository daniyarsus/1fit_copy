from main import routers
from src.api.v1.auth.services.signup.handlers import router as register_router

router = routers.append(register_router)
