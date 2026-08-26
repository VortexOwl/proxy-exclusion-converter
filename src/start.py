# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities.basic_utilities_project import add_workdir_in_PATH
add_workdir_in_PATH()
from router import web_start


def start() -> None:
    web_start()


if __name__ == "__main__":
    start()