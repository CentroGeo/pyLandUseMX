# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_mallas.ipynb.

# %% auto 0
__all__ = ['grid_from_layer', 'puntos_a_malla', 'lineas_a_malla']

# %% ../01_mallas.ipynb 3
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
from .descargas import *
import warnings

# %% ../01_mallas.ipynb 7
def grid_from_layer(layer: gpd.GeoDataFrame, # Capa que define la extensión espacial de la malla
                    size: float # Tamaño de los elementos de la malla (en las unidades de la proyección de `layer`)
                    ) -> gpd.GeoDataFrame:
    """ 
    Regresa un GeoDataFrame con la malla de la extensión de la capa (`layer`) que se le pase y de tamaño `size`.
    
    """
    xmin, ymin, xmax, ymax = layer.total_bounds
    cols = list(np.arange(xmin, xmax + size, size))
    rows = list(np.arange(ymin, ymax + size, size))

    polygons = []
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(Polygon([(x,y), (x + size, y), (x + size, y + size), (x, y + size)]))

    grid = (gpd
           .GeoDataFrame({'geometry':polygons})
           .set_crs(layer.crs)
           .reset_index()
           .rename({'index':'grid_id'}, axis=1))
    return grid

# %% ../01_mallas.ipynb 13
def puntos_a_malla(puntos:gpd.GeoDataFrame, # La malla en la que se va a agregar
                   grid:gpd.GeoDataFrame, # La capa de puntos a agregar
                   campo: str='cuenta', # Nombre del campo en el que se guarda el resultado
                   )-> gpd.GeoDataFrame:
    if grid.crs != puntos.crs:
        puntos = puntos.to_crs(grid.crs)
    agregado = (puntos
                .to_crs(malla.crs)
                .sjoin(malla)
                .groupby('grid_id')
                .size()
                .reset_index()
                .rename({0:campo}, axis=1)
                .merge(malla, on='grid_id', how='right').fillna(0))
    agregado = (gpd.GeoDataFrame(agregado)
               .set_crs(malla.crs))
    return agregado

# %% ../01_mallas.ipynb 19
def lineas_a_malla(lineas:gpd.GeoDataFrame, # La capa de líneas a agregar
                   malla: gpd.GeoDataFrame, # La malla para la agregación
                   campo: str='longitud', # Nombre del campo en el que se guarda el resultado
                   ):
    """ Regresa la malla con la longitud de las lineas agregadas en cada elemento. """ 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        union = (red
                .to_crs(malla.crs)
                .overlay(malla, how='union')
                .dissolve(by='grid_id')
                .length.reset_index()
                .rename({0:campo}, axis=1)   
            )
    union = (malla
            .merge(union, on='grid_id', how='left')
            .fillna(0)
        )
    return union
