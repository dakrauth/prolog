import pytest
from prolog import PrologConfig


@pytest.fixture
def cfg():
    return PrologConfig(
        "pyprologtest", load_env=False, load_user=False, load_local=False
    )
