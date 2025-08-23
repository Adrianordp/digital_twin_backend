"""Test suite for the RoomTemperature simulation model.

This module contains tests that verify the behavior of the room temperature model,
ensuring that:
- The room heats up with positive heater power
- The room cools down towards ambient temperature
- Temperature changes are proportional to time steps
- Temperature reporting works correctly
"""

from app.models.room_temperature import RoomTemperature


def test_heating() -> None:
    """Test that room temperature increases with positive heater power.

    This test:
    1. Creates a room at default temperature (20°C)
    2. Applies positive heater power
    3. Verifies temperature increases
    """
    room = RoomTemperature()
    initial_temp = room.temp
    room.step(heater_power=10.0)

    assert room.temp > initial_temp


def test_natural_cooling() -> None:
    """Test that room cools down to ambient when heater is off.

    This test verifies the natural cooling behavior when no heating is applied.
    The room should cool down towards the ambient temperature (20°C).
    """
    room = RoomTemperature(initial_temp=25.0)  # Start above ambient
    initial_temp = room.temp
    room.step(heater_power=0.0)

    assert room.temp < initial_temp  # Should cool down
    assert room.temp > 20.0  # But not instantly to ambient


def test_time_proportional() -> None:
    """Test that temperature change is proportional to time step size.

    Compares temperature changes with different time step sizes to verify
    the model's time-dependent behavior.
    """
    room1 = RoomTemperature()
    room2 = RoomTemperature()

    # Apply same power for different durations
    room1.step(heater_power=10.0, delta_time=1.0)
    room2.step(heater_power=10.0, delta_time=2.0)

    temp_change1 = room1.temp - 20.0
    temp_change2 = room2.temp - 20.0

    # Temperature change should be roughly proportional to time
    # (not exactly 2x due to cooling effects)
    assert temp_change2 > temp_change1


def test_initial_temperature() -> None:
    """Test that room is initialized with correct temperature."""
    initial_temp = 18.0
    room = RoomTemperature(initial_temp=initial_temp)

    assert room.temp == initial_temp


def test_get_state() -> None:
    """Test that get_state returns the correct format and value."""
    room = RoomTemperature(initial_temp=22.0)

    state = room.get_state()

    assert isinstance(state, dict)
    assert "temperature" in state
    assert isinstance(state["temperature"], float)
    assert state["temperature"] == room.temp
