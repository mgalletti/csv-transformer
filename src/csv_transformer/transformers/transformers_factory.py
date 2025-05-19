from typing import Dict

from csv_transformer.transformers import BaseTransformer
from csv_transformer.common.constants import TransformersType
from csv_transformer.transformers.format_date_transformer import FormatDatetimeTransformer
from csv_transformer.transformers.uuid_to_int_transformer import UUIDToIntTransformer
from csv_transformer.transformers.redact_data_transformer import RedactDataTransformer
from csv_transformer.common.logger import logger

# Mapping between the transformer name (used in the factory to load the transformer from the input definition)
DEFAULT_TRANSFORMER_REGISTRY: Dict[str, BaseTransformer] = {
    TransformersType.UUID_TO_INT: UUIDToIntTransformer,
    TransformersType.FORMAT_DATE: FormatDatetimeTransformer,
    TransformersType.REDACT_DATA: RedactDataTransformer,
}


class TransformerFactory:
    """
    A factory class for creating transformer instances.
    
    This class manages a registry of transformer classes and provides a method to instantiate
    transformers by name.
    
    Args:
        transformer_registry (Dict[str, BaseTransformer]): A dictionary mapping transformer names
        to their corresponding transformer classes. Defaults to DEFAULT_TRANSFORMER_REGISTRY.
    """
    def __init__(self, transformer_registry: Dict[str, BaseTransformer] = DEFAULT_TRANSFORMER_REGISTRY):
        self._registry = transformer_registry

    def get_instance(self, transformer_type: str, **kwargs) -> BaseTransformer:
        """
        Creates and returns an instance of the requested transformer.
        
        Args:
            transformer (str): The name of the transformer to instantiate
            **kwargs: Additional keyword arguments to pass to the transformer constructor
            
        Returns:
            BaseTransformer: An instance of the requested transformer
            
        Raises:
            ValueError: If the transformer name is not found in the registry
        """
        
        # Validate the transformer type is valid
        try:
            transformer_type = TransformersType(transformer_type)
        except ValueError as e:
            logger.exception(f"Invalid transformer type: {transformer_type}. Error: {e}")
            raise ValueError(f"Transformer '{transformer_type}' is not supported")
         
        transformer_class = self._registry.get(transformer_type, None)
        return transformer_class(**kwargs)
