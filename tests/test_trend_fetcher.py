import pytest

def mock_fetch_trends():
    """
    This simulates the future trend-fetching agent.
    Replace with real implementation later.
    """
    return None  # Intentional failure for TDD


def test_trend_data_contract():
    """
    Contract:
    [
        {
            "topic": str,
            "source": str,
            "score": float,
            "timestamp": str
        }
    ]
    """
    trends = mock_fetch_trends()

    assert isinstance(trends, list), "Trends must be a list"

    if len(trends) > 0:
        trend = trends[0]

        assert "topic" in trend
        assert isinstance(trend["topic"], str)

        assert "source" in trend
        assert isinstance(trend["source"], str)

        assert "score" in trend
        assert isinstance(trend["score"], float)

        assert "timestamp" in trend
        assert isinstance(trend["timestamp"], str)
