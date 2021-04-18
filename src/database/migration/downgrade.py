from alembic import command

from src.database.migration.config import alembic_cfg
from src.utils.logger import logger


def downgrade():
    logger.info("Downgrading database..")
    command.downgrade(alembic_cfg, "head")


if __name__ == "__main__":
    downgrade()
