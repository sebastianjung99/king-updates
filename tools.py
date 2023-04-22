import coloredlogs, logging


# configurate logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(coloredlogs.ColoredFormatter(log_format))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)