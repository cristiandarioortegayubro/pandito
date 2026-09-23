# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 15 - Notebook 04: Optimización catalyst y partitioning
# MAGIC
# MAGIC ## 🚀 Rendimiento de queries en Spark
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 15 - Delta Lake, Window Functions y Optimización  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos
# MAGIC
# MAGIC ✅ **Entender** el Optimizador Catalyst  
# MAGIC ✅ **Leer** planes de ejecución (EXPLAIN)  
# MAGIC ✅ **Aplicar** particionado de tablas  
# MAGIC ✅ **Usar** caching y persistencia  
# MAGIC ✅ **Identificar** Data Skew  
# MAGIC ✅ **Optimizar** joins con broadcast
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Notebooks 15_01 al 15_03 completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Catalyst Optimizer** - Cómo Spark optimiza queries
# MAGIC 2. **EXPLAIN** - Leer planes de ejecución
# MAGIC 3. **Partitioning** - Particionar tablas por columna
# MAGIC 4. **Caching** - Persistencia de DataFrames
# MAGIC 5. **Data Skew** - Detección y mitigación
# MAGIC 6. **Broadcast Joins** - Optimización de joins

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
from pyspark.sql.functions import col, broadcast

print("💾 SETUP PARA OPTIMIZACIÓN")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Tabla cargada: {df.count()} registros")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Optimización Catalyst
# MAGIC %md
# MAGIC ## 📚 Teoría: Optimización en Spark
# MAGIC
# MAGIC ### ⚙️ Catalyst Optimizer
# MAGIC
# MAGIC **Catalyst** es el motor de optimización de Spark que transforma tu código en un plan de ejecución eficiente.
# MAGIC
# MAGIC ```
# MAGIC Tu código (DataFrame API o SQL)
# MAGIC     ↓
# MAGIC 1. Análisis (resolución de columnas)
# MAGIC     ↓
# MAGIC 2. Optimización Lógica (reglas: pushdown filters, prune columns)
# MAGIC     ↓
# MAGIC 3. Optimización Física (join strategies, shuffle)
# MAGIC     ↓
# MAGIC 4. Ejecución (RDDs en cluster)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📖 EXPLAIN: Leer el Plan de Ejecución
# MAGIC
# MAGIC ```python
# MAGIC # Ver plan de ejecución
# MAGIC df.filter(col("ventas") > 50000).groupBy("sucursal_id").sum("ventas").explain()
# MAGIC
# MAGIC # == Physical Plan ==
# MAGIC # *(1) HashAggregate(keys=[sucursal_id])
# MAGIC # +- Exchange hashpartitioning(sucursal_id)
# MAGIC #    +- *(1) HashAggregate(keys=[sucursal_id])
# MAGIC #       +- *(1) Filter (ventas > 50000)    ← Filtro aplicado temprano
# MAGIC #          +- Scan ventas_mensuales_mendoza_h3
# MAGIC ```
# MAGIC
# MAGIC **Lectura del plan:**
# MAGIC * Lee de abajo hacia arriba
# MAGIC * `*` = etapa de ejecución
# MAGIC * `Exchange` = shuffle de datos entre nodos
# MAGIC * Menos `Exchange` = mejor performance
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📦 Partitioning
# MAGIC
# MAGIC ```sql
# MAGIC -- Crear tabla particionada por año
# MAGIC CREATE TABLE ventas_particionadas
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (anio)
# MAGIC AS SELECT *, YEAR(fecha) as anio 
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Consulta con pruneo de particiones
# MAGIC SELECT * FROM ventas_particionadas WHERE anio = 2024;
# MAGIC -- → Solo lee archivos de 2024, no toda la tabla
# MAGIC ```
# MAGIC
# MAGIC **Cuándo particionar:**
# MAGIC * Columna con baja cardinalidad (< 1000 valores)
# MAGIC * Consultas frecuentes por esa columna
# MAGIC * Tablas grandes (> 1GB)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💾 Caching y Persistencia
# MAGIC
# MAGIC ```python
# MAGIC # Cachear DataFrame en memoria
# MAGIC df.cache()
# MAGIC
# MAGIC # Persistir con nivel específico
# MAGIC from pyspark.storagelevel import StorageLevel
# MAGIC df.persist(StorageLevel.MEMORY_AND_DISK)
# MAGIC
# MAGIC # Liberar cache
# MAGIC df.unpersist()
# MAGIC ```
# MAGIC
# MAGIC **Cuándo cachear:**
# MAGIC * DataFrame usado múltiples veces
# MAGIC * Después de transformaciones costosas
# MAGIC * Antes de joins repetitivos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📐 Broadcast Joins
# MAGIC
# MAGIC ```python
# MAGIC # Cuando una tabla es pequeña (< 10MB), Spark la envía a todos los nodos
# MAGIC # Evita shuffle de datos
# MAGIC
# MAGIC df_large.join(broadcast(df_small), on="key")
# MAGIC # → df_small se copia a todos los executors
# MAGIC # → No hay Exchange (shuffle)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Optimización = velocidad y costo:**
# MAGIC * ⚡ Queries 10x-100x más rápidas
# MAGIC * 💰 Menos recursos = menor costo
# MAGIC * 📊 Dashboards responsivos
# MAGIC * 🚀 Pipelines que terminan a tiempo

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, broadcast, year
import warnings
warnings.filterwarnings('ignore')

print("💻 EJERCICIOS: OPTIMIZACIÓN EN SPARK")
print("="*70)

if USAR_DATOS_REALES:
    # Ejercicio 1: EXPLAIN de una consulta
    print("\n1️⃣ Plan de ejecución de una consulta compleja:")
    df.filter(col("ventas") > 50000) \
      .groupBy("sucursal_id") \
      .sum("ventas") \
      .explain(extended=True)

    # Ejercicio 2: Particionado
    print("\n2️⃣ Creando tabla particionada por año:")
    spark.sql("""
        CREATE TABLE IF NOT EXISTS pandito_ds.default.ventas_particionadas
        USING DELTA
        PARTITIONED BY (anio)
        AS SELECT *, YEAR(fecha) as anio 
        FROM pandito_ds.default.ventas_mensuales_mendoza_h3
    """)
    
    # Verificar particiones
    spark.sql("SHOW PARTITIONS pandito_ds.default.ventas_particionadas").show()

    # Ejercicio 3: Caching
    print("\n3️⃣ Caching de DataFrame:")
    df_cached = df.filter(col("ventas") > 30000).cache()
    count1 = df_cached.count()  # Primera vez: calcula y cachea
    count2 = df_cached.count()  # Segunda vez: usa cache (más rápido)
    print(f"   Registros cached: {count1}")
    print(f"   Segunda consulta (cacheada): {count2}")
    df_cached.unpersist()

    # Ejercicio 4: Broadcast Join
    print("\n4️⃣ Broadcast Join (tabla pequeña + grande):")
    df_small = spark.sql("SELECT DISTINCT sucursal_id FROM pandito_ds.default.ventas_mensuales_mendoza_h3")
    df_result = df.join(broadcast(df_small), on="sucursal_id")
    print(f"   Resultado del join: {df_result.count()} registros")
    
    # Limpiar
    spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_particionadas")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Optimización completada")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 15_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Catalyst Optimizer:**
# MAGIC    - Transforma código (DataFrame API o SQL) en un plan de ejecución eficiente
# MAGIC    - 4 fases: Análisis → Optimización Lógica → Optimización Física → Ejecución
# MAGIC    - Pushdown filters, column pruning, join reordering — todo automático
# MAGIC
# MAGIC 2. **EXPLAIN — leer el plan de ejecución:**
# MAGIC    - `df.explain()` — plan físico (más importante)
# MAGIC    - `df.explain(extended=True)` — plan lógico + físico completo
# MAGIC    - Se lee de abajo hacia arriba: `Exchange` = shuffle (costoso), `*` = etapa
# MAGIC    - Menos `Exchange` = mejor performance
# MAGIC
# MAGIC 3. **Partitioning — particionado de tablas:**
# MAGIC    - `PARTITIONED BY (col)` — divide físicamente por valor de columna
# MAGIC    - Consultas con `WHERE col = valor` solo leen la partición relevante (partition pruning)
# MAGIC    - Cardinalidad baja (< 1000 valores) y consultas frecuentes por esa columna
# MAGIC
# MAGIC 4. **Caching y Persistencia:**
# MAGIC    - `df.cache()` — guarda en memoria (MEMORY_AND_DISK por defecto)
# MAGIC    - `df.persist(StorageLevel.MEMORY_ONLY)` — nivel específico
# MAGIC    - `df.unpersist()` — libera memoria al terminar
# MAGIC    - Solo cachear si el DataFrame se usa múltiples veces
# MAGIC
# MAGIC 5. **Broadcast Joins:**
# MAGIC    - `df_large.join(broadcast(df_small), on="key")` — sin shuffle
# MAGIC    - Tabla pequeña (< 10 MB) se envía a todos los executors
# MAGIC    - 10-100x más rápido que Sort-Merge Join
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Filtrar ANTES de join o agregación**
# MAGIC ```python
# MAGIC # MALO: join primero, filtra después (procesa TODO)
# MAGIC df1.join(df2, "clave").filter(col("ventas") > 50000)
# MAGIC
# MAGIC # BUENO: filtra primero, join después (procesa MENOS)
# MAGIC df1.filter(col("ventas") > 50000).join(df2, "clave")
# MAGIC # Catalyst hace pushdown automáticamente, pero ser explícito es más claro
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Particionar por columna de baja cardinalidad**
# MAGIC ```sql
# MAGIC -- MALO: particionar por fecha exacta (cardinalidad alta, muchas particiones)
# MAGIC CREATE TABLE ventas USING DELTA PARTITIONED BY (fecha);
# MAGIC
# MAGIC -- BUENO: particionar por año o mes (cardinalidad baja, particiones útiles)
# MAGIC CREATE TABLE ventas USING DELTA PARTITIONED BY (anio)
# MAGIC AS SELECT *, YEAR(fecha) AS anio FROM fuente;
# MAGIC -- WHERE anio = 2024 → solo lee esa partición
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Cachear solo si se reutiliza, siempre hacer unpersist**
# MAGIC ```python
# MAGIC # MALO: cachear y nunca liberar (memory leak)
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()
# MAGIC # ... nunca se libera → memoria ocupada innecesariamente
# MAGIC
# MAGIC # BUENO: cachear, usar, liberar
# MAGIC df_cached = df.filter(col("ventas") > 1000).cache()
# MAGIC df_cached.count()   # materializa cache
# MAGIC df_cached.show()    # usa cache
# MAGIC df_cached.unpersist()  # libera memoria
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Ver plan de ejecución | `df.explain()` o `df.explain(extended=True)` |
# MAGIC | Reducir shuffle en join | `broadcast(df_small)` si tabla < 10 MB |
# MAGIC | Particionar tabla grande | `PARTITIONED BY (col_baja_cardinalidad)` |
# MAGIC | Acelerar queries por columna | `OPTIMIZE tabla ZORDER BY (col)` |
# MAGIC | Reutilizar DataFrame costoso | `df.cache()` + `df.unpersist()` al final |
# MAGIC | Filtrar antes de procesar | `.filter(...)` antes de `.join()` o `.groupBy()` |
# MAGIC | Detectar Data Skew | `df.groupBy("clave").count()` — buscar claves dominantes |
# MAGIC | Mitigar Skew | Salting: `concat(clave, "_", rand()*10)` |
# MAGIC | Compactar archivos pequeños | `OPTIMIZE tabla` |
# MAGIC | Verificar particiones | `SHOW PARTITIONS tabla` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🚀 ¡Optimización Catalyst y Partitioning dominados!</h3>
# MAGIC   <p><i>"Optimizar no es opcional: 10x más rápido = 10x menos costo y dashboards responsivos."</i></p>
# MAGIC </div>