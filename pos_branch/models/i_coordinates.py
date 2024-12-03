from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class ICoordinates(ABC):
    
    @abstractmethod
    def get_coordinates(self, address: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        pass
