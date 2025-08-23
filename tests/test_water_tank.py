"""Test suite for the WaterTank simulation model.

This module contains tests that verify the behavior of the water tank model,
ensuring that:
- The tank responds to positive inflow inputs
- The water level changes appropriately with time
"""

from app.models.water_tank import WaterTank


def test_step() -> None:
    """Test that water level increases with positive inflow.

    This test:
    1. Creates a tank with default parameters
    2. Applies a positive inflow for one time step
    3. Verifies that the water level increases above initial zero
    """
    tank = WaterTank()
    tank.step(10.0, 1.0)

    assert tank.level > 0
