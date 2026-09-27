# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import create_task as a_create_task
from asyncio import get_running_loop as a_get_running_loop
from asyncio import sleep as a_sleep
from contextlib import asynccontextmanager
from enum import Enum
from os import getpid as os_getpid
from os import kill as os_kill
from shutil import copyfileobj
from signal import SIGINT as signal_SIGINT
from typing import Annotated
from webbrowser import open as web_open

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, File, Form, Request, UploadFile, status
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
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


proxy_exception_converter = app.ProxyExceptionConverter()
tmp_files_clear = app.TemporaryFileCleaner()
set_proxy_exception = app.FirefoxProxySettings()
cfg: Config = Config()
log: SmartLogger = SmartLogger()
log.setLevel(cfg.log_level)
template_renderer = Jinja2Templates(directory="src/templates")


async def open_web_interface() -> None:
    """
    Открывает веб-интерфейс приложения в браузере.

    Функция ожидает запуска сервера, после чего открывает URL приложения
    в системном браузере.

    Notes:
        Используется только при запуске вне Docker-контейнера.
    """
    sc = ServerConfig()
    await a_sleep(1.5)
    loop = a_get_running_loop()
    loop.run_in_executor(None, web_open, f"http://{sc.host}:{sc.port}")


@asynccontextmanager
async def lifespan(web: FastAPI):
    """
    Управляет жизненным циклом FastAPI-приложения.

    При запуске записывает сообщение в журнал и при необходимости открывает
    веб-интерфейс в браузере. При завершении выполняет небольшую задержку,
    чтобы корректно завершить фоновые операции.

    Args:
        web: Экземпляр FastAPI-приложения.

    Yields:
        Управление приложению на время его работы.

    Returns:
        Ничего не возвращает после завершения жизненного цикла приложения.
    """
    log.info("🚀 Сервер запускается...", pretty=True)
    a_create_task(open_web_interface())
    yield

    log.info("🛑 Сервер останавливается...", pretty=True)
    log.debug("Начинается очистка временных файлов.", pretty=True)

    await tmp_files_clear.cleanup()
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
async def redirect() -> RedirectResponse:
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
        return template_renderer.TemplateResponse(
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
async def show_converter_form(request: Request) -> Response:
    """
    Отображает HTML-форму конвертации исключений прокси.

    Args:
        request: Текущий HTTP-запрос.

    Returns:
        HTML-страница с формой параметров конвертации исключений прокси.
    """
    return template_renderer.TemplateResponse(
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
async def convert_uploaded_file(
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
    """
    Конвертирует загруженный файл с исключениями прокси.

    Извлекает домены из загруженного Markdown-файла и возвращает
    результат в виде файла, HTML-страницы или обычного текста.

    Args:
        request: Текущий HTTP-запрос.
        marker: Маркер строк, содержащих домены.
        upload_file: Загруженный файл с исключениями прокси.
        is_save_file: Флаг сохранения результата в отдельный файл.

    Returns:
        Результат конвертации в формате файла, HTML-страницы или текста.
    """
    tmp_files_directory = cfg.path_tmp_folder
    path_uploaded_file = tmp_files_directory / upload_file.filename

    tmp_files_directory.mkdir(parents=True, exist_ok=True)

    with path_uploaded_file.open("wb") as buffer:
        copyfileobj(upload_file.file, buffer)

    if is_save_file == IsYesOrNo.YES:
        cfg.is_save_file = True
    else:
        cfg.is_save_file = False

    cfg.marker = marker

    converted_content, path_converted_file = proxy_exception_converter.convert(
        cfg=cfg, path_source_file=path_uploaded_file
    )

    if cfg.is_save_file:
        return FileResponse(
            path=path_converted_file,
            filename=path_converted_file.name,
            status_code=status.HTTP_200_OK,
            media_type="text/plain",
        )

    context = {
        "converted_content": converted_content,
    }
    if "text/html" in request.headers.get("accept", ""):
        return template_renderer.TemplateResponse(
            request=request,
            name="converter-response.html",
            context=context,
            status_code=status.HTTP_200_OK,
        )

    return PlainTextResponse(content=converted_content, status_code=status.HTTP_200_OK)


@web.post(path="/set-proxy-exception/firefox")
async def update_proxy_exceptions_firefox(
    request: Request,
    converted_content: Annotated[str, Form(alias="converted content")],
) -> Response:
    """
    Обновляет список исключений прокси в профиле Firefox.

    Args:
        request: Текущий HTTP-запрос. Используется для выбора формата
            ответа: HTML или JSON.
        converted_content: Список исключений прокси для записи в профиль
            браузера.

    Returns:
        HTML-страница или JSON-ответ с результатом обновления настроек.
    """
    log.info(
        msg="Запрос на обновление списка исключений прокси в профиле Firefox отправлен.",
        pretty=True,
    )
    set_proxy_exception.update_proxy_exceptions(
        cfg=cfg, proxy_content=converted_content
    )
    log.info(
        msg="Список прокси обновлен. Изменения вступят в силу после перезагрузки браузера.",
        pretty=True,
    )
    if "text/html" in request.headers.get("accept", ""):
        return template_renderer.TemplateResponse(
            request=request,
            name="set-proxy-exception-response.html",
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={
            "status": "ok",
            "message": "Список прокси обновлен. Изменения вступят в силу после перезагрузки браузера.",
        },
        status_code=status.HTTP_200_OK,
    )


@web.post(path="/set-proxy-exception/rollback-browser-config")
async def cleaning_up_changes(
    request: Request, browser: Annotated[str, Form(alias="browser")]
) -> Response:
    """
    Удаляет изменения настроек прокси из профиля браузера.

    Args:
        request: Текущий HTTP-запрос. Используется для выбора формата
            ответа: HTML или JSON.
        browser: Название браузера, отображаемое в ответе пользователю.

    Returns:
        HTML-страница или JSON-ответ с результатом очистки настроек.
    """
    log.info(
        msg="Запрос на откат изменения конфигурации браузера отправлен.", pretty=True
    )
    set_proxy_exception.cleaning_up_changes_proxy_exceptions(
        proxy_setting_name=cfg.proxy_exception_setting_name, cfg=cfg
    )
    context = {"browser_name": browser}
    log.info(
        msg="Проведен откат изменения конфигурации браузера приложением.", pretty=True
    )
    if "text/html" in request.headers.get("accept", ""):
        return template_renderer.TemplateResponse(
            request=request,
            context=context,
            name="rollback-browser-config.html",
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={
            "status": "ok",
            "message": "Проведен откат изменения конфигурации браузера приложением.",
        },
        status_code=status.HTTP_200_OK,
    )


@web.get(path="/update-config")
async def get_config(request: Request) -> Response:
    """
    Отображает HTML-форму конфигурации приложения.

    Args:
        request: Текущий HTTP-запрос.

    Returns:
        HTML-страница с формой параметров конфигурации приложения.
    """
    return template_renderer.TemplateResponse(
        request=request, name="config.html", status_code=status.HTTP_200_OK
    )


@web.post(path="/update-config")
async def update_config(
    request: Request,
    is_default: Annotated[IsYesOrNo | None, Form(alias="is default")] = None,
    browser_profile: Annotated[str | None, Form(alias="path profile")] = None,
) -> Response:
    """
    Обновляет настройки приложения.

    Если передан параметр ``is_default`` со значением «Да», используется
    профиль браузера по умолчанию. Иначе сохраняется переданный путь
    к пользовательскому профилю браузера.

    Args:
        request: Текущий HTTP-запрос. Используется для выбора формата
            ответа: HTML или JSON.
        is_default: Флаг использования профиля браузера по умолчанию.
            Если выбран вариант «Да», пользовательский путь удаляется.
        browser_profile: Путь к пользовательскому профилю браузера.
            Если не передан, текущая настройка не изменяется.

    Returns:
        HTML-страница или JSON-ответ с результатом обновления конфигурации.
    """
    if is_default == IsYesOrNo.YES:
        cfg.custom_browser_profile = None
        if "text/html" in request.headers.get("accept", ""):
            return template_renderer.TemplateResponse(
                request=request,
                name="config.html",
                status_code=status.HTTP_200_OK,
            )
        return JSONResponse(
            content={
                "status": "ok",
                "message": "Проведен откат изменения конфигурации приложения.",
            },
            status_code=status.HTTP_200_OK,
        )
    if browser_profile is not None:
        cfg.custom_browser_profile = browser_profile

    if "text/html" in request.headers.get("accept", ""):
        return template_renderer.TemplateResponse(
            request=request,
            name="config.html",
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={
            "status": "ok",
            "message": "Проведено обновление конфигурации приложения.",
        },
        status_code=status.HTTP_200_OK,
    )


def start_web_server() -> None:
    """
    Запускает FastAPI-приложение с помощью Uvicorn.

    Параметры хоста, порта, режима перезагрузки и флага журнала доступа
    считываются из конфигурации приложения.
    """
    sc = ServerConfig()
    uvicorn_run(
        f"{__name__}:web",
        host=sc.host,
        port=sc.port,
        reload=sc.is_reload,
        access_log=sc.access_log,
    )


if __name__ == "__main__":
    start_web_server()
