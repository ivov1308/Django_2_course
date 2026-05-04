import logging
import os
from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class Django:
    secret_key: str


@dataclass
class MailSettings:
    host: str
    port: int
    user: str
    password: str
    tls: bool
    ssl: bool


@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    password: str
    username: str


@dataclass
class LoggSettings:
    level: str
    format: str


@dataclass
class Config:
    db: DatabaseSettings
    redis: RedisSettings
    log: LoggSettings
    django: Django
    mail: MailSettings


def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)

    env.read_env(path)

    django = Django(
        secret_key=env('SECRET_KEY')
    )

    mail = MailSettings(
        host=env('EMAIL_HOST'),
        port=env.int('EMAIL_PORT'),
        user=env('EMAIL_HOST_USER'),
        password=env('EMAIL_HOST_PASSWORD'),
        tls=env.bool('EMAIL_USE_TLS'),
        ssl=env.bool('EMAIL_USE_SSL')
    )

    db = DatabaseSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )

    redis = RedisSettings(
        host=env("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        password=env("REDIS_PASSWORD", default=""),
        username=env("REDIS_USERNAME", default=""),
    )

    logg_settings = LoggSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT")
    )

    logger.info("Configuration loaded successfully")

    return Config(
        db=db,
        redis=redis,
        log=logg_settings,
        django=django,
        mail=mail
    )
