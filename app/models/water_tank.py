import numpy as np
from scipy.integrate import odeint


class WaterTank:
    def __init__(self, capacity=100.0, inflow=0.0, outflow_coeff=0.1):
        self.capacity = capacity
        self.level = 0.0
        self.inflow = inflow
        self.outflow_coeff = outflow_coeff

    def dynamics(self, level, _time, inflow):
        outflow = self.outflow_coeff * level
        return inflow - outflow

    def step(self, control_input, delta_time=1.0):
        time = [0, delta_time]
        self.level = odeint(
            self.dynamics, self.level, time, args=(control_input,)
        )[-1][0]

    def get_state(self):
        return {"level": self.level}
