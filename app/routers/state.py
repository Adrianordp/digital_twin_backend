from fastapi import APIRouter

from app.routers.simulate import systems

router = APIRouter()


@router.get("/state/{system_name}")
def get_state(system_name: str):
    system = systems.get(system_name)
    if not system:
        return {"error": "System not initialized"}
    return system.get_state()
