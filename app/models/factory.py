from .room_temperature import RoomTemperature
from .water_tank import WaterTank


def get_system(system_name: str):
    if system_name == "water_tank":
        return WaterTank()
    elif system_name == "room_temp":
        return RoomTemperature()
    else:
        raise ValueError(f"Unknown system: {system_name}")
