"""Star schema DDL generation."""
import pandas as pd
from typing import Dict, List

class SchemaGenerator:
    TYPE_MAP = {"int64": "INTEGER", "float64": "REAL", "object": "TEXT", "datetime64[ns]": "TEXT", "bool": "INTEGER"}

    def __init__(self):
        self.ddl_statements = []

    def infer_types(self, df):
        return {col: self.TYPE_MAP.get(str(df[col].dtype), "TEXT") for col in df.columns}

    def generate_dimension_ddl(self, name, columns_types, primary_key):
        cols = [f"  {col} {dtype}" for col, dtype in columns_types.items()]
        ddl = f"CREATE TABLE IF NOT EXISTS {name} (\n" + ",\n".join(cols) + f",\n  PRIMARY KEY ({primary_key})\n);"
        self.ddl_statements.append(ddl)
        return ddl

    def generate_fact_ddl(self, name, columns_types, dimension_keys, measures):
        cols = [f"  fact_id INTEGER PRIMARY KEY AUTOINCREMENT"]
        for col, dtype in columns_types.items():
            cols.append(f"  {col} {dtype}")
        ddl = f"CREATE TABLE IF NOT EXISTS {name} (\n" + ",\n".join(cols) + "\n);"
        self.ddl_statements.append(ddl)
        return ddl

    def generate_date_dimension(self, start, end):
        dates = pd.date_range(start, end, freq="D")
        df = pd.DataFrame({
            "date_id": range(len(dates)), "full_date": dates.strftime("%Y-%m-%d"),
            "year": dates.year, "quarter": dates.quarter, "month": dates.month,
            "month_name": dates.strftime("%B"), "week": dates.isocalendar().week,
            "day_of_week": dates.dayofweek, "day_name": dates.strftime("%A"),
            "is_weekend": (dates.dayofweek >= 5).astype(int),
        })
        return df

    def get_all_ddl(self):
        return "\n\n".join(self.ddl_statements)
