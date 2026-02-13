import time
import functools
import requests

from difflib import SequenceMatcher
from urllib.parse import urlparse
from config import DEBUG


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        duration = end_time - start_time
        if DEBUG:
            print(f"⏱️ '{func.__name__}': {duration:.4f} seconds")
        return result
    return wrapper

def calculate_similarity(store_name, url):
    path = urlparse(url).path
    slug = path.split('/')[-1] if not path.endswith('/') else path.split('/')[-2]
    
    clean_store_name = store_name.lower().replace(" ", "")
    clean_slug = slug.lower().replace("-", "").replace("_", "")
    
    similarity = SequenceMatcher(None, clean_store_name, clean_slug).ratio()
    
    return similarity
    
def get_normalized_name(name):
        normalized_name = name.lower().replace(" ", "-").replace("!", "")
        
        return normalized_name
    
def get_last_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        status_code = response.status_code
        if status_code == 200:
            return response.url.split("?")[0]
        elif status_code == 404:
            return None
        else:
            raise Exception(f"NEW ERROR: {status_code} --> {url}")
    except:
        return None