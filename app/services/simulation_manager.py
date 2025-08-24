"""Service to manage simulation sessions, state, history, and logs for all
models.

This module provides the SimulationManager class which handles multiple
simulation sessions, allowing creation, stepping, state retrieval, history
tracking, and logging.

Each simulation session is identified by a UUID and maintains its own model
instance, state, history, and logs. The manager supports creating sessions for
different model types, stepping simulations forward in time, retrieving current
state, history of states, and log messages, as well as resetting and updating
model parameters.
"""

import time
from typing import Any, Dict, List, Optional, Type
from uuid import UUID, uuid4


class SimulationManager:
    """Manages simulation sessions, state, history, and logs for all models."""

    SESSION_TIMEOUT_SECONDS = 30 * 60  # 30 minutes

    def __init__(self, model_registry: Optional[Dict[str, Type]] = None):
        """Initialize the SimulationManager.

        Args:
            model_registry (Optional[Dict[str, Type]]): Optional mapping of
                model names to model classes.
        """
        self._model_registry: Dict[str, Type] = model_registry or {}
        # Each session: UUID -> (model, last_access_time)
        self._sessions: Dict[UUID, Any] = {}

    def create_session(
        self, model_name: str, params: Optional[Dict[str, Any]] = None
    ) -> UUID:
        """Create a new simulation session for the given model."""
        self._cleanup_expired_sessions()

        if model_name not in self._model_registry:
            raise ValueError(f"Unknown model: {model_name}")

        model_cls = self._model_registry[model_name]
        params = params or {}
        model = model_cls(**params)
        session_id = uuid4()
        now = time.time()
        self._sessions[session_id] = (model, now)

        return session_id

    def step(
        self, session_id: UUID, control_input: Any, delta_time: float = 1.0
    ) -> Dict[str, Any]:
        """Advance the simulation by one step, update state/history/logs."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)
        model.step(control_input, delta_time)

        return model.get_state()

    def get_state(self, session_id: UUID) -> Dict[str, Any]:
        """Retrieve the current state for the given session."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)

        return model.get_state()

    def get_history(self, session_id: UUID) -> List[Dict[str, Any]]:
        """Retrieve the simulation history for the given session."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)

        return list(model.history)

    def get_logs(self, session_id: UUID) -> List[str]:
        """Retrieve the log messages for the given session."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)

        return list(model.logs)

    def reset(
        self, session_id: UUID, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Reset the simulation for the given session, optionally with new
        parameters."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)
        params = params or {}
        model.reset(**params)

        return model.get_state()

    def update_params(
        self, session_id: UUID, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update model parameters for the given session."""
        self._cleanup_expired_sessions()
        model = self.get_model(session_id)
        model.update_params(**params)

        return model.get_state()

    def register_model(self, name: str, model_cls: Type) -> None:
        """Register a model class with a given name."""
        self._model_registry[name] = model_cls

    def get_model(self, session_id: UUID) -> Any:
        """Retrieve the model instance for the given session ID and update last
        access time."""
        if session_id not in self._sessions:
            raise ValueError(f"Unknown session: {session_id}")

        model, _ = self._sessions[session_id]
        self._sessions[session_id] = (model, time.time())

        return model

    def _cleanup_expired_sessions(self):
        """Remove sessions that have expired based on last access time."""
        now = time.time()
        expired = [
            sid
            for sid, (_, last_access) in self._sessions.items()
            if now - last_access > self.SESSION_TIMEOUT_SECONDS
        ]

        for sid in expired:
            del self._sessions[sid]
