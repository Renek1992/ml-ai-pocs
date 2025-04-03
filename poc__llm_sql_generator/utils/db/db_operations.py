"""
DB operations
"""
import os
from typing import Dict, Any
from logging import Logger

from client.db_cnx import SnowflakeConnector




def get_table_schemas(logger: Logger, snowflake_connector: SnowflakeConnector, database: str, platform: str) -> Dict[str, Any]:
    """
    Retrieves the schema of all tables in the given database schema.
    
    :return: Dictionary with table names as keys and column details as values.
    """
    cnx = snowflake_connector(
        logger=logger,
        account=os.environ.get("ACCOUNT"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        warehouse=os.environ.get("WAREHOUSE"),
        database=os.environ.get("DATABASE"),
        schema=os.environ.get("SCHEMA")
    ).connect()
    if not cnx.connection:
        logger.error("Attempted to execute query without a valid connection.")
        raise ConnectionError("Not connected to Snowflake.")
    
    query = f"""
    SELECT table_name, column_name, data_type 
    FROM {database}.INFORMATION_SCHEMA.COLUMNS 
    WHERE table_schema = 'PUBLIC_MARTS'
    AND table_catalog = '{database}'
    AND table_name LIKE 'MRT_{platform}%'
    ;
    """
    
    try:
        with cnx.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            schema_dict = {}
            for table_name, column_name, data_type in result:
                if table_name not in schema_dict:
                    schema_dict[table_name] = []
                schema_dict[table_name].append({"column_name": column_name, "data_type": data_type})
            return schema_dict
        
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise