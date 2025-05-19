from typing import Dict
from csv_transformer.models.transformer_model import Transformation, TransformerDefinition
from csv_transformer.common.logger import logger

class TransformerArgsParser:
    
    @staticmethod
    def parse(transformation_definition: dict) -> Transformation:
        """
        Parses the dictionary that holds the transformer definitions into a Transformation object.
        
        Args:
            transformer_definition (dict): transformation input argument
            
        Example:
        ```
        {
            "transfomers":{
                "<transformer_name>": [{
                "column_name": <column_name>,
                "transformer_args": <JSON object with input args>
                }]
            },
            "column_order": [<column_name>, ...]
        }
        ```
            
        Returns:
            Transformation: fully defined model of the transfomation input argument
        """

        # Validation
        logger.info("Validating if 'transformation' input argument sticks to the expected model")
        transformers: Dict = transformation_definition.get("transfomers", {})
        if not transformers:
            raise ValueError("'transfomers' is a mandatory argument and must be a valid JSON object")
        
        column_order = transformation_definition.get("column_order")
        if column_order and not isinstance(column_order, list):
            raise ValueError("If 'colum_order' is defined, it must be a list containing all fields of the input CSV file")
        
        # Build "transfomers" attribute
        logger.info("Deserializing 'transfomers' input argument to the internal model")
        transformers_dict = {}
        for transfomer_name, transfomer_items in transformers.items():
            column_transformations = []
            for item in transfomer_items:
                column_transformations.append(TransformerDefinition(
                    column_name=item["column_name"],
                    transformer_args=item["transformer_args"]
                ))
            transformers_dict[transfomer_name] = column_transformations
            
        # Build "transformation" object
        transfomation_object = Transformation(
            transformers=transformers_dict,
            column_order=column_order,
        )
        logger.info("Deserializtion completed successfully")
        return transfomation_object