from typing import Any, Dict, List, Optional
from uuid import UUID

class SimulationManager:
    """Manages simulation sessions, state, history, and logs for all models."""

    def create_session(self, model_name: str, params: Optional[Dict[str, Any]] = None) -> UUID:
        """Create a new simulation session for the given model.

        Args:
            model_name (str): The name of the model to simulate (e.g., 'water_tank').
            params (Optional[Dict[str, Any]]): Optional parameters for model initialization.

        Returns:
            UUID: The session ID for the new simulation.
        """
        pass

    def step(self, session_id: UUID, control_input: Any, delta_time: float = 1.0) -> Dict[str, Any]:
        """Advance the simulation by one step, update state/history/logs.

        Args:
            session_id (UUID): The session ID.
            control_input (Any): The control input for the model.
            delta_time (float, optional): Time step duration. Defaults to 1.0.

        Returns:
            Dict[str, Any]: The updated state after stepping.
        """
        pass

    def get_state(self, session_id: UUID) -> Dict[str, Any]:
        """Retrieve the current state for the given session.

        Args:
            session_id (UUID): The session ID.

        Returns:
            Dict[str, Any]: The current state of the simulation.
        """
        pass

    def get_history(self, session_id: UUID) -> List[Dict[str, Any]]:
        """Retrieve the simulation history for the given session.

        Args:
            session_id (UUID): The session ID.

        Returns:
            List[Dict[str, Any]]: The simulation history (list of state snapshots).
        """
        pass

    def get_logs(self, session_id: UUID) -> List[str]:
        """Retrieve the log messages for the given session.

        Args:
            session_id (UUID): The session ID.

        Returns:
            List[str]: The log messages for the session.
        """
        pass

    def reset(self, session_id: UUID, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Reset the simulation for the given session, optionally with new parameters.

        Args:
            session_id (UUID): The session ID.
            params (Optional[Dict[str, Any]]): Optional new parameters for the model.

        Returns:
            Dict[str, Any]: The reset state of the simulation.
        """
        pass

    def update_params(self, session_id: UUID, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update model parameters for the given session.

        Args:
            session_id (UUID): The session ID.
            params (Dict[str, Any]): The parameters to update.

        Returns:
            Dict[str, Any]: The updated state after parameter change.
        """
        pass
