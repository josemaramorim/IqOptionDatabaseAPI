from alembic import command

from src.database.migration.config import alembic_cfg
from src.utils.logger import logger


def revision():
    logger.info("Reviewing database..")
    command.revision(alembic_cfg, autogenerate=True)


if __name__ == "__main__":
    revision()
