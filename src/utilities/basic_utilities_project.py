# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import dirname, abspath
from sys import path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities.config import BaseConfig


def add_workdir_in_PATH() -> None:
    """
    Добавляет рабочую директорию в PYTHONPATH. 
    Необходимо для импорта директории src в файлах проекта.
    """
    
    if BaseConfig.is_not_active:
        work_folder: str = dirname(dirname(dirname(abspath(__file__))))
        path.insert(0, work_folder)
        BaseConfig.is_not_active = False
        if BaseConfig.is_console_debug:
            print(
                f'Working folder: {work_folder}'
            )
