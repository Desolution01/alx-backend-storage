#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""

import redis
import requests
from functools import wraps

# Initialize the Redis connection
r = redis.Redis(host='127.0.0.1', port=6379)

def url_access_count(method):
    """Decorator for the get_page function.

    This decorator wraps the get_page function to provide caching and tracking features.

    Args:
        method (function): The function to be decorated.

    Returns:
        function: The wrapped function with caching and tracking.
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function for get_page.

        This function caches the HTML content of a URL and tracks its access count.

        Args:
            url (str): The URL to fetch HTML content from.

        Returns:
            str: The HTML content of the URL.
        """
        key = f"cached:{url}"
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = f"count:{url}"
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        return html_content

    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    results = requests.get(url)
    return results.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
