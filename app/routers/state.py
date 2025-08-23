"""State router for retrieving system states.

This module provides endpoints to query the current state of simulation systems.
It uses the shared systems dictionary from the simulate router to access
system instances.
"""

from typing import Dict, Union

from fastapi import APIRouter

from app.routers.simulate import systems

router = APIRouter()


@router.get("/state/{system_name}")
def get_state(system_name: str) -> Dict[str, Union[float, str]]:
    """Get the current state of a simulation system.

    Args:
        system_name (str): Name of the system to query. Must be previously
            initialized via the simulation endpoint.

    Returns:
        Dict[str, Union[float, str]]: Either the system state containing values
            like temperature or level, or an error message if the system is not
            initialized.
    """
    system = systems.get(system_name)
    if not system:
        return {"error": "System not initialized"}
    return system.get_state()
