"""Pytest configuration and fixtures for simulation manager tests.

Provides a DummyModel and a sim_manager fixture for isolated, repeatable testing
of the SimulationManager service.
"""

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
