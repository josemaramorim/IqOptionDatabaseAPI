from decouple import config

WORKERS = config("WORKERS", default=4, cast=int)
HOST = config("HOST")
PORT = config("PORT", default=8000, cast=int)
DEBUG = config("DEBUG", default=False, cast=bool)
BASE_PATH = config("BASE_PATH", default="")
AUTH_TOKEN = config("AUTH_TOKEN")
CHECK_AUTH_TOKEN = config("CHECK_AUTH_TOKEN", default=True, cast=bool)
SQLALCHEMY_DB_URI = config("SQLALCHEMY_DB_URI")
