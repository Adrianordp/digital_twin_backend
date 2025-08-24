"""Room temperature simulation model with heater control.

This module implements a simple thermal model where:
- Room temperature changes based on heater power input
- Natural cooling occurs towards ambient temperature (20°C)
- Uses a basic linear model for both heating and cooling
"""

from typing import Dict

from app.models.system_model import SystemModel


class RoomTemperature(SystemModel):
    """
    A simple room temperature model with heater control.

    Attributes:
        temp (float): Current room temperature in Celsius.
    """

    def __init__(self, initial_temp: float = 20.0) -> None:
        """Initialize the room temperature model.

        Args:
            initial_temp (float, optional): Initial room temperature in Celsius.
                Defaults to 20.0.
        """
        super().__init__()
        self.temp = initial_temp

    def step(self, control_input: float, delta_time: float = 1.0) -> None:
        """
        Advance the simulation by one time step.

        Updates temperature based on heater power and natural cooling.
        dT/dt = 0.5 * control_input - 0.1 * (T - T_ambient)
        where T_ambient = 20°C

        Args:
            control_input (float): Heater power input (arbitrary units).
            delta_time (float, optional): Time step size in seconds. Defaults to
                1.0.

        Raises:
            ValueError: If delta_time is not positive.
        """

        self.temp += 0.5 * control_input * delta_time - 0.1 * (self.temp - 20)

        self.history.append(self.get_state())
        self.logs.append(
            f"Stepped with input {control_input}, delta_time {delta_time}"
        )

    def get_state(self) -> Dict[str, float]:
        """
        Get the current state of the room.

        Returns:
            Dict[str, float]: Dictionary containing current temperature.
        """
        return {"temperature": self.temp}

    def reset(self, **kwargs) -> None:
        """
        Reset the room temperature model to initial state, optionally with new
        parameters.

        Args:
            **kwargs: Optional new parameter for initial_temp.
        """
        self.temp = kwargs.get("initial_temp", 20.0)
        self.history.clear()
        self.logs.append("Reset called")

    def update_params(self, **kwargs) -> None:
        """
        Update model parameters and log the change.

        Args:
            **kwargs: Model parameters to update (initial_temp).
        """
        if "initial_temp" in kwargs:
            self.temp = kwargs["initial_temp"]

        self.logs.append(f"Params updated: {kwargs}")
