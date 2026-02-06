FROM python:3.11-slim

# Install uv [cite: 374]
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Set environment variables for non-interactive installs
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies only for the final image
RUN uv sync --frozen --no-dev --no-install-project

# Copy project source
COPY . .

# Default command for the orchestrator
CMD ["uv", "run", "python", "-m", "apps.orchestrator"]