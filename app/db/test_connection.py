from app.core.logging import get_logger, setup_logging
from app.db.database import engine

setup_logging()
logger = get_logger(__name__)


def test_connection():
    with engine.connect() as connection:  # noqa: F841
        logger.info("Database connection successful!")


if __name__ == "__main__":
    test_connection()
