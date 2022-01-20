import pytest

@pytest.fixture
def some_fixture():
    return 12


def test_one(some_fixture):
    assert some_fixture == 120
