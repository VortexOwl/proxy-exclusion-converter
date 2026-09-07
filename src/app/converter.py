# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pathlib import Path
from shutil import rmtree

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.config import Config
from src.logs import get_smart_logger, SmartLogger
from src.utilities import Utilities 


cfg: Config = Config()
log: SmartLogger = get_smart_logger()
log.setLevel(cfg.log_level)
uts: Utilities = Utilities()


class ApplicationService:
    @classmethod
    def converter(cls, file_location: Path) -> Path:
        """Преобразование файла в список исключений для прокси."""
        marker = cfg.marker

        log.info("Начинается преобразование файла в список исключений для прокси.", pretty = True)
        result_location = Path(file_location.parent / f"{file_location.stem}.txt")
        with result_location.open('w', encoding = 'utf-8') as result_file:
            for line in uts.read_file_line_by_line(file_path = file_location):
                if len(line) > 0 and line[0] == marker:
                    result_file.write(f"{line[1:]}")

        log.info("Преобразование файла в список исключений для прокси прошло успешно.", pretty = True)
        return result_location

    @classmethod
    def clear_tmp_folder(cls, tmp_folder: Path) -> str | None:
        """Очистка папки."""
        try:
            if tmp_folder.exists():
                rmtree(tmp_folder)
            tmp_folder.mkdir(parents=True, exist_ok=True)
            return None
        except Exception as err:
            return str(err)