from fastapi import Request
from cachetools import TTLCache
import os

TTL = int(os.getenv("MAPPING_TTL", 300))
mapping_cache = TTLCache(maxsize=1000, ttl=TTL)


def get_client_ip(request: Request) -> str:

    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    client = request.client
    if client:
        return client.host

    return "unknown"


def save_hostname_ip(hostname: str, ip: str) -> None:
    mapping_cache[hostname] = ip


def get_ip_by_hostname(hostname: str) -> str | None:
    return mapping_cache.get(hostname)