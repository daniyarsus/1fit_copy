#import os

from dataclasses import dataclass

#from dotenv import load_dotenv

##dotenv_path = os.path.join(os.path.dirname(__file__), 'auth', 'app', '.env')

# Загрузка переменных из файла .env
#load_dotenv(dotenv_path=dotenv_path)


@dataclass
class PostgresDatabaseConfig:
    #DB_HOST = os.environ.get("DB_HOST2")
    #DB_PORT = os.environ.get("DB_PORT2")
    #DB_NAME = os.environ.get("DB_NAME2")
    #DB_USER = os.environ.get("DB_USER2")
    #DB_PASS = os.environ.get("DB_PASS2")

    DB_USER: str = "postgres"
    DB_PASS: str = "RhfMdjAVyrGSeDjMGCsImnpWCTCSthVh"
    DB_HOST: str = "roundhouse.proxy.rlwy.net"
    DB_PORT: str = "14793"
    DB_NAME: str = "railway"

    def __str__(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class JWTConfig:
    #SECRET_KEY = os.environ.get("SECRET_KEY")

    SECRET_KEY: str = "fuosdp82ipo21epoqwpoe129fdspom12"

    def __str__(self):
        return (
            f"{self.SECRET_KEY}"
        )


@dataclass
class RegisConfig:
    #REDIS_URL_JWT = os.environ.get("REDIS_URL_JWT")
    #REDIS_URL_REGISTER = os.environ("REDIS_URL_REGISTER")

    REDIS_URL_JWT: str = "redis://default:djeccefRRQKZqGoJBSbOKtprwgVvzHaN@viaduct.proxy.rlwy.net:41224"
    REDIS_URL_REGISTER: str = "redis://default:CijwltpFcTQzdvLjyEPmuVYnoigBMxkX@viaduct.proxy.rlwy.net:42928"
    REDIS_URL_PASSWORD: str = "redis://default:agRLsHFWsxRIxDdMVjzFeWRAuHGvUxBM@monorail.proxy.rlwy.net:16515"

    def __str__(self):
        return (
            f"REDIS_URL_JWT: {self.REDIS_URL_JWT}, "
            f"REDIS_URL_REGISTER: {self.REDIS_URL_REGISTER}, "
            f"REDIS_URL_PASSWORD: {self.REDIS_URL_PASSWORD}"
        )


@dataclass
class SMTPConfig:
    #DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    #SMTP_PORT = os.environ.get("SMTP_PORT)
    #API_KEY = os.environ.get("API_KEY")
    #EMAIL_FROM = os.environ.get("EMAIL_FROM")

    DOMAIN_NAME: str = "smtp.gmail.com"
    SMTP_PORT: str = "587"
    API_KEY: str = "bbtyxgcbnpozfepu"
    EMAIL_FROM: str = "y0ur.supp0rt4912385@gmail.com"

    def __str__(self):
        return (
            f"DOMAIN_NAME: {self.DOMAIN_NAME}, "
            f"SMTP_PORT: {self.SMTP_PORT}, "
            f"API_KEY: {self.API_KEY}, "
            f"EMAIL_FROM: {self.EMAIL_FROM}"
        )


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDatabaseConfig()
        self.jwt_config = JWTConfig()
        self.regis_config = RegisConfig()
        self.smtp_config = SMTPConfig()


settings: Settings = Settings()
