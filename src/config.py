# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
import sys
from pathlib import Path

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from pydantic_settings import BaseSettings

# ----------------------------------------------------------------------------#
# Application code                                                            #
# ----------------------------------------------------------------------------#


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
    is_save_file: bool = False
    log_level: int = 20 if getattr(sys, "frozen", False) else 10
    marker: str = "*"

    @property
    def path_data_folder(self) -> Path:
        return Path(self.data_folder)
