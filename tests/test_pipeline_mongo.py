import asyncio

import pytest
from pymongo import MongoClient


@pytest.mark.asyncio
async def test_planner_inserts_task():
    """Planner should insert at least one document into planner_queue in test DB.

    This test expects a local MongoDB at mongodb://localhost:27017 and will fail if
    Mongo is not available. Tests are intentionally failing by default until
    the environment is set up.
    """
    from apps.planner import main as planner_main

    mongo_uri = "mongodb://localhost:27017"
    db_name = "chimera_test"

    # cleanup before run
    client = MongoClient(mongo_uri)
    client.drop_database(db_name)

    # run planner (one-shot)
    await planner_main(mongo_uri, db_name)

    db = client[db_name]
    count = db.planner_queue.count_documents({})
    assert count > 0, "Expected planner_queue to contain at least one task"


@pytest.mark.asyncio
async def test_worker_creates_review_item():
    """Worker should read from planner_queue and write to review_queue.

    This test expects a local MongoDB and will fail if it's not available.
    """
    from apps.planner import main as planner_main
    from apps.worker import main as worker_main

    mongo_uri = "mongodb://localhost:27017"
    db_name = "chimera_test"

    client = MongoClient(mongo_uri)
    client.drop_database(db_name)

    await planner_main(mongo_uri, db_name)

    # run worker for a short time to process one item
    task = asyncio.create_task(worker_main(mongo_uri, db_name))
    await asyncio.sleep(3)
    task.cancel()

    db = client[db_name]
    review_count = db.review_queue.count_documents({})
    assert review_count > 0, "Expected review_queue to contain at least one item"


@pytest.mark.asyncio
async def test_judge_escalates_low_confidence():
    """Judge should insert into hitl_queue when confidence < 0.75.

    This test is environment-dependent and will fail until Mongo is available.
    """
    from apps.judge import main as judge_main
    from pymongo import MongoClient

    mongo_uri = "mongodb://localhost:27017"
    db_name = "chimera_test"

    client = MongoClient(mongo_uri)
    db = client[db_name]
    client.drop_database(db_name)

    # insert a low-confidence review item
    db.review_queue.insert_one({"contentId": "c1", "confidence": 0.5, "notes": "low"})

    # run judge briefly
    task = asyncio.create_task(judge_main(mongo_uri, db_name))
    await asyncio.sleep(2)
    task.cancel()

    hitl_count = db.hitl_queue.count_documents({})
    assert hitl_count > 0, "Expected hitl_queue to contain escalation events"
