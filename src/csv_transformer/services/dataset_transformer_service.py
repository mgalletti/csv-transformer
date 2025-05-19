from typing import List, Dict
from csv_transformer.models.transformer_model import TransformerDefinition
from csv_transformer.transformers.transformers_factory import TransformerFactory
from csv_transformer.transformers import BaseTransformer


    
def _build_fields_transformer_map(transfomers: Dict[str, List[TransformerDefinition]]) -> Dict[str, BaseTransformer]:
    mapping = {}
    transformer_factory = TransformerFactory()
    for transformer_name, transformer_definitions in transfomers.items():
        for definition in transformer_definitions:
            mapping[definition.column_name] = transformer_factory.get_instance(transformer_name, **definition.transformer_args)
        
    return mapping


class DatasetTransformerService:
    def __init__(self, field_names: List[str], transformer_defition: Dict[str, List[TransformerDefinition]]):
        self._field_names = set(field_names)
        self._fields_transformer_map = _build_fields_transformer_map(transformer_defition)


    def transform_dataset(self, dataset: List[Dict[str, str]]) -> List[Dict[str, str]]:
        output_dataset = []
        for row in dataset:
            output_dataset.append(self.transform_row(row))
            
        return output_dataset

    
    def transform_row(self, row: Dict[str, str]) -> Dict[str, str]:
        new_row = {}
        for field in self._field_names:
            if field in self._fields_transformer_map:
                new_row[field] = self._fields_transformer_map[field].transform(row[field])
            else:
                new_row[field] = row[field]
                
        return new_row
