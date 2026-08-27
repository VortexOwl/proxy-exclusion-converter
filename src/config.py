# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pydantic_settings import BaseSettings
import sys


class ServerConfig(BaseSettings):
    """
    Конфигурация uvicorn.
    """
    host: str = "127.0.0.1"
    port: int = 8000
    is_reload: bool = not getattr(sys, "frozen", False)
    access_log: bool = not getattr(sys, "frozen", False)


class Config(BaseSettings):
    """
    Конфигурация проекта.
    """
    data_folder: str = "data"
    marker: str = "*"
    log_level: int = 20 if getattr(sys, "frozen", False) else 10