import pytest
import tempfile
from pathlib import Path


@pytest.fixture(scope="session")
def temp_dir():
    with tempfile.TemporaryDirectory() as temp:
        yield Path(temp)
