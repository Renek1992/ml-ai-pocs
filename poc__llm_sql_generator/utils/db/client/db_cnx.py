"""
Client module for database connection
"""
from typing import Optional
from logging import Logger
import snowflake.connector
from db_cnx_base import BaseSnowflakeConnector

class SnowflakeConnector(BaseSnowflakeConnector):
    """
    Class for executing queries on Snowflake.
    """
    def __init__(self, logger: Logger, user: str, password: str, account: str, database: str, schema: str, warehouse: str, role: Optional[str] = None):
        """
        Initializes the SnowflakeQueryExecutor instance.
        
        :param logger: Logger instance
        :param user: Snowflake username
        :param password: Snowflake password
        :param account: Snowflake account identifier
        :param database: Target database
        :param schema: Target schema
        :param warehouse: Target warehouse
        :param role: (Optional) Role to use
        """
        self.logger = logger.getChild("SnowflakeConnector")

        super().__init__(user, password, account)
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.role = role
        self.connection = None

    def connect(self):
        """
        Establishes a connection to Snowflake.
        """
        try:
            self.connection = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account
            )
            self.logger.info("Successfully connected to Snowflake.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Snowflake: {e}")
            raise

    def close_connection(self):
        """
        Closes the Snowflake connection.
        """
        if self.connection:
            self.connection.close()
            self.logger.info("Snowflake connection closed.")
        else:
            self.logger.warning("Tried to close a connection that was not open.")