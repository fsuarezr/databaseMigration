import logging

# Configurando Logger
import logging.handlers as handlers

import yaml

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S",
    handlers=[logging.StreamHandler(),handlers.TimedRotatingFileHandler("audit.log", when="midnight", interval=1),],
)
logger = logging.getLogger(__name__)

__config = None


def config():
    global __config
    if not __config:
        with open("queries.yaml", mode="r") as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)

    return __config


def validate_tables(table_origin, table_target):
    if table_origin not in config()["tables"]:
        logger.error(f"Error: Table '{table_origin}' not found in queries.yaml")
        return False

    if table_target not in config()["tables"]:
        logger.error(f"Error: Table '{table_target}' not found in queries.yaml")
        return False

    return True


def validate_queries(table_origin, table_target):
    if "queries" not in config()["tables"][table_origin]:
        logger.error(
            f"Error: Missing 'queries' section for table '{table_origin}' in queries.yaml"
        )
        return False

    if "queries" not in config()["tables"][table_target]:
        logger.error(
            f"Error: Missing 'queries' section for table '{table_target}' in queries.yaml"
        )
        return False

    if "select" not in config()["tables"][table_origin]["queries"]:
        logger.error(
            f"Error: Missing 'select' query for table '{table_origin}' in queries.yaml"
        )
        return False

    if "insert" not in config()["tables"][table_target]["queries"]:
        logger.error(
            f"Error: Missing 'insert' query for table '{table_target}' in queries.yaml"
        )
        return False

    return True
