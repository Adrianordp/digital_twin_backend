# -------------------------------
# 1️⃣ Base Image
# -------------------------------
FROM python:3.13-slim

# -------------------------------
# 2️⃣ Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# 3️⃣ Install Poetry
# -------------------------------
RUN pip install --no-cache-dir poetry

# -------------------------------
# 4️⃣ Copy pyproject.toml and lock file (if exists)
# -------------------------------
COPY pyproject.toml poetry.lock* ./

# -------------------------------
# 5️⃣ Install dependencies (production only)
# -------------------------------
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# -------------------------------
# 6️⃣ Copy the app source code
# -------------------------------
COPY app ./app

# -------------------------------
# 7️⃣ Expose Uvicorn port
# -------------------------------
EXPOSE 8000

# -------------------------------
# 8️⃣ Run FastAPI with Uvicorn via Poetry
# -------------------------------
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
