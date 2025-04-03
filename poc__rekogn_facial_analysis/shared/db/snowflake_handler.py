"""

"""
from typing import Dict, Any
import os
from logging import Logger
import snowflake.connector


class SnowflakeHandler:
    def __init__(self, logger: Logger, table_name: str) -> None:
        self.logger = logger
        self.table_name = table_name
        self.cnx = snowflake.connector.connect(
            user=os.environ.get('SF_USER'),
            password=os.environ.get('SF_PASSWORD'),
            account=os.environ.get('SF_ACCOUNT'),
            warehouse=os.environ.get('SF_WAREHOUSE'),
            database=os.environ.get('SF_DATABASE'),
            schema=os.environ.get('SF_SCHEMA')
        )
        self._create_table_if_not_exist(self.table_name)

    def _create_table_if_not_exist(self, table_name: str) -> None:
        query = f'CREATE TABLE IF NOT EXISTS {table_name} (id STRING, profile_location STRING, age_range OBJECT, gender STRING, emotions ARRAY, generated_on TIMESTAMP, raw_payload STRING)'
        cur = self.cnx.cursor()
        cur.execute(query)
        return 
    
    def insert_data(self, result: Dict[str, Any]):
        query = f"""
            INSERT INTO {self.table_name} 
            SELECT 
                '{result['id']}', 
                '{result['profile_location']}', 
                OBJECT_CONSTRUCT( 'low_age', {result['age_range']['low_age']}, 'high_age', {result['age_range']['high_age']} ), 
                '{result['gender']}', 
                ARRAY_CONSTRUCT( '{result['emotions'][0] if len(result['emotions']) > 0 else ' '}' ), 
                '{result['generated_on']}',
                '{result['raw_payload']}'
            ;
        """
        
        cur = self.cnx.cursor()
        try:
            cur.execute(query)
        except Exception as e:
            self.logger.error(f'ERROR: {e} // Query: {query}')
            raise e
        return 