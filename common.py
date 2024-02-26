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


# Loading yaml file into config()
def config():
    global __config
    if not __config:
        with open("queries.yaml", mode="r") as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)

    return __config


def validate_tables(table_origin, table_target):
    logger.info(f'Validating if tables: {table_origin} and {table_target} exist in queries.yaml')
    # Check if the tables exist in the configuration
    tables_config = config()["tables"]

    if table_origin not in tables_config:
        logger.error(f"Error: Table '{table_origin}' does not exist in queries.yaml")
        return False
    
    if table_target not in tables_config:
        logger.error(f"Error: Table '{table_target}' does not exist in queries.yaml")
        return False
    
    logger.info('Successful validation')
    return True


def validate_queries(table_origin, table_target):
    tables_config = config()["tables"]

    # Check if 'queries' exist for the tables
    if "queries" not in tables_config[table_origin]:
        logger.error(f"Error: Missing 'queries' section for table '{table_origin}' in queries.yaml")
        return False
    
    if "queries" not in tables_config[table_target]:
        logger.error(f"Error: Missing 'queries' section for table '{table_target}' in queries.yaml")
        return False

    # Verify 'select' for table_origin and 'insert' for table_target
    origin_queries = tables_config[table_origin]["queries"]
    target_queries = tables_config[table_target]["queries"]
    
    if origin_queries is None:
        logger.error(f"Error: Missing 'queries' section for table '{table_origin}' in queries.yaml")
        return False
    if target_queries is None:
        logger.error(f"Error: Missing 'queries' section for table '{table_target}' in queries.yaml")
        return False

    # Check if 'select' query exists and is not empty
    if "select" not in origin_queries or not origin_queries["select"]:
        logger.error(f"Error: Missing or empty 'select' query for table '{table_origin}' in queries.yaml")
        return False

    # Check if 'insert' query exists and is not empty
    if "insert" not in target_queries or not target_queries["insert"]:
        logger.error(f"Error: Missing or empty 'insert' query for table '{table_target}' in queries.yaml")
        return False

    return True
