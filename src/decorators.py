import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции, результатов или ошибок.
    filename: имя файла для записи логов. Если None — логи в консоль (stdout).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            logger.propagate = False

            # Очищаем старые хендлеры, чтобы не дублировать при повторных вызовах
            if logger.hasHandlers():
                logger.handlers.clear()

            handler = (
                logging.FileHandler(filename, encoding="utf-8")
                if filename
                else logging.StreamHandler(sys.stdout)  # <-- пишем в stdout
            )

            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                logger.info(f"{func.__name__} start")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                args_repr = ", ".join(repr(a) for a in args)
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

                inputs_repr = f"({args_repr}"
                if args and kwargs:
                    inputs_repr += ", "
                if kwargs:
                    inputs_repr += kwargs_repr
                inputs_repr += ")"

                logger.error(
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs_repr}"
                )
                raise
            finally:
                logger.removeHandler(handler)
                handler.close()

        return wrapper

    return decorator
