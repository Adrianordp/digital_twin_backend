"""Test suite for the WaterTank simulation model.

This module contains tests that verify the behavior of the water tank model,
ensuring that:
- The tank responds to positive inflow inputs
- The water level changes appropriately with time
- The outflow behaves according to the configured coefficient
- The tank maintains its configured capacity
"""

from app.models.water_tank import WaterTank


def test_positive_inflow() -> None:
    """Test that water level increases with positive inflow.

    This test:
    1. Creates a tank with default parameters
    2. Applies a positive inflow for one time step
    3. Verifies that the water level increases above initial zero
    """
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)

    assert tank.level > 0


def test_zero_inflow() -> None:
    """Test that water level decreases with zero inflow due to outflow.

    This test verifies the natural draining behavior when no inflow is applied.
    """
    tank = WaterTank()
    # First add some water
    tank.step(10.0, delta_time=1.0)
    initial_level = tank.level

    # Then let it drain
    tank.step(0.0, delta_time=1.0)

    assert tank.level < initial_level


def test_outflow_coefficient() -> None:
    """Test that outflow coefficient affects drainage rate.

    Compares drainage rates between tanks with different outflow coefficients.
    """
    slow_tank = WaterTank(outflow_coeff=0.1)
    fast_tank = WaterTank(outflow_coeff=0.2)

    # Fill both tanks
    initial_input = 10.0
    slow_tank.step(initial_input, delta_time=1.0)
    fast_tank.step(initial_input, delta_time=1.0)

    # Let them drain
    slow_tank.step(0.0, delta_time=1.0)
    fast_tank.step(0.0, delta_time=1.0)

    assert fast_tank.level < slow_tank.level


def test_initial_state() -> None:
    """Test that tank is initialized with correct parameters."""
    capacity = 200.0
    inflow = 5.0
    outflow_coeff = 0.15

    tank = WaterTank(
        capacity=capacity, inflow=inflow, outflow_coeff=outflow_coeff
    )

    assert tank.capacity == capacity
    assert tank.inflow == inflow
    assert tank.outflow_coeff == outflow_coeff
    assert tank.level == 0.0  # Initial level should be zero


def test_get_state() -> None:
    """Test that get_state returns the correct format and value."""
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)

    state = tank.get_state()

    assert isinstance(state, dict)
    assert "level" in state
    assert isinstance(state["level"], float)
    assert state["level"] == tank.level
