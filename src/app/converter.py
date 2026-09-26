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
    class ClearReportService:
        """Очищает директорию для хранения временных файлов."""

        def __init__(self, cfg: Config | None = None):
            """
            Инициализирует сервис удаления временных файлов.

            Args:
                cfg: Конфигурация приложения. Если не передана,
                    используется конфигурация по умолчанию.
            """
            self._cfg = cfg if cfg is not None else Config()

        async def clear_data_folder(self) -> dict[str, int | tuple[str]]:
            """
            Удаляет файлы из каталога отчётов.

            Returns:
                Словарь со статистикой удаления: количеством успешно
                удалённых файлов и количеством ошибок.
            """
            return await uts.clearing_folder(clear_folder=self._cfg.data_folder)

    class ConverterService:
        def __init__(
            self, cfg: Config | None = None, log: SmartLogger | None = None
        ) -> None:
            self._cfg = cfg if cfg is not None else Config()
            self._log = log if log is not None else SmartLogger()
            self._log = log if log is not None else SmartLogger()
            self._log.setLevel(self._cfg.log_level)

        def converter(
            self,
            file_location: Path,
            cfg: Config | None = None,
            marker: str | None = None,
        ) -> tuple[str, Path | None]:
            """Преобразование файла в список исключений для прокси."""
            if cfg is None:
                cfg = self._cfg

            if marker is None:
                marker = cfg.marker

            self._log.info(
                "Начинается преобразование файла в список исключений для прокси.",
                pretty=True,
            )
            converted: str = ""
            converted_location: Path | None = None

            for line in uts.read_file_line_by_line(file_path=file_location):
                if len(line) > 0 and line[0] == marker:
                    converted = f"{converted}{line[1:]}"

            if cfg.is_save_file:
                converted_location = Path(
                    file_location.parent / f"{file_location.stem}.txt"
                )
                with converted_location.open("w", encoding="utf-8") as converted_file:
                    converted_file.write(converted)

            self._log.info(
                "Преобразование файла в список исключений для прокси прошло успешно.",
                pretty=True,
            )
            return converted, converted_location
