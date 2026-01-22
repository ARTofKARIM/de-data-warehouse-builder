# Data Warehouse Builder

Automated star schema data warehouse builder with dimension/fact table generation, ETL loading, and analytical query engine.

## Architecture
```
de-data-warehouse-builder/
├── src/
│   ├── schema_generator.py  # Star schema DDL generation
│   ├── etl_loader.py        # Dimension and fact loading
│   ├── query_engine.py      # Analytical SQL queries
│   └── visualization.py     # Sales trend plotting
├── config/warehouse.yaml
├── tests/test_schema.py
└── main.py
```
## Installation
```bash
git clone https://github.com/mouachiqab/de-data-warehouse-builder.git
cd de-data-warehouse-builder && pip install -r requirements.txt
python main.py
```
## Technologies
- Python 3.9+, SQLAlchemy, pandas, Jinja2, loguru












