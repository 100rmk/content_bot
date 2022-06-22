import io
import urllib.request


def get_content_bytes(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        dataset = io.BytesIO(resp.read())
    return dataset
