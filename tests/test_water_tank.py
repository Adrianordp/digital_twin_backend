from app.models.water_tank import WaterTank


def test_step():
    tank = WaterTank()
    tank.step(10.0, dt=1.0)
    assert tank.level > 0
