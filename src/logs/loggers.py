# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from logging import (
    Logger as LibLogger, StreamHandler as LibStreamHandler, 
    FileHandler as LibFileHandler, Formatter as LibFormatter, 
    addLevelName as libAddLevelName, setLoggerClass as libSetLoggerClass, 
    getLogger as libGetLogger, 
    DEBUG, INFO, ERROR, WARNING, CRITICAL, getLevelNamesMapping, LogRecord
    )
from os import makedirs
from sys import stdout, exit
from typing import Any, Optional, Dict

from colorama import Fore as color_Fore


class SmartLogger(LibLogger):
    """Logger с дополнительными возможностями форматирования и кастомными уровнями.

    Расширяет стандартный `logging.Logger`, добавляя:
    * флаг `raw` — вывод сообщения без стандартного форматирования;
    * флаг `empty_console` — подавление вывода в консоль;
    * метод `add_custom_level` для регистрации пользовательских уровней логирования.
    """

    def __init__(self, name: str):
        """Создает экземпляр SmartLogger.

        Args:
            name: Имя logger.
        """
        
        super().__init__(name=name)
    
    
    def __str__(self) -> str:
        """Возвращает строковое представление доступных уровней логирования."""
        
        return f"Logger levels: {getLevelNamesMapping()}"


    def _prepare_extra(
        self,
        raw: bool,
        empty_console: bool,
        pretty: bool,
        extra: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """Формирует поле `extra` с флагами форматирования.

        Если `raw` или `empty_console` заданы, то в словарь `extra`
        добавляются соответствующие ключи.

        Args:
            raw: Если True, форматирование сообщения упрощается до `{message}`.
            empty_console: Если True, сообщение не выводится в консоль.
            extra: Дополнительные данные для лог-записи.

        Returns:
            Обновлённый словарь `extra` или None.
        """

        if raw or empty_console or pretty: 
            if extra is None: extra = {}
            extra['raw'] = raw
            extra['empty_console'] = empty_console
            extra['pretty'] = pretty
        return extra


    def debug(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня DEBUG с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """

        extra = self._prepare_extra(raw=raw, empty_console=empty_console, pretty=pretty, extra=extra)
        super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)
    

    def info(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня INFO с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """

        extra = self._prepare_extra(raw=raw, empty_console=empty_console, pretty=pretty, extra=extra)
        super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def warning(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня WARNING с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """
        
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, pretty=pretty, extra=extra)
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def error(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня ERROR с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """

        extra = self._prepare_extra(raw=raw, empty_console=empty_console, pretty=pretty, extra=extra)
        super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def critical(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        is_continue: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня CRITICAL с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            is_continue: Если True, продолжает работу программы после своего вызова.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """
        
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, pretty=pretty, extra=extra)
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)

        if not is_continue:
            exit()
    
    def fatal(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        pretty: bool = False,
        is_continue: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        """Логирует сообщение уровня CRITICAL с дополнительными флагами форматирования.

        Args:
            msg: Сообщение для логирования.
            *args: Позиционные аргументы для форматирования сообщения.
            raw: Если True, сообщение выводится без стандартного форматирования.
            empty_console: Если True, подавляет вывод в консоль.
            is_continue: Если True, продолжает работу программы после своего вызова.
            exc_info: Информация об исключении или флаг для её добавления.
            stack_info: Если True, добавляет информацию о стеке.
            stacklevel: Смещение уровня стека для корректного указания места вызова.
            extra: Дополнительные данные для лог-записи.
            **kwargs: Дополнительные параметры, пробрасываемые в базовый logger.
        """
        
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)
        
        if not is_continue:
            exit()

    def add_custom_level(
        self, 
        level_name: str, 
        level_num: int, 
        is_duplicate_level_num: bool = False, 
        filename: Optional[str] = None, 
        is_create_file_level: bool = True
    ) -> None:
        """Регистрирует новый пользовательский уровень логирования и метод для него.

        Создает новый уровень в `logging`, добавляет соответствующий
        метод на класс `SmartLogger` и, при необходимости, файловый
        handler, пишущий только этот уровень.

        Args:
            level_name: Имя уровня (например, "TRACE").
            level_num: Числовое значение уровня.
            is_duplicate_level_num: Если False, проверяет, что число уровня не занято.
            filename: Имя файла для логов этого уровня. Если не указано,
                используется `logs/logs_<method_name>.log`.
            is_create_file_level: Если True, создается файловый handler для уровня.

        Raises:
            ValueError: Если `is_duplicate_level_num` False и уровень уже существует.
            AttributeError: Если метод с таким именем уже есть у `SmartLogger`.
        """

        if not is_duplicate_level_num:
            levels = getLevelNamesMapping()
            if level_num in levels.values():
                raise ValueError(f"Level number {level_num} is already used")
        
        method_name = level_name.lower()
        libAddLevelName(level_num, level_name)
        
        def custom_log_method(self, message, *args, **kwargs) -> None:
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, **kwargs, stacklevel=2)

        if hasattr(SmartLogger, method_name):
            raise AttributeError(f"Method '{method_name}' already exists in Logger")

        setattr(SmartLogger, method_name, custom_log_method)

        if is_create_file_level:
            makedirs(name="logs", exist_ok=True)
            if filename is None:
                filename = f"logs/logs_{method_name}.log"
            elif "/" not in filename:
                filename = f"logs/logs_{filename}.log"
            add_handler(logger=self, level=level_num, filename=filename, exact=True)


class StreamHandler(LibStreamHandler):
    """Обработчик вывода в поток с поддержкой 'raw' и 'empty_console' флагов.

    Использует разные форматеры в зависимости от полей записи лога:
    * `record.raw == True` — выводится только сообщение (`{message}`);
    * `record.empty_console == True` — запись не выводится в консоль.
    """

    def __init__(self, stream=None) -> None:
        """Создает StreamHandler с преднастоенными форматерами.

        Args:
            stream: Поток вывода (по умолчанию sys.stdout).
        """

        super().__init__(stream)

        self.normal_formatter = LibFormatter(
            fmt=basic_format, 
            style="{", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.raw_formatter = LibFormatter(
            fmt="{message}", 
            style="{"
        )

        info_fmt = f"{color_Fore.CYAN}{{levelname}}{color_Fore.RESET}:     {{message}}"
        debug_fmt = f"{color_Fore.GREEN}{{levelname}}{color_Fore.RESET}:     {{message}}"
        warning_fmt = f"{color_Fore.YELLOW}{{levelname}}{color_Fore.RESET}:     {{message}}"
        error_fmt = f"{color_Fore.RED}{{levelname}}{color_Fore.RESET}:     {{message}}"
        critical_fmt = f"{color_Fore.MAGENTA}{{levelname}}{color_Fore.RESET}:     {{message}}"

        self.debug_formatter = LibFormatter(fmt=debug_fmt, style="{")
        self.info_formatter = LibFormatter(fmt=info_fmt, style="{")
        self.warning_formatter = LibFormatter(fmt=warning_fmt, style="{")
        self.error_formatter = LibFormatter(fmt=error_fmt, style="{")
        self.critical_formatter = LibFormatter(fmt=critical_fmt, style="{")


    def emit(self, record: LogRecord) -> None:
        """Выводит лог-запись в поток в зависимости от флагов записи.

        Если у записи установлен `empty_console`, вывод подавляется.
        В противном случае выбирается форматер в зависимости от флага `raw`.

        Args:
            record: Лог-запись для вывода.
        """
        
        if getattr(record, 'empty_console', False):
            return None
        
        if getattr(record, 'raw', False):
            self.formatter = self.raw_formatter
        elif getattr(record, 'pretty', False):
            level = record.levelno
            if level == DEBUG:
                self.formatter = self.debug_formatter
            elif level == INFO:
                self.formatter = self.info_formatter
            elif level == WARNING:
                self.formatter = self.warning_formatter
            elif level == ERROR:
                self.formatter = self.error_formatter
            elif level == CRITICAL:
                self.formatter = self.critical_formatter
        else:
            self.formatter = self.normal_formatter
        
        super().emit(record)


def add_handler(logger: SmartLogger, level: int, filename: Optional[str] = None, exact: bool = False) -> None:
    """Добавляет обработчик к logger.

    В зависимости от `filename` добавляется либо файловый, либо потоковый
    обработчик. При `exact=True` обработчик будет получать только записи
    строго заданного уровня.

    Args:
        logger: Экземпляр SmartLogger, к которому добавляется обработчик.
        level: Уровень логирования для обработчика.
        filename: Путь к файлу логов. Если None, используется поток stdout.
        exact: Если True, обработчик фильтрует записи по точному соответствию
            уровня `level`.
    """
    
    if filename:
        handler = LibFileHandler(filename, encoding='utf-8')
        handler.setFormatter(LibFormatter(fmt=basic_format, style="{", datefmt="%Y-%m-%d %H:%M:%S"))
    else:
        handler = StreamHandler(stdout)
    handler.setLevel(level)
    if exact:
        handler.addFilter(lambda record: record.levelno == level)
    logger.addHandler(handler)


def basic_configuration(logger: SmartLogger, all_level: int = DEBUG) -> SmartLogger:
    """Выполняет базовую настройку SmartLogger.

    Настраивает:
    * уровень logger;
    * консольный обработчик;
    * файловые обработчики для уровней DEBUG, INFO, WARNING, ERROR, CRITICAL;
    * общий файловый лог для всех уровней, начиная с `all_level`.

    Args:
        logger: Экземпляр SmartLogger для настройки.
        all_level: Минимальный уровень логирования для консоли и общего файла.

    Returns:
        Настроенный экземпляр SmartLogger.
    """
    
    logger.setLevel(level=all_level)
    logger.propagate = False
    
    # Console
    add_handler(logger=logger, level=all_level)

    # File
    makedirs(name='logs', exist_ok=True)
    add_handler(logger=logger, level=DEBUG, filename="logs/logs_debug.log", exact=True)
    add_handler(logger=logger, level=INFO, filename="logs/logs_info.log", exact=True)
    add_handler(logger=logger, level=WARNING, filename="logs/logs_warning.log", exact=True)
    add_handler(logger=logger, level=ERROR, filename="logs/logs_error.log", exact=True)
    add_handler(logger=logger, level=CRITICAL, filename="logs/logs_critical.log", exact=True)

    add_handler(logger=logger, level=all_level, filename="logs/logs_all_levels.log")
    return logger


def get_smart_logger(name: str = "smart_logger", all_level: int = DEBUG) -> SmartLogger:
    """Возвращает настроенный экземпляр SmartLogger.

    Если logger с указанным именем еще не имеет обработчиков,
    к нему применяется `basic_configuration`.

    Args:
        name: Имя logger.
        all_level: Минимальный уровень логирования для базовой конфигурации.

    Returns:
        Экземпляр SmartLogger с установленными обработчиками.
    """
    
    logger: SmartLogger = libGetLogger(name=name)
    if not logger.handlers:
        basic_configuration(logger=logger, all_level=all_level)
    return logger


libSetLoggerClass(SmartLogger)
basic_format: str = ("{asctime} | {levelname} | "
    "{filename} -> {funcName}: line {lineno} | "
    "Message: {message}")
pretty_format: str = (color_Fore.GREEN + "{levelname}" + color_Fore.RESET + ":     {message}")
