"""Water tank simulation model with configurable inflow and outflow dynamics.

This module implements a water tank model with:
- Controllable inflow rate
- Configurable gravity-driven outflow coefficient
- Numerical integration using SciPy's ODE solver
"""

from typing import Dict

import numpy as np
from scipy.integrate import odeint


class WaterTank:
    """A water tank model with configurable inflow and outflow dynamics.

    Attributes:
        capacity (float): Maximum capacity of the tank.
        level (float): Current water level in the tank.
        inflow (float): Base inflow rate.
        outflow_coeff (float): Coefficient determining the outflow rate
            proportional to level.
    """

    def __init__(
        self,
        capacity: float = 100.0,
        inflow: float = 0.0,
        outflow_coeff: float = 0.1,
    ) -> None:
        """Initialize the water tank model.

        Args:
            capacity (float, optional): Tank capacity. Defaults to 100.0.
            inflow (float, optional): Initial inflow rate. Defaults to 0.0.
            outflow_coeff (float, optional): Outflow rate coefficient. Defaults
            to 0.1.

        Raises:
            ValueError: If capacity is not positive or outflow_coefficient is
                negative.
        """
        if capacity <= 0:
            raise ValueError("Tank capacity must be positive")

        self.capacity = capacity
        self.level = 0.0
        self.inflow = inflow
        self.outflow_coeff = outflow_coeff

    def dynamics(self, level: float, _time: float, inflow: float) -> float:
        """Calculate the rate of change of water level.

        Args:
            level (float): Current water level.
            _time (float): Time variable (unused, required by odeint).
            inflow (float): Current inflow rate.

        Returns:
            float: Rate of change of water level (dh/dt).

        Note:
            Negative inflow is allowed and represents active draining (e.g.,
            pumping out).
            Level constraints are handled in the step method.
        """
        # Apply outflow only if there's water in the tank
        outflow = self.outflow_coeff * max(0.0, level)

        return inflow - outflow

    def step(self, control_input: float, delta_time: float = 1.0) -> None:
        """Advance the simulation by the specified time step.

        Args:
            control_input (float): Input value controlling the inflow rate.
                Negative values represent active draining.
            delta_time (float, optional): Time step duration. Defaults to 1.0.

        Raises:
            ValueError: If delta_time is not positive.
        """
        if delta_time <= 0:
            raise ValueError("Time step must be positive")

        time = [0, delta_time]
        new_level = odeint(
            self.dynamics, self.level, time, args=(control_input,)
        )[-1][0]

        # Enforce physical constraints
        self.level = min(max(0.0, new_level), self.capacity)

    def get_state(self) -> Dict[str, float]:
        """Return the current state of the water tank.

        Returns:
            dict: Dictionary containing the current water level.
        """
        return {"level": self.level}
