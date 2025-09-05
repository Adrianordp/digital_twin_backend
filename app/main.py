"""Digital Twin Backend API.

This module serves as the main entry point for the FastAPI application that
provides a digital twin simulation and control API using session-based
management for isolated simulation instances.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.room_temperature import RoomTemperature
from app.models.water_tank import WaterTank
from app.routers import simulation as simulation_router
from app.services.sim_manager_instance import sim_manager

app = FastAPI(title="Dual-System Digital Twin")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register models with the shared SimulationManager instance
sim_manager.register_model("water_tank", WaterTank)
sim_manager.register_model("room_temperature", RoomTemperature)


app.include_router(simulation_router.router)
