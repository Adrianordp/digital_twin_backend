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

from app.routers import control, simulate, state

app = FastAPI(title="Dual-System Digital Twin")

app.include_router(simulate.router)
app.include_router(state.router)
app.include_router(control.router)
