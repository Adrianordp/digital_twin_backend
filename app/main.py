"""Digital Twin Backend API.

This module serves as the main entry point for the FastAPI application that
provides a digital twin simulation and control API using session-based
management for isolated simulation instances.
"""

from fastapi import FastAPI

from app.models.room_temperature import RoomTemperature
from app.models.water_tank import WaterTank
from app.routers import simulation as simulation_router
from app.services.sim_manager_instance import sim_manager

app = FastAPI(title="Dual-System Digital Twin")


# Register models with the shared SimulationManager instance
sim_manager.register_model("water_tank", WaterTank)
sim_manager.register_model("room_temperature", RoomTemperature)


app.include_router(simulation_router.router)
