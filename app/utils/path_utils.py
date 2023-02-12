import posixpath
import urllib.parse


def urljoin(prefix: str, *paths: str) -> str:
    parse = urllib.parse.urlparse(prefix)
    path = posixpath.join(parse.path, *paths)
    return urllib.parse.urlunparse(parse._replace(path=path))


def filejoin(prefix: str, *paths: str) -> str:
    return posixpath.join(prefix, *paths)
