import json

import falcon

from app.context import get_db_session


class ExampleResource:
    """
    Just a simple ExampleResource. 
    
    NOTE: Don't ever attach a session to a resource, as Resources
          are only instantiated once.
    """

    def on_get(self, req, resp):
        # One could use the database in the resource directly, if desired.
        sess = get_db_session()
        result = sess.execute("SELECT SUM(2+2)").scalar()
        resp.media = f"2+2 = {result}"

