import requests

import app.config as config
from app.service.log import logger


RETRY_COUNT = 2

session = requests.Session()


def retry_request_decorator(func):
    """
    Retry up to RETRY_COUNT times on timeout.

    Return None if request failed.
    """

    def wrapper(*args, **kwargs):
        for try_ in range(RETRY_COUNT + 1):
            try:
                return func(*args, **kwargs, timeout=config.timeout)
            except requests.Timeout as error:
                logger.error("Request timed out, retrying... (%d)", try_ + 1)
                continue
            except requests.RequestException as error:
                logger.error("Request failed: %s", error)
                return

    return wrapper


@retry_request_decorator
def get(*args, **kwargs):
    return session.get(*args, **kwargs)


@retry_request_decorator
def post(*args, **kwargs):
    return session.post(*args, **kwargs)
