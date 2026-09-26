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
    Хранит конфигурацию веб-сервера Uvicorn.

    Attributes:
        host: Хост, на котором запускается веб-сервер.
        port: Порт, на котором запускается веб-сервер.
        is_reload: Флаг автоматической перезагрузки при изменении кода.
        access_log: Флаг ведения журнала доступа.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    is_reload: bool = not getattr(sys, "frozen", False)
    access_log: bool = not getattr(sys, "frozen", False)


class Config(BaseSettings):
    """
    Хранит основные настройки приложения.

    Attributes:
        data_folder: Путь к директории для временных файлов.
        is_save_file: Флаг сохранения результата конвертации в файл.
        log_level: Уровень журналирования приложения.
        marker: Маркер строк, содержащих домены для конвертации.
    """

    data_folder: str = "data"
    is_save_file: bool = False
    log_level: int = 20 if getattr(sys, "frozen", False) else 10
    marker: str = "*"

    @property
    def path_data_folder(self) -> Path:
        """
        Возвращает путь к директории для хранения временных файлов.

        Returns:
            Путь к директории, заданной в настройке ``data_folder``.
        """
        return Path(self.data_folder)
