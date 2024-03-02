import psycopg2
import os

# Configurando Logger
import logging.handlers as handlers
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S",
    handlers=[logging.StreamHandler(),handlers.TimedRotatingFileHandler("audit.log", when="midnight", interval=1),],
)
logger = logging.getLogger(__name__)


class Database:
    @classmethod
    def getConnection(self, source):
        logger.info(f"Establishing connection to the Database {source}")

        try:
            # Getting env variables
            DB_NAME = os.getenv(f"DB_NAME_{source}")
            DB_USER = os.getenv(f"DB_USER_{source}")
            DB_PASSWORD = os.getenv(f"DB_PASSWORD_{source}")
            DB_PORT = os.getenv(f"DB_PORT_{source}")
            DB_HOST = os.getenv(f"DB_HOST_{source}")

            connection = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )

            logger.info("Connection to PostgreSQL DB successful")
            cursor = connection.cursor()

            return cursor

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                logger.info("PostgreSQL connection is closed")

    @classmethod
    def executeQuery(self, method, query, source, values=None, table=None):
        cursor = self.getConnection(source)

        try:
            if method == "select":
                logger.info(f"Getting data from {table}")
                cursor.execute(query)
                data = cursor.fetchall()
                return data

            elif method == "insert":
                logger.info(f"Inserting record into {table}")
                cursor.execute(query, values)
                cursor.connection.commit()
                return True

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            cursor.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
                logger.info("Cursor is closed")
