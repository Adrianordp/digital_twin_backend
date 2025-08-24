"""
Session storage backends for SimulationManager.

Provides InMemorySessionStore and RedisSessionStore, both supporting a common
interface for storing, retrieving, and deleting session data. Used to enable
in-memory or Redis-based persistence for simulation sessions.
"""

import pickle
import time
from typing import Any, Optional

try:
    import redis
except ImportError:
    redis = None


class InMemorySessionStore:
    """
    In-memory session store for simulation sessions.

    Stores session data in a local dictionary. Supports optional expiration.
    Used for development, testing, or when Redis is not available.
    """

    def __init__(self):
        """Initialize the in-memory session store."""
        self._sessions = {}

    def set(self, key: str, value: Any, ex: Optional[int] = None):
        """
        Store a session value by key, with optional expiration.

        Args:
            key (str): Session key.
            value (Any): Session value (usually a tuple).
            ex (Optional[int]): Expiration time in seconds, or None for no expiry.
        """
        self._sessions[key] = (
            value,
            ex,
            None if ex is None else self._now() + ex,
        )

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a session value by key, respecting expiration.

        Args:
            key (str): Session key.

        Returns:
            Optional[Any]: The session value, or None if not found or expired.
        """
        entry = self._sessions.get(key)

        if not entry:
            return None

        value, _ex, expiry = entry

        if expiry is not None and self._now() > expiry:
            del self._sessions[key]
            return None

        return value

    def delete(self, key: str):
        """
        Delete a session by key.

        Args:
            key (str): Session key.
        """
        if key in self._sessions:
            del self._sessions[key]

    def _now(self):
        """Return the current time as an integer timestamp."""

        return int(time.time())


class RedisSessionStore:
    """
    Redis-backed session store for simulation sessions.

    Stores session data in a Redis database, using pickle for serialization.
    Supports expiration via Redis key expiry.
    """

    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initialize the Redis session store.

        Args:
            host (str): Redis host.
            port (int): Redis port.
            db (int): Redis database number.
        """
        if redis is None:
            raise ImportError("redis package is not installed")

        self._client = redis.Redis(host=host, port=port, db=db)

    def set(self, key: str, value: Any, ex: Optional[int] = None):
        """
        Store a session value by key in Redis, using pickle serialization.

        Args:
            key (str): Session key.
            value (Any): Session value (usually a tuple).
            ex (Optional[int]): Expiration time in seconds, or None for no expiry.
        """
        pickled = pickle.dumps(value)
        self._client.set(key, pickled, ex=ex)

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a session value by key from Redis, unpickling the result.

        Args:
            key (str): Session key.

        Returns:
            Optional[Any]: The session value, or None if not found or expired.
        """
        data = self._client.get(key)

        if data is None:
            return None

        return pickle.loads(data)

    def delete(self, key: str):
        """
        Delete a session by key from Redis.

        Args:
            key (str): Session key.
        """
        self._client.delete(key)


# Factory for session store


def get_session_store(mode: str = "memory", **kwargs):
    """
    Factory function to get a session store backend.

    Args:
        mode (str): 'memory' for in-memory, 'redis' for Redis-backed.
        **kwargs: Additional arguments for the backend.

    Returns:
        InMemorySessionStore or RedisSessionStore
    """
    if mode == "redis":
        return RedisSessionStore(**kwargs)

    return InMemorySessionStore()
