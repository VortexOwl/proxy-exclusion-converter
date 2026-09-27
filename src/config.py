# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
import sys
from pathlib import Path
from platform import system

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
    browser: str = "Floorp"
    browser_folder: str = ".floorp"
    custom_browser_profile: str | None = None
    is_save_file: bool = False
    log_level: int = 20 if getattr(sys, "frozen", False) else 10
    marker: str = "*"
    proxy_exception_setting_name: str = "network.proxy.no_proxies_on"
    tmp_folder: str = "data"
    _default_profile_pattern: str = "*.default*"

    @property
    def path_tmp_folder(self) -> Path:
        """
        Возвращает путь к директории для хранения временных файлов.

        Returns:
            Путь к директории, заданной в настройке ``tmp_folder``.
        """
        return Path(self.tmp_folder)

    @property
    def path_browser_profile(self) -> Path | None:
        sys_name = system()
        path_user: Path = Path.home()
        path_browser: Path = Path(self.browser)
        path_browser_folder: Path = Path(self.browser_folder)
        path_profiles: Path

        if sys_name == "Windows":
            path_browser = Path("AppData") / "Roaming" / path_browser / "Profiles"
        elif sys_name == "Linux":
            path_browser = path_browser_folder
        else:
            return None

        path_profiles = path_user / path_browser

        if self.custom_browser_profile is not None:
            return path_profiles / self.custom_browser_profile
        
        default_profile: Path = next(
            (
                d
                for d in path_profiles.glob(self._default_profile_pattern)
                if d.is_dir()
            ),
            None,
        )
        return default_profile
