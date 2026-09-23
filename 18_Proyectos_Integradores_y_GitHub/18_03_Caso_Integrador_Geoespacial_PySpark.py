# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🗺️ Módulo 18 - Notebook 03: Caso Integrador - Geoespacial con PySpark
# MAGIC
# MAGIC ## 📍 Big Data Geoespacial: H3 + PySpark + Dashboards
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 18 - Proyectos Integradores y GitHub  
# MAGIC **Duración estimada:** 90 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos
# MAGIC
# MAGIC ✅ **Integrar** GeoPandas, H3, PySpark y SQL  
# MAGIC ✅ **Procesar** datos geoespaciales a escala  
# MAGIC ✅ **Crear** mapas de densidad de ventas  
# MAGIC ✅ **Optimizar** ubicaciones de sucursales  
# MAGIC ✅ **Publicar** dashboard geoespacial
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 10 (H3), 11-12 (PySpark), 16 (Dashboards)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. Carga de datos geoespaciales
# MAGIC 2. Indexación H3 con PySpark
# MAGIC 3. Análisis de densidad por hexágono
# MAGIC 4. Optimización de sucursales
# MAGIC 5. Dashboard geoespacial

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd

print("💾 CARGANDO DATOS GEOPSPACIALES")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Datos cargados: {len(df)} registros")
    if 'h3_index' in df.columns:
        print(f"   H3 indexes disponibles: {df['h3_index'].nunique()}")
    if 'lat' in df.columns and 'lon' in df.columns:
        print(f"   Lat: {df['lat'].min():.4f} a {df['lat'].max():.4f}")
        print(f"   Lon: {df['lon'].min():.4f} a {df['lon'].max():.4f}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Geoespacial
# MAGIC %md
# MAGIC ## 📚 Teoría: Big Data Geoespacial
# MAGIC
# MAGIC ### 🗺️ Análisis Geoespacial a Escala
# MAGIC
# MAGIC Combinar datos geoespaciales (lat/lon, H3) con PySpark permite procesar millones de puntos geográficos en paralelo.
# MAGIC
# MAGIC **Pipeline geoespacial:**
# MAGIC ```
# MAGIC Datos GPS (lat/lon)
# MAGIC     ↓
# MAGIC Indexación H3 (hexágonos)
# MAGIC     ↓
# MAGIC PySpark (procesamiento distribuido)
# MAGIC     ↓
# MAGIC Agregación por hexágono
# MAGIC     ↓
# MAGIC Dashboard geoespacial
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Casos de uso
# MAGIC * 🏪 Optimización de sucursales
# MAGIC * 📦 Rutas de distribución
# MAGIC * 👥 Densidad de clientes
# MAGIC * 🏆 Análisis territorial
# MAGIC * 📊 Cobertura de mercado

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("💻 PROYECTO: ANÁLISIS GEOPSPACIAL CON PySpark")
print("="*70)

if USAR_DATOS_REALES:
    # Análisis por zona
    if 'zona' in df.columns:
        print("\n1️⃣ VENTAS POR ZONA:")
        zona_stats = df.groupby('zona')['ventas'].agg(['count', 'sum', 'mean']).round(2)
        print(zona_stats)

    # Análisis por sucursal con ubicación
    print("\n2️⃣ UBICACIÓN DE SUCURSALES:")
    sucursal_loc = df.groupby('sucursal_id').agg({
        'lat': 'mean',
        'lon': 'mean',
        'ventas': 'sum'
    }).round(4)
    print(sucursal_loc)

    # Análisis temporal geoespacial
    print("\n3️⃣ EVOLUCIÓN DE VENTAS POR SUCURSAL:")
    df['anio'] = df['fecha'].dt.year
    pivot = df.pivot_table(values='ventas', index='sucursal_id', columns='anio', aggfunc='sum').round(2)
    print(pivot)

    # Identificar sucursal de mayor crecimiento
    if len(pivot.columns) >= 2:
        last_year = pivot.columns[-1]
        first_year = pivot.columns[0]
        pivot['crecimiento_pct'] = ((pivot[last_year] - pivot[first_year]) / pivot[first_year] * 100).round(2)
        print("\n4️⃣ CRECIMIENTO POR SUCURSAL:")
        print(pivot[[first_year, last_year, 'crecimiento_pct']].sort_values('crecimiento_pct', ascending=False))

    print(f"\n✅ Análisis geoespacial completado: {len(df)} registros")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🗺️ Teoría: Geoespacial ejecutivo
# MAGIC %md
# MAGIC ## 🗺️ Geoespacial ejecutivo de Los Andes Market
# MAGIC
# MAGIC ### 📍 H3 + PySpark para análisis territorial
# MAGIC
# MAGIC El dataset ya tiene `h3_index` y `lat/lon`. Podemos enriquecer el análisis con:
# MAGIC
# MAGIC ```python
# MAGIC # Agregar por hexágono H3
# MAGIC df.groupby('h3_index')['ventas'].sum()
# MAGIC
# MAGIC # Hot-spots: hexágonos con ventas > percentil 90
# MAGIC hot_spots = ventas_hex[ventas_hex > ventas_hex.quantile(0.9)]
# MAGIC
# MAGIC # Mapa interactivo con Plotly
# MAGIC px.scatter_mapbox(df, lat='lat', lon='lon', size='ventas', color='zona')
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué hexágonos concentran más ventas?
# MAGIC * ¿Hay hot-spots sin cobertura de sucursales?
# MAGIC * ¿Qué zonas tienen mayor potencial de expansión?

# COMMAND ----------

# DBTITLE 1,🗺️ Práctica: Geoespacial ejecutivo
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

print("🗺️ ANÁLISIS GEOPSPACIAL EJECUTIVO DE LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES:
    df['anio'] = df['fecha'].dt.year

    print("\n1️⃣  AGREGACIÓN POR HEXÁGONO H3")
    print("-"*70)

    if 'h3_index' in df.columns:
        hex_ventas = df.groupby('h3_index').agg(
            ventas=('ventas', 'sum'),
            promedio=('ventas', 'mean'),
            sucursales=('sucursal_id', 'nunique'),
            lat=('lat', 'mean'),
            lon=('lon', 'mean'),
            zona=('zona', 'first')
        ).round(0).reset_index()

        print(f"   Hexágonos únicos: {len(hex_ventas)}")
        print(f"   Ventas por hexágono (top 10):")
        print(hex_ventas.nlargest(10, 'ventas')[['h3_index', 'zona', 'ventas', 'sucursales']])

        print("\n" + "="*70)
        print("\n2️⃣  CLASIFICACIÓN DE HOT-SPOTS")
        print("-"*70)

        p75 = hex_ventas['ventas'].quantile(0.75)
        p90 = hex_ventas['ventas'].quantile(0.90)

        hex_ventas['categoria'] = 'Normal'
        hex_ventas.loc[hex_ventas['ventas'] >= p75, 'categoria'] = 'Alto'
        hex_ventas.loc[hex_ventas['ventas'] >= p90, 'categoria'] = 'Hot-Spot'

        print(f"   Normal: {(hex_ventas['categoria']=='Normal').sum()} hexágonos")
        print(f"   Alto: {(hex_ventas['categoria']=='Alto').sum()} hexágonos (>= P75)")
        print(f"   Hot-Spot: {(hex_ventas['categoria']=='Hot-Spot').sum()} hexágonos (>= P90)")
        print(f"   Umbral P75: ${p75:,.0f} | P90: ${p90:,.0f}")
    else:
        print("   ⚠️  No hay columna h3_index — usando lat/lon directo")
        hex_ventas = df.groupby(['lat', 'lon']).agg(
            ventas=('ventas', 'sum'),
            zona=('zona', 'first')
        ).reset_index()
        hex_ventas['categoria'] = 'Normal'
        p90 = hex_ventas['ventas'].quantile(0.90)
        hex_ventas.loc[hex_ventas['ventas'] >= p90, 'categoria'] = 'Hot-Spot'

    print("\n" + "="*70)
    print("\n3️⃣  MAPA INTERACTIVO DE SUCURSALES")
    print("-"*70)

    sucursal_map = df.groupby(['sucursal_id', 'sucursal_nombre', 'zona']).agg(
        lat=('lat', 'mean'),
        lon=('lon', 'mean'),
        ventas=('ventas', 'sum'),
        promedio=('ventas', 'mean')
    ).reset_index()

    fig_map = px.scatter_mapbox(
        sucursal_map, lat='lat', lon='lon',
        size='ventas', color='zona',
        hover_name='sucursal_nombre',
        hover_data={'ventas': ':,.0f', 'promedio': ':,.0f'},
        title='Sucursales Los Andes Market — Mendoza',
        mapbox_style='carto-positron',
        zoom=10, size_max=30
    )
    fig_map.show()

    print("\n" + "="*70)
    print("\n4️⃣  ANÁLISIS DE COBERTURA TERRITORIAL")
    print("-"*70)

    cobertura = df.groupby('zona').agg(
        sucursales=('sucursal_id', 'nunique'),
        ventas=('ventas', 'sum'),
        promedio=('ventas', 'mean'),
        superficie_hex=('h3_index', 'nunique') if 'h3_index' in df.columns else ('sucursal_id', 'count')
    ).round(0)
    cobertura['ventas_por_sucursal'] = (cobertura['ventas'] / cobertura['sucursales']).round(0)
    print("\n   Cobertura territorial por zona:")
    print(cobertura)

    print("\n" + "="*70)
    print("\n5️⃣  CRECIMIENTO GEOPSPACIAL INTERANUAL")
    print("-"*70)

    pivot_anual = df.pivot_table(values='ventas', index='sucursal_nombre', columns='anio', aggfunc='sum')
    if len(pivot_anual.columns) >= 2:
        first_yr = pivot_anual.columns[0]
        last_yr = pivot_anual.columns[-1]
        pivot_anual['crecimiento_pct'] = ((pivot_anual[last_yr] - pivot_anual[first_yr]) / pivot_anual[first_yr] * 100).round(1)
        pivot_anual = pivot_anual.sort_values('crecimiento_pct', ascending=False)
        print(f"\n   Crecimiento {first_yr} → {last_yr} por sucursal:")
        print(pivot_anual[[first_yr, last_yr, 'crecimiento_pct']])

    # Mapa de calor de crecimiento
    suc_growth = df.groupby(['sucursal_nombre', 'lat', 'lon']).apply(
        lambda x: ((x[x['fecha'].dt.year == x['fecha'].dt.year.max()]['ventas'].sum() -
                   x[x['fecha'].dt.year == x['fecha'].dt.year.min()]['ventas'].sum()) /
                  x[x['fecha'].dt.year == x['fecha'].dt.year.min()]['ventas'].sum() * 100) if len(x) > 0 else 0
    ).round(1).reset_index(name='crecimiento_pct')

    fig_growth = px.scatter_mapbox(
        suc_growth, lat='lat', lon='lon',
        color='crecimiento_pct', size='crecimiento',
        hover_name='sucursal_nombre',
        color_continuous_scale='RdYlGn',
        title='Crecimiento Interanual por Sucursal (%)',
        mapbox_style='carto-positron', zoom=10, size_max=25
    )
    fig_growth.show()
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 18_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Pipeline geoespacial end-to-end:**
# MAGIC    - Datos GPS (lat/lon) → Indexación H3 → PySpark → Agregación → Dashboard
# MAGIC    - Integración de GeoPandas, H3, PySpark y SQL en un solo flujo
# MAGIC    - Procesamiento distribuido de millones de puntos geográficos en paralelo
# MAGIC
# MAGIC 2. **Indexación H3 con PySpark:**
# MAGIC    - `h3.geo_to_h3(lat, lon, res)` aplicado con UDFs distribuidas en Spark
# MAGIC    - `spark.udf.register(...)` para usar H3 como función Spark
# MAGIC    - Agregación por hexágono: `df.groupBy('h3_index').agg(F.sum('ventas'))`
# MAGIC
# MAGIC 3. **Análisis de densidad por hexágono:**
# MAGIC    - Mapas de calor hexagonal: hexágonos rojos = alta densidad de ventas
# MAGIC    - Clasificación por percentiles: p75 = alto, p90 = hot-spot
# MAGIC    - Comparación de resoluciones (res 7, 8, 9) para diferentes escalas de análisis
# MAGIC
# MAGIC 4. **Optimización de sucursales:**
# MAGIC    - Cobertura: `h3.grid_disk(sucursal_hex, k=2)` para área de influencia
# MAGIC    - Canibalización: detectar solapamiento entre buffers de sucursales
# MAGIC    - Expansión: hot-spots sin cobertura = candidatos para nuevas sucursales
# MAGIC
# MAGIC 5. **Dashboard geoespacial:**
# MAGIC    - Plotly + GeoPandas para mapas interactivos
# MAGIC    - Heatmap de ventas por hexágono con filtros por año y zona
# MAGIC    - Marcadores por sucursal con ventas totales en hover
# MAGIC    - Publicado en AI/BI Dashboard para stakeholders
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Convertir a H3 antes de procesar en PySpark**
# MAGIC ```python
# MAGIC # MALO: operaciones geoespaciales con lat/lon raw en PySpark (lento, sin agregación)
# MAGIC df_spark = spark.createDataFrame(df)
# MAGIC df_spark.groupBy('lat', 'lon').agg(F.sum('ventas'))  # agregacion por punto, no util
# MAGIC
# MAGIC # BUENO: indexar H3 primero, luego agregar por hexagono
# MAGIC import h3
# MAGIC from pyspark.sql.functions import udf
# MAGIC from pyspark.sql.types import StringType
# MAGIC h3_udf = udf(lambda lat, lon: h3.geo_to_h3(lat, lon, 8), StringType())
# MAGIC df_spark = df_spark.withColumn('h3_index', h3_udf('lat', 'lon'))
# MAGIC df_spark.groupBy('h3_index').agg(F.sum('ventas').alias('ventas_hex'))
# MAGIC # Agregacion por area, no por punto individual
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Elegir resolución H3 según escala del análisis**
# MAGIC ```python
# MAGIC # MALO: res 11 (~0.002 km2) para analizar una ciudad entera
# MAGIC # Resultado: miles de hexagonos vacios o con 1 registro
# MAGIC
# MAGIC # BUENO: res 8 (~0.5 km2) para analisis urbano
# MAGIC df['h3_index'] = df.apply(lambda r: h3.geo_to_h3(r['lat'], r['lon'], 8), axis=1)
# MAGIC ventas_hex = df.groupby('h3_index')['ventas'].sum()
# MAGIC # ~50 hexagonos con datos significativos, visualizacion clara
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Validar cobertura antes de recomendar nueva sucursal**
# MAGIC ```python
# MAGIC # MALO: recomendar ubicacion solo por ventas altas del hexagono
# MAGIC hot_spots = hex_ventas.nlargest(5, 'ventas')
# MAGIC top = hot_spots.iloc[0]
# MAGIC lat, lon = h3.cell_to_latlng(top['h3_index'])
# MAGIC print(f'Nueva sucursal en ({lat}, {lon})')  # Sin verificar si ya hay cobertura
# MAGIC
# MAGIC # BUENO: cruzar hot-spots con areas sin cobertura
# MAGIC vecinos_existentes = set()
# MAGIC for h in sucursales['h3_index']:
# MAGIC     vecinos_existentes.update(h3.grid_disk(h, 2))
# MAGIC oportunidades = hot_spots[~hot_spots['h3_index'].isin(vecinos_existentes)]
# MAGIC top = oportunidades.sort_values('ventas', ascending=False).iloc[0]
# MAGIC lat, lon = h3.cell_to_latlng(top['h3_index'])
# MAGIC print(f'Nueva sucursal en ({lat}, {lon}) - zona sin cobertura')
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Indexar coordenadas a H3 | `h3.geo_to_h3(lat, lon, res)` con UDF en PySpark |
# MAGIC | Agregar ventas por hexágono | `df.groupBy('h3_index').agg(F.sum('ventas'))` |
# MAGIC | Mapa de densidad | Plotly + GeoPandas con escala de color |
# MAGIC | Clasificar hot-spots | Percentiles: p75 = alto, p90 = crítico |
# MAGIC | Cobertura de sucursal | `h3.grid_disk(sucursal_hex, k=2)` |
# MAGIC | Detectar canibalización | `h3.grid_distance(hex1, hex2) <= 3` |
# MAGIC | Recomendar nueva ubicación | Hot-spots sin cobertura existente |
# MAGIC | Cambiar de escala | `h3.h3_to_parent(hex, res_menor)` |
# MAGIC | Visualizar en mapa | `px.scatter_mapbox(df, lat, lon, size='ventas')` |
# MAGIC | Procesar millones de puntos | PySpark + UDF H3 (distribuido) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🗺️ ¡Big Data Geoespacial con PySpark dominado!</h3>
# MAGIC   <p><i>"H3 convierte coordenadas en decisiones: dónde abrir, dónde cerrar, dónde crecer — todo basado en datos espaciales a escala."</i></p>
# MAGIC </div>