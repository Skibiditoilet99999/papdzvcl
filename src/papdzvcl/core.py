import requests
from typing import Optional, Dict, Any
from .exceptions import Ok1Exception, Ok2Exception, Ok3Exception

class PapdzVCL:
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PapdzVCL/1.0.0',
            'Accept': 'application/json',
        })
    
    def Ok1(self, url: str, **kwargs):
        try:
            full_url = self._build_url(url)
            response = self.session.get(full_url, timeout=self.timeout, **kwargs)
            return response
        except Exception as e:
            raise Ok1Exception(f"Ok1 failed: {str(e)}")
    
    def Ok2(self, url: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        try:
            full_url = self._build_url(url)
            response = self.session.post(full_url, data=data, json=json, timeout=self.timeout, **kwargs)
            return response
        except Exception as e:
            raise Ok2Exception(f"Ok2 failed: {str(e)}")
    
    def Ok3(self, url: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        try:
            full_url = self._build_url(url)
            response = self.session.put(full_url, data=data, json=json, timeout=self.timeout, **kwargs)
            return response
        except Exception as e:
            raise Ok3Exception(f"Ok3 failed: {str(e)}")
    
    def _build_url(self, url: str) -> str:
        if self.base_url and not url.startswith(('http://', 'https://')):
            return f"{self.base_url}/{url.lstrip('/')}"
        return url
    
    def set_header(self, key: str, value: str):
        self.session.headers[key] = value
    
    def set_auth(self, token: str):
        self.session.headers['Authorization'] = f'Bearer {token}'

def Ok1(url: str, **kwargs):
    with PapdzVCL() as client:
        return client.Ok1(url, **kwargs)

def Ok2(url: str, **kwargs):
    with PapdzVCL() as client:
        return client.Ok2(url, **kwargs)

def Ok3(url: str, **kwargs):
    with PapdzVCL() as client:
        return client.Ok3(url, **kwargs)
