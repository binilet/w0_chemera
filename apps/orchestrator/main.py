"""Orchestrator: starts Planner once and runs Worker + Judge concurrently."""

from __future__ import annotations
import asyncio
import signal
from typing import Optional


async def _run_all(redis_url: str | None = None):
    # import services (absolute imports to work when run as `python -m apps.orchestrator`)
    from apps.planner import main as planner_main
    from apps.worker import main as worker_main
    from apps.judge import main as judge_main

    # run planner once to enqueue tasks
    print("Orchestrator: running planner (one-shot)")
    await planner_main(redis_url or "redis://localhost:6379/0")

    # start worker and judge as long-running tasks
    print("Orchestrator: starting worker and judge")
    worker_task = asyncio.create_task(worker_main(redis_url or "redis://localhost:6379/0"))
    judge_task = asyncio.create_task(judge_main(redis_url or "redis://localhost:6379/0"))

    # wait until cancelled
    done, pending = await asyncio.wait(
        [worker_task, judge_task], return_when=asyncio.FIRST_EXCEPTION
    )
    for t in pending:
        t.cancel()


def _handle_sigterm(loop: asyncio.AbstractEventLoop):
    for task in asyncio.all_tasks(loop):
        task.cancel()


def main(redis_url: str | None = None):
    loop = asyncio.new_event_loop()
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: _handle_sigterm(loop))
    except NotImplementedError:
        # Windows may raise for signal handlers in some contexts
        pass

    try:
        loop.run_until_complete(_run_all(redis_url))
    except asyncio.CancelledError:
        print("Orchestrator: cancelled, shutting down")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
