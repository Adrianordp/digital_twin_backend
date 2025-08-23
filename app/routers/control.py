"""Control router for applying inputs to existing systems.

This module provides endpoints to control already-initialized simulation
systems. It uses the shared systems dictionary from the simulate router to
access system instances.
"""

from typing import Dict, Union

from fastapi import APIRouter

from app.routers.simulate import systems

router = APIRouter()


@router.post("/control/{system_name}")
def apply_control(
    system_name: str, control_input: float
) -> Dict[str, Union[float, str]]:
    """Apply a control input to an existing system.

    This endpoint will:
    1. Check if the requested system exists
    2. If it exists, apply the control input and advance one time step
    3. Return the new system state or an error if system not initialized

    Args:
        system_name (str): Name of the system to control ('water_tank' or
            'room_temperature'). Must be previously initialized.
        control_input (float): Input value for the system (inflow rate for water
            tank, heater power for room).

    Returns:
        Dict[str, Union[float, str]]: Either the system state after applying the
            control input, or an error message if system not initialized.
    """
    system = systems.get(system_name)

    if not system:
        return {"error": "System not initialized"}

    system.step(control_input)

    return system.get_state()
