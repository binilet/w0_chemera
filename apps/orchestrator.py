"""Top-level orchestrator CLI for Project Chimera (Mongo variant).

Run with `python -m apps.orchestrator`.
"""

from __future__ import annotations
import asyncio
import argparse


async def run_sequence(mongo_url: str | None = None):
    from apps.planner import main as planner_main
    from apps.worker import main as worker_main
    from apps.judge import main as judge_main

    # run planner once
    print("Orchestrator: running planner (one-shot)")
    await planner_main(mongo_url or "mongodb://localhost:27017", "chimera")

    # run worker and judge concurrently
    print("Orchestrator: starting worker and judge")
    await asyncio.gather(
        worker_main(mongo_url or "mongodb://localhost:27017", "chimera"),
        judge_main(mongo_url or "mongodb://localhost:27017", "chimera"),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo", default="mongodb://localhost:27017", help="MongoDB URI")
    args = parser.parse_args()
    try:
        asyncio.run(run_sequence(args.mongo))
    except KeyboardInterrupt:
        print("Orchestrator stopped")


if __name__ == "__main__":
    main()
