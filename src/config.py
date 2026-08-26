# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    is_reload: bool = True


class Config(BaseSettings):
    data_folder:str = "data"
    marker: str = "*"