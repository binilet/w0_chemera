import pytest

@pytest.mark.parametrize("x,y,expected", [(1, 1, 2)], ids=["CI sanity check"])
def test_ci_sanity_pass(x, y, expected):
    assert x + y == expected 
