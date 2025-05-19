from csv_transformer.transformers import BaseTransformer

class UUIDToIntTransformer(BaseTransformer):
    """
    Convert UUIDs into a simple integer sequence, whilst maintaining their uniqueness.
    Additionally, this transformer maintains a mapping between UUID strings and integer IDs,
    assigning new IDs sequentially starting from an initial value, defaulted to 0.

    Args:
        initial_id (int): the integer that set the id to start from.
    """

    def __init__(self, initial_id: int = 0):
        super().__init__()
        self._initial_id = initial_id
        self._dict = {}
    
    def transform(self, value: str) -> str:
        """
        Transform a UUID string into an integer ID.

        Args:
            value (str): The UUID string to transform

        Returns:
            str: The string representation of the integer ID assigned to this UUID
        """
        if value in self._dict:
            return str(self._dict[value])
            
        id = self._initial_id
        self._dict[value] = id
        self._initial_id += 1
        return str(id)
