# Dual-System Digital Twin

A small FastAPI-based digital twin backend that provides lightweight simulation
and control endpoints for simple engineering systems. The project currently
implements two example systems:

- Water Tank: a continuous tank model solved with SciPy's ODE solver.
- Room Temperature: a simple linear temperature model with a heater input.

This repository is intentionally minimal and designed as a starting point for
building digital twins and control/simulation APIs.

## Features

- Session-based REST API for simulation management
- Multiple simulation instances with isolated state
- Session persistence (in-memory or Redis)
- Structured request/response models with Pydantic validation
- Comprehensive logging and monitoring
- Simple modular model structure (models in `app/models`)
- Comprehensive test suite with pytest

## Project structure

- `app/main.py` — FastAPI application entrypoint
- `app/routers/simulation.py` — Session-based simulation endpoints
    (`/simulate/*`)
- `app/models/` — System model implementations (factory, water_tank, room_temperature)
- `app/services/` — SimulationManager and session management services
- `app/schemas/` — Pydantic models for API request/response validation
- `tests/` — Comprehensive unit and integration tests

## Requirements

- Python 3.13+ (project uses modern Python features)
- Poetry (recommended) or pip for dependency management
- Dependencies (declared in `pyproject.toml`):
  - fastapi
  - uvicorn
  - pydantic
  - numpy
  - scipy
  - httpx (for API client examples)
  - redis (for session persistence)
  - pytest (development/testing)

## Quick start (with Poetry)

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Run the application locally:

   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Open the interactive docs at: http://127.0.0.1:8000/docs

## Docker

Build and run using Docker (the project includes a Dockerfile):

```bash
docker build -t digital-twin-backend .
docker run -p 8000:8000 digital-twin-backend
```


## API: Session-Based Workflow

The API provides session-based endpoints where each simulation runs in an isolated session with its own state, history, and logs.

### Session Lifecycle

1. **Initialize a Simulation Session**
   - Use `POST /simulate/init` to create a new session and return a session ID.

2. **Step the Simulation**
   - Use `POST /simulate/step` to advance the simulation by one time step.

3. **Query State, History, or Logs**
   - Use `GET /simulate/state/{session_id}` to get current state.
   - Use `GET /simulate/history/{session_id}` to get simulation history.
   - Use `GET /simulate/logs/{session_id}` to get model logs.

4. **Reset or Update Parameters**
   - Use `POST /simulate/reset` to reset the simulation with optional new parameters.
   - Use `PATCH /simulate/params` to update model parameters.

### Example Usage

#### 1. Initialize a New Session

```bash
curl -X POST "http://localhost:8000/simulate/init" \
  -H "Content-Type: application/json" \
  -d '{"model_name": "water_tank", "params": {}}'
```

Response:
```json
{"session_id": "123e4567-e89b-12d3-a456-426614174000"}
```

#### 2. Step the Simulation

```bash
curl -X POST "http://localhost:8000/simulate/step" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "control_input": 10.0,
    "delta_time": 1.0
  }'
```

#### 3. Get Current State

```bash
curl "http://localhost:8000/simulate/state/123e4567-e89b-12d3-a456-426614174000"
```

### Endpoints Summary

- `POST /simulate/init`: Initialize a new simulation session
- `POST /simulate/step`: Advance simulation by one step
- `GET /simulate/state/{session_id}`: Get current state
- `GET /simulate/history/{session_id}`: Get simulation history
- `GET /simulate/logs/{session_id}`: Get model logs
- `POST /simulate/reset`: Reset simulation with optional new parameters
- `PATCH /simulate/params`: Update model parameters


## Session Persistence

The simulation manager supports both in-memory and Redis-backed session persistence.

- **In-memory mode** (default): Sessions are stored in the process memory and lost on restart.
- **Redis mode**: Sessions are stored in Redis, allowing persistence across restarts and scaling to multiple processes.

### How to use Redis persistence

1. Install and run a Redis server (locally or in Docker):

   ```bash
   docker run -p 6379:6379 redis:7
   ```

2. Install the Python Redis client (already in Poetry dependencies):

   ```bash
   poetry add redis
   ```

3. Instantiate the simulation manager with Redis:

   ```python
   from app.services.simulation_manager import SimulationManager

   sim_manager = SimulationManager(
       model_registry=...,  # your models
       persistence='redis',
       redis_config={'host': 'localhost', 'port': 6379, 'db': 0}
   )
   ```

4. For in-memory mode (default):

   ```python
   sim_manager = SimulationManager(model_registry=...)
   ```

Sessions are automatically expired and cleaned up in both modes.


## Logging

The backend uses Python's built-in `logging` module for key events in the simulation manager (session creation, expiration, and errors).

To enable logging output, configure logging in your application entrypoint (e.g., `app/main.py`):

```python
import logging

# Log to 'digital_twin.log', overwrite file on each server start
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more detail
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    filename="digital_twin.log",
    filemode="w"  # Overwrite log file on each run
)
```

You can further customize logging handlers, levels, or direct logs to files as needed. All logs from the simulation manager use the logger name `SimulationManager`.


## Tests

Run the test suite with pytest:

```bash
poetry run pytest -q
```

To run tests with Redis persistence, ensure Redis is running and set up the simulation manager in your tests with `persistence='redis'` and the appropriate `redis_config`.

## Extending the project

- Add new models under `app/models` and register them in
  `app/models/factory.py` by updating `get_system`.
- Implement ML-based predictions in `app/services/ml_predictor.py` and expose
  endpoints in `app/routers`.
- Add structured request/response models in `app/schemas/api_models.py` using
  Pydantic.

## License

This project is provided as-is for learning and prototyping purposes. Add a
license file if you plan to publish or reuse the code.
