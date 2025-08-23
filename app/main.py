"""Digital Twin Backend API.

This module serves as the main entry point for the FastAPI application that
provides a digital twin simulation and control API. It includes endpoints for
simulating physical systems, controlling their states, and monitoring their
behavior.

The API is structured around routers that handle different aspects:
- simulate: System simulation and initialization
- control: System control inputs
- state: System state monitoring
"""

from fastapi import FastAPI

from app.models.room_temperature import RoomTemperature
from app.models.water_tank import WaterTank
from app.routers import control, simulate
from app.routers import simulation as simulation_router
from app.routers import state
from app.services.sim_manager_instance import sim_manager

app = FastAPI(title="Dual-System Digital Twin")


# Register models with the shared SimulationManager instance
sim_manager.register_model("water_tank", WaterTank)
sim_manager.register_model("room_temperature", RoomTemperature)


app.include_router(simulate.router)
app.include_router(state.router)
app.include_router(control.router)
app.include_router(simulation_router.router)
