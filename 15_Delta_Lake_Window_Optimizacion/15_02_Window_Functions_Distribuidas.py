# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🪟 Módulo 15 - Notebook 02: Window functions distribuidas
# MAGIC
# MAGIC ## 📊 Análisis avanzado con funciones de ventana en Spark
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 15 - Delta Lake, Window Functions y Optimización  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué son las Window Functions  
# MAGIC ✅ **Aplicar** ROW_NUMBER, RANK, DENSE_RANK  
# MAGIC ✅ **Usar** LAG y LEAD para comparar períodos  
# MAGIC ✅ **Calcular** promedios móviles con Window  
# MAGIC ✅ **Resolver** análisis de running totals y percentiles
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Notebook 15_01 completado (PySpark SQL)
# MAGIC * ✅ Conocimiento de GROUP BY y agregaciones
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Window Functions** - Concepto y sintaxis
# MAGIC 2. **ROW_NUMBER, RANK, DENSE_RANK** - Ranking
# MAGIC 3. **LAG y LEAD** - Comparación temporal
# MAGIC 4. **Running totals y promedios móviles** - Acumulados
# MAGIC 5. **PARTITION BY y ORDER BY** - Particionado de ventanas

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number, rank, dense_rank, lag, lead, sum as spark_sum, avg

print("💾 CARGANDO DATOS PARA WINDOW FUNCTIONS")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df_spark = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    df_spark.createOrReplaceTempView("ventas")
    print(f"✅ Tabla cargada: {df_spark.count()} registros")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Window Functions
# MAGIC %md
# MAGIC ## 📚 Teoría: Window Functions en PySpark
# MAGIC
# MAGIC ### 🪟 ¿Qué son las Window Functions?
# MAGIC
# MAGIC **Window Functions** calculan valores sobre un conjunto de filas relacionadas ("ventana") sin colapsarlas como GROUP BY.
# MAGIC
# MAGIC ```sql
# MAGIC -- GROUP BY: colapsa filas (una fila por grupo)
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas GROUP BY sucursal_id;
# MAGIC
# MAGIC -- WINDOW: mantiene filas + agrega columna calculada
# MAGIC SELECT 
# MAGIC   sucursal_id, fecha, ventas,
# MAGIC   SUM(ventas) OVER (PARTITION BY sucursal_id) as total_sucursal
# MAGIC FROM ventas;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Ranking: ROW_NUMBER, RANK, DENSE_RANK
# MAGIC
# MAGIC ```python
# MAGIC # En PySpark
# MAGIC from pyspark.sql.window import Window
# MAGIC from pyspark.sql.functions import row_number, rank, dense_rank
# MAGIC
# MAGIC window_spec = Window.partitionBy("sucursal_id").orderBy(col("ventas").desc())
# MAGIC
# MAGIC df_ranked = df.withColumn("row_num", row_number().over(window_spec)) \
# MAGIC               .withColumn("rank", rank().over(window_spec)) \
# MAGIC               .withColumn("dense_rank", dense_rank().over(window_spec))
# MAGIC ```
# MAGIC
# MAGIC | Función | Comportamiento |
# MAGIC |---------|---------------|
# MAGIC | ROW_NUMBER() | 1, 2, 3, 4... (siempre único) |
# MAGIC | RANK() | 1, 2, 2, 4... (saltos en empates) |
# MAGIC | DENSE_RANK() | 1, 2, 2, 3... (sin saltos) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⏪ LAG y LEAD: Comparar Períodos
# MAGIC
# MAGIC ```python
# MAGIC from pyspark.sql.functions import lag, lead
# MAGIC
# MAGIC window_spec = Window.partitionBy("sucursal_id").orderBy("fecha")
# MAGIC
# MAGIC df_with_lag = df.withColumn("venta_anterior", lag("ventas", 1).over(window_spec)) \
# MAGIC                 .withColumn("venta_siguiente", lead("ventas", 1).over(window_spec)) \
# MAGIC                 .withColumn("crecimiento", 
# MAGIC                     (col("ventas") - lag("ventas", 1).over(window_spec)) / lag("ventas", 1).over(window_spec) * 100)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📈 Running Totals y Promedios Móviles
# MAGIC
# MAGIC ```python
# MAGIC # Running total (acumulado)
# MAGIC window_running = Window.partitionBy("sucursal_id").orderBy("fecha").rowsBetween(Window.unboundedPreceding, Window.currentRow)
# MAGIC df = df.withColumn("running_total", spark_sum("ventas").over(window_running))
# MAGIC
# MAGIC # Promedio móvil (últimos 3 meses)
# MAGIC window_rolling = Window.partitionBy("sucursal_id").orderBy("fecha").rowsBetween(-2, Window.currentRow)
# MAGIC df = df.withColumn("promedio_movil_3m", avg("ventas").over(window_rolling))
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Window Functions son el poder oculto de SQL:**
# MAGIC * 📊 Top N por grupo (mejores vendedores por región)
# MAGIC * 📈 Crecimiento interanual (comparar con período anterior)
# MAGIC * 📉 Promedios móviles (suavizado de series temporales)
# MAGIC * 🏆 Rankings dinámicos (leaderboards)
# MAGIC * 📦 Acumulados (running totals para dashboards)

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number, rank, lag, lead, sum as spark_sum, avg, round as spark_round
import warnings
warnings.filterwarnings('ignore')

print("💻 EJERCICIOS: WINDOW FUNCTIONS")
print("="*70)

if USAR_DATOS_REALES:
    # Ejercicio 1: Ranking de ventas por sucursal
    print("\n1️⃣ Top 3 ventas por sucursal (ROW_NUMBER):")
    window_rank = Window.partitionBy("sucursal_id").orderBy(col("ventas").desc())
    df_ranked = df_spark.withColumn("ranking", row_number().over(window_rank))
    df_ranked.filter(col("ranking") <= 3).select("sucursal_id", "fecha", "ventas", "ranking").orderBy("sucursal_id", "ranking").show()

    # Ejercicio 2: Crecimiento mes a mes (LAG)
    print("\n2️⃣ Crecimiento mes a mes por sucursal (LAG):")
    window_lag = Window.partitionBy("sucursal_id").orderBy("fecha")
    df_growth = df_spark.withColumn("venta_anterior", lag("ventas", 1).over(window_lag)) \
        .withColumn("crecimiento_pct", spark_round((col("ventas") - col("venta_anterior")) / col("venta_anterior") * 100, 2))
    df_growth.select("sucursal_id", "fecha", "ventas", "venta_anterior", "crecimiento_pct").orderBy("sucursal_id", "fecha").show(10)

    # Ejercicio 3: Running total por sucursal
    print("\n3️⃣ Running total (acumulado) por sucursal:")
    window_running = Window.partitionBy("sucursal_id").orderBy("fecha").rowsBetween(Window.unboundedPreceding, Window.currentRow)
    df_running = df_spark.withColumn("acumulado", spark_sum("ventas").over(window_running))
    df_running.select("sucursal_id", "fecha", "ventas", spark_round("acumulado", 2).alias("acumulado")).orderBy("sucursal_id", "fecha").show(10)

    # Ejercicio 4: Promedio móvil 3 meses
    print("\n4️⃣ Promedio móvil (3 meses):")
    window_rolling = Window.partitionBy("sucursal_id").orderBy("fecha").rowsBetween(-2, Window.currentRow)
    df_rolling = df_spark.withColumn("promedio_3m", spark_round(avg("ventas").over(window_rolling), 2))
    df_rolling.select("sucursal_id", "fecha", "ventas", "promedio_3m").orderBy("sucursal_id", "fecha").show(10)
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Window Functions completado")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 15_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Window Functions vs GROUP BY:**
# MAGIC    - GROUP BY colapsa filas (una fila por grupo)
# MAGIC    - Window Functions mantienen filas + agregan columna calculada
# MAGIC    - `SUM(ventas) OVER (PARTITION BY sucursal_id)` — sin colapsar
# MAGIC
# MAGIC 2. **ROW_NUMBER, RANK, DENSE_RANK:**
# MAGIC    - `ROW_NUMBER()` — siempre único (1, 2, 3, 4...)
# MAGIC    - `RANK()` — saltos en empates (1, 2, 2, 4...)
# MAGIC    - `DENSE_RANK()` — sin saltos (1, 2, 2, 3...)
# MAGIC    - Útiles para Top N por grupo y leaderboards
# MAGIC
# MAGIC 3. **LAG y LEAD — comparación temporal:**
# MAGIC    - `lag('ventas', 1).over(window)` — valor del período anterior
# MAGIC    - `lead('ventas', 1).over(window)` — valor del período siguiente
# MAGIC    - Crecimiento %: `(ventas - lag(ventas)) / lag(ventas) * 100`
# MAGIC
# MAGIC 4. **Running totals y promedios móviles:**
# MAGIC    - `rowsBetween(Window.unboundedPreceding, Window.currentRow)` — acumulado
# MAGIC    - `rowsBetween(-2, Window.currentRow)` — últimos 3 períodos
# MAGIC    - Ideal para dashboards de KPIs acumulados y suavizado de series
# MAGIC
# MAGIC 5. **PARTITION BY y ORDER BY:**
# MAGIC    - `PARTITION BY` define el grupo (equivalente a GROUP BY pero sin colapsar)
# MAGIC    - `ORDER BY` define el orden dentro de cada partición
# MAGIC    - Combinar ambos = análisis por grupo ordenado temporalmente
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: ORDER BY define el orden, PARTITION BY define el grupo**
# MAGIC ```python
# MAGIC # MALO: sin ORDER BY, LAG/RANK no tienen orden definido
# MAGIC window = Window.partitionBy("sucursal_id")
# MAGIC df.withColumn("ranking", row_number().over(window))  # orden aleatorio
# MAGIC
# MAGIC # BUENO: ORDER BY define el criterio de ranking
# MAGIC window = Window.partitionBy("sucursal_id").orderBy(col("ventas").desc())
# MAGIC df.withColumn("ranking", row_number().over(window))  # top ventas primero
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: rowsBetween para ventanas deslizantes**
# MAGIC ```python
# MAGIC # MALO: sin rowsBetween, la ventana incluye TODAS las filas
# MAGIC window = Window.partitionBy("sucursal_id").orderBy("fecha")
# MAGIC df.withColumn("promedio", avg("ventas").over(window))  # promedio de TODO
# MAGIC
# MAGIC # BUENO: definir el rango de la ventana
# MAGIC # Acumulado: desde el inicio hasta la fila actual
# MAGIC window_running = Window.partitionBy("sucursal_id").orderBy("fecha")\
# MAGIC     .rowsBetween(Window.unboundedPreceding, Window.currentRow)
# MAGIC # Móvil: últimos 3 meses
# MAGIC window_rolling = Window.partitionBy("sucursal_id").orderBy("fecha")\
# MAGIC     .rowsBetween(-2, Window.currentRow)
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: LAG necesita ORDER BY por fecha**
# MAGIC ```python
# MAGIC # MALO: sin ORDER BY temporal, LAG toma filas en orden aleatorio
# MAGIC window = Window.partitionBy("sucursal_id")
# MAGIC df.withColumn("anterior", lag("ventas", 1).over(window))  # ⚠️ orden indefinido
# MAGIC
# MAGIC # BUENO: ORDER BY fecha garantiza período anterior correcto
# MAGIC window = Window.partitionBy("sucursal_id").orderBy("fecha")
# MAGIC df.withColumn("anterior", lag("ventas", 1).over(window))  # ✅ mes anterior
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Top N por grupo | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC)` + `WHERE ranking <= N` |
# MAGIC | Ranking con empates | `RANK()` (saltos) o `DENSE_RANK()` (sin saltos) |
# MAGIC | Valor del período anterior | `lag('col', 1).over(Window.partitionBy(g).orderBy('fecha'))` |
# MAGIC | Valor del período siguiente | `lead('col', 1).over(Window.partitionBy(g).orderBy('fecha'))` |
# MAGIC | Crecimiento % | `(col - lag(col)) / lag(col) * 100` |
# MAGIC | Acumulado (running total) | `sum('col').over(window.rowsBetween(unboundedPreceding, currentRow))` |
# MAGIC | Promedio móvil N períodos | `avg('col').over(window.rowsBetween(-(N-1), currentRow))` |
# MAGIC | Total por grupo sin colapsar | `sum('col').over(Window.partitionBy('grupo'))` |
# MAGIC | Sin PARTITION BY | Ventana global (todas las filas) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🪟 ¡Window Functions distribuidas dominadas!</h3>
# MAGIC   <p><i>"Window Functions: el poder de GROUP BY sin perder filas. Análisis avanzado sin colapsar datos."</i></p>
# MAGIC </div>