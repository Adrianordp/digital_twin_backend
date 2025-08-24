# Roadmap

## Simulation API Integration Roadmap

1. **Model Registration**
   ✅ Done! Models are registered via a public method, and tests are in place.

2. **Router Integration**
   ✅ Done! The new session-based simulation router is included in your FastAPI app.

3. **Schema & Validation Enhancements**
   ✅ Done! Schemas are well-documented and validated.

4. **Testing**
   ✅ Done! Comprehensive unit tests for SimulationManager, including model registration.

5. **Frontend/Client Integration**
   ⬜ Next: Document/test the new endpoints with a client or frontend.

6. **Session Management Improvements**
   ⬜ Optional: Add session expiration, cleanup, or persistence if needed.

7. **Monitoring & Logging**
   ⬜ Optional: Add logging/metrics for production.

8. **Documentation**
   ⬜ Next: Update README and API docs to reflect the new session-based workflow.

---

## Next Steps

- **Test the API Endpoints:** Use curl, httpie, or Swagger UI to verify the new endpoints work as expected.
- **Integrate with Frontend:** If you have a frontend, update it to use the new session-based endpoints.
- **Add API/Integration Tests:** (Optional) Write tests that hit the FastAPI endpoints directly.
- **Document the API:** Update your README and/or OpenAPI docs.

# Dual-System Digital Twin

A small FastAPI-based digital twin backend that provides lightweight simulation
and control endpoints for simple engineering systems. The project currently
implements two example systems:

- Water Tank: a continuous tank model solved with SciPy's ODE solver.
- Room Temperature: a simple linear temperature model with a heater input.

This repository is intentionally minimal and designed as a starting point for
building digital twins and control/simulation APIs.

## Features

- REST endpoints to create/simulate systems and read their state
- Simple modular model structure (models in `app/models`)
- Example test for the water tank model

## Project structure

- `app/main.py` — FastAPI application entrypoint
- `app/routers/simulate.py` — `/simulate/{system_name}` (POST) to advance a
  system by one time step using a control input
- `app/routers/control.py` — `/control/{system_name}` (POST) to apply control
  to an already-initialized system
- `app/routers/state.py` — `/state/{system_name}` (GET) to read a system's
  current state
- `app/models/` — system model implementations (factory, water_tank,
  room_temperature)
- `app/services/` — placeholder for ML or other services
- `tests/` — basic pytest unit tests

## Requirements

- Python 3.13+ (project uses modern Python features)
- Poetry (recommended) or pip for dependency management
- Dependencies (declare in `pyproject.toml`):
  - fastapi
  - uvicorn
  - numpy
  - scipy
  - pytest

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

## API

All endpoints are defined in `app/routers` and accept simple scalar control
inputs.

- POST /simulate/{system_name}
  - Description: Initialize (if needed) and step the named system by one time
    step using the provided control input.
  - Parameters:
    - Path: `system_name` — e.g. `water_tank` or `room_temperature`
    - Query/body: `control_input` (float)
  - Response: JSON state returned by the model's `get_state()` method.

  Example:

  ```bash
  curl -X POST \
    "http://localhost:8000/simulate/water_tank?control_input=10.0"
  ```

- POST /control/{system_name}
  - Description: Apply a control input to an already-initialized system (the
    project shares state between simulate and control routers).
  - Parameters: same as `/simulate/{system_name}`

  Example:

  ```bash
  curl -X POST \
    "http://localhost:8000/control/water_tank?control_input=5.0"
  ```

- GET /state/{system_name}
  - Description: Return the current state of the named system.

  Example:

  ```bash
  curl "http://localhost:8000/state/water_tank"
  ```

Notes

- The endpoints accept `control_input` as a query parameter for the simple
  function signatures used in the code. You can adapt the routers to accept
  JSON bodies or pydantic models when more structure is needed.
- Systems are kept in-memory in the running process
  (`app.routers.simulate.systems`). For production use you will likely want
  persistent state or a dedicated simulation manager.

## Tests

Run the test suite with pytest:

```bash
poetry run pytest -q
```

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
