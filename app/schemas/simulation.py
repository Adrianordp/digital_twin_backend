"""Pydantic schemas for simulation session management and generic API payloads.

Defines request and response models for initializing, stepping, resetting, and
updating simulation sessions.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SessionInitRequest(BaseModel):
    """Request payload for initializing a simulation session.

    Attributes:
        model_name (str): The name of the model to simulate (e.g.,
            'water_tank').
        params (dict, optional): Model-specific initialization parameters.
    """

    model_name: str = Field(..., example="water_tank")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SessionInitResponse(BaseModel):
    """Response payload containing the session ID for a new simulation."""

    session_id: UUID


class StepRequest(BaseModel):
    """Request payload for advancing a simulation by one step.

    Attributes:
        session_id (UUID): The session identifier.
        control_input (Any): The control input for the model.
        delta_time (float, optional): Time step duration. Defaults to 1.0.
    """

    session_id: UUID
    control_input: Any
    delta_time: float = 1.0


class StateResponse(BaseModel):
    """Response payload containing the current state of the simulation."""

    state: Dict[str, Any]


class HistoryResponse(BaseModel):
    """Response payload containing the simulation history."""

    history: List[Dict[str, Any]]


class LogsResponse(BaseModel):
    """Response payload containing the simulation logs."""

    logs: List[str]


class ResetRequest(BaseModel):
    """Request payload for resetting a simulation session.

    Attributes:
        session_id (UUID): The session identifier.
        params (dict, optional): New model parameters for reset.
    """

    session_id: UUID
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UpdateParamsRequest(BaseModel):
    """Request payload for updating model parameters in a session.

    Attributes:
        session_id (UUID): The session identifier.
        params (dict): Parameters to update.
    """

    session_id: UUID
    params: Dict[str, Any]
    params: Dict[str, Any]
