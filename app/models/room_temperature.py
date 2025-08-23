class RoomTemperature:
    def __init__(self, initial_temp=20.0):
        self.temp = initial_temp

    def step(self, heater_power, dt=1.0):
        self.temp += 0.5 * heater_power * dt - 0.1 * (self.temp - 20)

    def get_state(self):
        return {"temperature": self.temp}
