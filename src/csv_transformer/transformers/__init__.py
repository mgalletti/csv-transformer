from abc import ABC, abstractmethod

class BaseTransformer(ABC):
    
    @abstractmethod
    def transform(self, value: str) -> str:
        raise NotImplementedError("Method 'transform' must be implemented")
    