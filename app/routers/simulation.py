"""Simulation router for session-based simulation management.

Provides endpoints to initialize, step, query state/history/logs, reset, and
update parameters for simulation sessions using the SimulationManager service.
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.simulation import (
    HistoryResponse,
    LogsResponse,
    ResetRequest,
    SessionInitRequest,
    SessionInitResponse,
    StateResponse,
    StepRequest,
    UpdateParamsRequest,
)
from app.services.simulation_manager import SimulationManager

# Shared SimulationManager instance (could be replaced with DI or app state)
sim_manager = SimulationManager()

router = APIRouter(prefix="/simulate", tags=["simulation"])


@router.post("/init", response_model=SessionInitResponse)
def init_simulation(request: SessionInitRequest):
    """Initialize a new simulation session."""
    try:
        session_id = sim_manager.create_session(
            request.model_name, request.params
        )
        return SessionInitResponse(session_id=session_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/step", response_model=StateResponse)
def step_simulation(request: StepRequest):
    """Advance the simulation by one step and return the new state."""
    try:
        state = sim_manager.step(
            request.session_id, request.control_input, request.delta_time
        )
        return StateResponse(state=state)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/state/{session_id}", response_model=StateResponse)
def get_state(session_id: UUID):
    """Get the current state of a simulation session."""
    try:
        state = sim_manager.get_state(session_id)
        return StateResponse(state=state)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: UUID):
    """Get the history of a simulation session."""
    try:
        history = sim_manager.get_history(session_id)
        return HistoryResponse(history=history)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/logs/{session_id}", response_model=LogsResponse)
def get_logs(session_id: UUID):
    """Get the logs of a simulation session."""
    try:
        logs = sim_manager.get_logs(session_id)
        return LogsResponse(logs=logs)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/reset", response_model=StateResponse)
def reset_simulation(request: ResetRequest):
    """Reset a simulation session, optionally with new parameters."""
    try:
        state = sim_manager.reset(request.session_id, request.params)
        return StateResponse(state=state)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/params", response_model=StateResponse)
def update_params(request: UpdateParamsRequest):
    """Update model parameters for a simulation session."""
    try:
        state = sim_manager.update_params(request.session_id, request.params)
        return StateResponse(state=state)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
