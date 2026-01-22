"""Tests for schema generator."""
import unittest
import pandas as pd
from src.schema_generator import SchemaGenerator

class TestSchemaGenerator(unittest.TestCase):
    def test_infer_types(self):
        df = pd.DataFrame({"id": [1], "name": ["a"], "val": [1.5]})
        gen = SchemaGenerator()
        types = gen.infer_types(df)
        self.assertEqual(types["id"], "INTEGER")
        self.assertEqual(types["name"], "TEXT")

    def test_generate_date(self):
        gen = SchemaGenerator()
        df = gen.generate_date_dimension("2025-01-01", "2025-01-31")
        self.assertEqual(len(df), 31)
        self.assertIn("year", df.columns)

if __name__ == "__main__":
    unittest.main()
