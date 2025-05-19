import arrow
from csv_transformer.transformers import BaseTransformer

class FormatDatetimeTransformer(BaseTransformer):
    """
    A transformer class that converts a timestamps to the appropriate datetime format assigned.

    Args:
        input_datetime_format (str): The format string to convert the date from (e.g. 'YYYY-MM-DD')
        output_datetime_format (str): The format string to convert the date to (e.g. 'YYYY-MM-DD')
    """

    def __init__(self, input_datetime_format: str="YYYY-MM-DD", output_datetime_format: str="YYYY-MM-DD"):
        super().__init__()
        self._input_datetime_format = input_datetime_format
        self._output_datetime_format = output_datetime_format

    def transform(self, value: str) -> str:
        """
        Transforms a date string to the specified datetime format.

        Args:
            value (str): Input date string to transform

        Returns:
            str: Date string formatted according to output_datetime_format
        """
        date = arrow.get(value, self._input_datetime_format)
        return date.format(self._output_datetime_format)
