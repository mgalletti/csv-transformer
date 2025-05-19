from csv_transformer.cli import transform_csv

def test_transform_csv_smoke_test():
    assert transform_csv("input.csv", "output.csv", '{"transformer_name": [{"column_name": "column1", "args": {"arg1": "value1"}}]}')