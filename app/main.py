from fastapi import FastAPI

from app.routers import control, simulate, state

app = FastAPI(title="Dual-System Digital Twin")

app.include_router(simulate.router)
app.include_router(state.router)
app.include_router(control.router)
