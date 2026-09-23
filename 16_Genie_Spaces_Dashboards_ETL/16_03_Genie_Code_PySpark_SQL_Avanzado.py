# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 16 - Notebook 03: Genie Code PySpark/SQL avanzado
# MAGIC
# MAGIC ## 🤖 Generación de código con IA para Pipelines complejos
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 16 - Genie Spaces, Dashboards AI/BI y ETL  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio-Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Generar** código PySpark complejo con Genie Code  
# MAGIC ✅ **Migrar** código Pandas a PySpark con IA  
# MAGIC ✅ **Optimizar** consultas SQL con asistencia  
# MAGIC ✅ **Debuggear** pipelines con Genie  
# MAGIC ✅ **Validar** código generado por IA  
# MAGIC ✅ **Aplicar** patrones ETL con Genie Code
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 12-15 completados (PySpark, SQL, Delta Lake)
# MAGIC * ✅ Notebook 02_01 (Genie Code básico)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Genie Code avanzado** - Más allá de lo básico
# MAGIC 2. **Migración Pandas → PySpark** - Traducción automática
# MAGIC 3. **SQL optimizado con Genie** - Consultas complejas
# MAGIC 4. **Patrones ETL** - Pipelines con IA
# MAGIC 5. **Validación** - Revisar código generado

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
from pyspark.sql.functions import col

print("💾 SETUP: GENIE CODE AVANZADO")
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

print("\n📌 PROMPTS PARA GENIE CODE AVANZADO:")
print("\n1. Migración Pandas → PySpark:")
print('   "Convierte este código Pandas a PySpark: df.groupby("sucursal_id")["ventas"].agg(["sum","mean"])"')
print("\n2. SQL optimizado:")
print("   "Optimiza esta consulta SQL con window functions para calcular ranking de ventas por sucursal"")
print("\n3. Pipeline ETL:")
print("   "Crea un pipeline ETL que lea de ventas_mensuales_mendoza_h3, limpie nulos, agregue columnas de año y mes, y guarde en una tabla Delta"")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Genie Code Avanzado
# MAGIC %md
# MAGIC ## 📚 Teoría: Genie Code Avanzado para PySpark y SQL
# MAGIC
# MAGIC ### 🤖 Generación de Código con IA
# MAGIC
# MAGIC Ahora que dominas PySpark, SQL y Delta Lake, Genie Code se convierte en tu copiloto para escribir código complejo más rápido.
# MAGIC
# MAGIC **Regla de oro:** "Genie genera, tú validas"
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Migración Pandas → PySpark
# MAGIC
# MAGIC Genie puede traducir automáticamente código Pandas a PySpark:
# MAGIC
# MAGIC | Pandas | PySpark (Genie genera) |
# MAGIC |--------|-------------------------|
# MAGIC | `df.groupby('col').sum()` | `df.groupBy('col').sum()` |
# MAGIC | `df.merge(other, on='key')` | `df.join(other, on='key')` |
# MAGIC | `df.fillna(0)` | `df.na.fill(0)` |
# MAGIC | `df.pivot(index='a', columns='b')` | `df.groupBy('a').pivot('b').sum()` |
# MAGIC | `df['x'].rolling(3).mean()` | `Window.partitionBy().orderBy().rowsBetween(-2,0)` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Prompts Efectivos para Código Complejo
# MAGIC
# MAGIC **Prompt: Pipeline ETL completo**
# MAGIC ```
# MAGIC Crea un pipeline ETL que:
# MAGIC 1. Lea de pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC 2. Filtre ventas > 0
# MAGIC 3. Agregue columnas: anio, mes, trimestre
# MAGIC 4. Calcule ventas acumuladas por sucursal (window function)
# MAGIC 5. Clasifique ventas en Alto/Medio/Bajo (CASE WHEN)
# MAGIC 6. Guarde en tabla Delta pandito_ds.default.ventas_procesadas
# MAGIC 7. Agregue control de calidad al final
# MAGIC ```
# MAGIC
# MAGIC **Prompt: SQL con Window Functions**
# MAGIC ```
# MAGIC Escribe una consulta SQL que:
# MAGIC - Calcule el ranking de cada sucursal por mes (ROW_NUMBER)
# MAGIC - Compare ventas con el mes anterior (LAG)
# MAGIC - Calcule el promedio móvil de 3 meses
# MAGIC - Solo para el año 2023
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Validación de Código Generado
# MAGIC
# MAGIC ```python
# MAGIC # 1. ¿Hace lo que necesitas?
# MAGIC df_result.show(5)  # Verifica las primeras filas
# MAGIC
# MAGIC # 2. ¿Es eficiente?
# MAGIC df_result.explain()  # Revisa el plan de ejecución
# MAGIC
# MAGIC # 3. ¿Entiendes cómo funciona?
# MAGIC # Si no entiendes algo, pregunta a Genie que lo explique
# MAGIC
# MAGIC # 4. ¿Maneja edge cases?
# MAGIC df_result.filter(col('ventas').isNull()).count()  # Nulos
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Genie Code avanzado = 10x productividad:**
# MAGIC * 🚀 Código complejo en segundos
# MAGIC * 🔄 Migración Pandas → PySpark automática
# MAGIC * 📊 SQL optimizado sin memorizar sintaxis
# MAGIC * 🐛 Debugging asistido por IA
# MAGIC * ✅ Validación de lógica de negocio

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, year, month, quarter, when, sum as spark_sum
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, lag, avg, round as spark_round
import warnings
warnings.filterwarnings('ignore')

print("💻 EJEMPLO: PIPELINE GENERADO CON GENIE CODE")
print("="*70)

if USAR_DATOS_REALES:
    # Pipeline ETL completo (ejemplo de lo que Genie generaría)
    print("\n1️⃣ EXTRACT:")
    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
    print(f"   Registros leídos: {df_raw.count()}")

    print("\n2️⃣ TRANSFORM:")
    df_t = df_raw.filter(col("ventas") > 0) \
        .withColumn("anio", year("fecha")) \
        .withColumn("mes", month("fecha")) \
        .withColumn("trimestre", quarter("fecha")) \
        .withColumn("categoria", when(col("ventas") > 80000, "Alto")
            .when(col("ventas") > 50000, "Medio")
            .otherwise("Bajo"))
    print(f"   Registros transformados: {df_t.count()}")
    print(f"   Columnas: {df_t.columns}")

    print("\n3️⃣ WINDOW FUNCTIONS (Ranking y LAG):")
    w_rank = Window.partitionBy("sucursal_id").orderBy(col("ventas").desc())
    w_lag = Window.partitionBy("sucursal_id").orderBy("fecha")
    df_w = df_t.withColumn("ranking", row_number().over(w_rank)) \
        .withColumn("venta_anterior", lag("ventas").over(w_lag)) \
        .withColumn("crecimiento_pct", spark_round((col("ventas") - col("venta_anterior")) / col("venta_anterior") * 100, 2))
    df_w.select("sucursal_id", "fecha", "ventas", "ranking", "crecimiento_pct").orderBy("sucursal_id", "fecha").show(10)

    print("\n4️⃣ LOAD (verificar sin escribir):")
    print(f"   Total registros finales: {df_w.count()}")
    print("   Categorías:")
    df_w.groupBy("categoria").count().orderBy("categoria").show()

    print("\n5️⃣ CONTROL DE CALIDAD:")
    nulos = df_w.filter(col("ventas").isNull()).count()
    print(f"   Nulos en ventas: {nulos}")
    print(f"   Duplicados: {df_w.count() - df_w.dropDuplicates().count()}")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Pipeline con Genie Code avanzado completado")

# COMMAND ----------

# DBTITLE 1,⚡ Teoría: Genie Code con datos reales
# MAGIC %md
# MAGIC ## ⚡ Genie Code aplicado a Los Andes Market
# MAGIC
# MAGIC ### 🤖 Pipeline ETL con asistencia de IA
# MAGIC
# MAGIC Genie Code puede generar un pipeline completo para **Los Andes Market** con un solo prompt estructurado:
# MAGIC
# MAGIC ```
# MAGIC Crea un pipeline ETL que:
# MAGIC 1. Lea de pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC 2. Filtre ventas > 0
# MAGIC 3. Agregue columnas: anio, mes, ventas_iva (×1.21), categoria (Alto/Medio/Bajo)
# MAGIC 4. Calcule ranking mensual por zona con ROW_NUMBER
# MAGIC 5. Calcule crecimiento vs mes anterior con LAG
# MAGIC 6. Guarde en tabla Delta pandito_ds.default.ventas_enriquecidas
# MAGIC 7. Agregue control de calidad al final
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Migración Pandas → PySpark con Genie
# MAGIC
# MAGIC | Pandas | PySpark (Genie traduce) |
# MAGIC |--------|------------------------|
# MAGIC | `df.groupby('zona')['ventas'].sum()` | `df.groupBy('zona').agg(sum('ventas'))` |
# MAGIC | `df.pivot_table(...)` | `df.groupBy(...).pivot(...).agg(...)` |
# MAGIC | `df['ventas'].rolling(3).mean()` | `Window.partitionBy(...).rowsBetween(-2, 0)` |
# MAGIC | `pd.merge(df1, df2, on='key')` | `df1.join(df2, on='key')` |

# COMMAND ----------

# DBTITLE 1,⚡ Práctica: Pipeline con Genie Code
from pyspark.sql.functions import col, year, month, round as spark_round, when, sum as spark_sum, avg, count
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, lag

print("⚡ PIPELINE ETL GENERADO CON GENIE CODE PARA LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and 'df' in dir():
    print("\n1️⃣  EXTRACT: Leer desde Unity Catalog")
    print("-"*70)
    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
    n_raw = df_raw.count()
    print(f"   Registros: {n_raw:,}")

    print("\n" + "="*70)
    print("\n2️⃣  TRANSFORM: Limpieza + enriquecimiento")
    print("-"*70)
    df_t = (df_raw
        .dropDuplicates()
        .na.drop(subset=["ventas", "fecha"])
        .filter(col("ventas") > 0)
        .withColumn("anio", year("fecha"))
        .withColumn("mes", month("fecha"))
        .withColumn("ventas_iva", spark_round(col("ventas") * 1.21, 2))
        .withColumn("categoria",
            when(col("ventas") > 100000, "Alto")
            .when(col("ventas") > 50000, "Medio")
            .otherwise("Bajo")))
    n_t = df_t.count()
    print(f"   Registros después de limpieza: {n_t:,}")
    print(f"   Columnas agregadas: anio, mes, ventas_iva, categoria")
    df_t.select("sucursal_nombre", "zona", "fecha", "ventas", "ventas_iva", "categoria").show(5, truncate=30)

    print("\n" + "="*70)
    print("\n3️⃣  WINDOW FUNCTIONS: Ranking y crecimiento")
    print("-"*70)
    w_rank = Window.partitionBy("zona", "mes").orderBy(col("ventas").desc())
    w_lag = Window.partitionBy("sucursal_id").orderBy("fecha")

    df_w = (df_t
        .withColumn("rank_zona_mes", row_number().over(w_rank))
        .withColumn("venta_anterior", lag("ventas").over(w_lag))
        .withColumn("crecimiento_pct", spark_round(
            (col("ventas") - col("venta_anterior")) / col("venta_anterior") * 100, 2)))

    print("   Top 3 por zona y mes:")
    (df_w.filter(col("rank_zona_mes") <= 2)
        .select("zona", "mes", "sucursal_nombre", spark_round("ventas", 0).alias("ventas"), "rank_zona_mes")
        .orderBy("zona", "mes", "rank_zona_mes")
        .show(15, truncate=25))

    print("\n" + "="*70)
    print("\n4️⃣  LOAD: Guardar como tabla Delta")
    print("-"*70)
    df_w.write.format("delta").mode("overwrite")\
        .saveAsTable("pandito_ds.default.ventas_enriquecidas_genie")
    print("   Tabla 'ventas_enriquecidas_genie' creada")

    print("\n" + "="*70)
    print("\n5️⃣  VALIDATE: Control de calidad")
    print("-"*70)
    df_result = spark.table("pandito_ds.default.ventas_enriquecidas_genie")
    print(f"   Total registros: {df_result.count():,}")
    print("   Distribución por categoría:")
    df_result.groupBy("categoria").agg(
        count("*").alias("registros"),
        spark_round(spark_sum("ventas"), 0).alias("ventas_total")
    ).orderBy("categoria").show()

    nulos = df_result.filter(col("ventas").isNull()).count()
    print(f"   Nulos en ventas: {nulos}")
    print("   ✅ Pipeline validado correctamente")

    # Limpieza
    spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_enriquecidas_genie")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 16_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Genie Code avanzado para PySpark:**
# MAGIC    - Genera pipelines completos con un prompt estructurado
# MAGIC    - Traduce Pandas a PySpark automáticamente (groupby → groupBy, fillna → na.fill)
# MAGIC    - Window functions, CASE WHEN, joins — todo con IA
# MAGIC
# MAGIC 2. **Migración Pandas → PySpark:**
# MAGIC    - `df.groupby('col').sum()` → `df.groupBy('col').sum()`
# MAGIC    - `df.merge(other, on='key')` → `df.join(other, on='key')`
# MAGIC    - `df.fillna(0)` → `df.na.fill(0)`
# MAGIC    - `df['x'].rolling(3).mean()` → `Window.partitionBy().orderBy().rowsBetween(-2, 0)`
# MAGIC
# MAGIC 3. **SQL optimizado con Genie:**
# MAGIC    - Window functions: ROW_NUMBER, RANK, LAG, promedios móviles
# MAGIC    - CTEs para consultas legibles paso a paso
# MAGIC    - Optimización automática de joins y filtros
# MAGIC
# MAGIC 4. **Patrones ETL con Genie Code:**
# MAGIC    - EXTRACT → TRANSFORM → LOAD → VALIDATE en un solo prompt
# MAGIC    - Columnas calculadas: anio, mes, trimestre, categoria
# MAGIC    - Control de calidad: nulos, duplicados, assertions
# MAGIC
# MAGIC 5. **Validación de código generado:**
# MAGIC    - `df.show(5)` — verificar primeras filas
# MAGIC    - `df.explain()` — revisar plan de ejecución
# MAGIC    - Contar nulos y duplicados después del pipeline
# MAGIC    - Si no entiendes algo, pedir a Genie que lo explique
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Prompt estructurado = mejor código**
# MAGIC ```python
# MAGIC # MALO: prompt vago
# MAGIC "Haz un ETL de ventas"
# MAGIC
# MAGIC # BUENO: prompt estructurado con pasos
# MAGIC "Crea un pipeline ETL que:
# MAGIC 1. Lea de pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC 2. Filtre ventas > 0
# MAGIC 3. Agregue columnas: anio, mes, trimestre
# MAGIC 4. Calcule ventas acumuladas por sucursal (window function)
# MAGIC 5. Clasifique ventas en Alto/Medio/Bajo
# MAGIC 6. Guarde en tabla Delta
# MAGIC 7. Agregue control de calidad"
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Genie genera, tu validas**
# MAGIC ```python
# MAGIC # MALO: ejecutar codigo generado sin revisar
# MAGIC df_result = spark.sql("...codigo generado...")
# MAGIC df_result.write.saveAsTable("tabla_produccion")  # 💥 sin validar
# MAGIC
# MAGIC # BUENO: validar antes de producir
# MAGIC df_result.show(5)                    # ver datos
# MAGIC df_result.explain()                  # ver plan
# MAGIC df_result.filter(col('ventas').isNull()).count()  # nulos
# MAGIC # Solo cuando todo es correcto → escribir
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Si no entiendes, pide explicacion**
# MAGIC ```python
# MAGIC # MALO: aceptar codigo sin entender
# MAGIC # (si falla en produccion, no sabras como arreglarlo)
# MAGIC
# MAGIC # BUENO: pedir a Genie que explique
# MAGIC "Explica este codigo linea por linea:
# MAGIC [PEGAR CODIGO]
# MAGIC En particular, explica que hace la linea X y por que usa Y"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Prompt para Genie |
# MAGIC |-----------|-----------------|
# MAGIC | Migrar Pandas a PySpark | "Convierte este codigo Pandas a PySpark: [PEGAR]" |
# MAGIC | Pipeline ETL completo | "Crea un ETL que: 1. lea... 2. filtre... 3. agregue... 4. guarde..." |
# MAGIC | SQL con window functions | "Escribe SQL con ROW_NUMBER y LAG para ranking por sucursal" |
# MAGIC | Debuggear error | "Este codigo da error: [PEGAR]. Explica el problema y corrigelo" |
# MAGIC | Optimizar query lenta | "Optimiza esta consulta: [PEGAR SQL]. Contexto: N millones de filas" |
# MAGIC | Explicar codigo | "Explica este codigo linea por linea: [PEGAR]" |
# MAGIC | Agregar control de calidad | "Agrega validaciones de nulos y duplicados a este pipeline" |
# MAGIC | Clasificar con CASE WHEN | "Clasifica ventas en Alto/Medio/Bajo con when/otherwise" |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🤖 ¡Genie Code PySpark/SQL Avanzado dominado!</h3>
# MAGIC   <p><i>"Genie genera, tu validas: 10x productividad sin perder control de tu codigo."</i></p>
# MAGIC </div>