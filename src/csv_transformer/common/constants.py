from enum import Enum

class TransformersType(Enum):
    """
    Enum for the different types of transformations that can be applied to a column.
    """
    UUID_TO_INT = "uuid_to_int"
    FORMAT_DATE = "format_date"
    REDACT_DATA = "redact_data"