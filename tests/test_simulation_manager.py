"""Tests for the SimulationManager service.

These tests use a DummyModel to simulate behavior without relying on actual
model implementations. They verify that:
- Sessions can be created and return valid UUIDs
- Stepping the simulation updates state correctly
- History and logs are recorded properly
- Resetting and updating parameters work as expected
"""

from uuid import UUID


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
