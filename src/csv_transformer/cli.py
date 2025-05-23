#!/usr/bin/env python3

import sys
import argparse
from csv_transformer.common.logger import logger
from csv_transformer.common.utils import get_json_from_input
from csv_transformer.services.csv_transformer_service import CSVTransformerService

def transform_csv(input_file: str, output_file: str, transformations: str) -> bool:
    """
    Transform a CSV file based on specified transformations.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
        transformations: definition of transformation and re-ordering of input csv fields. It can be either a escaped JSON or a JSON file
    
    Returns:
        bool: True if transformation was successful, False otherwise
    """
    try:
        payload = {
            'input': input_file,
            'output': output_file,
            'transformations': transformations
        }
        logger.info(f"Input payload: {payload}")
        transformations_json = get_json_from_input(transformations)
        logger.info(f"Transformations definition: {transformations_json}")
        
        service = CSVTransformerService(input_file, output_file)
        service.transform(transformations_json)
        
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='CSV transformer. Applies transformations to fields as per definition.')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('output', help='Output CSV file')
    parser.add_argument('-t', '--transform',
        help="""Transformations definition. Passed as escaped JSON object or path to a JSON file. Format:
        {
        "tramsformations":{
            "<transformer_name>": [{
            "column_name": <column_name>,
            "transformer_args": <JSON object with input args>
            }]
        },
        column_order: [<column_name>, ...]
        }
        """
    )
    
    args = parser.parse_args()
    
    success = transform_csv(args.input, args.output, args.transform)
    
    if success:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
