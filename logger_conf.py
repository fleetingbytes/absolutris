root_formatter_conf = {
    "format": "{asctime}.{msecs:03.0f} {levelname:>9s} {module} {funcName}: {message}",
    "style": "{",
    # "datefmt": "%Y-%m-%d %H:%M:%S",
    "datefmt": "%a %H:%M:%S",
}

verbose_formatter_conf = root_formatter_conf

formatters_dict = {
    "root_formatter": root_formatter_conf,
    "verbose_formatter": verbose_formatter_conf,
}

root_handler_conf = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "root_formatter",
    "stream": "ext://sys.stdout",
}

logfile_handler_conf = {
    "class": "logging.FileHandler",
    "level": "DEBUG",
    "formatter": "verbose_formatter",
    "filename": "logfile.txt",
    "mode": "w",
    "encoding": "utf-8",
}

handlers_dict = {
    "root_handler": root_handler_conf,
    "logfile_handler": logfile_handler_conf,
}

verbose_file_logger_conf = {
    "propagate": True,
    "handlers": ["logfile_handler"],
    "level": "DEBUG",
}

root_logger_conf = {
    "handlers": ["root_handler"],
    "level": "DEBUG",
}

loggers_dict = {
    "verbose_file_logger": verbose_file_logger_conf
}

final_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": formatters_dict,
    "handlers": handlers_dict,
    "loggers": loggers_dict,
    "root": root_logger_conf,
    "incremental": False,
}
