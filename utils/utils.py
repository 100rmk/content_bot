import io
import urllib.request

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
