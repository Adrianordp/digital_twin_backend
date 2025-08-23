"""Factory module for creating simulation system instances.

This module provides a factory function to instantiate different types of
simulation systems based on their names. Currently supports:
- water_tank: Water tank with configurable inflow/outflow
- room_temp: Room with temperature control
"""

from typing import Union

from .room_temperature import RoomTemperature
from .water_tank import WaterTank


def get_system(system_name: str) -> Union[WaterTank, RoomTemperature]:
    """Create and return a new instance of the requested simulation system.

    Args:
        system_name (str): Name of the system to create. Valid values are
            'water_tank' or 'room_temp'.

    Returns:
        Union[WaterTank, RoomTemperature]: A new instance of the requested system.

    Raises:
        ValueError: If the system_name is not recognized.
    """
    if system_name == "water_tank":
        return WaterTank()
    elif system_name == "room_temp":
        return RoomTemperature()
    else:
        raise ValueError(f"Unknown system: {system_name}")
