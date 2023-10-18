#!/usr/bin/env python3
"""A module for web-related functions."""

import requests
import redis
from cachetools import TTLCache
from functools import wraps
from typing import Callable

# Create a cache with a TTL (time to live) of 10 seconds
cache = TTLCache(maxsize=128, ttl=10)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def redis_cache(func: Callable) -> Callable:
    """A decorator for caching function results using Redis."""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Check if the result is cached in Redis
        cached_result = redis_client.get(f'count:{url}')
        if cached_result is not None:
            return cached_result.decode('utf-8')
        
        # If not cached, call the original function and cache the result
        result = func(url)
        redis_client.set(f'count:{url}', result)
        return result

    return wrapper

@redis_cache
def get_page(url: str) -> str:
    """Get the HTML content of a URL and cache the result with a 10-second expiration."""
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    # Example usage of the get_page function
    html_content = get_page('http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com')
    print(html_content)
