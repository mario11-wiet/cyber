from urllib.parse import urlparse, urlunparse


def parse(url):
    if not urlparse(url).scheme:
        https_url = urlparse('https://' + url)
        https_url = urlunparse(https_url._replace(scheme='https', netloc=url))
        return https_url

    return url


def url_parse(func):
    def wrapper(*args, **kwargs):
        modified_args = args[0], *[parse(arg) for arg in args[1:]]
        return func(*modified_args, **kwargs)

    return wrapper
