from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class IApiData(ABC):
    
    @abstractmethod
    def get_coordinates(self, address: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        pass
    
    @abstractmethod
    def get_distances_matrix_path(self, terminal_coords: Tuple[float, float], branch_coords_list: List[Tuple[str, Tuple[float, float]]], mode: str = 'walking') -> Tuple[Optional[str], float, Optional[Tuple[float, float]]]:
        pass