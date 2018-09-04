from server import create_app
import pytest

"""
This file is required for pytest to run. Nothing special happening here.
"""

@pytest.fixture
def app():
    app = create_app()
    return app