# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 13 - Notebook 01: Caching, persist y memory management
# MAGIC
# MAGIC ## 🧠 Optimización de memoria en Spark
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 13 - Performance Spark y Optimización  
# MAGIC **Duración estimada:** 50 minutos  
# MAGIC **Dificultad:** 🟠 Intermedio-Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC Al finalizar este notebook serás capaz de:
# MAGIC
# MAGIC ✅ **Entender** la diferencia entre cache y persist  
# MAGIC ✅ **Aplicar** StorageLevel según el caso de uso  
# MAGIC ✅ **Identificar** cuándo cachear un DataFrame  
# MAGIC ✅ **Liberar** memoria con unpersist  
# MAGIC ✅ **Diagnosticar** problemas de memoria en Spark
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Módulos 11 y 12 completados (PySpark Core y Transformación)
# MAGIC * ✅ Entender lazy evaluation y transformaciones vs acciones
# MAGIC * ✅ Conocimiento básico de particiones y executors
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. Lazy Evaluation y recálculo innecesario
# MAGIC 2. cache() vs persist() vs StorageLevel
# MAGIC 3. Cuándo cachear (y cuándo NO)
# MAGIC 4. unpersist() y gestión de memoria
# MAGIC 5. Diagnóstico con Spark UI
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 💡 Por qué importa
# MAGIC
# MAGIC **Sin caching:** cada acción recalcula TODO el DAG desde el origen  
# MAGIC **Con caching:** el resultado se guarda en memoria, las siguientes acciones son instantáneas  
# MAGIC
# MAGIC **Impacto real:** 10-100x más rápido en pipelines con múltiples acciones sobre el mismo DataFrame.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⚠️ Regla de Oro
# MAGIC
# MAGIC > **"Cachea solo si usas el DataFrame más de una vez"**
# MAGIC > 
# MAGIC > Cachear cuesta memoria. Si solo haces una acción, el cache es desperdicio.
# MAGIC > 
# MAGIC > * Cachea → usa → unpersist()
# MAGIC > * No cachear DataFrames que solo se leen una vez

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
from pyspark.sql.functions import col, sum as _sum, avg, count, year, month
import time

print("💾 CARGANDO DATOS DESDE UNITY CATALOG")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Datos cargados: {df.count():,} registros")
    print(f"   Columnas: {len(df.columns)}")
    df.printSchema()
except Exception as e:
    print(f"⚠️  Tabla no encontrada: {e}")
    print("   Ejecuta primero: 00_05_Preparacion_Datos_Empresariales.ipynb")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Caching y Memory Management
# MAGIC %md
# MAGIC ## 📚 Teoría: Caching y Memory Management
# MAGIC
# MAGIC ### 🔄 El problema del recálculo
# MAGIC
# MAGIC Spark es **lazy**: las transformaciones no ejecutan hasta que hay una acción. Pero cada acción recalcula TODO el DAG desde el origen.
# MAGIC
# MAGIC ```
# MAGIC Sin cache:
# MAGIC df.filter(...).groupBy(...).count()  → Ejecuta TODO
# MAGIC df.filter(...).groupBy(...).show()   → Ejecuta TODO OTRA VEZ
# MAGIC df.filter(...).groupBy(...).write()  → Ejecuta TODO OTRA VEZ
# MAGIC
# MAGIC Con cache:
# MAGIC df_cached = df.filter(...).groupBy(...).cache()
# MAGIC df_cached.count()  → Ejecuta y cachea
# MAGIC df_cached.show()   → USA CACHE (instantáneo)
# MAGIC df_cached.write()  → USA CACHE (instantáneo)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧠 cache() vs persist()
# MAGIC
# MAGIC | Método | StorageLevel | Descripción |
# MAGIC |--------|-------------|-------------|
# MAGIC | `cache()` | MEMORY_AND_DISK | En memoria, spill a disco si falta RAM |
# MAGIC | `persist(MEMORY_ONLY)` | MEMORY_ONLY | Solo memoria, no spill (puede fallar) |
# MAGIC | `persist(MEMORY_AND_DISK)` | MEMORY_AND_DISK | Memoria + disco (default de cache) |
# MAGIC | `persist(DISK_ONLY)` | DISK_ONLY | Solo disco, libera toda la RAM |
# MAGIC | `persist(MEMORY_ONLY_SER)` | MEMORY_ONLY_SER | Serializado, usa menos RAM |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 StorageLevel explicado
# MAGIC
# MAGIC * **MEMORY_ONLY:** Más rápido, pero si no cabe en RAM → error o recálculo
# MAGIC * **MEMORY_AND_DISK:** Balance ideal, spill a disco si falta RAM (default)
# MAGIC * **DISK_ONLY:** Para DataFrames grandes que no caben en RAM
# MAGIC * **MEMORY_ONLY_SER:** Serializado, ~3x menos RAM pero ~20% más lento
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Cuándo NO cachear
# MAGIC
# MAGIC * DataFrame que solo se usa **una vez** → desperdicio de memoria
# MAGIC * DataFrame que se filtra y se descarta → cachear después del filtro
# MAGIC * Tabla muy grande que no cabe en memoria → usar DISK_ONLY o no cachear

# COMMAND ----------

# DBTITLE 1,🧪 Experimento: Cache vs Sin Cache
from pyspark import StorageLevel

print("🧪 EXPERIMENTO: CON CACHE vs SIN CACHE")
print("="*70)

# --- SIN CACHE: 3 acciones = 3 cálculos completos ---
print("\n1️⃣  SIN CACHE (3 acciones, 3 cálculos)")
start = time.time()
df_filtrado = df.filter(col("ventas") > 100000)
df_filtrado.count()                          # Cálculo 1
df_filtrado.agg(_sum("ventas")).collect()    # Cálculo 2
df_filtrado.groupBy("sucursal_id").count().collect()  # Cálculo 3
tiempo_sin_cache = time.time() - start
print(f"   Tiempo: {tiempo_sin_cache:.2f}s")

# --- CON CACHE: 3 acciones = 1 cálculo + 2 desde cache ---
print("\n2️⃣  CON CACHE (3 acciones, 1 cálculo + 2 cache)")
start = time.time()
df_cached = df.filter(col("ventas") > 100000).cache()
df_cached.count()                          # Cálculo + cachea
df_cached.agg(_sum("ventas")).collect()    # USA CACHE
df_cached.groupBy("sucursal_id").count().collect()  # USA CACHE
tiempo_con_cache = time.time() - start
print(f"   Tiempo: {tiempo_con_cache:.2f}s")

# --- LIBERAR MEMORIA ---
df_cached.unpersist()
print("\n✅ Cache liberado con unpersist()")

# --- COMPARACIÓN ---
print(f"\n📊 COMPARACIÓN:")
print(f"   Sin cache: {tiempo_sin_cache:.2f}s")
print(f"   Con cache: {tiempo_con_cache:.2f}s")
if tiempo_sin_cache > 0:
    speedup = tiempo_sin_cache / tiempo_con_cache if tiempo_con_cache > 0 else 0
    print(f"   Speedup: {speedup:.1f}x")

print("\n" + "="*70)

# --- DIFERENTES STORAGE LEVELS ---
print("\n3️⃣  DIFERENTES STORAGE LEVELS")
print("-"*70)

# MEMORY_AND_DISK (default de cache)
df_mad = df.filter(col("ventas") > 100000).persist(StorageLevel.MEMORY_AND_DISK)
df_mad.count()
print("✅ MEMORY_AND_DISK: balance ideal (memoria + disco si falta)")
df_mad.unpersist()

# MEMORY_ONLY (más rápido pero puede fallar)
# df_mo = df.filter(col("ventas") > 100000).persist(StorageLevel.MEMORY_ONLY)
# df_mo.count()
# print("✅ MEMORY_ONLY: máximo速度, sin spill a disco")
# df_mo.unpersist()

print("\n💡 MEMORY_ONLY_SER: serializado, 3x menos RAM pero 20% más lento")
print("💡 DISK_ONLY: para DataFrames que no caben en RAM")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🧠 Teoría: Caching aplicado a Los Andes Market
# MAGIC %md
# MAGIC ## 🧠 Caching aplicado a Los Andes Market
# MAGIC
# MAGIC ### 📊 ¿Dónde cachear en un pipeline real de ventas?
# MAGIC
# MAGIC Un análisis típico de **Los Andes Market** involucra múltiples pasos sobre el mismo DataFrame filtrado:
# MAGIC
# MAGIC ```python
# MAGIC # Pipeline sin cache (recalcula 3 veces)
# MAGIC df_filtrado = df.filter(col("ventas") > 100000)
# MAGIC df_filtrado.count()                              # Cálculo 1
# MAGIC df_filtrado.groupBy("zona").sum("ventas").show()  # Cálculo 2
# MAGIC df_filtrado.groupBy("sucursal_id").avg("ventas").show() # Cálculo 3
# MAGIC
# MAGIC # Pipeline con cache (calcula 1 vez, reusa 2)
# MAGIC df_cached = df.filter(col("ventas") > 100000).cache()
# MAGIC df_cached.count()   # Cálculo + cachea
# MAGIC df_cached.groupBy("zona").sum("ventas").show()     # Cache
# MAGIC df_cached.groupBy("sucursal_id").avg("ventas").show() # Cache
# MAGIC df_cached.unpersist()  # Liberar al terminar
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💼 Casos de negocio donde caching es clave
# MAGIC
# MAGIC 1. **Dashboard ejecutivo:** Múltiples KPIs sobre el mismo filtro → cachear el filtro
# MAGIC 2. **Reporte mensual:** Ventas por zona, por sucursal, por año → cachear el DataFrame del mes
# MAGIC 3. **Análisis comparativo:** Comparar ventas de N sucursales → cachear el agregado
# MAGIC 4. **Iteración de modelo:** Feature engineering repetido → cachear features
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ En Los Andes Market: ¿Qué cachear?
# MAGIC
# MAGIC | DataFrame | ¿Cachear? | Por qué |
# MAGIC |-----------|-----------|--------|
# MAGIC | `df.filter(ventas > 100k)` usado 3+ veces | ✅ Sí | Recálculo costoso |
# MAGIC | `df.groupBy('zona').sum('ventas')` usado 1 vez | ❌ No | Una sola acción |
# MAGIC | `df_sucursales` (20 filas) en joins repetidos | ✅ Sí | Tabla pequeña, reusada |
# MAGIC | `df` completo (miles de filas) | ⚠️ Tal vez | Solo si se usa múltiples veces |

# COMMAND ----------

# DBTITLE 1,🧠 Práctica: Caching aplicado a Los Andes Market
from pyspark.sql.functions import col, sum as _sum, avg, count, year, month, desc
import time

print("🧠 CACHING APLICADO A LOS ANDES MARKET")
print("="*70)

if 'df' in dir() and df is not None:
    print("\n1️⃣  PIPELINE SIN CACHE: Dashboard ejecutivo (3 KPIs)")
    print("-"*70)

    # Simular un dashboard con 3 KPIs sobre el mismo filtro
    df_filtrado = df.filter(col("ventas") > 100000)

    start = time.time()
    kpi1 = df_filtrado.count()  # KPI 1: total registros
    kpi2 = df_filtrado.groupBy("zona").agg(_sum("ventas").alias("total")).orderBy(desc("total")).collect()  # KPI 2
    kpi3 = df_filtrado.groupBy("sucursal_id").agg(avg("ventas").alias("promedio")).orderBy(desc("promedio")).collect()  # KPI 3
    t_sin = time.time() - start

    print(f"\n   KPI 1 - Registros con ventas > 100k: {kpi1:,}")
    print(f"   KPI 2 - Ventas por zona (top 3):")
    for row in kpi2[:3]:
        print(f"      {row['zona']}: ${row['total']:,.0f}")
    print(f"   KPI 3 - Sucursal con mayor promedio: {kpi3[0]['sucursal_id']} (${kpi3[0]['promedio']:,.0f})")
    print(f"   ⏱️  Tiempo sin cache (3 cálculos): {t_sin:.2f}s")

    print("\n" + "="*70)
    print("\n2️⃣  PIPELINE CON CACHE: Mismos 3 KPIs")
    print("-"*70)

    df_cached = df.filter(col("ventas") > 100000).cache()

    start = time.time()
    kpi1c = df_cached.count()  # Cálculo + cachea
    kpi2c = df_cached.groupBy("zona").agg(_sum("ventas").alias("total")).orderBy(desc("total")).collect()  # Cache
    kpi3c = df_cached.groupBy("sucursal_id").agg(avg("ventas").alias("promedio")).orderBy(desc("promedio")).collect()  # Cache
    t_con = time.time() - start

    print(f"\n   KPI 1 - Registros con ventas > 100k: {kpi1c:,}")
    print(f"   KPI 2 - Ventas por zona (top 3):")
    for row in kpi2c[:3]:
        print(f"      {row['zona']}: ${row['total']:,.0f}")
    print(f"   KPI 3 - Sucursal con mayor promedio: {kpi3c[0]['sucursal_id']} (${kpi3c[0]['promedio']:,.0f})")
    print(f"   ⏱️  Tiempo con cache (1 cálculo + 2 cache): {t_con:.2f}s")

    speedup = t_sin / t_con if t_con > 0 else 0
    print(f"\n   📊 Speedup: {speedup:.1f}x")
    print(f"   💡 Mismos resultados, menos tiempo gracias al cache")

    df_cached.unpersist()
    print("   ✅ Cache liberado con unpersist()")

    print("\n" + "="*70)
    print("\n3️⃣  CASO REAL: Cachear sucursales para joins repetidos")
    print("-"*70)

    # Tabla pequeña de sucursales (candidata a cache por uso repetido)
    df_suc = df.select("sucursal_id", "sucursal_nombre", "zona", "lat", "lon").dropDuplicates().cache()
    df_suc.count()  # Materializar cache

    # 3 joins diferentes usando la misma tabla de sucursales
    print("\n   3 joins reutilizando sucursales cacheadas:")

    join1 = df.filter(col("ventas") > 150000).join(df_suc, "sucursal_id", "inner")
    print(f"      Join 1 (ventas > 150k): {join1.count()} registros")

    join2 = df.filter(year(col("fecha")) == 2023).join(df_suc, "sucursal_id", "inner")
    print(f"      Join 2 (año 2023): {join2.count()} registros")

    join3 = df.filter(col("zona") == "Corredor Comercial").join(df_suc, "sucursal_id", "inner")
    print(f"      Join 3 (Corredor Comercial): {join3.count()} registros")

    print("\n   💡 Sin cache, cada join releería la tabla de sucursales")
    print("   💡 Con cache, la tabla está en memoria para los 3 joins")

    df_suc.unpersist()
    print("   ✅ Cache de sucursales liberado")
else:
    print("⚠️  No hay datos disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 13_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **El problema del recálculo:**
# MAGIC    - Sin cache, cada acción recalcula todo el DAG desde el origen
# MAGIC    - 3 acciones sobre el mismo DataFrame = 3 cálculos completos
# MAGIC    - Con cache: 1 cálculo + 2 lecturas desde memoria (instantáneo)
# MAGIC
# MAGIC 2. **cache() vs persist():**
# MAGIC    - `cache()` = `persist(MEMORY_AND_DISK)` (default, balance ideal)
# MAGIC    - `persist(StorageLevel.X)` permite elegir el nivel de almacenamiento
# MAGIC    - MEMORY_ONLY: más rápido pero sin spill (puede fallar si no cabe)
# MAGIC    - DISK_ONLY: para DataFrames que no caben en RAM
# MAGIC
# MAGIC 3. **StorageLevel y trade-offs:**
# MAGIC    - MEMORY_AND_DISK: balance ideal, spill a disco si falta RAM
# MAGIC    - MEMORY_ONLY_SER: serializado, ~3x menos RAM, ~20% más lento
# MAGIC    - DISK_ONLY: libera RAM pero más lento en lectura
# MAGIC    - Elegir según tamaño del DataFrame y memoria disponible
# MAGIC
# MAGIC 4. **Cuándo cachear (y cuándo NO):**
# MAGIC    - ✅ Cachear: DataFrame usado en 2+ acciones
# MAGIC    - ✅ Cachear: después de filtrar (reduce tamaño antes de cachear)
# MAGIC    - ❌ NO cachear: DataFrame usado una sola vez
# MAGIC    - ❌ NO cachear: DataFrame enorme que no cabe en memoria
# MAGIC
# MAGIC 5. **Gestión de memoria con unpersist():**
# MAGIC    - `df.unpersist()` libera la memoria inmediatamente
# MAGIC    - Siempre llamar unpersist al terminar de usar el cache
# MAGIC    - Evita memory leaks en pipelines largos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Cachea solo si usas el DataFrame más de una vez**
# MAGIC ```python
# MAGIC # MALO: cachear y usar una sola vez
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()  # única acción
# MAGIC df_cached.unpersist()  # desperdicio: cachear para 1 acción
# MAGIC
# MAGIC # BUENO: cachear cuando hay múltiples acciones
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()                          # cálculo + cachea
# MAGIC df_cached.agg(_sum("ventas")).collect()     # usa cache
# MAGIC df_cached.groupBy("sucursal").count().show() # usa cache
# MAGIC df_cached.unpersist()  # libera al terminar
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Filtrar ANTES de cachear**
# MAGIC ```python
# MAGIC # MALO: cachear todo el DataFrame original (demasiada memoria)
# MAGIC df_cached = df.cache()  # 300 registros, muchos innecesarios
# MAGIC df_cached.filter(col("ventas") > 1000).count()
# MAGIC
# MAGIC # BUENO: filtrar primero, cachear el resultado más pequeño
# MAGIC df_filtrado = df.filter(col("ventas") > 1000).cache()  # solo los relevantes
# MAGIC df_filtrado.count()
# MAGIC df_filtrado.agg(_sum("ventas")).show()
# MAGIC df_filtrado.unpersist()
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Siempre unpersist() al terminar**
# MAGIC ```python
# MAGIC # MALO: cachear y nunca liberar (memory leak)
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()
# MAGIC # ... código que olvida liberar → memoria ocupada innecesariamente
# MAGIC
# MAGIC # BUENO: patrón cache → usar → liberar
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()
# MAGIC df_cached.show()
# MAGIC df_cached.unpersist()  # libera memoria inmediatamente
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | DataFrame usado 2+ veces | `df.cache()` + `df.unpersist()` al final |
# MAGIC | DataFrame usado 1 vez | No cachear (desperdicio) |
# MAGIC | DataFrame pequeño (< 1 GB) | `persist(MEMORY_ONLY)` |
# MAGIC | DataFrame mediano (1-10 GB) | `cache()` (MEMORY_AND_DISK) |
# MAGIC | DataFrame grande (> 10 GB) | `persist(DISK_ONLY)` |
# MAGIC | Ahorrar RAM prioritario | `persist(MEMORY_ONLY_SER)` |
# MAGIC | Liberar memoria | `df.unpersist()` |
# MAGIC | Ver qué está cacheado | Spark UI > Storage tab |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🧠 ¡Caching y memory management dominados!</h3>
# MAGIC   <p><i>"Cachear bien es 10x más rápido. Cachear mal es 10x más lento por memory pressure."</i></p>
# MAGIC </div>