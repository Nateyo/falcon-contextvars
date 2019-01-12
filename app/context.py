"""
Very basic ContextVar module.
"""
import falcon
from sqlalchemy.orm import Session

from contextvars import ContextVar, Token

db_session = ContextVar("db_session")


def get_db_session() -> Session:
    """
    Simple wrapper for retrieving the database session.

    Raises:
        falcon.HTTPInternalServerError: Raised if ContextVar lookup fails.

    Returns:
        (Session): Context specific SQLAlchemy Session.
    """
    try:
        return db_session.get()
    except LookupError:
        raise falcon.HTTPInternalServerError(
            "Context Failure", "The database session could not be retrieved."
        )


def set_db_session(session: Session) -> Token:
    """
    Simple wrapper for setting the database session.

    Args:
        session (Session): An active SQLAlchemy session.

    Returns:
        Token: ContextVar token.
    """
    return db_session.set(session)


def reset_db_session(token: Token):
    """
    Simple wrapper for reseting the database ContextVar.
    
    Args:
        token (Token): The token that was returned from a .set() call.
    """
    db_session.reset(token)

