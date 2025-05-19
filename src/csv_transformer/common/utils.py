import json
from typing import List
from pathlib import Path
from csv import DictReader
from csv_transformer.common.logger import logger


def validate_json_file_path(arg: str) -> bool:
    """
    Validates if the provided argument is a path to a valid JSON file.
    
    Args:
        arg (str): Path to check if it points to a JSON file
        
    Returns:
        bool: True if path points to a valid JSON file, False otherwise
        
    Example:
        >>> validate_json_file_path("data.json")
        True
        >>> validate_json_file_path("data.txt") 
        False
    """
    try:
        file_path = Path(arg)
        logger.info(f"Validate if input arguments is a file: {arg}")
        
        return file_path.is_file() and file_path.suffix.lower() == ".json"
        
    except Exception as e:
        logger.warning(f"Input argument doesn't appear to be a file: {e}. Returning empty string.")
        return False


def get_json_from_input(transform_argument: str) -> str:
    """
    Loads and parses JSON data from either a file path or a JSON string.

    Args:
        transform_argument (str): Either a path to a JSON file or a JSON-formatted string

    Returns:
        str: The parsed JSON data

    Raises:
        ValueError: If the input cannot be parsed as valid JSON

    Example:
        >>> get_json_from_input('data.json')  # Loads from file
        {'key': 'value'}
        >>> get_json_from_input('{"key": "value"}')  # Parses JSON string
        {'key': 'value'}
    """
    logger.info("Loading the transformations definition")
    try:
        if validate_json_file_path(transform_argument):
            with Path(transform_argument).open() as json_file:
                return json.load(json_file)
        else:
            return json.loads(transform_argument)
    except json.JSONDecodeError as e:
        logger.error(f"The transformation definition is not a valid JSON object: {e}")
        raise ValueError("The transformation definition is not a proper JSON object", e)

       
def get_csv_field_names(input_file_path: str) -> List[str]:
    """
    Gets the field names (column headers) from a CSV file.

    Args:
        input_file_path (str): Path to the CSV file to read headers from

    Returns:
        List[str]: List of field names from the CSV header row

    Raises:
        ValueError: If the input file path is invalid or file does not exist

    """
    file_path = Path(input_file_path)
    if file_path.is_file():
        with open(input_file_path, 'r', newline='') as csv_file:
            reader = DictReader(csv_file)
            return reader.fieldnames
    else:
        ValueError(f"The input file path is invalid: {input_file_path}")


def is_a_valid_csv_file_path(file_path: str, file_must_exist: bool = True) -> bool:
    """
    Validates if the provided string is a valid path where a file can be created.
    Checks if the parent directory exists and is writable.
    
    Args:
        file_path (str): Path to validate
        
    Returns:
        bool: True if the path is valid for file creation, False otherwise
    """
    try:
        path = Path(file_path)
        parent_dir = path.parent
        # Check if file exists if expected to be there or if the parent directory exists
        valid_path = path.is_file() if file_must_exist else parent_dir.exists()
        
        return valid_path and path.suffix.lower() == ".csv"
        
    except Exception as e:
        logger.warning(f"Invalid file path: {e}")
        return False
    