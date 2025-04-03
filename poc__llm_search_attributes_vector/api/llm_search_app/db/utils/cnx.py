"""
db connection.
"""
import lancedb
import logging

class DBCnx:
    def get_cnx(logger: logging.Logger, uri: str) -> lancedb.DBConnection:
        try:
            db = lancedb.connect(uri)
        except Exception as e:
            logger.error(e)
            raise e
        return db