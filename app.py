import sys
from datetime import datetime

from dotenv import load_dotenv

from common import validate_queries, validate_tables
from database import Database
from common import config

load_dotenv()

import logging

# Configuring Logger
import logging.handlers as handlers

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S",
    handlers=[logging.StreamHandler(),handlers.TimedRotatingFileHandler("audit.log", when="midnight", interval=1),],
)
logger = logging.getLogger(__name__)

# Configuring parameters to pass when running the program
import argparse
parser = argparse.ArgumentParser(description = 'Database migration for tables in PostgreSQL')
parser.add_argument('-id','--initDate', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help='Init date to fetch records from database -format YYYY-MM-DD', required=True, metavar='')
parser.add_argument('-ed','--endDate', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help='End date to fetch records from database -format YYYY-MM-DD', required=True, metavar='')
parser.add_argument('-to','--tableOrigin', type=str, help='Table to extraxt data', required=True, metavar='')
parser.add_argument('-tt','--tableTarget', type=str, help='Table to migrate data', required=True, metavar='')
args = parser.parse_args()


def runMigration(initDate, endDate, tableOrigin, tableTarget):
    if not validate_tables(table_origin=tableOrigin, table_target=tableTarget):
        sys.exit()

    if not validate_queries(table_origin=tableOrigin, table_target=tableTarget):
        sys.exit()

    query_select = config()["tables"][tableOrigin]["queries"]["select"]
    getDataOrigin = Database.executeQuery(
        source="ORIGIN", method="select", query=query_select, table=tableOrigin
    )

    logger.info(f'Records found on {tableOrigin}: {len(getDataOrigin)}')

    if len(getDataOrigin) == 0:
        logger.info(f'No records found on {tableOrigin}')
        sys.exit()

    # Get column names from the target table configuration
    target_columns = config()["tables"][tableTarget]["columns"]

    records_inserted = 0

    for element in getDataOrigin:
        logger.info(' ')
        logger.info(f'Saving record {element} into: {tableTarget}')
        query_insert = config()["tables"][tableTarget]["queries"]["insert"]
        # Extract values based on column names, handling potential mismatches
        values = [element[target_columns.index(col)] if col in target_columns else None for col in target_columns]
        insert_result = Database.executeQuery(
            method="insert", query=query_insert, source="TARGET", values=values, table=tableTarget
        )
        logger.info(f'Record saved on {tableTarget}: {insert_result}')
        records_inserted +=1

    logger.info(f'{records_inserted} records were inserted on {tableTarget}')

if __name__ == "__main__":
    runMigration(args.initDate, args.endDate, args.tableOrigin, args.tableTarget)

