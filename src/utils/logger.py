from logging import INFO, Formatter, Logger, StreamHandler

logger = Logger("iqoption_database_api")
formatter = Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
handler = StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(INFO)
