import os
from datetime import datetime
from dotenv import load_dotenv
from database import Database

load_dotenv()

# Configurando Logger
import logging.handlers as handlers
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%d/%m/%Y %I:%M:%S", handlers=[ logging.StreamHandler(), handlers.TimedRotatingFileHandler('audit.log', when='midnight', interval=1) ])
logger = logging.getLogger(__name__)

# Configurando parámetros a pasar al ejecutar el programa
import argparse
parser = argparse.ArgumentParser(description = 'Database migration for tables in PostgreSQL')
parser.add_argument('-id','--initDate', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help='Init date to fetch records from database -format YYYY-MM-DD', required=True, metavar='')
parser.add_argument('-ed','--endDate', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help='End date to fetch records from database -format YYYY-MM-DD', required=True, metavar='')
parser.add_argument('-to','--tableOrigin', type=str, help='Table to migrate', required=True, metavar='')
parser.add_argument('-tt','--tableTarget', type=str, help='Table to migrate', required=True, metavar='')
args = parser.parse_args()


def runMigration(initDate, endDate, tableOrigin, tableTarget):
   print(initDate, endDate, tableOrigin, tableTarget)
   query_select =f'SELECT * FROM {tableOrigin}'
   getDataOrigin = Database.executeQuery(source='ORIGIN',method='select',query=query_select)

   for element in getDataOrigin:
      print(element)
      print(element[4])
      query_insert = f"INSERT INTO {tableTarget} (first_name, last_name, email, password, is_active) VALUES (%s, %s, %s, %s, %s)"
      values = (element[1], element[2], element[3], element[4], element[5])
      asd = Database.executeQuery(method='insert', query=query_insert, source='TARGET', values=values)
      print(asd)

if __name__ == '__main__':
   runMigration(args.initDate, args.endDate, args.tableOrigin, args.tableTarget)