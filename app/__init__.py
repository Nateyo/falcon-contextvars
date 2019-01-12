import falcon
from sqlalchemy import create_engine

from app.resources.example import ExampleResource
from app.middleware.db_session import DbSessionMiddleware


def create_app() -> falcon.API:
    """
    Typical application factory style setup.
    
    Returns:
        falcon.API: The falcon API object.
    """

    engine = create_engine("sqlite:///")

    app = falcon.API(middleware=[DbSessionMiddleware(engine)])

    app.add_route("/", ExampleResource())

    return app
