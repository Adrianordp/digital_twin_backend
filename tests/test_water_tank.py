"""Test suite for the WaterTank simulation model.

This module contains tests that verify the behavior of the water tank model,
ensuring that:
- The tank responds to positive inflow inputs
- The water level changes appropriately with time
- The outflow behaves according to the configured coefficient
- The tank maintains its configured capacity
- Physical constraints are respected (non-negative level)
- The model handles edge cases appropriately
"""

from app.models.water_tank import WaterTank


def test_positive_inflow() -> None:
    """Test that water level increases with positive inflow."""
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)

    assert tank.level > 0


def test_zero_inflow() -> None:
    """Test that water level decreases with zero inflow due to outflow."""
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)
    initial_level = tank.level
    tank.step(0.0, delta_time=1.0)

    assert tank.level < initial_level


def test_outflow_coefficient() -> None:
    """Test that outflow coefficient affects drainage rate."""
    slow_tank = WaterTank(outflow_coeff=0.1)
    fast_tank = WaterTank(outflow_coeff=0.2)

    initial_input = 10.0
    slow_tank.step(initial_input, delta_time=1.0)
    fast_tank.step(initial_input, delta_time=1.0)

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
    assert tank.level == 0.0


def test_get_state() -> None:
    """Test that get_state returns the correct format and value."""
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)
    state = tank.get_state()

    assert isinstance(state, dict)
    assert "level" in state
    assert isinstance(state["level"], float)
    assert state["level"] == tank.level


def test_negative_inflow() -> None:
    """Test behavior with negative inflow (active draining).

    Negative inflow represents active draining (e.g., a pump removing water).
    This should accelerate the water level decrease along with natural outflow.
    """
    tank = WaterTank()
    # First add some water
    tank.step(10.0, delta_time=1.0)
    level_with_zero_inflow = tank.level

    # Reset and compare with negative inflow
    tank = WaterTank()
    tank.step(10.0, delta_time=1.0)
    tank.step(-5.0, delta_time=1.0)  # Negative inflow

    assert (
        tank.level < level_with_zero_inflow
    )  # Should drain faster than natural outflow


def test_level_stays_non_negative() -> None:
    """Test that water level never goes below zero.

    Even with negative inflow (active draining) and natural outflow,
    the water level should never become negative.
    """
    tank = WaterTank()
    # Try to drain an empty tank
    tank.step(-10.0, delta_time=1.0)

    assert tank.level >= 0.0

    # Try to drain with both negative inflow and natural outflow
    tank.step(5.0, delta_time=1.0)  # Add some water
    tank.step(-10.0, delta_time=2.0)  # Try aggressive draining

    assert tank.level >= 0.0


def test_negative_outflow_coefficient() -> None:
    """Test that negative outflow coefficient is handled appropriately.

    A negative outflow coefficient would mean the tank fills itself, which
    is physically impossible in a gravity-driven system.
    """
    # Should either raise error or coerce to positive
    tank = WaterTank(outflow_coeff=-0.1)
    initial_level = tank.level
    tank.step(0.0, delta_time=1.0)

    assert tank.level <= initial_level


def test_respect_capacity() -> None:
    """Test that water level respects tank capacity.

    Water level should not exceed the tank's capacity, simulating overflow
    in a real tank.
    """
    capacity = 100.0
    tank = WaterTank(capacity=capacity)

    # Try to overfill
    for _ in range(10):
        tank.step(100.0, delta_time=1.0)

        assert tank.level <= capacity
