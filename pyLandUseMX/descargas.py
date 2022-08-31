# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_descargas.ipynb.

# %% auto 0
__all__ = ['descarga_denue_inegi']

# %% ../00_descargas.ipynb 3
import pandas as pd
import geopandas as gpd
import requests
import xml.etree.ElementTree as ET
import os
from zipfile import ZipFile
import shutil
from pathlib import Path

# %% ../00_descargas.ipynb 5
def descarga_denue_inegi():
    DOWNLOADS_PATH = "datos/descargas/denue/"
    Path(DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
    Path(DOWNLOADS_PATH + '/extracted').mkdir(parents=True, exist_ok=True)
    tree = ET.parse("datos/DescargaMasivaOD.xml")
    root = tree.getroot()
    datos = []
    for archivo in root.iter('Archivo'):
        s = archivo.text
        tipo = s.rsplit("/")[-1].split(".")[-2].split("_")[-1]
        if tipo == 'shp' and (s.rsplit("/")[-2].split("_")[0] not in ['denue', 'esenciales']):
            url = archivo.text
            year = archivo.text.rsplit("/")[-2].split("_")[0]
            fname = s.rsplit("/")[-1]
            if os.path.exists(DOWNLOADS_PATH + fname):
                pass
            else:
                r = requests.get(url, allow_redirects=True)
                open(DOWNLOADS_PATH + fname, 'wb').write(r.content)
            try:
                gdf = gpd.read_file(DOWNLOADS_PATH + fname)
            except:
                try:
                    zf = ZipFile(DOWNLOADS_PATH + fname)
                    for f in zf.namelist():
                        zinfo = zf.getinfo(f)
                        if (zinfo.is_dir()):
                            if f.split("/")[-2] == 'conjunto_de_datos':
                                shps = [n for n in zf.namelist() if (n.startswith(f) and not n.endswith('/'))]
                                for s in shps:
                                    basename = os.path.basename(s)
                                    source = zf.open(s)
                                    target = open(os.path.join('datos/descargas/denue/extracted/', basename), 'wb')
                                    with source, target:
                                        shutil.copyfileobj(source, target)
                    gdf = gpd.read_file(os.path.join('datos/descargas/denue/extracted/', basename.split(".")[0] + '.shp'))
                    [f.unlink() for f in Path('datos/descargas/denue/extracted/').glob("*") if f.is_file()] 
                except:
                    print(f'El archivo {fname} está corrupto')                
            campos = ['nom_estab', 'raz_social', 'codigo_act', 'nombre_act', 
                    'per_ocu', 'tipoCenCom', 'cve_ent', 'cve_mun', 'cve_loc', 
                    'ageb', 'manzana', 'geometry']
            gdf = gdf.loc[:,campos]
            gdf['cvegeo'] = gdf['cve_ent'] + gdf['cve_mun'] + gdf['cve_loc'] + gdf['ageb'] + gdf['manzana']
            gdf['year'] = year
            datos.append(gdf)
            
    denue_total = pd.concat(datos)
    return denue_total
