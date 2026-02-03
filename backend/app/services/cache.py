from __future__ import annotations

import json
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings

_client: Redis | None = None


def _get_client() -> Redis | None:
    global _client
    if settings.redis_url is None:
        return None
    if _client is None:
        _client = Redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def cache_get(key: str) -> Any | None:
    client = _get_client()
    if client is None:
        return None
    try:
        raw = client.get(key)
    except RedisError:
        return None
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def cache_set(key: str, value: Any, ttl_seconds: int | None = None) -> None:
    client = _get_client()
    if client is None:
        return
    try:
        payload = json.dumps(value, ensure_ascii=True)
        client.set(key, payload, ex=ttl_seconds)
    except (TypeError, RedisError):
        return


def cache_delete(key: str) -> None:
    client = _get_client()
    if client is None:
        return
    try:
        client.delete(key)
    except RedisError:
        return


def cache_delete_pattern(pattern: str) -> None:
    client = _get_client()
    if client is None:
        return
    try:
        keys = list(client.scan_iter(match=pattern))
        if keys:
            client.delete(*keys)
    except RedisError:
        return
