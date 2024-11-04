from typing import Optional
import socket
import ssl
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """检查URL是否有效"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def get_ip_address(domain: str) -> Optional[str]:
    """获取域名对应的IP地址"""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_ssl_expiry(hostname: str) -> Optional[dict]:
    """检查SSL证书过期时间"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return cert
    except Exception:
        return None 