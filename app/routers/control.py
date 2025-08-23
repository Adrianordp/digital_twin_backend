from fastapi import APIRouter

from app.routers.simulate import systems

router = APIRouter()


@router.post("/control/{system_name}")
def apply_control(system_name: str, control_input: float):
    system = systems.get(system_name)
    if not system:
        return {"error": "System not initialized"}
    system.step(control_input)
    return system.get_state()
