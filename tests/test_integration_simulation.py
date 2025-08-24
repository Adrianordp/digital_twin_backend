"""
Integration tests for the simulation session API endpoints.

This file uses FastAPI's TestClient to verify the full lifecycle of a simulation
session, including session creation, stepping, state/history/logs retrieval,
reset, and parameter updates.

These tests are marked with @pytest.mark.integration and are not run by default
with pytest.

Run them explicitly with: pytest -m integration
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.integration
def test_simulation_lifecycle():
    """
    Full integration test for the simulation session lifecycle.

    This test covers:
    - Creating a simulation session for the water tank model
    - Stepping the simulation with a control input
    - Retrieving the current state, history, and logs
    - Resetting the simulation with new parameters
    - Updating model parameters

    The test ensures that all main simulation endpoints are reachable and function as expected.
    """
    # 1. Create a session for the water tank model
    response = client.post("/simulate/init", json={"model_name": "water_tank"})

    assert response.status_code == 200

    session_id = response.json()["session_id"]

    # 2. Step the simulation
    response = client.post(
        "/simulate/step",
        json={
            "session_id": session_id,
            "control_input": 5.0,
            "delta_time": 1.0,
        },
    )

    assert response.status_code == 200

    # 3. Get state
    response = client.get(f"/simulate/state/{session_id}")

    assert response.status_code == 200
    assert "state" in response.json()

    # 4. Get history
    response = client.get(f"/simulate/history/{session_id}")

    assert response.status_code == 200
    assert "history" in response.json()

    # 5. Get logs
    response = client.get(f"/simulate/logs/{session_id}")

    assert response.status_code == 200
    assert "logs" in response.json()

    # 6. Reset the simulation
    response = client.post(
        "/simulate/reset",
        json={"session_id": session_id, "params": {"capacity": 200.0}},
    )

    assert response.status_code == 200

    # 7. Update parameters
    response = client.patch(
        "/simulate/params",
        json={"session_id": session_id, "params": {"inflow": 10.0}},
    )

    assert response.status_code == 200
