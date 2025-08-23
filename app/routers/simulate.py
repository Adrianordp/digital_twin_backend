"""Simulation router for initializing and stepping system states.

This module provides endpoints to create and simulate system instances. It maintains
a dictionary of active systems that can be accessed by other routers.
"""

from typing import Dict, Union

from fastapi import APIRouter

from app.models.factory import get_system
from app.models.room_temperature import RoomTemperature
from app.models.water_tank import WaterTank

router = APIRouter()
systems: Dict[str, Union[WaterTank, RoomTemperature]] = {}


@router.post("/simulate/{system_name}")
def simulate(
    system_name: str, control_input: float
) -> Dict[str, Union[float, str]]:
    """Create (if needed) and simulate one step of a system.

    This endpoint will:
    1. Create a new system instance if one doesn't exist
    2. Apply the control input to advance the simulation by one time step
    3. Return the new system state

    Args:
        system_name (str): Name of the system to simulate ('water_tank' or
            'room_temperature').
        control_input (float): Input value for the system (inflow rate for
            water tank, heater power for room).

    Returns:
        Dict[str, Union[float, str]]: The system state after simulation,
            containing values like temperature or level.
    """
    if system_name not in systems:
        systems[system_name] = get_system(system_name)

    system = systems[system_name]
    system.step(control_input)

    return system.get_state()
