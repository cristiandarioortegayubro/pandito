# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🏗️ Módulo 15 - Notebook 05: ETL Pipeline de Producción
# MAGIC
# MAGIC ## 🚀 Pipeline completo: Extract → Transform → Load → Parquet
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 15 - Delta Lake, Window Functions y Optimización  
# MAGIC **Duración estimada:** 80 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos
# MAGIC
# MAGIC ✅ **Construir** un pipeline ETL completo  
# MAGIC ✅ **Aplicar** Extract, Transform, Load  
# MAGIC ✅ **Escribir** datos en formato Parquet/Delta  
# MAGIC ✅ **Implementar** control de calidad  
# MAGIC ✅ **Automatizar** con Jobs de Databricks  
# MAGIC ✅ **Monitorear** ejecución de pipelines
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 12-15 completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **ETL** - Concepto y etapas
# MAGIC 2. **Extract** - Cargar desde Unity Catalog
# MAGIC 3. **Transform** - Limpieza, agregaciones, enriquecimiento
# MAGIC 4. **Load** - Escribir a Delta/Parquet
# MAGIC 5. **Control de calidad** - Validaciones
# MAGIC 6. **Pipeline completo** - Caso integrador

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
from pyspark.sql.functions import col, year, month, round as spark_round, when, count, isnull

print("💾 SETUP: PIPELINE ETL")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df_raw = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Datos extraídos: {df_raw.count()} registros")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: ETL Pipeline
# MAGIC %md
# MAGIC ## 📚 Teoría: ETL Pipeline de Producción
# MAGIC
# MAGIC ### 🏗️ ¿Qué es un Pipeline ETL?
# MAGIC
# MAGIC **ETL (Extract, Transform, Load)** es el proceso de mover y transformar datos desde fuentes hacia destinos analíticos.
# MAGIC
# MAGIC ```
# MAGIC ┌──────────┐    ┌──────────────┐    ┌──────────┐
# MAGIC │ EXTRACT  │ →  │  TRANSFORM   │ →  │  LOAD    │
# MAGIC │          │    │              │    │          │
# MAGIC | Leer de  │    | Limpiar      │    | Guardar  │
# MAGIC | fuente   │    | Agregar      │    | en Delta │
# MAGIC | (UC, CSV)│    | Enriquecer   │    | Parquet  │
# MAGIC └──────────┘    └──────────────┘    └──────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📋 Etapas del Pipeline
# MAGIC
# MAGIC **1️⃣ EXTRACT**
# MAGIC ```python
# MAGIC # Leer desde Unity Catalog
# MAGIC df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
# MAGIC
# MAGIC # O leer desde archivos
# MAGIC df_raw = spark.read.csv("/path/to/data.csv", header=True, inferSchema=True)
# MAGIC ```
# MAGIC
# MAGIC **2️⃣ TRANSFORM**
# MAGIC ```python
# MAGIC # Limpieza
# MAGIC df_clean = df_raw.dropDuplicates() \
# MAGIC     .na.drop(subset=["ventas", "fecha"]) \
# MAGIC     .withColumn("ventas", col("ventas").cast("double"))
# MAGIC
# MAGIC # Enriquecimiento
# MAGIC df_enriched = df_clean \
# MAGIC     .withColumn("anio", year("fecha")) \
# MAGIC     .withColumn("mes", month("fecha")) \
# MAGIC     .withColumn("categoria_venta", 
# MAGIC         when(col("ventas") > 80000, "Alto")
# MAGIC         .when(col("ventas") > 50000, "Medio")
# MAGIC         .otherwise("Bajo"))
# MAGIC ```
# MAGIC
# MAGIC **3️⃣ LOAD**
# MAGIC ```python
# MAGIC # Escribir en formato Delta
# MAGIC df_enriched.write \
# MAGIC     .format("delta") \
# MAGIC     .mode("overwrite") \
# MAGIC     .saveAsTable("pandito_ds.default.ventas_procesadas")
# MAGIC
# MAGIC # O en formato Parquet
# MAGIC df_enriched.write \
# MAGIC     .mode("overwrite") \
# MAGIC     .parquet("/path/to/output/")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ✅ Control de Calidad
# MAGIC
# MAGIC ```python
# MAGIC # Validaciones después del ETL
# MAGIC df_result = spark.table("pandito_ds.default.ventas_procesadas")
# MAGIC
# MAGIC # 1. Conteo de registros
# MAGIC assert df_result.count() > 0, "Sin datos después del ETL"
# MAGIC
# MAGIC # 2. Nulos
# MAGIC nulls = df_result.select([count(when(isnull(c), c)).alias(c) for c in df_result.columns])
# MAGIC nulls.show()
# MAGIC
# MAGIC # 3. Rangos válidos
# MAGIC stats = df_result.describe("ventas")
# MAGIC stats.show()
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **ETL pipelines = datos confiables:**
# MAGIC * 📊 Datos limpios y procesados para análisis
# MAGIC * ⏰ Automatización: ejecuta en horario
# MAGIC * 📦 Reproducibilidad: mismo resultado cada vez
# MAGIC * 📈 Escalabilidad: de MB a TB sin cambiar código
# MAGIC * 🏢 Producción: pipelines que corren en Databricks Jobs

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, year, month, round as spark_round, when, count, isnull
import warnings
warnings.filterwarnings('ignore')

print("💻 PIPELINE ETL COMPLETO")
print("="*70)

if USAR_DATOS_REALES:
    # === EXTRACT ===
    print("\n1️⃣ EXTRACT: Leyendo datos de Unity Catalog")
    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
    print(f"   Registros extraídos: {df_raw.count()}")

    # === TRANSFORM ===
    print("\n2️⃣ TRANSFORM: Limpiando y enriqueciendo")
    df_clean = df_raw.dropDuplicates() \
        .na.drop(subset=["ventas", "fecha"]) \
        .withColumn("ventas", col("ventas").cast("double")) \
        .withColumn("anio", year("fecha")) \
        .withColumn("mes", month("fecha")) \
        .withColumn("categoria_venta", 
            when(col("ventas") > 80000, "Alto")
            .when(col("ventas") > 50000, "Medio")
            .otherwise("Bajo"))
    print(f"   Registros después de limpieza: {df_clean.count()}")

    # === LOAD ===
    print("\n3️⃣ LOAD: Guardando en tabla Delta")
    df_clean.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable("pandito_ds.default.ventas_procesadas_etl")
    print(f"   Tabla 'ventas_procesadas_etl' creada")

    # === CONTROL DE CALIDAD ===
    print("\n4️⃣ CONTROL DE CALIDAD:")
    df_result = spark.table("pandito_ds.default.ventas_procesadas_etl")
    
    total = df_result.count()
    print(f"   Total registros: {total}")
    
    # Categorías
    df_result.groupBy("categoria_venta").count().orderBy("categoria_venta").show()
    
    # Estadísticas
    df_result.describe("ventas").show()

    # Limpieza
    spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_procesadas_etl")
    print("\n✅ Pipeline ETL completado exitosamente")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Módulo 15 completo - Delta Lake, Window Functions y Optimización")

# COMMAND ----------

# DBTITLE 1,🏗️ Teoría: ETL con datos reales
# MAGIC %md
# MAGIC ## 🏗️ ETL Pipeline aplicado a Los Andes Market
# MAGIC
# MAGIC ### 📊 Pipeline real: de ventas crudas a KPIs de negocio
# MAGIC
# MAGIC Un pipeline ETL completo sobre `ventas_mensuales_mendoza_h3`:
# MAGIC
# MAGIC ```
# MAGIC EXTRACT (Unity Catalog) → TRANSFORM (limpieza + enriquecimiento) → LOAD (Delta) → VALIDATE
# MAGIC ```
# MAGIC
# MAGIC ```python
# MAGIC # EXTRACT
# MAGIC df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
# MAGIC
# MAGIC # TRANSFORM: agregar IVA, categorías, año/mes
# MAGIC df_clean = (df_raw
# MAGIC     .dropDuplicates()
# MAGIC     .withColumn("ventas_iva", col("ventas") * 1.21)
# MAGIC     .withColumn("categoria", when(col("ventas") > 80000, "Alto").otherwise("Bajo")))
# MAGIC
# MAGIC # LOAD: guardar como tabla Delta
# MAGIC df_clean.write.format("delta").mode("overwrite").saveAsTable("...")
# MAGIC
# MAGIC # VALIDATE: verificar nulos, rangos, conteo
# MAGIC assert df_result.count() > 0
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Control de calidad en el pipeline
# MAGIC * **Conteo:** ¿el número de registros es razonable?
# MAGIC * **Nulos:** ¿hay columnas críticas con nulos?
# MAGIC * **Rangos:** ¿ventas son positivas?
# MAGIC * **Duplicados:** ¿hay registros duplicados?

# COMMAND ----------

# DBTITLE 1,🏗️ Práctica: ETL con datos reales
from pyspark.sql.functions import col, year, month, when, count, isnull, sum as spark_sum, round as spark_round

print("🏗️ ETL PIPELINE APLICADO A LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and 'df_raw' in dir():
    # === EXTRACT ===
    print("\n1️⃣  EXTRACT: Leer desde Unity Catalog")
    print("-"*70)
    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
    n_raw = df_raw.count()
    print(f"   Registros extraídos: {n_raw:,}")

    # === TRANSFORM ===
    print("\n2️⃣  TRANSFORM: Limpieza + enriquecimiento")
    print("-"*70)
    df_clean = (df_raw
        .dropDuplicates()
        .na.drop(subset=["ventas", "fecha"])
        .filter(col("ventas") > 0)  # Solo ventas positivas
        .withColumn("anio", year("fecha"))
        .withColumn("mes", month("fecha"))
        .withColumn("ventas_iva", spark_round(col("ventas") * 1.21, 2))
        .withColumn("margen_estimado", spark_round(col("ventas") * 0.15, 2))
        .withColumn("categoria_venta",
            when(col("ventas") > 100000, "Alto")
            .when(col("ventas") > 50000, "Medio")
            .otherwise("Bajo")))
    n_clean = df_clean.count()
    print(f"   Registros después de limpieza: {n_clean:,}")
    print(f"   Columnas agregadas: anio, mes, ventas_iva, margen_estimado, categoria_venta")

    # === LOAD ===
    print("\n3️⃣  LOAD: Guardar como tabla Delta")
    print("-"*70)
    df_clean.write.format("delta").mode("overwrite")\
        .saveAsTable("pandito_ds.default.ventas_los_andes_etl")
    print("   Tabla 'ventas_los_andes_etl' creada en formato Delta")

    # === VALIDATE ===
    print("\n4️⃣  VALIDATE: Control de calidad")
    print("-"*70)
    df_result = spark.table("pandito_ds.default.ventas_los_andes_etl")

    # Conteo
    total = df_result.count()
    print(f"   Total registros: {total:,}")
    assert total > 0, "❌ Sin datos después del ETL"
    print("   ✅ Conteo válido")

    # Nulos
    nulls = df_result.select([count(when(isnull(c), c)).alias(c) for c in ["ventas", "fecha", "sucursal_id"]])
    print("\n   Nulos en columnas críticas:")
    nulls.show()

    # Estadísticas
    print("   Estadísticas de ventas:")
    df_result.describe("ventas").show()

    # Categorías
    print("   Distribución por categoría:")
    df_result.groupBy("categoria_venta").agg(
        count("*").alias("registros"),
        spark_round(spark_sum("ventas"), 0).alias("ventas_totales")
    ).orderBy("categoria_venta").show()

    # === RESUMEN ETL ===
    print("\n" + "="*70)
    print("\n5️⃣  RESUMEN DEL PIPELINE ETL")
    print("-"*70)
    print(f"   📥 Extract:  {n_raw:,} registros desde Unity Catalog")
    print(f"   🔄 Transform: {n_clean:,} registros después de limpieza + enriquecimiento")
    print(f"   📤 Load:     Tabla Delta 'ventas_los_andes_etl' creada")
    print(f"   ✅ Validate: Conteo, nulos, estadísticas y categorías verificados")

    # Limpieza
    spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_los_andes_etl")
    print("\n   Tabla temporal eliminada")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 15_05
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **EXTRACT — extracción desde Unity Catalog:**
# MAGIC    ```python
# MAGIC    # Desde Unity Catalog (recomendado)
# MAGIC    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
# MAGIC    
# MAGIC    # Desde archivos
# MAGIC    df_raw = spark.read.csv("/path/to/data.csv", header=True, inferSchema=True)
# MAGIC    df_raw = spark.read.parquet("/path/to/data.parquet")
# MAGIC    ```
# MAGIC
# MAGIC 2. **TRANSFORM — limpieza y enriquecimiento:**
# MAGIC    ```python
# MAGIC    # Limpieza: duplicados, nulos, tipos
# MAGIC    df_clean = (df_raw
# MAGIC        .dropDuplicates()
# MAGIC        .na.drop(subset=["ventas", "fecha"])
# MAGIC        .withColumn("ventas", col("ventas").cast("double"))
# MAGIC    )
# MAGIC    
# MAGIC    # Enriquecimiento: columnas calculadas
# MAGIC    df_enriched = (df_clean
# MAGIC        .withColumn("anio", year("fecha"))
# MAGIC        .withColumn("mes", month("fecha"))
# MAGIC        .withColumn("categoria_venta",
# MAGIC            when(col("ventas") > 80000, "Alto")
# MAGIC            .when(col("ventas") > 50000, "Medio")
# MAGIC            .otherwise("Bajo"))
# MAGIC    )
# MAGIC    ```
# MAGIC
# MAGIC 3. **LOAD — escritura a Delta/Parquet:**
# MAGIC    ```python
# MAGIC    # Delta Lake (recomendado para producción)
# MAGIC    df_enriched.write \
# MAGIC        .format("delta") \
# MAGIC        .mode("overwrite") \
# MAGIC        .saveAsTable("pandito_ds.default.ventas_procesadas_etl")
# MAGIC    
# MAGIC    # Parquet (sin ACID, para lectura externa)
# MAGIC    df_enriched.write \
# MAGIC        .mode("overwrite") \
# MAGIC        .parquet("/path/to/output/")
# MAGIC    ```
# MAGIC
# MAGIC 4. **Control de calidad — validaciones post-ETL:**
# MAGIC    ```python
# MAGIC    df_result = spark.table("pandito_ds.default.ventas_procesadas_etl")
# MAGIC    
# MAGIC    # Conteo
# MAGIC    assert df_result.count() > 0, "Sin datos después del ETL"
# MAGIC    
# MAGIC    # Nulos por columna
# MAGIC    nulls = df_result.select(
# MAGIC        [count(when(isnull(c), c)).alias(c) for c in df_result.columns]
# MAGIC    )
# MAGIC    nulls.show()
# MAGIC    
# MAGIC    # Estadísticas
# MAGIC    df_result.describe("ventas").show()
# MAGIC    ```
# MAGIC
# MAGIC 5. **Pipeline completo y automatización:**
# MAGIC    - Pipeline ETL: EXTRACT → TRANSFORM → LOAD → VALIDATE en un solo notebook
# MAGIC    - Databricks Jobs: programar ejecución diaria/semanal/mensual
# MAGIC    - Alertas: notificación por email si el pipeline falla
# MAGIC    - Idempotente: `mode("overwrite")` garantiza el mismo resultado cada ejecución
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de ETL Pipeline
# MAGIC
# MAGIC **Caso 1: Pipeline ETL básico (4 etapas)**
# MAGIC ```python
# MAGIC # EXTRACT
# MAGIC df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
# MAGIC # TRANSFORM
# MAGIC df_clean = df_raw.dropDuplicates().na.drop(subset=["ventas"]).withColumn("anio", year("fecha"))
# MAGIC # LOAD
# MAGIC df_clean.write.format("delta").mode("overwrite").saveAsTable("pandito_ds.default.ventas_etl")
# MAGIC # VALIDATE
# MAGIC assert spark.table("pandito_ds.default.ventas_etl").count() > 0
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Enriquecimiento con columnas calculadas**
# MAGIC ```python
# MAGIC df_enriched = (df_clean
# MAGIC     .withColumn("anio", year("fecha"))
# MAGIC     .withColumn("mes", month("fecha"))
# MAGIC     .withColumn("categoria", when(col("ventas") > 80000, "Alto").otherwise("Bajo"))
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Control de calidad con assertions**
# MAGIC ```python
# MAGIC df_result = spark.table("pandito_ds.default.ventas_etl")
# MAGIC assert df_result.count() > 0, "Sin datos"
# MAGIC assert df_result.filter(col("ventas").isNull()).count() == 0, "Hay nulos en ventas"
# MAGIC print("✅ Control de calidad pasado")
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Escritura idempotente**
# MAGIC ```python
# MAGIC # mode("overwrite") = reemplaza todo, mismo resultado cada ejecución
# MAGIC df.write.format("delta").mode("overwrite").saveAsTable("tabla")
# MAGIC # mode("append") = agrega datos (requiere cuidado con duplicados)
# MAGIC df.write.format("delta").mode("append").saveAsTable("tabla")
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Limpiar tabla temporal después del ETL**
# MAGIC ```python
# MAGIC spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_procesadas_etl")
# MAGIC print("✅ Limpieza completada")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 15
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **15_01 - PySpark SQL Consultas Declarativas:** spark.sql(), vistas temporales, SQL vs DataFrame API
# MAGIC 2. **15_02 - Window Functions Distribuidas:** ROW_NUMBER, RANK, LAG/LEAD, running totals, promedios móviles
# MAGIC 3. **15_03 - Delta Lake ACID y Time Travel:** USING DELTA, VERSION AS OF, MERGE, OPTIMIZE, VACUUM
# MAGIC 4. **15_04 - Optimización Catalyst y Partitioning:** EXPLAIN, broadcast joins, partitioning, caching
# MAGIC 5. **15_05 - ETL Pipeline de Producción:** EXTRACT → TRANSFORM → LOAD → VALIDATE, control de calidad
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Construir pipelines ETL completos con Spark
# MAGIC * ✅ Aplicar window functions para análisis avanzado
# MAGIC * ✅ Usar Delta Lake con ACID y Time Travel
# MAGIC * ✅ Optimizar consultas con Catalyst y broadcast
# MAGIC * ✅ Implementar control de calidad y validaciones
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🏗️ ¡Módulo 15 Completado!</h3>
# MAGIC   <p><i>"Dominas Delta Lake, Window Functions y ETL de producción. Ahora puedes construir pipelines que escalan de MB a TB con calidad garantizada."</i></p>
# MAGIC </div>