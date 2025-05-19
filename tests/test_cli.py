import pytest
from pathlib import Path
from csv_transformer.cli import transform_csv
from csv_transformer.common.utils import get_csv_field_names


@pytest.mark.parametrize("transformation_definition",[
    "{\"transfomers\":{\"uuid_to_int\":[{\"column_name\":\"user_id\",\"transformer_args\":{\"initial_id\":1}}]},\"column_order\":[\"manager_id\",\"start_date\",\"user_id\",\"name\",\"email_address\",\"last_login\"]}", # inline
    "{\"transfomers\":{\"uuid_to_int\":[{\"column_name\":\"user_id\",\"transformer_args\":{\"initial_id\":1}}]}}", # inline
    "data/transformation_definition.json", # file path
])
def test_transform_csv_smoke_test(transformation_definition):
    
    def count_file_lines(file_path: str) -> int:
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)
    input_file = "data/user_sample.csv"
    output_file = "data/output.csv"
    transform_csv(input_file, output_file, transformation_definition)
    
    # output file exists
    assert Path(output_file).is_file()
    
    input_csv_field_names = get_csv_field_names(input_file)
    output_csv_field_names = get_csv_field_names(output_file)
    # same field names
    assert set(input_csv_field_names) == set(output_csv_field_names)
    # same row count
    assert count_file_lines(input_file) == count_file_lines(output_file)