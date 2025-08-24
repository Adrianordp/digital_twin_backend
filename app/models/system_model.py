"""Abstract base class for all simulation system models."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SystemModel(ABC):
    """
    Base class for simulation system models with history and logging support.
    Attributes:
        history (List[Dict[str, Any]]): List of historical state snapshots.
        logs (List[str]): List of log messages."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.logs: List[str] = []

    @abstractmethod
    def step(self, control_input: Any, delta_time: float = 1.0) -> None:
        """Advance the simulation by one time step.
        Args:
            control_input (Any): The control input for the model.
            delta_time (float, optional): Time step duration. Defaults to 1.0.
        """

    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Return the current state of the model."""

    @abstractmethod
    def reset(self, **kwargs) -> None:
        """Reset the model to its initial state.
        Args:
            **kwargs: Optional parameters for resetting the model."""

    @abstractmethod
    def update_params(self, **kwargs) -> None:
        """Update model parameters.
        Args:
            **kwargs: Parameters to update.
        """
