"""Room temperature simulation model with heater control.

This module implements a simple thermal model where:
- Room temperature changes based on heater power input
- Natural cooling occurs towards ambient temperature (20°C)
- Uses a basic linear model for both heating and cooling
"""

from typing import Dict


class RoomTemperature:
    """A simple room temperature model with heater control.

    Attributes:
        temp (float): Current room temperature in Celsius.
    """

    def __init__(self, initial_temp: float = 20.0) -> None:
        """Initialize the room temperature model.

        Args:
            initial_temp (float, optional): Initial room temperature in Celsius.
                Defaults to 20.0.
        """
        self.temp = initial_temp

    def step(self, heater_power: float, delta_time: float = 1.0) -> None:
        """Advance the simulation by one time step.

        Updates temperature based on heater power and natural cooling.
        dT/dt = 0.5 * heater_power - 0.1 * (T - T_ambient)
        where T_ambient = 20°C

        Args:
            heater_power (float): Heater power input (arbitrary units).
            delta_time (float, optional): Time step size in seconds. Defaults to
                1.0.
        """
        self.temp += 0.5 * heater_power * delta_time - 0.1 * (self.temp - 20)

    def get_state(self) -> Dict[str, float]:
        """Get the current state of the room.

        Returns:
            Dict[str, float]: Dictionary containing current temperature.
        """
        return {"temperature": self.temp}
