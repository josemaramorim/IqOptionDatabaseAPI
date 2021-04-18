from alembic import command

from src.database.migration.config import alembic_cfg
from src.utils.logger import logger


def upgrade():
    logger.info("Upgrading database..")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    upgrade()
