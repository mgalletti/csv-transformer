from typing import Dict, List
from csv import DictReader, DictWriter

from csv_transformer.common.parsers import TransformerArgsParser
from csv_transformer.models.transformer_model import Transformation
from csv_transformer.services.dataset_transformer_service import DatasetTransformerService
from csv_transformer.common.logger import logger
from csv_transformer.common.utils import get_csv_field_names, is_a_valid_csv_file_path


def validate_csv_file_path(csv_file_path: str, file_must_exist: bool = True):
    if not is_a_valid_csv_file_path(csv_file_path, file_must_exist):
        raise ValueError(f"The path is not valid: {csv_file_path}")


class CSVTransformerService():
    """Service for transforming CSV files based on defined transformations.
    """

    def __init__(self, input_file: str, output_file: str):
        """Initialize the CSV transformer service.

        Args:
            input_file (str): Path to the input CSV file
            output_file (str): Path where the transformed CSV will be written
        """
        validate_csv_file_path(input_file)
        validate_csv_file_path(output_file, False)
        self._input_file = input_file
        self._output_file = output_file
        self._field_names = get_csv_field_names(input_file)


    def transform(self, transformations_definition: dict):
        """Transform the input CSV file using the provided transformers definition.
        
        Args:
            transformers_definition (dict): Dictionary containing the transformation rules
            
        Raises:
            RuntimeError: If an error occurs during CSV processing
        """
        logger.info(f"Start processing file {self._input_file}")
        parser = TransformerArgsParser()
        transformations: Transformation = parser.parse(transformations_definition)
        dataset_transfomer = DatasetTransformerService(self._field_names, transformations.transformers)
        column_order = self._field_names if not transformations.column_order else transformations.column_order
        if set(self._field_names) != set(column_order):
            raise ValueError(f"All column to be re-ordered must be listed. Provided: {column_order}")
        
        try:
            transformations.transformers
            output_rows = self._transform_input_file(dataset_transfomer)
            self._write_transformation_output(output_rows, column_order)
            
        except Exception as e:
            logger.error(f"Error while processing the input CSV: {e}")
            raise RuntimeError(f"An error occurred when processing the csv file '{self._input_file}': {e}")
    
    

    def _transform_input_file(self, dataset_transfomer: DatasetTransformerService) -> List[Dict[str, str]]:
        """Transform each row in the input CSV file using the dataset transformer.
        
        Args:
            dataset_transfomer (DatasetTransformerService): Service to transform individual rows
            
        Returns:
            List[Dict[str]]: List of transformed rows as dictionaries
            
        """
        logger.info(f"Reading file: {self._input_file}")
        try:
            with open(self._input_file, 'r', newline='') as csv_file:
                reader = DictReader(csv_file)
                
                logger.info("Applying transformation")
                output_rows = []
                for row in reader:
                    new_row = dataset_transfomer.transform_row(row)
                    output_rows.append(new_row)
                
            logger.info(f"{len(output_rows)} rows processed correctly")
            return output_rows
        except Exception as e:
            logger.error(f"Error while reading or transforming the input CSV file: {e}")
            raise
        
            

    def _write_transformation_output(self, rows: List[Dict[str, str]], reordered_fields):
        """Write the transformed rows to the output CSV file.
        
        Args:
            rows (List[Dict[str]]): List of transformed rows to write
            
        """
        try:
            logger.info(f"Writing output file {self._output_file} with transformed data")
            with open(self._output_file, 'w') as output_csv:
                writer = DictWriter(output_csv, fieldnames=reordered_fields)
                writer.writeheader()
                writer.writerows(rows)
            logger.info("File created correctly")
        except Exception as e:
            logger.error(f"Error while writing the output CSV file: {e}")
            raise
