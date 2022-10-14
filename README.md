pyLandUseMX
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

<div>

![CI](https://github.com/CentroGeo/pyLandUseMX/actions/workflows/test.yaml/badge.svg)

![Docs](https://github.com/CentroGeo/pyLandUseMX/actions/workflows/deploy.yaml/badge.svg)

</div>

El uso de suelo es un insumo básico para diferentes investigaciones en
el contexto urbano: criminología, movilidad y diseño urbano, por
ejemplo, son campos en los que contar con información sobre el uso real
del suelo resulta fundamental para realizar investigaciones
cuantitativas. Esta librería busca ofrecer diferentes opciones para
construir variables e índices para caracterizar el uso de suelo *real*,
es decir el uso observado, en el contexto de las ciudades mexicanas.

Además de mediciones sobre uso de suelo, la librería provee métodos para
extraer variables de estructura urbana como mezcla e intensidad de uso
de suelo. También implementa algunas herramientas básicas de análisis
para extraer patrones y relaciones en diferentes escalas.

La librería aprovecha diferentes fuentes de datos públicas como el DENUE
y el Censo para estimar variables de uso de suelo y su cambio en el
tiempo. Provee métodos para definir tipos de uso de suelo y agregarlo en
diferentes unidades espaciales: mallas regulares, hexágonos y polígonos
arbitrarios (como colonias o AGEBS).

## Instalación

Por lo pronto, la manera más fácil de instalar la librería es usando
`pip` para instalar desde el repositorio. Antes es necesario asegurarse
de que las dependencias del sistema están instaladas:

- `gdal`
- `rtree`
- `libgeos`
- `proj`

En sistemas basados en `apt`:

``` sh
sudo apt-get install -y gdal-bin python3-gdal python3-rtree libspatialindex-dev libgeos-dev libproj-dev
```

Ya con las dependencias instaladas:

``` sh
pip install git+https://github.com/CentroGeo/pyLandUseMX
```

## Uso

La librería contiene una serie de módulos para realizar diferentes
tareas para la extracción y proceso de variables de uso de suelo.

La organización general de los módulos es:

- descargas: herramientas para bajar bases preprocesadas sobre el medio
  urbano
- coberturas: herramientas para la integración de datos en doferentes
  soportes geográficos
- análisis: métodos analíticos

## Descargas

El módulo de `descargas`, provee funciones para edscargar de nuestros
repositorios algunas capas que contienen variables relevantes para la
extracción y análisis de uso de suelo en México. Cada función descarga
los datos en la carpeta `datos/descargas` del directorio de instalación.
Cada función regresa el *path* al archivo descargado.

#### Red de transporte

Por lo pronto tenemos disponible para descarga la red de transporte
obtenida de [OpenStreetMap](https://www.openstreetmap.org/) para la
región central del país (la Zona Metropolitana del Valle de México).
Para descargar estos datos simplemente llamamos a la función
correspondiente:

``` python
pth_redes = descarga_redes() # descarga la red
red = gpd.read_file(pth_redes) # leemos con geopandas
red = red.loc[red.tag_id.isin([104,108,106,101])] # seleccionamos vialidades primarias
red.plot()
```

    El archivo ya está descargado

    <AxesSubplot:>

![](index_files/figure-gfm/cell-2-output-3.png)

#### Polígonos del Sistema Urbano Nacional

También tenemos disponibles para descarga los polígonos de las ciudades
del [Sistema Urbano
Nacional](https://www.gob.mx/conapo/acciones-y-programas/sistema-urbano-nacional-y-zonas-metropolitanas)
(SUN) del 2018. Estos representan los límites de las principales
aglomeraciones urbanas del país.

``` python
pth_sun = descarga_poligonos_ciudades()
```

##### Colonias CDMX

Tenemos una base de colonias para la CDMX basadas en la que se publica
en [Datos Abiertos CDMX](https://datos.cdmx.gob.mx/) con algunas
correcciones topológicas.

``` python
pth_colonias = descarga_colonias_cdmx()
```

#### DENUE

Por lo pronto tenemos una base del DENUE integrada para el año 2022 en
la Ciudad de México. Eventualmete estaremos publicando una actualización
con datos históricos, desde el 2015, para las principales ciudades del
país.

``` python
pth_denue = descarga_denue()
```

## Coberturas

Regularmente para trabajos sobre análisis de uso de suelo y cobertura
urbana se parte de la integración de la información en algún soporte
espacial. El módulo `coberturas` provee métodos para estructurar las
fuentes de datos en dos grandes tipos de soporte:

- Mallas regulares
- Polígonos arbitrarios

Supongamos que tenemos una capa de puntos que representa la ocurrencia
de algún uso de suelo y las vialidades primarias. Podemos fácilmente
agregar las dos capas en una malla regular, obtener rasters y
visualizarlos

``` python
puntos = gpd.read_file("../datos/points_sample.zip") # Leemos los puntos
puntos = puntos.to_crs(32614)
malla = Malla.desde_capa(puntos, 1000) # Creamos una malla del tamaño de los puntos
malla = (malla
             .agrega_puntos(puntos, campo="puntos")
             .agrega_lineas(red, campo='metros_vialidad')
             )
malla.datos
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>grid_id</th>
      <th>puntos</th>
      <th>geometry</th>
      <th>metros_vialidad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0.0</td>
      <td>POLYGON ((404331.782 2029252.065, 405331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.0</td>
      <td>POLYGON ((404331.782 2030252.065, 405331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>0.0</td>
      <td>POLYGON ((404331.782 2031252.065, 405331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>0.0</td>
      <td>POLYGON ((404331.782 2032252.065, 405331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>0.0</td>
      <td>POLYGON ((404331.782 2033252.065, 405331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>50499</th>
      <td>50499</td>
      <td>0.0</td>
      <td>POLYGON ((639331.782 2238252.065, 640331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>50500</th>
      <td>50500</td>
      <td>1.0</td>
      <td>POLYGON ((639331.782 2239252.065, 640331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>50501</th>
      <td>50501</td>
      <td>0.0</td>
      <td>POLYGON ((639331.782 2240252.065, 640331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>50502</th>
      <td>50502</td>
      <td>0.0</td>
      <td>POLYGON ((639331.782 2241252.065, 640331.782 2...</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>50503</th>
      <td>50503</td>
      <td>0.0</td>
      <td>POLYGON ((639331.782 2242252.065, 640331.782 2...</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>50504 rows × 4 columns</p>
</div>

Podemos ver los rasters

``` python
cube = malla.to_xarray()
cube.metros_vialidad.plot()
```

    <matplotlib.collections.QuadMesh>

![](index_files/figure-gfm/cell-4-output-2.png)

``` python
cube = malla.to_xarray()
cube.puntos.plot()
```

    <matplotlib.collections.QuadMesh>

![](index_files/figure-gfm/cell-5-output-2.png)

## DENUE

Este módulo provee funcionalidades para trabajar con datos del
Directorio Nacional de Unidades Económicas y obtener algunas variables
de uso de suelo.

Permite seleccionar actividades económicas por clave SCIAN o agregar
estas actividades en categorías usando expresiones regulares.

Por ejemplo, supongamos que queremos tomar los puntos del DENUE y
generar una clasificación en tres grupos de usus de suelo: manufacturas,
oficinas y comercio. Entonces, a partir de una selección sobre las
claves SCIAN podemos hacer:

``` python
pth = descarga_denue(tipo='ejemplo')
denue = Denue.desde_archivo(pth)
categorias = {
    'Manufacturas': ['^31.*5$', '^32.*5$', '^33.*5$'],
    'Oficinas': ['^51', '^521', '^523', '^524', '^5312', '^5313', '^541', '^55'],
    'Comercio': ['^46[123456]']
}
usos = denue.agrega_en_usos(categorias)
usos.datos.loc[~usos.datos.Categoria.isnull()].head()
```

    El archivo ya está descargado

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nom_estab</th>
      <th>raz_social</th>
      <th>codigo_act</th>
      <th>nombre_act</th>
      <th>per_ocu</th>
      <th>tipoCenCom</th>
      <th>cve_ent</th>
      <th>cve_mun</th>
      <th>cve_loc</th>
      <th>ageb</th>
      <th>...</th>
      <th>index_right</th>
      <th>OBJECTID</th>
      <th>Shape_Leng</th>
      <th>NOM_CIUDAD</th>
      <th>Shape_Le_1</th>
      <th>Shape_Area</th>
      <th>CVE_SUN</th>
      <th>SUN</th>
      <th>geometry</th>
      <th>Categoria</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>TIENDA NATURISTA EL ARTE DE LA NATURALEZA</td>
      <td>None</td>
      <td>464113</td>
      <td>Comercio al por menor de productos naturistas,...</td>
      <td>0 a 5 personas</td>
      <td>None</td>
      <td>09</td>
      <td>007</td>
      <td>0001</td>
      <td>1814</td>
      <td>...</td>
      <td>53</td>
      <td>54</td>
      <td>630172.981156</td>
      <td>Valle de México</td>
      <td>630.172981</td>
      <td>781912.110166</td>
      <td>13</td>
      <td>13.0</td>
      <td>POINT (-99.06312 19.33782)</td>
      <td>Comercio</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SIN NOMBRE</td>
      <td>None</td>
      <td>461130</td>
      <td>Comercio al por menor de frutas y verduras fre...</td>
      <td>0 a 5 personas</td>
      <td>None</td>
      <td>09</td>
      <td>008</td>
      <td>0001</td>
      <td>0423</td>
      <td>...</td>
      <td>53</td>
      <td>54</td>
      <td>630172.981156</td>
      <td>Valle de México</td>
      <td>630.172981</td>
      <td>781912.110166</td>
      <td>13</td>
      <td>13.0</td>
      <td>POINT (-99.25436 19.30129)</td>
      <td>Comercio</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ADMINISTRACION MERCADO CONCENTRACION VOCEADORES</td>
      <td>GOBIERNO DE LA CIUDAD DE MEXICO</td>
      <td>531311</td>
      <td>Servicios de administración de bienes raíces</td>
      <td>0 a 5 personas</td>
      <td>MERCADO PUBLICO</td>
      <td>09</td>
      <td>007</td>
      <td>0001</td>
      <td>2371</td>
      <td>...</td>
      <td>53</td>
      <td>54</td>
      <td>630172.981156</td>
      <td>Valle de México</td>
      <td>630.172981</td>
      <td>781912.110166</td>
      <td>13</td>
      <td>13.0</td>
      <td>POINT (-99.03318 19.38744)</td>
      <td>Oficinas</td>
    </tr>
    <tr>
      <th>6</th>
      <td>ABARROTES LA TIA</td>
      <td>None</td>
      <td>461110</td>
      <td>Comercio al por menor en tiendas de abarrotes,...</td>
      <td>0 a 5 personas</td>
      <td>None</td>
      <td>15</td>
      <td>121</td>
      <td>0001</td>
      <td>1763</td>
      <td>...</td>
      <td>53</td>
      <td>54</td>
      <td>630172.981156</td>
      <td>Valle de México</td>
      <td>630.172981</td>
      <td>781912.110166</td>
      <td>13</td>
      <td>13.0</td>
      <td>POINT (-99.19269 19.58976)</td>
      <td>Comercio</td>
    </tr>
    <tr>
      <th>7</th>
      <td>BIZUTERIA SIN NOMBRE</td>
      <td>None</td>
      <td>463215</td>
      <td>Comercio al por menor de bisutería y accesorio...</td>
      <td>0 a 5 personas</td>
      <td>None</td>
      <td>15</td>
      <td>122</td>
      <td>0001</td>
      <td>0847</td>
      <td>...</td>
      <td>53</td>
      <td>54</td>
      <td>630172.981156</td>
      <td>Valle de México</td>
      <td>630.172981</td>
      <td>781912.110166</td>
      <td>13</td>
      <td>13.0</td>
      <td>POINT (-98.94058 19.31219)</td>
      <td>Comercio</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>
