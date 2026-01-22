"""ETL loading for warehouse dimensions and facts."""
import pandas as pd
from sqlalchemy import create_engine, text
import os

class WarehouseLoader:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def execute_ddl(self, ddl):
        with self.engine.connect() as conn:
            for stmt in ddl.split(";"):
                stmt = stmt.strip()
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()

    def load_dimension(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")

    def load_fact(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")

    def query(self, sql):
        return pd.read_sql(text(sql), self.engine)

    def get_table_counts(self):
        with self.engine.connect() as conn:
            tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            counts = {}
            for (table,) in tables:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                counts[table] = count
        return counts
