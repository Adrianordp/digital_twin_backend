"""Pydantic schema for RoomTemperature model parameters.

Defines the expected input parameters for initializing or updating a room
temperature simulation.
"""

from typing import Optional

from pydantic import BaseModel, Field


class RoomTemperatureParams(BaseModel):
    """Parameters for the RoomTemperature simulation model.

    Attributes:
        initial_temp (float, optional): Initial temperature of the room (°C).
            Defaults to 20.0.
        ambient_temp (float, optional): Ambient (outside) temperature (°C).
            Defaults to 20.0.
        heat_transfer_coeff (float, optional): Heat transfer coefficient.
            Defaults to 0.1.
        heater_power (float, optional): Power of the heater.
            Defaults to 1.0.
    """

    initial_temp: Optional[float] = Field(20.0)
    ambient_temp: Optional[float] = Field(20.0)
    heat_transfer_coeff: Optional[float] = Field(0.1)
    heater_power: Optional[float] = Field(1.0)
    heater_power: Optional[float] = Field(1.0)
