import pytest

from auth_backend.app import create_app


@pytest.fixture
def app():
    app = create_app()

    app.app_context().push()
    app.db.create_all()

    return app
