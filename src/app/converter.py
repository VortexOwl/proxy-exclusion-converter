# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pathlib import Path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.config import Config
from src.logs import SmartLogger
from src.utilities import Utilities as uts

# ----------------------------------------------------------------------------#
# Application code                                                            #
# ----------------------------------------------------------------------------#


class ApplicationService:
    class TemporaryFilesCleanupService:
        """
        Очищает директорию для хранения временных файлов.
        """

        def __init__(self, cfg: Config | None = None):
            """
            Инициализирует сервис удаления временных файлов.

            Args:
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация по умолчанию.
            """
            self._cfg = cfg if cfg is not None else Config()

        async def clear_temporary_files(self) -> dict[str, int | tuple[str]]:
            """
            Очищает директорию временных файлов.

            Returns:
                Словарь со статистикой удаления: количеством успешно
                удалённых файлов и количеством ошибок.
            """
            return await uts.clearing_folder(clear_folder=self._cfg.tmp_folder)

    class ProxyExceptionConverterService:
        """
        Преобразует файлы со списком исключений прокси.
        """

        def __init__(
            self, cfg: Config | None = None, log: SmartLogger | None = None
        ) -> None:
            """
            Инициализирует сервис конвертации файлов.

            Args:
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация по умолчанию.
                log: Логгер приложения. Если не передан,
                    создаётся новый экземпляр.
            """
            self._cfg = cfg if cfg is not None else Config()
            self._log = log if log is not None else SmartLogger()
            self._log.setLevel(self._cfg.log_level)

        def convert_file(
            self,
            path_source_file: Path,
            cfg: Config | None = None,
            marker: str | None = None,
        ) -> tuple[str, Path | None]:
            """
            Преобразует файл в список исключений для прокси.

            Из файла выбираются строки, начинающиеся с указанного маркера.
            По необходимости результат сохраняется в отдельный текстовый файл.

            Args:
                path_source_file: Путь к исходному файлу.
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация сервиса.
                marker: Маркер строк, содержащих исключения. Если не передан,
                    используется маркер из конфигурации.

            Returns:
                Кортеж из преобразованного текста и пути к сохранённому файлу.
                Если результат не сохраняется, путь будет равен ``None``.
            """
            if cfg is None:
                cfg = self._cfg

            if marker is None:
                marker = cfg.marker

            self._log.info(
                "Начинается преобразование файла в список исключений для прокси.",
                pretty=True,
            )
            converted_content: str = ""
            path_output_file: Path | None = None

            for line in uts.read_file_line_by_line(file_path=path_source_file):
                if len(line) > 0 and line[0] == marker:
                    converted_content = f"{converted_content}{line[1:]}"

            if cfg.is_save_file:
                path_output_file = Path(
                    path_source_file.parent / f"{path_source_file.stem}.txt"
                )
                with path_output_file.open("w", encoding="utf-8") as converted_file:
                    converted_file.write(converted_content)
            if converted_content == "":
                converted_content = " "
            self._log.info(
                "Преобразование файла в список исключений для прокси прошло успешно.",
                pretty=True,
            )
            return converted_content, path_output_file

    class SetProxyException:
        """
        Изменяет список исключений прокси в браузере.
        """

        def __init__(self, cfg: Config | None = None):
            """
            Инициализирует сервис изменения списка исключений
            прокси в FireFox и его форках

            Args:
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация по умолчанию.
            """
            self._cfg = cfg if cfg is not None else Config()

        def set_proxy_firefox(
            self, converted_content: str, cfg: Config | None = None
        ) -> None:
            """
            Добавляет список исключений прокси в профиль Firefox.

            Args:
                converted_content: Список исключений прокси.
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация сервиса.
            """
            if cfg is None:
                cfg = self._cfg

            if converted_content != "" and converted_content[0] == " ":
                converted_content = converted_content[1:]

            proxy_exception_name = "network.proxy.no_proxies_on"
            set_proxy_pattern = (
                f'user_pref("{proxy_exception_name}", "{converted_content}");'
            )
            path_user_js = cfg.path_browser_profile / "user.js"

            path_user_js.touch()

            user_js_content: list = [
                line
                for line in uts.read_file_line_by_line(file_path=path_user_js)
                if proxy_exception_name not in line
            ]
            user_js_content.append(f"\n{set_proxy_pattern}\n")
            path_user_js.write_text("\n".join(user_js_content) + "\n", encoding="utf-8")
