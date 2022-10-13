# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/00_descargas.ipynb.

# %% auto 0
__all__ = ['DOWNLOADS_PATH', 'descarga_denue', 'descarga_redes', 'descarga_poligonos_ciudades', 'descarga_colonias_cdmx',
           'descarga_manzanas_ejemplo', 'descarga_raster_ejemplo', 'descarga_datos_completos']

# %% ../nbs/api/00_descargas.ipynb 3
import pandas as pd
import geopandas as gpd
import requests
import xml.etree.ElementTree as ET
import os
from zipfile import ZipFile
import shutil
from pathlib import Path

DOWNLOADS_PATH = os.path.abspath("../../datos/descargas/")

# %% ../nbs/api/00_descargas.ipynb 5
def descarga_denue(
        tipo:str='zmvm_2022' # Qué archivo vamos a descargar: ejemplo, zmvm_2022, zmvm_full, mexico_2022, mexico_full
    ) -> None:
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    if tipo == 'zmvm_2022':
        fname = 'denue_2022_zmvm.gpkg'
        url = 'https://www.dropbox.com/s/cxyekc0wzzq6pc4/denue_2022_zmvm.gpkg?dl=1'
    elif tipo == 'ejemplo':
        fname = 'ejemplo_denue.gpkg'
        url = 'https://www.dropbox.com/s/670yx6un0t4sqal/ejemplo_denue.gpkg?dl=1'
    else:
        print(f'El tipo {tipo} todavía no está implementado')
        return
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(absp):
        print("El archivo ya está descargado")
    else:
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp
    


# %% ../nbs/api/00_descargas.ipynb 8
def descarga_redes():
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    fname = 'red_zmvm.gpkg'
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(absp):
        print("El archivo ya está descargado")
    else:
        url = 'https://www.dropbox.com/s/0fq8e8v2axyxxoc/red_zmvm.gpkg?dl=1'
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp

# %% ../nbs/api/00_descargas.ipynb 11
def descarga_poligonos_ciudades():
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    fname = 'silhuetas.shp.zip'
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(absp):
        print("El archivo ya está descargado")
    else:
        url = 'https://www.dropbox.com/s/kofmn5qws911ktg/silhueta_100_ciudades.zip?dl=1'
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp

# %% ../nbs/api/00_descargas.ipynb 14
def descarga_colonias_cdmx():
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    fname = 'colonias_cdmx.zip'
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(DOWNLOADS_PATH + fname):
        print("El archivo ya está descargado")
    else:
        url = 'https://www.dropbox.com/s/6dbyk1izvlub3xv/colonias_cdmx.zip?dl=1'
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp

# %% ../nbs/api/00_descargas.ipynb 17
def descarga_manzanas_ejemplo():
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    fname = 'manzanas_ejemplo.zip'
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(absp):
        print("El archivo ya está descargado")
    else:
        url = 'https://www.dropbox.com/s/kpn5z35a04ql4pp/manzanas_ejemplo.zip?dl=1'
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp

# %% ../nbs/api/00_descargas.ipynb 20
def descarga_raster_ejemplo():
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    fname = 'raster_ejemplo.tif'
    absp = os.path.abspath(os.path.join(DOWNLOADS_PATH, fname))
    if os.path.exists(absp):
        print("El archivo ya está descargado")
    else:
        url = 'https://www.dropbox.com/s/grsuex468iu62sn/raster_ejemplo.tif?dl=1'
        r = requests.get(url, allow_redirects=True)
        open(absp, 'wb').write(r.content)
    return absp

# %% ../nbs/api/00_descargas.ipynb 22
def descarga_datos_completos():
    descarga_poligonos_ciudades()
    descarga_redes()
