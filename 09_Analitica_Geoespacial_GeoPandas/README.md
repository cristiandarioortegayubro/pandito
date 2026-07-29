# 🗺️ Módulo 09: Analítica Geoespacial con GeoPandas

## 🎯 Objetivo del Módulo

**Domina el análisis de datos espaciales** para decisiones basadas en ubicación: expansión de sucursales, optimización de rutas, análisis de mercados geográficos.

La **geolocalización** es una dimensión crítica de negocio ignorada por muchos analistas. Este módulo te convierte en experto en datos espaciales.

**Al finalizar este módulo podrás:**
* ✅ Trabajar con GeoDataFrames y geometrías (puntos, líneas, polígonos)
* ✅ Leer y escribir formatos geoespaciales (GeoJSON, Shapefile)
* ✅ Realizar operaciones espaciales (buffer, intersección, distancia)
* ✅ Hacer spatial joins (unir datos por proximidad)
* ✅ Visualizar mapas interactivos con Folium
* ✅ Analizar densidad de puntos y heatmaps geográficos

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 03-06 completados
* Conceptos básicos de geografía (latitud, longitud, coordenadas)

**Datasets:**
* `ubicaciones_sucursales.geojson`
* `ventas_retail.csv` (con coordenadas lat/lon)

**Librerías necesarias:**
```python
%pip install geopandas folium shapely
```

**Tiempo estimado:** 3.5 horas

---

## 📚 Contenido del Módulo

### 09_01_Introduccion_GeoPandas_y_Geometrias
**Duración:** 50 min | **Dificultad:** Principiante

**Temas:**
* GeoDataFrame vs DataFrame
* Tipos de geometrías: Point, LineString, Polygon, MultiPolygon
* Creación desde lat/lon: `gpd.points_from_xy()`
* Leer GeoJSON, Shapefile
* Sistemas de coordenadas (CRS): EPSG:4326 (WGS84), EPSG:3857 (Web Mercator)

**Casos de uso:**
* Cargar ubicaciones de sucursales
* Convertir direcciones a coordenadas
* Visualizar puntos en mapa

---

### 09_02_Operaciones_Espaciales
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* **Buffer:** área de influencia alrededor de punto
* **Distance:** distancia entre geometrías
* **Contains / Within:** si un punto está dentro de polígono
* **Intersects / Crosses:** si geometrías se tocan
* **Centroid:** centro geométrico de polígono
* **Area / Length:** área de polígono, longitud de línea

**Aplicaciones:**
* Identificar sucursales a menos de 5km de un punto
* Calcular área de cobertura de servicio
* Determinar si dirección está en zona de entrega

---

### 09_03_Spatial_Joins_y_Analisis_Proximidad
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* `gpd.sjoin()`: unir GeoDataFrames por ubicación
* Predicados: intersects, within, contains
* Nearest neighbor join (sucursal más cercana)
* Agregaciones espaciales (conteo de puntos por polígono)

**Casos de uso:**
* Asignar cada cliente a sucursal más cercana
* Contar transacciones por zona geográfica
* Identificar competidores en radio de 2km

---

### 09_04_Visualizacion_Mapas_Folium
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* Crear mapas interactivos con Folium
* Marcadores (Marker), popups personalizados
* Heatmaps con HeatMap plugin
* Circle markers con tamaño por métrica
* Choropleth maps (polígonos coloreados por valor)
* Exportar a HTML

**Aplicaciones:**
* Mapa de calor de densidad de clientes
* Mapa de sucursales con popup de KPIs
* Mapa de regiones coloreadas por revenue

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar tipos de geometrías en GeoPandas
* Identificar sistemas de coordenadas comunes
* Nombrar operaciones espaciales disponibles

### Nivel 2: Comprensión
* Explicar diferencia entre GeoDataFrame y DataFrame
* Describir qué hace un buffer de 500m
* Interpretar un spatial join con predicado 'within'

### Nivel 3: Aplicación
* Crear GeoDataFrame desde lat/lon
* Calcular distancia entre dos puntos
* Realizar spatial join para asignar clientes a sucursales
* Visualizar datos en mapa interactivo

### Nivel 4: Análisis
* Identificar ubicación óptima para nueva sucursal
* Analizar cobertura geográfica de servicio
* Evaluar canibalización entre sucursales cercanas

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Análisis de Cobertura Geográfica
```
"Tengo:
- GeoDataFrame 'sucursales' con Point geometries
- GeoDataFrame 'clientes' con Point geometries

Analiza:
1. Para cada sucursal, crear buffer de 5km
2. Contar clientes dentro de cada buffer
3. Identificar clientes no cubiertos (fuera de todos los buffers)
4. Calcular % de cobertura total
5. Visualizar en mapa: buffers + clientes cubiertos/no cubiertos con colores

Recomienda dónde abrir nueva sucursal para maximizar cobertura."
```

### Prompt 2: Heatmap de Densidad de Transacciones
```
"Crea mapa de calor de transacciones:
- Dataset: transacciones con lat, lon, monto
- Generar heatmap donde intensidad = sum(monto) por área
- Añadir marcadores en top 5 zonas con más revenue
- Popups con: zona, revenue total, # transacciones, ticket promedio

Identifica 3 zonas de alta densidad para estrategia de marketing local."
```

### Prompt 3: Análisis de Competencia Geográfica
```
"Tengo ubicaciones de:
- Nuestras sucursales
- Competidores

Genera:
1. Mapa con ambos sets de puntos (colores diferentes)
2. Para cada sucursal nuestra, identificar competidores a < 1km
3. Calcular 'índice de competencia' = # competidores / área de influencia
4. Choropleth map de zonas coloreadas por índice de competencia
5. Lista de sucursales en 'zona roja' (alta competencia)

Sugiere estrategias para las 3 sucursales más amenazadas."
```

---

## 🔧 Solución de Problemas

### Problema 1: KeyError 'geometry' al crear GeoDataFrame
**Causa:** Columna de geometrías no se llama 'geometry'  
**Solución:** Especifica columna explícitamente
```python
gdf = gpd.GeoDataFrame(df, geometry='mi_columna_geom')
# o renombra
df = df.rename(columns={'mi_columna_geom': 'geometry'})
```

### Problema 2: CRS warnings al hacer operaciones
**Causa:** GeoDataFrames con CRS diferentes  
**Solución:** Reproyecta a mismo CRS
```python
gdf1 = gdf1.to_crs("EPSG:4326")
gdf2 = gdf2.to_crs("EPSG:4326")
```

### Problema 3: Spatial join muy lento con muchos puntos
**Causa:** Complejidad O(n×m) sin índice espacial  
**Solución:** Usa spatial index o simplifica geometrías
```python
# Crear índice espacial automáticamente
gdf.sindex

# O pre-filtrar con bounding box
bbox = gdf1.total_bounds
gdf2_filtered = gdf2.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
```

---

## 📖 Recursos Adicionales

### Documentación
* [GeoPandas](https://geopandas.org/en/stable/)
* [Shapely](https://shapely.readthedocs.io/)
* [Folium](https://python-visualization.github.io/folium/)

### Datos Geoespaciales
* [Natural Earth Data](https://www.naturalearthdata.com/)
* [GADM (límites administrativos)](https://gadm.org/)
* [OpenStreetMap](https://www.openstreetmap.org/)

### Herramientas
* [QGIS](https://qgis.org/) - GIS desktop
* [Kepler.gl](https://kepler.gl/) - Visualización avanzada

---

## ✅ Checklist

**Fundamentos:**
- [ ] Crear GeoDataFrame desde lat/lon
- [ ] Leer GeoJSON, Shapefile
- [ ] Entender sistemas de coordenadas (CRS)
- [ ] Reproyectar entre CRS

**Operaciones Espaciales:**
- [ ] Buffer (área de influencia)
- [ ] Distance (distancia entre puntos)
- [ ] Contains / Within
- [ ] Intersects

**Spatial Joins:**
- [ ] sjoin() con predicados
- [ ] Nearest neighbor
- [ ] Agregaciones espaciales

**Visualización:**
- [ ] Mapas básicos con Folium
- [ ] Heatmaps
- [ ] Choropleth maps
- [ ] Markers con popups

---

## 🚀 Próximo Módulo

**➡️ [Módulo 10: Indexación Hexagonal con Uber H3](../10_Indexacion_Hexagonal_Uber_H3/)**

---

[📖 Volver al Índice](../README.md)
