import logging
import logging.handlers
from pathlib import Path
import sys

from .constants import (
    DEFAULT_LOG_DATE_FMT,
    DEFAULT_LOG_FMT,
    LOG_BACKUP_COUNT,
    LOG_MESSAGE_SIZE_FILE,
    LOG_MESSAGE_SIZE_STREAM,
    MAX_LOG_FILE_SIZE,
)


def prepare_logger(log_file_path: Path):
    root_logger = logging.getLogger()

    def close_handler(old_handler: logging.Handler):
        old_handler.flush()
        old_handler.close()
        root_logger.removeHandler(old_handler)

    for old_handler in root_logger.handlers[::]:
        close_handler(old_handler)

    main_file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path, maxBytes=MAX_LOG_FILE_SIZE, backupCount=LOG_BACKUP_COUNT
    )
    main_file_formatter = logging.Formatter(DEFAULT_LOG_FMT % (LOG_MESSAGE_SIZE_FILE,), DEFAULT_LOG_DATE_FMT)
    main_file_formatter = logging.Formatter(DEFAULT_LOG_FMT % (LOG_MESSAGE_SIZE_FILE,), DEFAULT_LOG_DATE_FMT)
    main_file_handler.setLevel(logging.DEBUG)
    main_file_handler.setFormatter(main_file_formatter)
    root_logger.addHandler(main_file_handler)

    main_stream_handler = logging.StreamHandler(sys.stdout)
    main_stream_formatter = logging.Formatter(DEFAULT_LOG_FMT % (LOG_MESSAGE_SIZE_STREAM,), DEFAULT_LOG_DATE_FMT)
    main_stream_handler.setLevel(logging.INFO)
    main_stream_handler.setFormatter(main_stream_formatter)
    root_logger.addHandler(main_stream_handler)

    root_logger.setLevel(logging.NOTSET)
