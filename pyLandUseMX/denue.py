# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/02_denue.ipynb.

# %% auto 0
__all__ = ['Denue']

# %% ../nbs/api/02_denue.ipynb 3
from fastcore.basics import *
import matplotlib.pyplot as plt
import geopandas as gpd
from .descargas import *
import warnings

# %% ../nbs/api/02_denue.ipynb 6
class Denue(object):
    """ Clase para guardar una capa del DENUE para procesarla."""
    def __init__(self,
                 datos:gpd.GeoDataFrame=None
                ) -> None:
        self.datos = datos

    @classmethod
    def desde_archivo(cls, path):
        gdf = gpd.read_file(path)
        d = cls(gdf)
        return d

# %% ../nbs/api/02_denue.ipynb 10
@patch
def filtra_scian(
        self:Denue,
        filtro:list, # Lista con las claves a filtrar
        categoria:str=None # Si se especifica agregamos una columna Categoría 
                           # y la populamos con el valor especificado
    )-> Denue:
    d = self.datos.loc[self.datos.codigo_act.str.startswith(tuple(filtro), na=False),:]
    if categoria is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            d.loc[:,'Categoria'] = categoria
    return Denue(d)

# %% ../nbs/api/02_denue.ipynb 18
@patch
def agrega_en_usos(
        self: Denue,
        categorias: dict, # Diccionario con la asociación entre cadenas de búsqueda en codigo_act y categorías de Uso de Suelo
        columna:str='Categoria' # Nombre de la columna en la que se va a guardar la categoría
    ) -> Denue:
    datos = self.datos.copy()
    datos[columna] = None
    for cat, pat in categorias.items():
        datos.loc[datos.codigo_act.str.contains('|'.join(pat)), 'Categoria'] = cat
    return Denue(datos)

# %% ../nbs/api/02_denue.ipynb 23
@patch
def pesa_unidades(self:Denue,
                  pesos:dict, # Diccionario con la relación per_ocu: peso asignado
                  columna:str='pesos', # Columna en donde vamos a guardar los pesos
    )->Denue:
    datos = self.datos.copy()
    datos[columna] = datos.per_ocu.map(pesos)
    return Denue(datos)

