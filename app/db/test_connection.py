from app.core.logging import get_logger
from app.db.session import engine

logger = get_logger(__name__)


def test_connection():
    with engine.connect() as connection:  # noqa: F841
        logger.info("Database connection successful!")


if __name__ == "__main__":
    test_connection()
