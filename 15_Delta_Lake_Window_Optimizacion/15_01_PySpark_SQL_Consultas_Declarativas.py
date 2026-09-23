# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 15 - Notebook 01: PySpark SQL y consultas declarativas
# MAGIC
# MAGIC ## 🗄️ SQL distribuido con Apache Spark
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
# MAGIC ✅ **Ejecutar** consultas SQL distribuidas con spark.sql()  
# MAGIC ✅ **Comparar** Spark SQL vs DataFrame API  
# MAGIC ✅ **Crear** tablas temporales y vistas en Spark  
# MAGIC ✅ **Aplicar** consultas complejas sobre datos distribuidos  
# MAGIC ✅ **Optimizar** consultas SQL en cluster
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Módulos 12-14 completados (PySpark Core, Transformación, SQL Editor)
# MAGIC * ✅ Conocimiento de SQL tradicional
# MAGIC * ✅ Familiaridad con Spark DataFrames
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **PySpark SQL** - spark.sql() y consultas declarativas
# MAGIC 2. **Tablas temporales** - createOrReplaceTempView
# MAGIC 3. **Spark SQL vs DataFrame API** - Cuándo usar cada uno
# MAGIC 4. **Consultas complejas** - Subconsultas, CTEs en Spark
# MAGIC 5. **Caso integrador** - Análisis de ventas distribuido

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
from pyspark.sql import SparkSession

print("💾 CARGANDO DATOS PARA PYSPARK SQL")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df_spark = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Tabla cargada desde Unity Catalog: {df_spark.count()} registros")
    df_spark.createOrReplaceTempView("ventas")
    print("   Vista temporal 'ventas' creada")
    print(f"   Columnas: {df_spark.columns}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: PySpark SQL
# MAGIC %md
# MAGIC ## 📚 Teoría: PySpark SQL y Consultas Declarativas
# MAGIC
# MAGIC ### 🗄️ Spark SQL: SQL sobre Big Data
# MAGIC
# MAGIC **Spark SQL** permite ejecutar consultas SQL estándar sobre datos distribuidos en un cluster Spark.
# MAGIC
# MAGIC ```python
# MAGIC # Registrar DataFrame como vista temporal
# MAGIC df.createOrReplaceTempView("ventas")
# MAGIC
# MAGIC # Ejecutar SQL distribuido
# MAGIC resultado = spark.sql("""
# MAGIC     SELECT sucursal_id, SUM(ventas) as total
# MAGIC     FROM ventas
# MAGIC     GROUP BY sucursal_id
# MAGIC     ORDER BY total DESC
# MAGIC """)
# MAGIC resultado.show()
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Spark SQL vs DataFrame API
# MAGIC
# MAGIC | Aspecto | DataFrame API | Spark SQL |
# MAGIC |---------|-------------|-----------|
# MAGIC | Sintaxis | `df.filter(col("x") > 5)` | `WHERE x > 5` |
# MAGIC | Lectibilidad | Encadenado de métodos | SQL estándar |
# MAGIC | Optimización | Catalyst optimiza igual | Catalyst optimiza igual |
# MAGIC | Flexibilidad | Más programático | Más declarativo |
# MAGIC | Quién usa | Data Engineers | Analistas SQL |
# MAGIC
# MAGIC **Ambos generan el mismo plan de ejecución** - Catalyst optimiza ambos igual.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Funciones SQL en Spark
# MAGIC
# MAGIC ```sql
# MAGIC -- Funciones de agregación
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS registros,
# MAGIC   SUM(ventas) AS total_ventas,
# MAGIC   ROUND(AVG(ventas), 2) AS promedio,
# MAGIC   MIN(ventas) AS minimo,
# MAGIC   MAX(ventas) AS maximo
# MAGIC FROM ventas
# MAGIC GROUP BY sucursal_id
# MAGIC ORDER BY total_ventas DESC;
# MAGIC
# MAGIC -- Funciones de fecha
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   MONTH(fecha) AS mes,
# MAGIC   SUM(ventas) AS ventas
# MAGIC FROM ventas
# MAGIC GROUP BY YEAR(fecha), MONTH(fecha)
# MAGIC ORDER BY anio, mes;
# MAGIC
# MAGIC -- CASE WHEN
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   ventas,
# MAGIC   CASE 
# MAGIC     WHEN ventas > 80000 THEN 'Alto'
# MAGIC     WHEN ventas > 50000 THEN 'Medio'
# MAGIC     ELSE 'Bajo'
# MAGIC   END AS nivel
# MAGIC FROM ventas;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Spark SQL democratiza Big Data:**
# MAGIC * 📊 Analistas SQL pueden trabajar con TB de datos
# MAGIC * 🔗 Integración con BI tools (Tableau, Power BI)
# MAGIC * 🏢 Estándar: mismo SQL que en Databricks SQL Editor
# MAGIC * 🚀 Performance: Catalyst optimiza automáticamente

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, year, month, round as spark_round
import warnings
warnings.filterwarnings('ignore')

print("💻 EJERCICIOS: PYSPARK SQL DISTRIBUIDO")
print("="*70)

if USAR_DATOS_REALES:
    # Ejercicio 1: Consulta SQL directa
    print("\n1️⃣ Top 5 sucursales por ventas totales:")
    spark.sql("""
        SELECT sucursal_id, 
               COUNT(*) as meses,
               ROUND(SUM(ventas), 2) as ventas_totales,
               ROUND(AVG(ventas), 2) as promedio
        FROM ventas
        GROUP BY sucursal_id
        ORDER BY ventas_totales DESC
        LIMIT 5
    """).show()

    # Ejercicio 2: Análisis temporal con SQL
    print("\n2️⃣ Ventas por año:")
    spark.sql("""
        SELECT YEAR(fecha) as anio, 
               COUNT(*) as meses,
               ROUND(SUM(ventas), 2) as total_anual,
               ROUND(AVG(ventas), 2) as promedio_mensual
        FROM ventas
        GROUP BY YEAR(fecha)
        ORDER BY anio
    """).show()

    # Ejercicio 3: CTE en Spark SQL
    print("\n3️⃣ CTE para ranking:")
    spark.sql("""
        WITH ranking_ventas AS (
            SELECT sucursal_id, fecha, ventas,
                   RANK() OVER (PARTITION BY sucursal_id ORDER BY ventas DESC) as ranking
            FROM ventas
        )
        SELECT sucursal_id, fecha, ventas, ranking
        FROM ranking_ventas
        WHERE ranking <= 3
        ORDER BY sucursal_id, ranking
    """).show()
else:
    print("⚠️  No hay datos reales disponibles. Ejecuta 02_05_Preparacion_Datos_Empresariales.ipynb")

print("\n" + "="*70)
print("✅ PySpark SQL completado")

# COMMAND ----------

# DBTITLE 1,⚡ Teoría: Spark SQL con datos reales
# MAGIC %md
# MAGIC ## ⚡ Spark SQL aplicado a Los Andes Market
# MAGIC
# MAGIC ### 📊 De DataFrame API a SQL distribuido
# MAGIC
# MAGIC Ya sabemos usar la DataFrame API de PySpark. Ahora podemos ejecutar las mismas consultas en SQL distribuido sobre `ventas_mensuales_mendoza_h3`:
# MAGIC
# MAGIC ```python
# MAGIC df_spark.createOrReplaceTempView("ventas")
# MAGIC resultado = spark.sql("""
# MAGIC   SELECT zona, SUM(ventas) as total FROM ventas GROUP BY zona
# MAGIC """)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio con spark.sql()
# MAGIC * ¿Qué zona genera más ventas?
# MAGIC * ¿Qué sucursal tiene el mejor promedio mensual?
# MAGIC * ¿Hay estacionalidad por mes del año?
# MAGIC * ¿Cuáles son los meses outliers por sucursal?

# COMMAND ----------

# DBTITLE 1,⚡ Práctica: Spark SQL con datos reales
from pyspark.sql.functions import col

print("⚡ SPARK SQL APLICADO A LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and 'df_spark' in dir():
    df_spark.createOrReplaceTempView("ventas")

    print("\n1️⃣  KPIs POR ZONA (spark.sql)")
    print("-"*70)
    spark.sql("""
        SELECT zona,
               COUNT(*) AS registros,
               COUNT(DISTINCT sucursal_id) AS sucursales,
               ROUND(SUM(ventas), 0) AS ventas_totales,
               ROUND(AVG(ventas), 0) AS ventas_promedio,
               ROUND(MAX(ventas), 0) AS venta_max,
               ROUND(MIN(ventas), 0) AS venta_min
        FROM ventas
        GROUP BY zona
        ORDER BY ventas_totales DESC
    """).show(truncate=30)

    print("\n" + "="*70)
    print("\n2️⃣  ESTACIONALIDAD: Ventas por mes del año")
    print("-"*70)
    spark.sql("""
        SELECT MONTH(fecha) AS mes,
               COUNT(*) AS registros,
               ROUND(SUM(ventas), 0) AS ventas_mes,
               ROUND(AVG(ventas), 0) AS promedio_sucursal
        FROM ventas
        GROUP BY MONTH(fecha)
        ORDER BY mes
    """).show()

    print("\n" + "="*70)
    print("\n3️⃣  CASE WHEN + CTE: Clasificación y outliers")
    print("-"*70)
    spark.sql("""
        WITH stats_sucursal AS (
            SELECT sucursal_nombre, zona,
                   AVG(ventas) AS promedio,
                   STDDEV(ventas) AS desviacion
            FROM ventas
            GROUP BY sucursal_nombre, zona
        )
        SELECT v.sucursal_nombre, v.zona, v.fecha,
               ROUND(v.ventas, 0) AS ventas,
               ROUND(s.promedio, 0) AS promedio,
               ROUND((v.ventas - s.promedio) / s.desviacion, 2) AS z_score,
               CASE 
                   WHEN ABS((v.ventas - s.promedio) / s.desviacion) > 2 THEN 'Outlier'
                   WHEN ABS((v.ventas - s.promedio) / s.desviacion) > 1 THEN 'Atípico'
                   ELSE 'Normal'
               END AS categoria
        FROM ventas v
        JOIN stats_sucursal s ON v.sucursal_nombre = s.sucursal_nombre
        ORDER BY ABS((v.ventas - s.promedio) / s.desviacion) DESC
        LIMIT 15
    """).show(truncate=25)

    print("\n" + "="*70)
    print("\n4️⃣  SQL vs DATAFRAME API: Misma consulta, dos sintaxis")
    print("-"*70)

    import time
    # SQL
    start = time.time()
    result_sql = spark.sql("""
        SELECT sucursal_id, ROUND(AVG(ventas), 0) AS promedio
        FROM ventas WHERE ventas > 50000
        GROUP BY sucursal_id ORDER BY promedio DESC LIMIT 5
    """)
    result_sql.show()
    t_sql = time.time() - start

    # DataFrame API
    start = time.time()
    (df_spark.filter(col("ventas") > 50000)
        .groupBy("sucursal_id")
        .agg({"ventas": "avg"})
        .orderBy(col("avg(ventas)").desc())
        .limit(5)).show()
    t_df = time.time() - start

    print(f"\n   ⏱️  Spark SQL: {t_sql:.3f}s")
    print(f"   ⏱️  DataFrame API: {t_df:.3f}s")
    print("   💡 Catalyst optimiza ambos igual — elegir por legibilidad del equipo")

    print("\n" + "="*70)
    print("\n5️⃣  EXPLAIN: Ver plan de ejecución SQL")
    print("-"*70)
    result_sql.explain()
    print("\n   💡 Buscar 'PushedFilters' = filter pushdown por Catalyst")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 15_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **spark.sql() — SQL distribuido en Spark:**
# MAGIC    - `spark.sql("SELECT ... FROM tabla")` ejecuta SQL sobre datos distribuidos
# MAGIC    - El resultado es un DataFrame de Spark (no Pandas)
# MAGIC    - Catalyst Optimizer genera el mismo plan que la DataFrame API
# MAGIC
# MAGIC 2. **Vistas temporales (createOrReplaceTempView):**
# MAGIC    - `df.createOrReplaceTempView("ventas")` registra un DataFrame como tabla SQL
# MAGIC    - La vista existe solo en la sesión actual (no persiste)
# MAGIC    - Permite mezclar DataFrame API y SQL en el mismo pipeline
# MAGIC
# MAGIC 3. **Spark SQL vs DataFrame API:**
# MAGIC    - DataFrame API: encadenado de métodos, más programático (`df.filter(col("x") > 5)`)
# MAGIC    - Spark SQL: sintaxis SQL estándar, más declarativo (`WHERE x > 5`)
# MAGIC    - Ambos generan el mismo plan de ejecución (Catalyst)
# MAGIC    - Data Engineers → DataFrame API, Analistas SQL → Spark SQL
# MAGIC
# MAGIC 4. **Consultas complejas en Spark SQL:**
# MAGIC    - CTEs: `WITH nombre AS (SELECT ...) SELECT ... FROM nombre`
# MAGIC    - Subconsultas en WHERE, SELECT y FROM
# MAGIC    - Window functions: `RANK() OVER (PARTITION BY ... ORDER BY ...)`
# MAGIC    - CASE WHEN, GROUP BY, HAVING, JOINs — todo el SQL estándar disponible
# MAGIC
# MAGIC 5. **Caso integrador:**
# MAGIC    - Top 5 sucursales por ventas totales con `spark.sql()`
# MAGIC    - Análisis temporal con `YEAR()`, `MONTH()`, `GROUP BY`
# MAGIC    - Ranking con CTE + `RANK() OVER (PARTITION BY ...)`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: createOrReplaceTempView antes de spark.sql()**
# MAGIC ```python
# MAGIC # MALO: spark.sql() sin vista registrada
# MAGIC resultado = spark.sql("SELECT * FROM ventas")  # 💥 Table not found
# MAGIC
# MAGIC # BUENO: registrar vista primero
# MAGIC df.createOrReplaceTempView("ventas")
# MAGIC resultado = spark.sql("SELECT * FROM ventas")  # ✅
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Elegir DataFrame API o SQL según audiencia**
# MAGIC ```python
# MAGIC # Equipo de Data Engineers → DataFrame API (programático, tipado)
# MAGIC df.filter(col("ventas") > 50000).groupBy("sucursal").sum("ventas")
# MAGIC
# MAGIC # Equipo de Analistas SQL → Spark SQL (declarativo, familiar)
# MAGIC spark.sql("""
# MAGIC   SELECT sucursal, SUM(ventas) FROM ventas
# MAGIC   WHERE ventas > 50000 GROUP BY sucursal
# MAGIC """)
# MAGIC # Ambos generan el mismo plan en Catalyst
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: show() para debug, display() para visualización**
# MAGIC ```python
# MAGIC # MALO: collect() trae todo al driver
# MAGIC spark.sql("SELECT * FROM ventas").collect()  # 💥 si la tabla es grande
# MAGIC
# MAGIC # BUENO: show() para debug rápido
# MAGIC spark.sql("SELECT * FROM ventas LIMIT 10").show()
# MAGIC # display() para visualización interactiva en Databricks
# MAGIC display(spark.sql("SELECT sucursal, SUM(ventas) FROM ventas GROUP BY sucursal"))
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Registrar DataFrame como tabla SQL | `df.createOrReplaceTempView("nombre")` |
# MAGIC | Ejecutar SQL distribuido | `spark.sql("SELECT ... FROM nombre")` |
# MAGIC | Consulta simple de exploración | `spark.sql("SELECT * FROM tabla LIMIT 10").show()` |
# MAGIC | Agregación por grupo | `spark.sql("SELECT col, SUM(val) FROM t GROUP BY col")` |
# MAGIC | Ranking con CTE | `WITH r AS (SELECT ..., RANK() OVER ...) SELECT ... FROM r` |
# MAGIC | Pipeline mixto API + SQL | `df.filter(...).createOrReplaceTempView("v")` + `spark.sql(...)` |
# MAGIC | Debug rápido | `.show()` o `.show(10)` |
# MAGIC | Visualización en Databricks | `display(spark.sql(...))` |
# MAGIC | Equipo de Data Engineers | DataFrame API (programático) |
# MAGIC | Equipo de Analistas SQL | Spark SQL (declarativo) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🗄️ ¡PySpark SQL y consultas declarativas dominados!</h3>
# MAGIC   <p><i>"Spark SQL democratiza Big Data: los analistas SQL pueden procesar TB sin aprender la DataFrame API."</i></p>
# MAGIC </div>