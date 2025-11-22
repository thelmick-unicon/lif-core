import psycopg2
from psycopg2 import Error
import mysql.connector
import os

from lif.mdr_utils.logger_config import get_logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logger = get_logger(__name__)


DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PASSWORD')}@{os.getenv('POSTGRESQL_HOST')}:{os.getenv('POSTGRESQL_PORT')}/{os.getenv('POSTGRESQL_DB')}"
logger.info(f"DATABASE_URL : {DATABASE_URL}")
# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async sessionmaker
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_db_connection(db_type: str):
    # We can use
    try:
        match db_type:
            case "POSTGRESQL":
                # Connect to your PostgreSQL database
                logger.info("DB type is POSTGRESQL")
                connection = psycopg2.connect(
                    user=os.environ["POSTGRESQL_USER"],
                    password=os.environ["POSTGRESQL_PASSWORD"],
                    host=os.environ["POSTGRESQL_HOST"],
                    port=os.environ["POSTGRESQL_PORT"],
                    database=os.environ["POSTGRESQL_DB"],
                )
                logger.info("Connection Done")

            case "MYSQL":
                logger.info("DB type is MYSQL")
                connection = mysql.connector.connect(
                    host=os.environ["MYSQL_HOST"],
                    port=os.environ["MYSQL_PORT"],
                    user=os.environ["MYSQL_USER"],
                    password=os.environ["MYSQL_PASSWORD"],
                    database=os.environ["MYSQL_DB"],
                )
                logger.info("Connection Done")
            case _:
                logger.info("Specified database type is not configured : %s", db_type)
                raise Exception

        return connection
    except (Exception, Error) as error:
        logger.error("Error while connecting DB doe the DB type: %s.  Error : %s", db_type, error)
        raise
