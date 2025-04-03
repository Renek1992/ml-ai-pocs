import os
import logging
import lancedb
import polars as pl
from typing import List, Dict
from api.llm_search_app.db.utils.cnx import DBCnx
from api.llm_search_app.db.__data.data_extract import extract_data

class DBManager:
    def __init__(self, logger: logging.Logger) -> None:
        self.db: lancedb.DBConnection = DBCnx.get_cnx(
            logger=logger, 
            uri=os.environ.get('DB_URI')
        )
        self.logger = logger


    def create_table(self, name: str, data: List[Dict]):
        tbl = self.db.create_table(
            name=name,
            data=data,
            mode="overwrite"
        )
        if tbl:
            self.logger.info("Created table in LanceDB")


    def load_dataset(self) -> pl.DataFrame:
        df = extract_data(logger=self.logger)
        self.logger.info("Loaded dataset")
        return df
    


    def open_table(self, table_name: str) -> lancedb.table:
        tbl = self.db.open_table(name=table_name)
        self._show_table(table_name=table_name)
        return tbl
        

    def _show_table(self, table_name: str):
        df = self.db[table_name].to_polars()
        self.logger.debug(df.collect().limit(10))