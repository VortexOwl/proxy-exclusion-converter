# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import to_thread as asyncio_to_thread
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from logs import get_smart_logger


@dataclass
class Utilities:
    _log = get_smart_logger()

    @staticmethod
    def read_file_line_by_line(file_path: Path, encoding = 'utf-8') -> Iterator[str]:
        """
        Читает файл построчно передавая в буфер данные по одной строке.
        Полезен при файлах большого объема.
        """
        with file_path.open('r', encoding=encoding) as file:
            for line in file:
                yield line.strip()

    @classmethod
    async def clearing_folder(cls, clear_folder: str) -> dict[str, int | tuple[str]]:
        """
        Асинхронно и безопасно очищает папку от файлов.
        Возвращает статистику по успешным удалениям и ошибкам.
        """
        path_clear_folder = Path.cwd() / clear_folder
        
        if not path_clear_folder.exists() or not path_clear_folder.is_dir():
            name_err = f"Путь не существует или не является папкой: {path_clear_folder}"
            cls._log.warning(msg=name_err)
            return {"success": 0, "errors": 1, "names of errors": (name_err)}

        stats = {"success": 0, "errors": 0}
        names_err = set()

        for file_name in path_clear_folder.iterdir():
            try:
                if file_name.is_file():
                    await asyncio_to_thread(file_name.unlink, missing_ok=True)
                    stats["success"] += 1

            except PermissionError:
                name_err = f"Нет прав на удаление файла: {file_name}"
                cls._log.error(msg=name_err)
                stats["errors"] += 1
                names_err.add(name_err)

            except FileNotFoundError:
                pass
                
            except Exception as err:
                name_err = f"Не удалось удалить {file_name}. Ошибка: {err}"
                cls._log.exception(msg=name_err)
                stats["errors"] += 1
                names_err.add(name_err)
        
        stats["names of errors"] = tuple(names_err)
        cls._log.info(msg=f"В директории {clear_folder} была проведена очистка от файлов.")
        cls._log.debug(msg=f"Сводка выполнения очистки:\n{stats}")
        return stats