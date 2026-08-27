# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from shutil import copyfileobj
from typing import Annotated
from time import sleep as time_sleep
from webbrowser import open as web_open

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.config import ServerConfig, Config
from src.combinator import combinator, clear_tmp_folder
from src.logs import get_smart_logger, SmartLogger

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from uvicorn import run as uvicorn_run


cfg: Config = Config()
log: SmartLogger = get_smart_logger()
log.setLevel(cfg.log_level)


async def open_browser():
    sc = ServerConfig()
    await asyncio.sleep(1.5)
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, web_open, f"http://{sc.host}:{sc.port}")


@asynccontextmanager
async def lifespan(web: FastAPI):
    data_folder = Path(cfg.data_folder)

    log.info("🚀 Сервер запускается...", pretty=True)
    asyncio.create_task(open_browser())
    yield

    log.info("🛑 Сервер останавливается...", pretty=True)
    log.debug("Начинается очистка временных файлов.", pretty=True)

    err_clear_folder = clear_tmp_folder(data_folder)
    if err_clear_folder is None:
        log.debug("Очистка временных файлов прошла успешно.", pretty=True)
    else:
        log.debug(f"Очистка временных файлов прошла с ошибкой: {err_clear_folder}", pretty=True)
    time_sleep(4.5)

        

web = FastAPI(
    title = "🌌 Proxy Combinator API",
    swagger_ui_parameters = {
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "filter": True,
        "displayRequestDuration": True
    },
    lifespan=lifespan
)


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
    data_folder = Path(cfg.data_folder)
    data_folder.mkdir(parents=True, exist_ok=True)
    file_location = data_folder / upload_file.filename
    
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
        reload = sc.is_reload,
        access_log=sc.access_log
    )


if __name__ == "__main__":
    web_start()