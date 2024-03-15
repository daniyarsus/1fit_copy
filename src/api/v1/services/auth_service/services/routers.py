from api.services.v1.auth_service.main import routers
from api.services.v1.auth_service.services.signup.handlers import router as register_router

router = routers.append(register_router)
