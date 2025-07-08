from urllib.parse import urlparse

def clean_url(url):
    """Remove fragments and trailing slashes for consistency."""
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip('/')

def is_valid_url(url):
    """Basic check to validate URL format."""
    return url.startswith("http://") or url.startswith("https://")

def is_same_domain(url, base):
    """Check if the URL belongs to the same domain as base."""
    return urlparse(url).netloc == urlparse(base).netloc
