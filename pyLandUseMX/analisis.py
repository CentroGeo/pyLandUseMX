# AUTOGENERATED! DO NOT EDIT! File to edit: ../03_analisis.ipynb.

# %% auto 0
__all__ = ['Canasta']

# %% ../03_analisis.ipynb 3
from fastcore.basics import *
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from .descargas import *
from .denue import *
from .mallas import *


# %% ../03_analisis.ipynb 6
class Canasta (object):
    def __init__(self,
                 puntos:gpd.GeoDataFrame, # Los puntos que representan las actividades o items
                 malla: Malla, # Los polígonos en los que se agregan los items  
            ) -> None:
        self.puntos = puntos
        self.malla = malla

# %% ../03_analisis.ipynb 12
@patch
def asocia(self:Canasta,
           campo:str # Columna de `puntos` que clasifica a las observaciones
    ) -> Canasta:
    malla = self.malla.agrega_puntos(self.puntos, clasificacion=campo)
    return Canasta(self.puntos, malla) 

# %% ../03_analisis.ipynb 16
@patch
def codifica_transaccion(self:Canasta) -> pd.DataFrame:
    t = self.malla.malla.drop(columns='geometry').set_index('grid_id')
    # lambda x: (False) ix x <= 0 else True
    t = t.applymap(lambda x: False if x <= 0 else True)
    return t