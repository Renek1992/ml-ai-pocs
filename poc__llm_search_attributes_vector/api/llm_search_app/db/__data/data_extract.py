import os
import polars as pl
import snowflake.connector
import logging
from api.common.logging import PythonLogger


def extract_data(logger: logging.Logger):
    try:
        conn = snowflake.connector.connect(
            user=os.environ.get('SF_USER'),
            password=os.environ.get('SF_PASSWORD'),
            account=os.environ.get('SF_ACCOUNT'),
            warehouse=os.environ.get('SF_WAREHOUSE'),
            database=os.environ.get('SF_DATABASE'),
            schema=os.environ.get('SF_SCHEMA')
        )

        query = f'SELECT * FROM "{os.environ.get('SF_TABLE')}" ORDER BY rank'
        cur = conn.cursor()
        logger.info(f"Retrieving data set for table: {os.environ.get('SF_TABLE')}")
        cur.execute(query)
        rows = cur.fetchall()

        columns = [desc[0] for desc in cur.description]

        data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}
        df = pl.DataFrame(data)
        logger.info(f"\n{df.head()}")
        return df

    except snowflake.connector.errors.ProgrammingError as e:
        err_msg = f"Snowflake ProgrammingError: {e}"
        logger.error(err_msg)
        raise err_msg

    except snowflake.connector.errors.DatabaseError as e:
        err_msg = f"Snowflake DatabaseError: {e}"
        logger.error(err_msg)
        raise err_msg
    
    except Exception as e:
        err_msg = f"An error occurred: {e}"
        logger.error(err_msg)
        raise err_msg
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    logger = PythonLogger.get_logger("test")
    extract_data(logger)
