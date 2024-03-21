import os

from typing import Optional

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDatabaseConfig:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")

    #DB_USER: str = "postgres"
    #DB_PASS: str = "POqtSKRshJavfUCVuLCGsBKVrlRTACmV"
    #DB_HOST: str = "roundhouse.proxy.rlwy.net"
    #DB_PORT: str = "57119"
    #DB_NAME: str = "railway"

    def __str__(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@dataclass
class JWTConfig:
    SECRET_KEY = str(os.environ.get("SECRET_KEY"))
    ALGORITHM = str(os.environ.get("ALGORITHM"))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))

    #SECRET_KEY: str = "fuosdp82ipo21epoqwpoe129fdspom12"
    #ALGORITHM: str = 'HS256'
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    #REFRESH_TOKEN_EXPIRE_DAYS: int = 5 * 24 * 60 * 60

    def __str__(self):
        return (
            f"SECRET_KEY: {self.SECRET_KEY},"
            f"ALGORITHM: {self.ALGORITHM}, "
            f"ACCESS_TOKEN_EXPIRE_MINUTES: {self.ACCESS_TOKEN_EXPIRE_MINUTES}, "
            f"REFRESH_TOKEN_EXPIRE_DAYS: {self.REFRESH_TOKEN_EXPIRE_DAYS}"
        )


@dataclass
class RegisConfig:
    REDIS_URL_JWT: str = str(os.environ.get("REDIS_URL_JWT"))
    REDIS_URL_REGISTER: str = str(os.environ.get("REDIS_URL_REGISTER"))
    REDIS_URL_PASSWORD: str = str(os.environ.get("REDIS_URL_PASSWORD"))
    REDIS_URL_USER: str = str(os.environ.get("REDIS_URL_USER"))

    #REDIS_URL_JWT: str = "redis://default:djeccefRRQKZqGoJBSbOKtprwgVvzHaN@viaduct.proxy.rlwy.net:41224"
    #REDIS_URL_REGISTER: str = "redis://default:CijwltpFcTQzdvLjyEPmuVYnoigBMxkX@viaduct.proxy.rlwy.net:42928"
    #REDIS_URL_PASSWORD: str = "redis://default:agRLsHFWsxRIxDdMVjzFeWRAuHGvUxBM@monorail.proxy.rlwy.net:16515"
    #REDIS_URL_USER: str = "redis://default:OwOnXncfvETHiSzBSiChjgsQTdHMynrs@roundhouse.proxy.rlwy.net:48250"

    def __str__(self):
        return (
            f"REDIS_URL_JWT: {self.REDIS_URL_JWT}, "
            f"REDIS_URL_REGISTER: {self.REDIS_URL_REGISTER}, "
            f"REDIS_URL_PASSWORD: {self.REDIS_URL_PASSWORD}, "
            f"REDIS_URL_USER: {self.REDIS_URL_USER}"
        )


@dataclass
class SMTPConfig:
    #DOMAIN_NAME: str = str(os.environ.get("DOMAIN_NAME"))
    #SMTP_PORT: str = str(os.environ.get("SMTP_PORT"))
    #API_KEY: str = str(os.environ.get("SMTP_API_KEY"))
    #EMAIL_FROM: str = str(os.environ.get("SMTP_EMAIL_FROM"))

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
