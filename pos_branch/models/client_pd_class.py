from dataclasses import dataclass, field
from numpy import double
from typing import Optional
import pandas as pd
import ast


@dataclass
class CustomPDColumn:
    sours_name: str
    sours_type: type = str
    is_in_final: bool = True
    class_name: Optional[str] = None
    final_name: Optional[str] = None
    final_type: Optional[type] = None
    is_in_class: bool = True
    type_name: str = field(init=False)

    def __post_init__(self):
        self.type_name = self.get_pandas_type_name(self.sours_type)
        self.final_type = self.final_type if self.final_type else self.sours_type
        self.class_name = self.class_name if self.class_name else self.sours_name
        self.final_name = self.final_name if self.final_name else self.sours_name

    
    def get_pandas_type_name(self, dtype: type) -> str:
        
        if isinstance(dtype, int):
            return "int"
        if isinstance(dtype, float):
            return "float"
        return "string"
        
    
    def __call__(self):
        return self.class_name


@dataclass
class CustomPDColumns:
    
    def get_columns(self):
        raise Exception('get_columns not implemented')
    # AGE: CustomPDColumn = CustomPDColumn('age', sours_type=int)
    # SALARY: CustomPDColumn = CustomPDColumn('salary', sours_type=float)
    # NAME: CustomPDColumn = CustomPDColumn('Joe')


class ClientClass:
    
    def __init__(self, clms: CustomPDColumns, df: pd.DataFrame, table_name: str = 'table_name') -> None:
        self.clms: CustomPDColumns = clms
        self._cls_df: pd.DataFrame = self._init_df(df)
        self._table_name: str = table_name
        
    @property
    def cls_df(self) -> pd.DataFrame:
        return self._cls_df
    
    @cls_df.setter
    def cls_df(self, df: pd.DataFrame) -> None:
        df.name = self._table_name
        self._cls_df = df
        
    def _init_df(self, df: pd.DataFrame) -> pd.DataFrame:
        for clm in vars(self.clms).values():
            if isinstance(clm, CustomPDColumn) and clm.sours_name not in df.columns:
                continue
            if isinstance(clm, CustomPDColumn) and clm.is_in_class and clm.final_type in (str, int, float):
                df[clm()] = df.pop(clm.sours_name).astype(clm.final_type) 
            if isinstance(clm, CustomPDColumn) and clm.is_in_class and clm.final_type in (list, dict):
                df[clm()] = df.pop(clm.sours_name).apply(ast.literal_eval)
        return df
         
        
