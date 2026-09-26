# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import create_task as a_create_task
from asyncio import get_running_loop as a_get_running_loop
from asyncio import sleep as a_sleep
from enum import Enum
from contextlib import asynccontextmanager
from os import getpid as os_getpid
from os import kill as os_kill
from shutil import copyfileobj
from signal import SIGINT as signal_SIGINT
from typing import Annotated
from webbrowser import open as web_open

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, File, UploadFile, Form, Request, status
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as uvicorn_run

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.app import ApplicationService as app
from src.config import Config, ServerConfig
from src.logs import SmartLogger

# ----------------------------------------------------------------------------#
# Application code                                                            #
# ----------------------------------------------------------------------------#


app_converter = app.ConverterService()
app_clear = app.ClearReportService()
cfg: Config = Config()
log: SmartLogger = SmartLogger()
log.setLevel(cfg.log_level)
templates = Jinja2Templates(directory="src/templates")


async def open_browser() -> None:
    """
    Открывает веб-интерфейс приложения в браузере.

    Функция ожидает запуска сервера, после чего открывает URL приложения
    в системном браузере. Используется только при запуске не в Docker-контейнере.
    """
    sc = ServerConfig()
    await a_sleep(1.5)
    loop = a_get_running_loop()
    loop.run_in_executor(None, web_open, f"http://{sc.host}:{sc.port}")


@asynccontextmanager
async def lifespan(web: FastAPI):
    log.info("🚀 Сервер запускается...", pretty=True)
    a_create_task(open_browser())
    yield

    log.info("🛑 Сервер останавливается...", pretty=True)
    log.debug("Начинается очистка временных файлов.", pretty=True)

    err_clear_folder = await app_clear.clear_data_folder()
    if err_clear_folder is None:
        log.debug("Очистка временных файлов прошла успешно.", pretty=True)
    else:
        log.debug(
            f"Очистка временных файлов прошла с ошибкой: {err_clear_folder}",
            pretty=True,
        )
    await a_sleep(4.5)


web = FastAPI(
    title="🌌 Proxy converter API",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "filter": True,
        "displayRequestDuration": True,
    },
    lifespan=lifespan,
)

web.mount(path="/static", app=StaticFiles(directory="src/static"), name="static")


class IsYesOrNo(str, Enum):
    """
    Перечисление вариантов ответа «да» или «нет».
    """

    YES = "Да"
    NO = "Нет"


@web.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """
    Перенаправляет пользователя на HTML-форму конвертации.

    Returns:
        HTTP-редирект на страницу ``/converter``.
    """
    return RedirectResponse(
        url="/converter", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@web.get(
    "/shutdown",
    description="Посылает запрос на остановку веб-сервера.",
    tags=["⚙️ Конфигурация"],
    summary="Остановить веб-сервер",
)
async def shutdown(request: Request) -> PlainTextResponse:
    """
    Отправляет текущему процессу сигнал остановки веб-сервера.

    Args:
        request: Текущий HTTP-запрос. Используется для выбора формата
            ответа: HTML или JSON.

    Returns:
        HTML-страница или JSON-ответ с подтверждением отправки сигнала.
    """
    os_kill(os_getpid(), signal_SIGINT)
    log.info(msg="Запрос на остановку сервера отправлен...", pretty=True)
    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(
            request=request,
            name="shutdown.html",
            status_code=status.HTTP_202_ACCEPTED,
        )
    return JSONResponse(
        content={
            "status": "ok",
            "message": "Запрос на остановку сервера отправлен",
        },
        status_code=status.HTTP_202_ACCEPTED,
    )


@web.get(path="/converter")
async def get_converter(request: Request):
    """
    Отображает HTML-форму поиска слов.

    Args:
        request: Текущий HTTP-запрос.

    Returns:
        HTML-страница с формой параметров поиска.
    """
    return templates.TemplateResponse(
        request=request, name="converter-form.html", status_code=status.HTTP_200_OK
    )


@web.post(
    path="/converter",
    tags=["📦 Комбинатор"],
    summary="Комбинатор исключений для прокси.",
    description=(
        "На вход подается Markdown файл. Комбинатор вытаскивает домены "
        "из списков, что содержатся в файле и сохраняет их в новый файл."
        f' Маркером строки с доменами служит "{cfg.marker}".'
    ),
)
async def post_converter(
    request: Request,
    marker: Annotated[
        str,
        Form(
            alias="marker",
            description="🏷️ Маркер",
            examples="*",
        ),
    ],
    upload_file: Annotated[
        UploadFile, File(alias="proxy exception", description="Файл исключений прокси")
    ],
    is_save_file: Annotated[
        IsYesOrNo,
        Form(
            alias="saving file",
            description="💾 Сохранить файл.",
            examples=[IsYesOrNo.NO],
        ),
    ],
) -> FileResponse:
    data_folder = cfg.path_data_folder
    file_location = data_folder / upload_file.filename

    data_folder.mkdir(parents=True, exist_ok=True)

    with file_location.open("wb") as buffer:
        copyfileobj(upload_file.file, buffer)

    if is_save_file == IsYesOrNo.YES:
        cfg.is_save_file = True
    else:
        cfg.is_save_file = False

    cfg.marker = marker

    converted, converted_location = app_converter.converter(
        cfg=cfg, file_location=file_location
    )

    if cfg.is_save_file:
        return FileResponse(
            path=converted_location,
            filename=converted_location.name,
            status_code=status.HTTP_200_OK,
            media_type="text/plain",
        )
    
    context = {
            "converted": converted,
        }
    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(
            request=request,
            name="converter-response.html",
            context=context,
            status_code=status.HTTP_200_OK,
        )
    
    return PlainTextResponse(content=converted, status_code=status.HTTP_200_OK)


def web_start() -> None:
    sc = ServerConfig()
    uvicorn_run(
        f"{__name__}:web",
        host=sc.host,
        port=sc.port,
        reload=sc.is_reload,
        access_log=sc.access_log,
    )


if __name__ == "__main__":
    web_start()
