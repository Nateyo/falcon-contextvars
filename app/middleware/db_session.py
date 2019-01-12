"""
The DbSessionMiddleware handles creating and closing
sqlalchemy sessions and placing them in ContextVars for
use across the falcon application.
"""

import falcon

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from app.context import get_db_session, set_db_session, reset_db_session


class DbSessionMiddleware:
    def __init__(self, db_engine: engine):
        """
        Initialize the middleware with an engine.
        
        Args:
            db_engine (engine): Pre-configured sqlalchemy engine.
        """
        self.session_maker = sessionmaker(bind=db_engine)

    def process_resource(self, req, resp, resource, params):
        """
        Create a Session object and place it in the appropriate
        ContextVar.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """

        # Keep track of the token in req context, so it can be reset later.
        req.context["session_token"] = set_db_session(self.session_maker())

    def process_response(self, req, resp, resource, req_succeeded):
        """
        Cleanup the Session and reset the ContextVar. Resetting
        the ContextVar may not be strictly necessary, but appears
        to be good practice.

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """

        sess = get_db_session()

        try:
            if not req_succeeded:
                sess.rollback()
            else:
                sess.commit()
        except Exception:
            # Should be excepting IntegrityError, DatabaseError etc.
            raise falcon.HTTPInternalServerError(
                "Exception", "Something bad happened cleaning up sessions!"
            )
        finally:
            sess.close()
            reset_db_session(req.context["session_token"])
