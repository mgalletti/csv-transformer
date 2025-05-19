from csv_transformer.transformers import BaseTransformer
import random
import string

class RedactDataTransformer(BaseTransformer):
    """
    A transformer class that redacts fields to replace data that is sensitive with similar looking random data
    """

    def __init__(self):
        super().__init__()
    
    def transform(self, value: str) -> str:
        """
        Generate a random value preserving the same char type and string length
        Preserves character types (digits, lowercase, uppercase, special chars) and length.
        
        Args:
            value: The input string to analyze and match format
            
        Returns:
            A randomly generated string matching the format of the input
        """
        if not value:
            return ""
        
        result = []
        
        for char in value:
            if char.isdigit():
                result.append(random.choice(string.digits))
            elif char.islower():
                result.append(random.choice(string.ascii_lowercase))
            elif char.isupper():
                result.append(random.choice(string.ascii_uppercase))
            else:
                # keep same special characters
                result.append(char)
        
        return ''.join(result)
