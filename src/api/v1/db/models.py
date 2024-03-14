from src.api.v1.auth.core.models import User


class UserModel:
    user: User


class Model:
    def __init__(self):
        self.user = User


models: Model = Model()
