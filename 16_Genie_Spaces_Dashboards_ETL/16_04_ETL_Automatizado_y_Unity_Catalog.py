# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🏗️ Módulo 16 - Notebook 04: ETL Automatizado y Unity Catalog
# MAGIC
# MAGIC ## 🔄 Automatización de Pipelines y Gobernanza de Datos
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
# MAGIC ✅ **Automatizar** pipelines con Databricks Jobs  
# MAGIC ✅ **Configurar** catálogos y schemas en Unity Catalog  
# MAGIC ✅ **Aplicar** gobernanza de datos  
# MAGIC ✅ **Programar** ejecuciones recurrentes  
# MAGIC ✅ **Monitorear** pipelines automatizados  
# MAGIC ✅ **Integrar** Genie Code en ETL productivos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 14-15 completados (SQL Editor, Delta Lake)
# MAGIC * ✅ Notebook 16_03 (Genie Code avanzado)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Unity Catalog** - Arquitectura de gobernanza
# MAGIC 2. **Databricks Jobs** - Automatización de notebooks
# MAGIC 3. **Programación** - Cron y triggers
# MAGIC 4. **Monitoreo** - Alertas y notificaciones
# MAGIC 5. **Pipeline productivo** - Caso integrador completo

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd

print("💾 SETUP: ETL AUTOMATIZADO")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

# Verificar estructura de Unity Catalog
print("\n📂 Estructura de Unity Catalog:")
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    spark.sql(f"USE SCHEMA {SCHEMA}")
    print(f"   Catálogo: {CATALOG}")
    print(f"   Schema: {SCHEMA}")
    tables = spark.sql(f"SHOW TABLES IN {CATALOG}.{SCHEMA}").collect()
    for t in tables:
        print(f"   Tabla: {t['tableName']}")
except Exception as e:
    print(f"   Error: {e}")

print("\n📌 Para automatizar con Jobs:")
print("   1. Crea un notebook con el pipeline ETL")
print("   2. Ve a Databricks > Jobs > Create Job")
print("   3. Selecciona el notebook")
print("   4. Configura el schedule (cron)")
print("   5. Agrega alertas si falla")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: ETL y Unity Catalog
# MAGIC %md
# MAGIC ## 📚 Teoría: ETL Automatizado y Unity Catalog
# MAGIC
# MAGIC ### 🗄️ Unity Catalog: Gobernanza Completa
# MAGIC
# MAGIC ```
# MAGIC Metastore (Cuenta Databricks)
# MAGIC └── Catálogo: pandito_ds
# MAGIC     └── Schema: default
# MAGIC         ├── Tabla: ventas_mensuales_mendoza_h3
# MAGIC         ├── Tabla: ventas_procesadas
# MAGIC         └── Vista: vw_kpis_sucursal
# MAGIC     └── Schema: staging (futuro)
# MAGIC         └── Tabla: raw_ventas
# MAGIC ```
# MAGIC
# MAGIC **Niveles de permisos:**
# MAGIC * `USE CATALOG`: Acceso al catálogo
# MAGIC * `USE SCHEMA`: Acceso al schema
# MAGIC * `SELECT`: Leer tablas
# MAGIC * `MODIFY`: Modificar datos
# MAGIC * `CREATE`: Crear tablas/vistas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⏰ Databricks Jobs: Automatización
# MAGIC
# MAGIC **Jobs** ejecutan notebooks en horarios programados o por eventos.
# MAGIC
# MAGIC | Tipo de Trigger | Cuándo usar | Ejemplo |
# MAGIC |-----------------|------------|--------|
# MAGIC | **Cron** | Ejecución periódica | Diario a las 8 AM |
# MAGIC | **File arrival** | Cuando llega un archivo | Nuevo CSV en S3 |
# MAGIC | **Manual** | Bajo demanda | Ejecutar ahora |
# MAGIC
# MAGIC ```python
# MAGIC # Ejemplo de schedule cron
# MAGIC # Ejecutar todos los días a las 8 AM
# MAGIC "0 0 8 * * ?"  # Quartz cron
# MAGIC
# MAGIC # Ejecutar cada lunes a las 6 AM
# MAGIC "0 0 6 ? * MON"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔔 Monitoreo y Alertas
# MAGIC
# MAGIC ```python
# MAGIC # Configurar alertas en Jobs:
# MAGIC # 1. Email notification si falla
# MAGIC # 2. Slack/webhook notification
# MAGIC # 3. Retry automático (hasta 3 intentos)
# MAGIC # 4. Timeout (ej: 2 horas máximo)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📦 Arquitectura de un Pipeline Productivo
# MAGIC
# MAGIC ```
# MAGIC ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
# MAGIC │  RAW (Bronze)│ →  │ CLEAN (Silver)│ →  │  GOLD (BI)   │
# MAGIC │              │    │              │    │              │
# MAGIC | Datos crudos │    | Limpieza     │    | Agregados    │
# MAGIC | Sin validar  │    | Validados    │    | Dashboard    │
# MAGIC | CSV/JSON     │    | Delta Lake   │    | Delta Lake   │
# MAGIC └──────────────┘    └──────────────┘    └──────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **ETL automatizado = datos confiables siempre:**
# MAGIC * ⏰ Ejecución sin intervención humana
# MAGIC * 📊 Datos frescos cada mañana
# MAGIC * 🔔 Alertas si algo falla
# MAGIC * 📦 Arquitectura Bronze/Silver/Gold
# MAGIC * 🏢 Producción real en empresas

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, year, month, sum as spark_sum, round as spark_round, when, count, isnull
import warnings
warnings.filterwarnings('ignore')

print("💻 PIPELINE ETL PRODUCTIVO COMPLETO")
print("="*70)

# === EXTRACT ===
print("\n1️⃣ EXTRACT: Leyendo de Unity Catalog")
try:
    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
    print(f"   Registros: {df_raw.count()}")
except Exception as e:
    print(f"   Error: {e}")
    raise SystemExit

# === TRANSFORM ===
print("\n2️⃣ TRANSFORM: Limpieza y enriquecimiento")
df_clean = df_raw.dropDuplicates() \
    .na.drop(subset=["ventas", "fecha"]) \
    .withColumn("anio", year("fecha")) \
    .withColumn("mes", month("fecha")) \
    .withColumn("nivel_ventas", 
        when(col("ventas") > 80000, "Alto")
        .when(col("ventas") > 50000, "Medio")
        .otherwise("Bajo"))
print(f"   Registros limpios: {df_clean.count()}")
print(f"   Columnas: {df_clean.columns}")

# === LOAD ===
print("\n3️⃣ LOAD: Escribiendo a tabla Delta")
spark.sql("CREATE SCHEMA IF NOT EXISTS pandito_ds.staging")
df_clean.write.format("delta").mode("overwrite") \
    .saveAsTable("pandito_ds.staging.ventas_silver")
print("   Tabla: pandito_ds.staging.ventas_silver")

# === GOLD (agregados para BI) ===
print("\n4️⃣ GOLD: Agregados para dashboards")
df_gold = df_clean.groupBy("sucursal_id", "anio") \
    .agg(
        spark_sum("ventas").alias("ventas_anuales"),
        spark_round(spark_sum("ventas") / 12, 2).alias("promedio_mensual"),
        count("*").alias("meses_con_datos")
    )
df_gold.write.format("delta").mode("overwrite") \
    .saveAsTable("pandito_ds.default.ventas_gold_anual")
print("   Tabla: pandito_ds.default.ventas_gold_anual")

# === VERIFICACIÓN ===
print("\n5️⃣ VERIFICACIÓN:")
df_check = spark.table("pandito_ds.default.ventas_gold_anual")
print(f"   Registros en Gold: {df_check.count()}")
df_check.orderBy("sucursal_id", "anio").show()

# Limpiar tablas de prueba
spark.sql("DROP TABLE IF EXISTS pandito_ds.staging.ventas_silver")
spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_gold_anual")

print("\n" + "="*70)
print("✅ Pipeline ETL productivo completado")
print("   📌 Para automatizar: crear Job con este notebook")
print("   📌 Schedule: diario a las 8 AM con cron '0 0 8 * * ?'")

# COMMAND ----------

# DBTITLE 1,🏗️ Teoría: ETL automatizado con datos reales
# MAGIC %md
# MAGIC ## 🏗️ ETL Automatizado para Los Andes Market
# MAGIC
# MAGIC ### 📦 Arquitectura Bronze/Silver/Gold
# MAGIC
# MAGIC Un pipeline productivo de **Los Andes Market** sigue la arquitectura medallion:
# MAGIC
# MAGIC ```
# MAGIC BRONZE (raw)          SILVER (clean)         GOLD (BI)
# MAGIC ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
# MAGIC │ ventas_raw   │ →    │ ventas_clean │ →    │ ventas_kpis  │
# MAGIC │ Sin validar  │      │ Limpia+valid│      │ Agregados   │
# MAGIC │ Delta Lake   │      │ Delta Lake   │      │ Delta Lake  │
# MAGIC └──────────────┘      └──────────────┘      └──────────────┘
# MAGIC ```
# MAGIC
# MAGIC ```python
# MAGIC # Bronze: datos crudos de ventas
# MAGIC df_raw.write.format("delta").saveAsTable("pandito_ds.staging.ventas_bronze")
# MAGIC
# MAGIC # Silver: limpios + enriquecidos
# MAGIC (df_raw.dropDuplicates().na.drop(...)
# MAGIC     .write.format("delta").saveAsTable("pandito_ds.staging.ventas_silver"))
# MAGIC
# MAGIC # Gold: agregados para dashboards
# MAGIC (df_silver.groupBy("zona", "anio").agg(sum("ventas"))
# MAGIC     .write.format("delta").saveAsTable("pandito_ds.default.ventas_gold"))
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Automatización con Databricks Jobs
# MAGIC * **Trigger:** Cron diario a las 8 AM (`0 0 8 * * ?`)
# MAGIC * **Notebook:** El notebook con el pipeline ETL
# MAGIC * **Alertas:** Email si falla + retry 3 veces
# MAGIC * **Monitoreo:** Spark UI + Job runs history

# COMMAND ----------

# DBTITLE 1,🏗️ Práctica: Pipeline Bronze/Silver/Gold
from pyspark.sql.functions import col, year, month, sum as spark_sum, avg, count, round as spark_round, when, isnull

print("🏗️ PIPELINE BRONZE/SILVER/GOLD PARA LOS ANDES MARKET")
print("="*70)

print("\n1️⃣  BRONZE: Datos crudos desde Unity Catalog")
print("-"*70)
df_bronze = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
n_bronze = df_bronze.count()
print(f"   Registros crudos: {n_bronze:,}")
print(f"   Columnas: {len(df_bronze.columns)}")

print("\n" + "="*70)
print("\n2️⃣  SILVER: Limpieza + enriquecimiento")
print("-"*70)
df_silver = (df_bronze
    .dropDuplicates()
    .na.drop(subset=["ventas", "fecha", "sucursal_id"])
    .filter(col("ventas") > 0)
    .withColumn("anio", year("fecha"))
    .withColumn("mes", month("fecha"))
    .withColumn("trimestre", when(month("fecha") <= 3, "Q1")
        .when(month("fecha") <= 6, "Q2")
        .when(month("fecha") <= 9, "Q3")
        .otherwise("Q4"))
    .withColumn("categoria_venta",
        when(col("ventas") > 100000, "Alto")
        .when(col("ventas") > 50000, "Medio")
        .otherwise("Bajo")))
n_silver = df_silver.count()
print(f"   Registros limpios: {n_silver:,}")
print(f"   Columnas nuevas: anio, mes, trimestre, categoria_venta")

# Guardar Silver
spark.sql("CREATE SCHEMA IF NOT EXISTS pandito_ds.staging")
df_silver.write.format("delta").mode("overwrite")\
    .saveAsTable("pandito_ds.staging.ventas_silver_los_andes")
print("   Tabla Delta: pandito_ds.staging.ventas_silver_los_andes")

print("\n" + "="*70)
print("\n3️⃣  GOLD: Agregados para dashboards BI")
print("-"*70)

# Gold 1: KPIs anuales por sucursal
df_gold_sucursal = (df_silver.groupBy("sucursal_id", "sucursal_nombre", "zona", "anio")
    .agg(
        spark_sum("ventas").alias("ventas_anuales"),
        spark_round(avg("ventas"), 0).alias("promedio_mensual"),
        count("*").alias("meses_con_datos")))
    .orderBy("sucursal_id", "anio"))

df_gold_sucursal.write.format("delta").mode("overwrite")\
    .saveAsTable("pandito_ds.default.ventas_gold_sucursal_anual")
print("   Gold 1: ventas_gold_sucursal_anual")
df_gold_sucursal.show(10, truncate=25)

# Gold 2: KPIs por zona y trimestre
df_gold_zona = (df_silver.groupBy("zona", "anio", "trimestre")
    .agg(
        spark_sum("ventas").alias("ventas_trimestrales"),
        count("*").alias("registros"))
    .orderBy("zona", "anio", "trimestre"))

df_gold_zona.write.format("delta").mode("overwrite")\
    .saveAsTable("pandito_ds.default.ventas_gold_zona_trimestral")
print("\n   Gold 2: ventas_gold_zona_trimestral")
df_gold_zona.show(10, truncate=25)

print("\n" + "="*70)
print("\n4️⃣  VERIFICACIÓN: Control de calidad")
print("-"*70)

df_check = spark.table("pandito_ds.staging.ventas_silver_los_andes")
total = df_check.count()
print(f"   Total registros Silver: {total:,}")

nulos = df_check.filter(col("ventas").isNull() | col("fecha").isNull()).count()
print(f"   Nulos en columnas críticas: {nulos}")

negativos = df_check.filter(col("ventas") <= 0).count()
print(f"   Ventas <= 0: {negativos}")

print("\n   Distribución por categoría:")
df_check.groupBy("categoria_venta").agg(
    count("*").alias("registros"),
    spark_round(spark_sum("ventas"), 0).alias("ventas_total")
).orderBy("categoria_venta").show()

print("\n   ✅ Pipeline Bronze/Silver/Gold completado")
print("\n" + "="*70)
print("\n📌 PARA AUTOMATIZAR CON DATABRICKS JOBS:")
print("   1. Ve a Databricks > Jobs > Create Job")
print("   2. Selecciona este notebook")
print("   3. Schedule: Cron diario '0 0 8 * * ?' (8 AM)")
print("   4. Alertas: Email si falla + 3 retries")
print("   5. El pipeline correrá automáticamente cada día")

# Limpieza
spark.sql("DROP TABLE IF EXISTS pandito_ds.staging.ventas_silver_los_andes")
spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_gold_sucursal_anual")
spark.sql("DROP TABLE IF EXISTS pandito_ds.default.ventas_gold_zona_trimestral")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 16_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Unity Catalog — gobernanza completa:**
# MAGIC    ```sql
# MAGIC    -- Jerarquia: Metastore > Catalogo > Schema > Tabla
# MAGIC    SHOW CATALOGS;
# MAGIC    SHOW SCHEMAS IN pandito_ds;
# MAGIC    SHOW TABLES IN pandito_ds.default;
# MAGIC    DESCRIBE TABLE pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC    ```
# MAGIC
# MAGIC 2. **Databricks Jobs — automatizacion de notebooks:**
# MAGIC    ```python
# MAGIC    # Flujo: Notebook con pipeline ETL > Jobs > Create Job
# MAGIC    # Trigger: Cron (periodico), File arrival (evento), Manual
# MAGIC    # Cron diario a las 8 AM: "0 0 8 * * ?"
# MAGIC    # Cron cada lunes a las 6 AM: "0 0 6 ? * MON"
# MAGIC    ```
# MAGIC
# MAGIC 3. **Arquitectura Bronze/Silver/Gold:**
# MAGIC    ```python
# MAGIC    # Bronze (Raw): datos crudos sin validar
# MAGIC    df_raw.write.format("delta").saveAsTable("pandito_ds.staging.ventas_bronze")
# MAGIC    # Silver (Clean): limpios, validados, enriquecidos
# MAGIC    df_clean.write.format("delta").saveAsTable("pandito_ds.staging.ventas_silver")
# MAGIC    # Gold (BI): agregados para dashboards
# MAGIC    df_gold.write.format("delta").saveAsTable("pandito_ds.default.ventas_gold")
# MAGIC    ```
# MAGIC
# MAGIC 4. **Pipeline ETL productivo completo:**
# MAGIC    ```python
# MAGIC    # EXTRACT: leer de Unity Catalog
# MAGIC    df_raw = spark.table("pandito_ds.default.ventas_mensuales_mendoza_h3")
# MAGIC    # TRANSFORM: limpiar + enriquecer
# MAGIC    df_clean = (df_raw.dropDuplicates()
# MAGIC        .na.drop(subset=["ventas", "fecha"])
# MAGIC        .withColumn("anio", year("fecha"))
# MAGIC        .withColumn("nivel", when(col("ventas") > 80000, "Alto").otherwise("Bajo")))
# MAGIC    # LOAD: escribir a Delta
# MAGIC    df_clean.write.format("delta").mode("overwrite").saveAsTable("pandito_ds.staging.ventas_silver")
# MAGIC    # VERIFY: control de calidad
# MAGIC    assert spark.table("pandito_ds.staging.ventas_silver").count() > 0
# MAGIC    ```
# MAGIC
# MAGIC 5. **Monitoreo y alertas:**
# MAGIC    - Email notification si el Job falla
# MAGIC    - Retry automatico (hasta 3 intentos)
# MAGIC    - Timeout (ej: 2 horas maximo)
# MAGIC    - Slack/webhook para alertas en tiempo real
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de ETL Automatizado
# MAGIC
# MAGIC **Caso 1: Pipeline Bronze/Silver/Gold**
# MAGIC ```python
# MAGIC # Bronze
# MAGIC df_raw.write.format("delta").mode("overwrite").saveAsTable("pandito_ds.staging.bronze")
# MAGIC # Silver (limpieza)
# MAGIC df_clean = df_raw.dropDuplicates().na.drop(subset=["ventas"])
# MAGIC df_clean.write.format("delta").mode("overwrite").saveAsTable("pandito_ds.staging.silver")
# MAGIC # Gold (agregados para BI)
# MAGIC df_gold = df_clean.groupBy("sucursal_id", "anio").agg(sum("ventas").alias("total"))
# MAGIC df_gold.write.format("delta").mode("overwrite").saveAsTable("pandito_ds.default.gold")
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Programar Job con cron**
# MAGIC ```python
# MAGIC # Diario a las 8 AM
# MAGIC schedule = "0 0 8 * * ?"
# MAGIC # Cada lunes a las 6 AM
# MAGIC schedule = "0 0 6 ? * MON"
# MAGIC # Cada 15 minutos
# MAGIC schedule = "0 0/15 * * * ?"
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Control de calidad con assertions**
# MAGIC ```python
# MAGIC df_result = spark.table("pandito_ds.default.ventas_gold_anual")
# MAGIC assert df_result.count() > 0, "Sin datos en Gold"
# MAGIC assert df_result.filter(col("ventas_anuales").isNull()).count() == 0, "Nulos en ventas"
# MAGIC print("Control de calidad pasado")
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Permisos en Unity Catalog**
# MAGIC ```sql
# MAGIC GRANT USE CATALOG ON CATALOG pandito_ds TO `user@email.com`;
# MAGIC GRANT USE SCHEMA ON SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC GRANT SELECT ON TABLE pandito_ds.default.ventas_gold_anual TO `user@email.com`;
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Configurar alertas de Job**
# MAGIC ```python
# MAGIC # En Databricks Jobs UI:
# MAGIC # 1. Job > Edit > Notifications
# MAGIC # 2. Email on failure: data-team@company.com
# MAGIC # 3. Retry on failure: 3 intentos
# MAGIC # 4. Timeout: 2 horas
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 16
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **16_01 - Genie Spaces Consultas Conversacionales:** Lenguaje natural a SQL, democratizacion de datos
# MAGIC 2. **16_02 - Dashboards AI/BI Lakeview:** Dashboards nativos, widgets, filtros drag-and-drop
# MAGIC 3. **16_03 - Genie Code PySpark/SQL Avanzado:** Migracion Pandas a PySpark, ETL con IA, validacion
# MAGIC 4. **16_04 - ETL Automatizado y Unity Catalog:** Jobs, Bronze/Silver/Gold, gobernanza, monitoreo
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Crear Genie Spaces para consultas conversacionales
# MAGIC * ✅ Construir dashboards AI/BI con Lakeview
# MAGIC * ✅ Generar pipelines ETL con Genie Code
# MAGIC * ✅ Automatizar ejecuciones con Databricks Jobs
# MAGIC * ✅ Implementar arquitectura Bronze/Silver/Gold con gobernanza
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🏗️ ¡Módulo 16 Completado!</h3>
# MAGIC   <p><i>"Dominas Genie Spaces, Dashboards AI/BI y ETL Automatizado. Ahora puedes construir pipelines productivos con gobernanza de datos."</i></p>
# MAGIC </div>