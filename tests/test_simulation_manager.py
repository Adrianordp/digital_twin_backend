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


def test_get_model_returns_model_instance(sim_manager):
    """Test that get_model returns the correct model instance for a session."""
    session_id = sim_manager.create_session("dummy")
    model = sim_manager.get_model(session_id)

    # Should be a DummyModel instance and reflect state changes
    assert hasattr(model, "step")
    assert hasattr(model, "get_state")

    # Stepping via the model should affect the session state
    model.step(7)
    state = sim_manager.get_state(session_id)

    assert state["dummy"] == 7


def test_register_model_allows_session_creation():
    """Registering a model should allow creating a session with that name."""

    class MinimalModel:
        def __init__(self, **_kwargs):
            pass

        # Minimal interface to avoid usage during this test
        def step(self, *_args, **_kwargs):
            pass

        def get_state(self):
            return {}

        def reset(self, **_kwargs):
            pass

        def update_params(self, **_kwargs):
            pass

    manager = SimulationManager()
    manager.register_model("minimal", MinimalModel)

    session_id = manager.create_session("minimal")

    assert isinstance(session_id, UUID)


def test_register_model_overwrites_existing_without_error():
    """Registering an existing name should overwrite the previous model class."""

    class ModelA:
        def __init__(self, **_kwargs):
            # If this constructor is called after overwrite, the test should fail
            raise RuntimeError("ModelA should have been overwritten")

    class ModelB:
        def __init__(self, **_kwargs):
            pass

        def step(self, *_args, **_kwargs):
            pass

        def get_state(self):
            return {}

        def reset(self, **_kwargs):
            pass

        def update_params(self, **_kwargs):
            pass

    manager = SimulationManager({"foo": ModelA})
    # Overwrite existing registration
    manager.register_model("foo", ModelB)

    # Should not raise (i.e., should use ModelB, not ModelA)
    _ = manager.create_session("foo")


def test_create_session_with_unregistered_model_raises_error():
    """Creating a session for an unknown model should raise ValueError."""

    manager = SimulationManager()

    with pytest.raises(ValueError):
        manager.create_session("not_registered")
