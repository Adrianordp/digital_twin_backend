"""Pydantic schema for WaterTank model parameters.

Defines the expected input parameters for initializing or updating a water tank
simulation.
"""

from typing import Optional

from pydantic import BaseModel, Field


class WaterTankParams(BaseModel):
    """Parameters for the WaterTank simulation model.

    Attributes:
        capacity (float, optional): Maximum tank capacity. Defaults to 100.0.
        inflow (float, optional): Initial inflow rate. Defaults to 0.0.
        outflow_coeff (float, optional): Outflow rate coefficient. Defaults to
            0.1.
    """

    capacity: Optional[float] = Field(100.0, gt=0)
    inflow: Optional[float] = Field(0.0)
    outflow_coeff: Optional[float] = Field(0.1)
