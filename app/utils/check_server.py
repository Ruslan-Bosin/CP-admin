import requests
from config import BASE_URL


def check_server():
    url = f"{BASE_URL}/is_server_on"
    timeout = 5
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
