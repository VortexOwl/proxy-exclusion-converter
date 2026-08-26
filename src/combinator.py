# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pathlib import Path
# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.config import Config
from src.logs import get_smart_logger, SmartLogger
from src.utilities import Utilities


cfg: Config = Config()
logs: SmartLogger = get_smart_logger()
uts: Utilities = Utilities()


def combinator(file_location: Path) -> Path:
    marker = cfg.marker
    
    result_location = Path(file_location.parent / f"{file_location.stem}.txt")
    with result_location.open('w', encoding = 'utf-8') as result_file:
        for line in uts.read_file_line_by_line(file_path = file_location):
            if len(line) > 0 and line[0] == marker:
                result_file.write(f"{line[1:]}")

    return result_location
