from fastapi import APIRouter

from app.models.factory import get_system

router = APIRouter()
systems = {}


@router.post("/simulate/{system_name}")
def simulate(system_name: str, control_input: float):

    if system_name not in systems:
        systems[system_name] = get_system(system_name)

    system = systems[system_name]
    system.step(control_input)

    return system.get_state()
