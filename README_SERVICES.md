Project Chimera — Service scaffolds

Run each service locally (requires Python 3.10+, Pydantic v2, redis-py):

1. Start Redis locally:

```bash
redis-server --daemonize yes
```

2. Run Planner (enqueues tasks):

```bash
python -m apps.planner.main
```

3. Run Worker (consumes tasks, pushes review items):

```bash
python -m apps.worker.main
```

4. Run Judge (consumes review items, logs decisions):

```bash
python -m apps.judge.main
```

Notes:
- Services use `redis://localhost:6379/0` by default. Set a different URL by passing it to `main()` functions.
- These are mock implementations for local development and testing only.
