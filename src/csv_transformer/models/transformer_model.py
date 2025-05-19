import json
from typing import List, Dict, Optional
from dataclasses import dataclass

"""
These models implements the structure of the transformation definition:
{
  "transfomers":{
    "<transformer_name>": [{
      "column_name": <column_name>,
      "transformer_args": <JSON object with input args>
    }]
  },
  "column_order": [<column_name>, ...]
}
"""


@dataclass(frozen=True)
class TransformerDefinition:
    column_name: str
    transformer_args: dict

    def __repr__(self):
        return json.dumps({
            "column_name": self.column_name,
            "transformer_args": self.transformer_args
        })

@dataclass(frozen=True)
class Transformation:
    transformers: Dict[str, List[TransformerDefinition]]
    column_order: Optional[List[str]] = None