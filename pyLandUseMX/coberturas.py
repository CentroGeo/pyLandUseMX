# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/01_coberturas.ipynb.

# %% auto 0
__all__ = ['Cobertura', 'Malla', 'Poligonos']

# %% ../nbs/api/01_coberturas.ipynb 3
from abc import ABC, abstractmethod
from fastcore.basics import *
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import rasterio
from pyproj.crs import crs
from rasterio.features import shapes
from shapely.geometry import Polygon
from geocube.api.core import make_geocube
import numpy as np
from .descargas import *
from .denue import *
import warnings
import random
from typing import Union
from pathlib import Path

# %% ../nbs/api/01_coberturas.ipynb 6
class Cobertura(ABC):
    """Clase abstracta que define la interfaz para los diferentes tipos de cobertura."""
    @abstractmethod
    def agrega_puntos(self,
                      puntos:gpd.GeoDataFrame,
                      campo:str,
                      clasificacion:str
        ):
        """ Debe proveer la funcionalidad para agregar puntos en los elementos de la cobertura."""
        pass

    @abstractmethod
    def agrega_lineas(self,
                      lineas:gpd.GeoDataFrame,
                      campo:str
        ):
        """ Debe proveer la funcionalidad para agregar líneas en los elementos de la cobertura."""
        pass
    
    @abstractmethod
    def agrega_manzanas(self,
                        manzanas:gpd.GeoDataFrame,
                        variables: str                        
        ):
        """ Debe agregar variables del censo en la cobertura. """
        pass

    @abstractmethod
    def to_crs(self,
               to_crs:Union[int, str, crs.CRS]
    ):
        """ Se encarga de transformar de coordenadas."""
        pass

# %% ../nbs/api/01_coberturas.ipynb 8
class Malla(Cobertura):
    """ Representa una malla para procesar variables de uso de suelo."""
    def __init__ (self,
                  datos:gpd.GeoDataFrame=None, # La malla vectorial
                  size:float=1000, # Tamaño de los elementos de la malla (en las unidades de la proyección de `layer`)
        ) -> None:
        self.size = size
        self.datos = datos
        self.crs = datos.crs
    
    @classmethod
    def desde_capa(cls, 
                  capa:gpd.GeoDataFrame, # La capa que define la extensión de la malla 
                  size:float # Tamaño de la malla en unidades de la proyección
        ):
        xmin, ymin, xmax, ymax = capa.total_bounds
        cols = list(np.arange(xmin, xmax + size, size))
        rows = list(np.arange(ymin, ymax + size, size))

        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x,y), (x + size, y), (x + size, y + size), (x, y + size)]))

        grid = (gpd
            .GeoDataFrame({'geometry':polygons})
            .set_crs(capa.crs)
            .reset_index()
            .rename({'index':'grid_id'}, axis=1))
        malla = cls(grid, size)
        return malla
    
    @classmethod
    def desde_raster(cls,
                    raster: Union[str, Path] # El raster a partir del que vamos a crear la malla.
        ):
        mask = None
        with rasterio.Env():
            with rasterio.open(raster) as src:
                image = src.read(1).astype('float32') # Habría que probar esto con raster diferentes
                results = (
                    {'properties': {'grid_id': i}, 'geometry': s}
                    for i, (s, v) 
                    in enumerate(
                        shapes(image, mask=mask, transform=src.transform))
                )
        geoms = list(results)
        gdf = gpd.GeoDataFrame.from_features(geoms).set_crs(src.crs.to_string())
        print(gdf.crs)
        return cls(gdf, src.res[0])

    def to_crs(self, to_crs: Union[int, str, crs.CRS]):
        ...

    def agrega_lineas(self, lineas: gpd.GeoDataFrame, campo: str=None):
        ...
    
    def agrega_puntos(self, puntos: gpd.GeoDataFrame, campo: str=None, clasificacion: str=None):
        ...
    def agrega_manzanas(self, manzanas: gpd.GeoDataFrame, variables):
        ...

# %% ../nbs/api/01_coberturas.ipynb 18
@patch
def to_crs(self:Malla,
           to_crs: Union[int, str, crs.CRS] # El crs al que queremos reproyectar
    ) -> Malla:
    datos = self.datos.to_crs(to_crs)
    m = Malla(datos, self.size)
    return m

# %% ../nbs/api/01_coberturas.ipynb 21
@patch
def agrega_puntos(self:Malla,
                  puntos:gpd.GeoDataFrame, # La malla en la que se va a agregar
                  campo: str='cuenta', # Nombre del campo en el que se guarda el resultado
                  clasificacion: str=None, # Columna de `puntos` que clasifica a las observaciones (ignora `campo`) 
                  pesos:str=None # Columna con pesos para las unidades 
    ) -> Malla:
    """ Regresa una `Malla` con los conteos de puntos en cada elemento."""
    if self.crs != puntos.crs:
        puntos = puntos.to_crs(self.crs)
    if 'index_right' in puntos.columns:
        puntos = puntos.drop(columns='index_right')
    
    cols_agrupa = ['grid_id']
    if clasificacion is not None:
        cols_agrupa.append(clasificacion)
    
    if pesos is None:
        # Tenemos que seleccionar una columna calquiera pero que no sea clasificacion
        columnas = list(puntos.columns)
        columnas.remove(clasificacion) if clasificacion in columnas else None
        c = random.choice(columnas)
        agregador = {c: 'count'}
    else:
        c = pesos
        agregador = {pesos: 'sum'}

    agregado = (puntos
                .sjoin(self.datos)
                .groupby(cols_agrupa)
                .aggregate(agregador)
                .reset_index()
                )
    if clasificacion is not None:
        agregado = agregado.pivot(index='grid_id', columns=clasificacion, values=c)
    else:
        agregado = agregado.rename({c:campo}, axis=1)
    agregado = agregado.merge(self.datos, on='grid_id', how='right').fillna(0)
    agregado = gpd.GeoDataFrame(agregado).set_crs(self.crs)
    m = Malla(agregado, self.size)
    return m

# %% ../nbs/api/01_coberturas.ipynb 37
@patch
def agrega_lineas(self:Malla,
                  lineas:gpd.GeoDataFrame, # La capa de líneas a agregar
                  campo: str='longitud', # Nombre del campo en el que se guarda el resultado
                 ) -> Malla:
    """ Regresa una `Malla` con la longitud de las lineas agregadas en cada elemento."""
    if lineas.crs != self.crs:
        lineas = lineas.to_crs(self.crs) 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        union = (lineas
                .overlay(self.datos, how='union')
                .dissolve(by='grid_id')
                .length.reset_index()
                .rename({0:campo}, axis=1)   
            )
    union = (self.datos
            .merge(union, on='grid_id', how='left')
            .fillna(0)
        )
    m = Malla(union, self.size)
    return m

# %% ../nbs/api/01_coberturas.ipynb 48
@patch
def agrega_manzanas(self:Malla,
                    manzanas:gpd.GeoDataFrame, # Las manzanas (`descarga_manzanas_ejempolo`).
                    variables:dict, # Diccionario de las variables que querems agregar y el método para agregarlas (p, ej. {'OCUPVIVPAR':'sum'})
                    metodo: str='centro' # centro/area, método para resolver sobreposiciones
    ) -> Malla:
    pd.options.mode.chained_assignment = None
    if manzanas.crs != self.crs:
        manzanas = manzanas.to_crs(self.crs)
    # Primero asignamos el id de la malla a todos los contenidos
    manzanas = (manzanas
                 .sjoin(self.datos, predicate='covered_by', how='left')
                 .drop(columns='index_right'))
    # resolvemos los demás de acuerdo al método selecionado
    sin_asignar = manzanas.loc[manzanas['grid_id'].isna(),:]
    if metodo == 'centro':       
        sin_asignar['geometry'] = sin_asignar['geometry'].centroid
        # sin_asignar.loc[:, 'geometry'] = sin_asignar['geometry'].centroid
        sin_asignar = (sin_asignar
                      .drop(columns='grid_id')
                      .sjoin(self.datos)
                      .drop(columns='index_right'))
    elif metodo == 'area':
        sin_asignar = (sin_asignar
                      .drop(columns='grid_id')
                      .overlay(self.datos))
        sin_asignar['area'] = sin_asignar.geometry.area
        sin_asignar = (sin_asignar
                      .sort_values('area')
                      .drop_duplicates(sin_asignar.columns, keep='last')
                      .drop(columns='geometry'))
    else:
        print("metodo debe ser centro o area")
        raise NotImplementedError


    # Completamos los grid_id en los poligonos    
    manzanas = manzanas.merge(sin_asignar[['CVEGEO', 'grid_id']], on='CVEGEO', how='left')
    manzanas['grid_id'] = (manzanas['grid_id_y']
                            .fillna(manzanas['grid_id_x']))
    manzanas = manzanas.drop(columns=['grid_id_x', 'grid_id_y'])
    manzanas['grid_id'] = manzanas['grid_id'].astype(int)
    # Agrupamos y agregamos
    malla = (manzanas
             .drop(columns=['CVEGEO', 'geometry'])
             .groupby('grid_id')
             .aggregate(variables)
             .reset_index())
    malla = self.datos.merge(malla, on='grid_id', how='left').fillna(0)
    malla = Malla(malla, self.size)
    # return poligonos
    return malla


# %% ../nbs/api/01_coberturas.ipynb 56
@patch
def to_xarray(self:Malla,
              campos: list=None # Lista de campos a convertir, se convierten en bandas del raster
             ):
    """ Regresa un xarray con los `campos` seleccionados como variables."""
    if campos is None:
        campos = [c for c in self.datos.columns if c not in ['geometry', 'grid_id']]     
    cube = make_geocube(vector_data=self.datos, 
                        measurements=campos, 
                        resolution=(self.size, -self.size), 
                       )
    return cube

# %% ../nbs/api/01_coberturas.ipynb 62
class Poligonos(Cobertura):
    """ Representa una cobertura de polígonos de forma arbitraria 
        para procesar variables de uso de suelo."""
    def __init__ (self,
                 datos:gpd.GeoDataFrame=None, # La malla vectorial
                 id_col:str=None, # Columna que se va a usar para identificar a cada polígono
        ) -> None:
        self.id_col = id_col
        self.datos = datos
        self.crs = datos.crs
    
    @classmethod
    def desde_archivo(cls,
                      path:str, # Path al archivo de datos (cualquiera soportado por GeoPandas), 
                      id_col:str,  # Columna que se va a usar para identificar a cada polígono
                      layer=None
        ):
        gdf = gpd.read_file(path)
        return cls(gdf, id_col)
    def to_crs(self, to_crs: Union[int, str, crs.CRS]):
        ...
        
    def agrega_lineas(self, lineas: gpd.GeoDataFrame, campo: str=None):
        pass
    
    def agrega_puntos(self, puntos: gpd.GeoDataFrame, campo: str=None, clasificacion: str=None):
        pass

    def agrega_manzanas(self, manzanas: gpd.GeoDataFrame, variables):
        ...

# %% ../nbs/api/01_coberturas.ipynb 67
@patch
def to_crs(self:Poligonos,
           to_crs: Union[int, str, crs.CRS] # El crs al que queremos reproyectar
    ) -> Malla:
    datos = self.datos.to_crs(to_crs)
    m = Poligonos(datos, self.id_col)
    return m

# %% ../nbs/api/01_coberturas.ipynb 70
@patch
def agrega_puntos(self:Poligonos,
                  puntos:gpd.GeoDataFrame, # La malla en la que se va a agregar
                  campo: str='cuenta', # Nombre del campo en el que se guarda el resultado
                  clasificacion: str=None # Columna de `puntos` que clasifica a las observaciones. En este caso se agregan
                                          # tantas columnas a la malla como valores distintos haya en la columna
                                          # (en este caso se ignora `campo`)
                ) -> Poligonos:
    """ Regresa un `Poligonos` con los conteos de puntos en cada unidad."""
    if self.crs != puntos.crs:
        puntos = puntos.to_crs(self.crs)
    if 'index_right' in puntos.columns:
        puntos = puntos.drop(columns='index_right')
    if self.id_col in puntos.columns:
        puntos = puntos.drop(columns=self.id_col)
    if clasificacion is None:
        agregado = (puntos
                    .sjoin(self.datos)
                    .groupby(self.id_col)
                    .size()
                    .reset_index()
                    .rename({0:campo}, axis=1)
                    .merge(self.datos, on=self.id_col, how='right').fillna(0))

    else:
        agregado = (puntos
                    .sjoin(self.datos)
                    .groupby([clasificacion, self.id_col])
                    .size()
                    .reset_index()
                    .pivot(index=self.id_col, columns=clasificacion, values=0)                    
                    .merge(self.datos, on=self.id_col, how='right')
                    .fillna(0))
    agregado = (gpd.GeoDataFrame(agregado)
                .set_crs(self.crs))
    p = Poligonos(agregado, self.id_col)
    return p

# %% ../nbs/api/01_coberturas.ipynb 77
@patch
def agrega_lineas(self:Poligonos,
                  lineas:gpd.GeoDataFrame, # La capa de líneas a agregar
                  campo: str='longitud', # Nombre del campo en el que se guarda el resultado
                  proporcion:bool=True # ¿Debemos hacer el cálculo por unidad de área?
                 ) -> Malla:
    """ Regresa un `Poligonos` con la longitud de las lineas agregadas en cada elemento."""
    if lineas.crs != self.crs:
        lineas = lineas.to_crs(self.crs) 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        union = (lineas
                .overlay(self.datos, how='union')
                .dissolve(by=self.id_col)
                .length.reset_index()
                .rename({0:campo}, axis=1)   
            )
    union = (self.datos
            .merge(union, on=self.id_col, how='left')
            .fillna(0)
        )
    if proporcion:
        union['area'] = union.geometry.area
        union[campo] = union[campo].divide(union['area'])
        union = union.drop(columns='area')
    p = Poligonos(union, self.id_col)
    return p

# %% ../nbs/api/01_coberturas.ipynb 81
@patch
def agrega_manzanas(self:Poligonos, 
                    manzanas:gpd.GeoDataFrame, # Las manzanas (`descarga_manzanas_ejempolo`).
                    variables:dict # Diccionario de las variables que querems agregar y el método para agregarlas (p, ej. {'OCUPVIVPAR':'sum'})
    )-> Poligonos:
    if manzanas.crs != self.crs:
        manzanas = manzanas.to_crs(self.crs)
    relacion = manzanas[["CVEGEO", "geometry"]]
    relacion["geometry"] = manzanas.centroid
    relacion = relacion.sjoin(self.datos).drop(columns=['index_right', 'geometry'])
    manzanas = manzanas.merge(relacion, on="CVEGEO")
    poligonos = (manzanas
                 .groupby(self.id_col)
                 .aggregate(variables)
                 .reset_index())
    poligonos = self.datos.merge(poligonos, on=self.id_col, how='left').fillna(0)
    p = Poligonos(poligonos, self.id_col)
    return p
