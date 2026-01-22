"""Analytical query engine for the data warehouse."""
import pandas as pd

class QueryEngine:
    def __init__(self, loader):
        self.loader = loader

    def sales_by_dimension(self, dimension, measure="amount"):
        dim_table = f"dim_{dimension}"
        key = f"{dimension}_id"
        sql = f"""SELECT d.*, SUM(f.{measure}) as total_{measure}
                  FROM fact_sales f JOIN {dim_table} d ON f.{key} = d.{key}
                  GROUP BY f.{key} ORDER BY total_{measure} DESC"""
        return self.loader.query(sql)

    def time_series_sales(self, granularity="month"):
        col_map = {"year": "d.year", "quarter": "d.quarter", "month": "d.month", "week": "d.week"}
        group_col = col_map.get(granularity, "d.month")
        sql = f"""SELECT {group_col} as period, SUM(f.amount) as revenue, COUNT(*) as orders
                  FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id
                  GROUP BY {group_col} ORDER BY period"""
        return self.loader.query(sql)

    def top_products(self, n=10):
        sql = f"""SELECT p.*, SUM(f.amount) as revenue, SUM(f.quantity) as units_sold
                  FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id
                  GROUP BY f.product_id ORDER BY revenue DESC LIMIT {n}"""
        return self.loader.query(sql)
