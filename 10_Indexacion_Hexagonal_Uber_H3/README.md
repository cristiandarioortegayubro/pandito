# 🔷 Módulo 10: Indexación Hexagonal con Uber H3

## 🎯 Objetivo del Módulo

**Domina análisis geoespacial escalable** con Uber H3: indexación hexagonal para agregaciones eficientes, análisis de densidad y visualizaciones de big data geográfico.

H3 es la tecnología que usan **Uber, Lyft, Amazon** para análisis geográfico a escala. Este módulo te enseña técnicas de geoespacial de clase mundial.

**Al finalizar este módulo podrás:**
* ✅ Convertir coordenadas a celdas H3 hexagonales
* ✅ Agregar datos geográficos eficientemente por celda
* ✅ Analizar vecindad y distancia entre celdas
* ✅ Visualizar heatmaps hexagonales en Kepler.gl
* ✅ Escalar análisis geoespacial a millones de puntos
* ✅ Implementar casos de uso: zonas de entrega, pricing dinámico, cobertura

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 09 (GeoPandas) completado
* Familiaridad con lat/lon y coordenadas geográficas

**Datasets:**
* `ventas_retail.csv` (con lat/lon)
* `transacciones_financieras.parquet`

**Librerías:**
```python
%pip install h3 keplergl geopandas
```

**Tiempo estimado:** 3 horas

---

## 📚 Contenido del Módulo

### 10_01_Fundamentos_H3_Resolutions
**Duración:** 45 min | **Dificultad:** Principiante

**Temas:**
* ¿Qué es H3 y por qué hexágonos?
* Resolutions (0-15): de país (res 0) a edificio (res 15)
* `h3.geo_to_h3()`: convertir lat/lon a celda H3
* `h3.h3_to_geo()`: obtener centro de celda
* `h3.h3_to_geo_boundary()`: obtener polígono de celda

**Decisiones de resolution:**
* Res 5-6: ciudades, regiones metropolitanas
* Res 8-9: barrios, zonas de entrega
* Res 10-11: manzanas, coverage granular

---

### 10_02_Agregaciones_y_Hotspots
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* Agrupar datos por celda H3
* Agregaciones: count, sum, mean por celda
* Identificación de hotspots (celdas con alta actividad)
* Smoothing: promediar con celdas vecinas
* k-ring: celdas en radio k

**Casos de uso:**
* Identificar zonas de alta demanda
* Mapa de calor de transacciones
* Cobertura de servicio por celda

---

### 10_03_Analisis_Vecindad_y_Distancia
**Duración:** 45 min | **Dificultad:** Intermedio

**Temas:**
* `h3.k_ring()`: celdas vecinas a distancia k
* `h3.hex_ring()`: anillo de celdas a distancia exacta k
* `h3.h3_distance()`: distancia entre celdas
* Compact sets: comprimir conjuntos de celdas
* Polyfill: llenar polígono con celdas H3

**Aplicaciones:**
* Expandir zona de influencia (buffer hexagonal)
* Calcular cobertura de punto de servicio
* Optimizar asignación de zonas de reparto

---

### 10_04_Visualizacion_Kepler_gl
**Duración:** 40 min | **Dificultad:** Intermedio

**Temas:**
* Integrar H3 con Kepler.gl en Databricks
* Visualizar hexágonos coloreados por métrica
* Extrusión 3D (altura por valor)
* Filtros interactivos por tiempo/categoría
* Exportar configuración de mapa

**Resultado:** Dashboard geoespacial interactivo de clase mundial

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Explicar qué es indexación H3
* Listar resolutions H3 disponibles (0-15)
* Identificar ventajas de hexágonos vs cuadrados

### Nivel 2: Comprensión
* Describir cuándo usar resolution 8 vs 11
* Interpretar un heatmap hexagonal
* Explicar qué es un k-ring

### Nivel 3: Aplicación
* Convertir lat/lon a celdas H3
* Agregar transacciones por celda
* Identificar hotspots de demanda
* Visualizar en Kepler.gl

### Nivel 4: Análisis
* Seleccionar resolution óptima para caso de uso
* Comparar densidad entre zonas geográficas
* Diseñar sistema de zonas de entrega con H3

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Heatmap Hexagonal de Revenue
```
"Tengo DataFrame de transacciones con lat, lon, revenue.
Genera heatmap hexagonal:
1. Convierte cada transacción a celda H3 resolution 9
2. Agrega revenue total por celda
3. Identifica top 20 celdas con mayor revenue
4. Para cada top celda, obtén k-ring de 2 (celdas vecinas)
5. Calcula revenue promedio de vecindad
6. Visualiza en Kepler.gl con escala de color por revenue

Identifica 3 zonas para expansión de servicio."
```

### Prompt 2: Análisis de Cobertura de Sucursales
```
"Tengo GeoDataFrame de sucursales.
Para cada sucursal:
1. Genera buffer hexagonal de radio 3km usando H3
2. Marca todas las celdas H3 res 10 dentro del buffer
3. Identifica overlap de cobertura (celdas servidas por >1 sucursal)
4. Calcula % de celdas con cobertura 0, 1, 2, 3+ sucursales
5. Visualiza con colores: sin cobertura (rojo), 1 sucursal (amarillo), 2+ (verde)

Recomienda dónde abrir nueva sucursal para maximizar cobertura sin overlap."
```

### Prompt 3: Sistema de Pricing Dinámico por Zona
```
"Diseña sistema de pricing H3:
1. Divide ciudad en celdas H3 res 8
2. Para cada celda calcula:
   - Demanda promedio (# pedidos históricos)
   - Competencia (# competidores en k-ring 2)
   - Poder adquisitivo (ticket promedio)
3. Crea índice de precio = f(demanda, competencia, ticket)
4. Clasifica celdas en 5 tiers de precio
5. Visualiza mapa de pricing con Kepler

Genera tabla de recomendaciones: celda → tier → precio_sugerido."
```

---

## 🔧 Solución de Problemas

### Problema 1: h3.geo_to_h3() devuelve 0
**Causa:** Coordenadas inválidas (fuera de rango)  
**Solución:** Valida lat (-90 a 90), lon (-180 a 180)
```python
def safe_geo_to_h3(lat, lon, resolution):
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return h3.geo_to_h3(lat, lon, resolution)
    return None
```

### Problema 2: Kepler.gl map no se muestra
**Causa:** Formato de datos incorrecto  
**Solución:** Asegura GeoJSON válido
```python
# Convierte H3 cells a GeoJSON
from shapely.geometry import Polygon
import json

def h3_to_geojson(h3_cell):
    boundary = h3.h3_to_geo_boundary(h3_cell, geo_json=True)
    return Polygon(boundary)

gdf['geometry'] = gdf['h3_cell'].apply(h3_to_geojson)
```

### Problema 3: Agregaciones H3 muy lentas
**Causa:** No usar groupby eficiente  
**Solución:** Pre-convierte y usa pandas/spark
```python
# Convierte todas las coordenadas a H3 primero
df['h3_cell'] = df.apply(lambda row: h3.geo_to_h3(row['lat'], row['lon'], 9), axis=1)

# Luego agrupa (rápido)
agg = df.groupby('h3_cell').agg({'revenue': 'sum', 'qty': 'count'})
```

---

## 📖 Recursos Adicionales

### Documentación
* [H3 Documentation](https://h3geo.org/)
* [H3-py (Python bindings)](https://github.com/uber/h3-py)
* [Kepler.gl](https://kepler.gl/)

### Artículos
* [Why Hexagons?](https://eng.uber.com/h3/)
* [H3 Use Cases at Uber](https://www.uber.com/blog/h3/)

### Herramientas
* [H3 Resolution Table](https://h3geo.org/docs/core-library/restable/)
* [H3 Explorer](https://wolf-h3-viewer.glitch.me/)

---

## ✅ Checklist

**Fundamentos:**
- [ ] Entender por qué hexágonos > cuadrados
- [ ] Elegir resolution apropiada
- [ ] Convertir lat/lon a H3
- [ ] Obtener geometría de celda

**Agregaciones:**
- [ ] Agrupar datos por celda H3
- [ ] Identificar hotspots
- [ ] Smoothing con vecinos

**Vecindad:**
- [ ] k-ring para buffers
- [ ] Calcular distancia entre celdas
- [ ] Polyfill de polígonos

**Visualización:**
- [ ] Integrar con Kepler.gl
- [ ] Heatmap hexagonal
- [ ] Extrusión 3D
- [ ] Exportar mapa interactivo

**Casos de Uso:**
- [ ] Sistema de zonas de entrega
- [ ] Pricing dinámico por zona
- [ ] Análisis de cobertura

---

## 🚀 Próximo Módulo

**➡️ [Módulo 11: PySpark Fundamentos](../11_PySpark_Core_y_DataFrames/)**

¡Entramos al mundo de Big Data con PySpark!

---

[📖 Volver al Índice](../README.md)
