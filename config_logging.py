import loguru


def setup_logger():
    logger = loguru.logger
    logger.remove()
    logger.add(f"logs.logs", format="{time} {level} {message}", level="INFO", rotation="10 MB")
    return logger
