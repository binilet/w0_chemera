Project Chimera — Mongo service scaffolds

Run each service locally (requires Python 3.10+, Pydantic v2, Motor & pymongo):

1. Start MongoDB locally (example):

```bash
# on macOS / Linux with brew or package manager
mongod --dbpath ./data/db --bind_ip 127.0.0.1
```

2. Run Planner (enqueues tasks into `planner_queue`):

```bash
python -m apps.planner.main
```

3. Run Worker (consumes from `planner_queue`, writes to `review_queue`):

```bash
python -m apps.worker.main
```

4. Run Judge (consumes from `review_queue`, logs decisions, writes to `hitl_queue` on low confidence):

```bash
python -m apps.judge.main
```

5. Orchestrator (runs planner once, then worker+judge):

```bash
python -m apps.orchestrator
```

Notes:
- Default MongoDB URI is `mongodb://localhost:27017` and default DB name is `chimera`.
- Tests in `tests/` expect a local MongoDB instance and will fail by default until Mongo is available.
- These are mock implementations for local development only.



