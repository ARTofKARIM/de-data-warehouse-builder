"""Main entry point for data warehouse builder."""
import argparse
import yaml
import pandas as pd
from src.schema_generator import SchemaGenerator
from src.etl_loader import WarehouseLoader
from src.query_engine import QueryEngine

def main():
    parser = argparse.ArgumentParser(description="Data Warehouse Builder")
    parser.add_argument("--config", default="config/warehouse.yaml")
    args = parser.parse_args()
    with open(args.config) as f:
        config = yaml.safe_load(f)
    gen = SchemaGenerator()
    loader = WarehouseLoader(config["warehouse"]["connection"])
    for dim in config.get("dimensions", []):
        if dim.get("auto_generate"):
            df = gen.generate_date_dimension(*dim["range"])
            loader.load_dimension(dim["name"], df)
        elif "source" in dim:
            df = pd.read_csv(dim["source"])
            types = gen.infer_types(df)
            gen.generate_dimension_ddl(dim["name"], types, dim["key"])
            loader.load_dimension(dim["name"], df)
    print("Warehouse built.")
    counts = loader.get_table_counts()
    for table, count in counts.items():
        print(f"  {table}: {count} rows")

if __name__ == "__main__":
    main()
