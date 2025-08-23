"""Tests for the SimulationManager service.

These tests use a DummyModel to simulate behavior without relying on actual
model implementations. They verify that:
- Sessions can be created and return valid UUIDs
- Stepping the simulation updates state correctly
- History and logs are recorded properly
- Resetting and updating parameters work as expected
"""

from uuid import UUID

import pytest

from app.services.simulation_manager import SimulationManager


class DummyModel:
    """A dummy model for testing SimulationManager behavior."""

    def __init__(self, **kwargs):
        """Initialize the dummy model with optional parameters."""
        self.state = {"dummy": 0}
        self.params = kwargs
        self.history = []
        self.logs = []

    def step(self, control_input, _delta_time=1.0):
        """Advance the dummy state by the control input.

        Args:
            control_input (int): Value to increment the dummy state.
            delta_time (float, optional): Unused, for interface compatibility.
        """
        self.state["dummy"] += control_input
        self.history.append(self.state.copy())
        self.logs.append(f"Stepped with input {control_input}")

    def get_state(self):
        """Return a copy of the current state."""
        return self.state.copy()

    def reset(self, **kwargs):
        """Reset the dummy state and update parameters.

        Args:
            **kwargs: Parameters to update.
        """
        self.state = {"dummy": 0}
        self.params.update(kwargs)
        self.history = []
        self.logs = ["Reset"]

    def update_params(self, **kwargs):
        """Update model parameters and log the change.

        Args:
            **kwargs: Parameters to update.
        """
        self.params.update(kwargs)
        self.logs.append(f"Params updated: {kwargs}")



@pytest.fixture
def sim_manager():
    """Fixture to provide a SimulationManager with a test model registry."""
    return SimulationManager(model_registry={"dummy": DummyModel})


def test_create_session(sim_manager):
    """Test that a session can be created and returns a UUID."""
    session_id = sim_manager.create_session("dummy", {"foo": "bar"})

    assert isinstance(session_id, UUID)


def test_step_and_state(sim_manager):
    """Test stepping the simulation updates the state correctly."""
    session_id = sim_manager.create_session("dummy")
    state1 = sim_manager.get_state(session_id)
    sim_manager.step(session_id, 5)
    state2 = sim_manager.get_state(session_id)

    assert state2["dummy"] == state1["dummy"] + 5


def test_history(sim_manager):
    """Test that simulation history is recorded correctly."""
    session_id = sim_manager.create_session("dummy")
    sim_manager.step(session_id, 1)
    sim_manager.step(session_id, 2)
    history = sim_manager.get_history(session_id)

    assert len(history) == 2
    assert history[0]["dummy"] == 1
    assert history[1]["dummy"] == 3


def test_logs(sim_manager):
    """Test that log messages are recorded for each step."""
    session_id = sim_manager.create_session("dummy")
    sim_manager.step(session_id, 1)
    logs = sim_manager.get_logs(session_id)

    assert any("Stepped" in log for log in logs)


def test_reset(sim_manager):
    """Test that resetting the simulation clears state and history."""
    session_id = sim_manager.create_session("dummy")
    sim_manager.step(session_id, 10)
    sim_manager.reset(session_id)
    state = sim_manager.get_state(session_id)

    assert state["dummy"] == 0

    history = sim_manager.get_history(session_id)

    assert history == []


def test_update_params(sim_manager):
    """Test that updating parameters logs the change."""
    session_id = sim_manager.create_session("dummy")
    sim_manager.update_params(session_id, {"foo": 42})
    logs = sim_manager.get_logs(session_id)

    assert any("Params updated" in log for log in logs)

    logs = sim_manager.get_logs(session_id)

    assert any("Params updated" in log for log in logs)
