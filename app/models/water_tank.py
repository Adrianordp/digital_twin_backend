"""Water tank simulation model with configurable inflow and outflow dynamics.

This module implements a water tank model with:
- Controllable inflow rate
- Configurable gravity-driven outflow coefficient
- Numerical integration using SciPy's ODE solver
"""

from typing import Dict

from scipy.integrate import odeint

from app.models.system_model import SystemModel


class WaterTank(SystemModel):
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
        """
        Initialize a WaterTank instance.

        Args:
            capacity (float, optional): Maximum capacity of the tank. Must be
                positive. Defaults to 100.0.
            inflow (float, optional): Base inflow rate. Defaults to 0.0.
            outflow_coeff (float, optional): Outflow coefficient. Defaults to
                0.1.

        Raises:
            ValueError: If capacity is not positive.
        """
        super().__init__()

        if capacity <= 0:
            raise ValueError("Tank capacity must be positive")

        self.capacity = capacity
        self.level = 0.0
        self.inflow = inflow
        self.outflow_coeff = outflow_coeff

    def dynamics(self, level: float, _time: float, inflow: float) -> float:
        """
        Calculate the rate of change of water level.

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
        """
        Advance the simulation by the specified time step.

        Args:
            control_input (float): The inflow rate to apply during this step.
            delta_time (float, optional): The time increment for the simulation
                step. Defaults to 1.0.

        Raises:
            ValueError: If delta_time is not positive.
        """
        if delta_time <= 0:
            raise ValueError("Time step must be positive")

        time = [0, delta_time]
        new_level = odeint(
            self.dynamics, self.level, time, args=(control_input,)
        )[-1][0]

        self.level = min(max(0.0, new_level), self.capacity)

        self.history.append(self.get_state())
        self.logs.append(
            f"Stepped with input {control_input}, delta_time {delta_time}"
        )

    def get_state(self) -> Dict[str, float]:
        """
        Return the current state of the water tank.

        Returns:
            Dict[str, float]: Dictionary containing the current water level.
        """
        return {"level": self.level}

    def reset(self, **kwargs) -> None:
        """
        Reset the water tank to initial state, optionally with new parameters.

        Args:
            **kwargs: Optional new parameters for capacity, inflow, and
                outflow_coeff.
        """
        self.capacity = kwargs.get("capacity", self.capacity)
        self.inflow = kwargs.get("inflow", self.inflow)
        self.outflow_coeff = kwargs.get("outflow_coeff", self.outflow_coeff)
        self.level = 0.0
        self.history.clear()
        self.logs.append("Reset called")

    def update_params(self, **kwargs) -> None:
        """
        Update model parameters and log the change.

        Args:
            **kwargs: Model parameters to update (capacity, inflow,
                outflow_coeff).
        """
        for k, v in kwargs.items():

            if hasattr(self, k):
                setattr(self, k, v)

        self.logs.append(f"Params updated: {kwargs}")
