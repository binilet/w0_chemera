

# Project Chimera — AI Rules & System Instructions

##  Project Architecture (Context)

Project Chimera is a microservices-based autonomous influencer system.

* **Data Backbone:** MongoDB (used as a message broker/queue).
* **Core Loop:** `Planner` (Decomposition) → `Worker` (Execution) → `Judge` (Validation).
* **Entry Point:** `apps.orchestrator` manages service concurrency via `asyncio`.

##  Prime Directives

1. **Spec-First Development (SDD):** Before writing any implementation code, verify the corresponding file in `specs/`. If a feature isn't in the spec, ask to update the spec first.
2. **Test-Driven Reliability:** Always suggest creating a failing test in `tests/` that mirrors the technical requirements before providing the solution.

##  MongoDB Queue Patterns

* **Atomic Operations:** When implementing worker logic, always use `find_one_and_update` with `$set: {"status": "inProgress"}` to prevent race conditions.
* **Status Enum:** Strictly adhere to: `pending` | `inProgress` | `review` | `complete`.

##  Governance & Safety

* **Traceability:** Every code block must be preceded by a "Plan" summary.
* **The 0.90 Rule:** If logic involves probabilistic outputs (LLM stubs), include a confidence check. If `confidence < 0.90`, the code must route to the `HITL` (Human-In-The-Loop) escalation path.
* **Role Isolation:** - `Planner` creates tasks.
* `Worker` executes and moves to `review`.
* `Judge` validates and moves to `complete`.
* *Never* allow a Worker to mark a task as `complete`.



##  Coding Standards

* **Tooling:** Use `uv` for dependency management and `ruff` for linting.
* **Async:** Use `motor` for MongoDB and `asyncio` for service loops.
* **Models:** All data structures must be Pydantic v2 `BaseModel` classes.


