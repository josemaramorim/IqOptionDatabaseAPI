import os

from alembic.config import Config

from src.settings import BASE_DIR, SQLALCHEMY_DB_URI


def update_config(config: Config) -> Config:
    config.set_main_option("script_location", f"{BASE_DIR}/src/database/migration")
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DB_URI)


alembic_cfg = Config(os.path.dirname(__file__), "alembic.ini")
update_config(alembic_cfg)
