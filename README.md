# Project Chimera

Project Chimera is a research sandbox for an autonomous influencer network. It provides a mocked, end-to-end pipeline that takes goals, decomposes them into tasks, processes those tasks, and evaluates outcomes with a human-in-the-loop (HITL) escalation path. The current implementation focuses on local development with MongoDB-backed queues and simple mock logic for each service.

## What's included

- **Planner service**: Reads goals and inserts tasks into the `planner_queue` collection.
- **Worker service**: Consumes tasks from `planner_queue`, simulates content generation, and writes outputs to `review_queue`.
- **Judge service**: Evaluates outputs from `review_queue` and either approves them or escalates to HITL via `hitl_queue`.
- **Orchestrator**: Runs the planner once, then starts worker + judge loops concurrently.
- **Specs, skills, governance, and research**: Supporting material for specification-driven development and agent governance experiments.

## Repository layout

```
apps/            Service implementations (planner, worker, judge, orchestrator).
research/        Notes and research artifacts.
skills/          Reusable skills and agent workflows.
specs/           Requirements/specification documents.
governance/      Safety and governance materials.
tests/           Test suite (expects MongoDB).
README_SERVICES.md  Service-focused run instructions.
```

## Requirements

- Python 3.11
- MongoDB (local or via Docker)

Python dependencies are listed in `pyproject.toml`.

## Quick start (local)

1. Start MongoDB locally, or use Docker Compose.

   **Local MongoDB:**
   ```bash
   mongod --dbpath ./data/db --bind_ip 127.0.0.1
   ```

   **Docker Compose:**
   ```bash
   docker compose up --build
   ```

2. Run the orchestrator (runs planner once, then worker + judge):

   ```bash
   uv run python -m apps.orchestrator
   ```

3. For service-by-service instructions, see `README_SERVICES.md`.

## Testing

Tests expect a running MongoDB instance.

```bash
uv run pytest
```

## Notes

- The services are intentionally mocked for local experimentation.
- Default MongoDB connection is `mongodb://localhost:27017` and database name is `chimera`.