import inspect
import pytest


def mock_skill_handler(task_id, payload, metadata):
    """
    Placeholder skill function.
    Will be replaced with real skills module.
    """
    return None


def test_skill_function_signature():
    """
    Skill functions MUST accept:
    - task_id: str
    - payload: dict
    - metadata: dict
    """

    sig = inspect.signature(mock_skill_handler)
    params = list(sig.parameters.keys())

    assert params == ["task_id", "payload", "metadata"], (
        f"Skill signature mismatch. Expected "
        f"(task_id, payload, metadata), got {params}"
    )
