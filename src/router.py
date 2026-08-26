# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pathlib import Path
from shutil import copyfileobj
from typing import Annotated
# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.config import ServerConfig, Config
from src.combinator import combinator
from src.logs import get_smart_logger, SmartLogger

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from uvicorn import run as uvicorn_run


web = FastAPI(
    title = "🌌 Proxy Combinator API",
    swagger_ui_parameters = {
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "filter": True,
        "displayRequestDuration": True
    }
)

cfg: Config = Config()
log: SmartLogger = get_smart_logger()


@web.get('/', include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(
        url='/docs',
        status_code=307
    )


@web.post(
        path='/combinator', 
        tags=["📦 Комбинатор"], 
        summary="Комбинатор исключений для прокси.", 
        description=(
            "На вход подается Markdown файл. Комбинатор вытаскивает домены "
            "из списков, что содержатся в файле и сохраняет их в новый файл."
            f" Маркером строки с доменами служит \"{cfg.marker}\".")
        )
async def web_combinator(upload_file: Annotated[UploadFile, File(alias="Proxy exception")]) -> FileResponse:
    data_folder = cfg.data_folder

    file_location = Path(data_folder) / upload_file.filename
    log.debug(msg=file_location)
    
    with file_location.open('wb') as buffer:
        copyfileobj(upload_file.file, buffer)

    result_location = combinator(file_location=file_location)
    return FileResponse(
        path=result_location,
        filename=result_location.name,
        status_code=200, 
        media_type='text/plain'
    )


def web_start() -> None:
    sc = ServerConfig()
    uvicorn_run(
        f"{__name__}:web",
        host = sc.host,
        port = sc.port,
        reload = sc.is_reload
    )


if __name__ == "__main__":
    web_start()