from logging import ERROR
from logging import Formatter
from logging import getLogger
from logging import Logger
from os import path

__DIR_PATH: str = path.dirname(path.realpath(__file__))
__LOG_FILE_NAME: str = f'{__DIR_PATH}/log_error.log'
__LOGGING_FORMAT_PATTER: str = '%(asctime)s - %(module)s - %(filename)s - %(pathname)s - %(levelname)s - %(levelno)s - %(lineno)d  - %(message)s'


def __loggerror(expt: Exception) -> None:
    print(f'Error: {expt}')


def __get_start(name: str) -> Logger:
    logger: Logger = getLogger(name=name)
    try:
        # basicConfig(filename=__LOG_FILE_NAME, filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=DEBUG)
        Formatter(fmt=__LOGGING_FORMAT_PATTER, datefmt=None, style='%', validate=True)
        logger.setLevel(ERROR)

        # fh = FileHandler(__LOG_FILE_NAME)
        # fh.setLevel(DEBUG)
        # logger.addHandler(fh)

    except Exception as err:
        __loggerror(expt=err)

    return logger


def set_logging_debug(msg: str, tracing: str, name: str) -> None:
    try:

        msg_info: str = f'{msg}. {tracing}'
        logger: Logger = __get_start(name=name)
        logger.debug(msg=msg_info, exc_info=True, stack_info=True)

    except Exception as err:
        __loggerror(expt=err)


def set_logging_info(msg: str, tracing: str, name: str) -> None:
    try:
        logger: Logger = __get_start(name=name)
        logger.info(msg=f'{msg}. {tracing}', exc_info=True, stack_info=True)

    except Exception as err:
        __loggerror(expt=err)


def set_logging_warning(msg: str, tracing: str, name: str) -> None:
    try:
        logger: Logger = __get_start(name=name)
        logger.warning(msg=f'{msg}. {tracing}', exc_info=True, stack_info=True)
    except Exception as err:
        __loggerror(expt=err)


def set_logging_error(msg: str, tracing: str, name: str) -> None:
    try:
        logger: Logger = __get_start(name=name)
        logger.error(msg=f'{msg}. {tracing}', exc_info=True, stack_info=True)
    except Exception as err:
        __loggerror(expt=err)


def set_logging_exception(exc: Exception) -> None:
    try:
        logger: Logger = __get_start(__name__)
        logger.exception(exc)
    except Exception as err:
        __loggerror(expt=err)


def set_logging_critical(msg: str, tracing: str, name: str) -> None:
    try:
        logger: Logger = __get_start(name=name)
        logger.critical(msg=f'{msg}. {tracing}', exc_info=True, stack_info=True)
    except Exception as err:
        __loggerror(expt=err)

