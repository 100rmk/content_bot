import io
import logging
import urllib.request
from logging import Handler

from etc.exceptions import ConfigError


def get_content_bytes(url: str):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        dataset = io.BytesIO(resp.read())
    return dataset


def check_config(config: object):
    for key, value in config.__dict__.items():
        if not key.startswith('__'):
            if not value:
                raise ConfigError(f'Missed config parameter {key}')

def init_logger(name: str, level: int, handler: Handler):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
