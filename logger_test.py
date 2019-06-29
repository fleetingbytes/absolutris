import logging
import logging.config
import logger_conf

logging.config.dictConfig(logger_conf.final_conf)
logger = logging.getLogger("verbose_file_logger")

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical error message")