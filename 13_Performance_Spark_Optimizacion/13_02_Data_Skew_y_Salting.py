# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 13 - Notebook 02: Data Skew y Salting
# MAGIC
# MAGIC ## ⚖️ Detección y mitigación de asimetría en Spark
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
# MAGIC ✅ **Detectar** data skew en particiones de Spark  
# MAGIC ✅ **Entender** cómo el skew mata el paralelismo  
# MAGIC ✅ **Aplicar** salting para mitigar skew extremo  
# MAGIC ✅ **Elegir** entre repartition, coalesce y salting  
# MAGIC ✅ **Diagnosticar** partitioning con Spark UI
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebook 13_01 completado (Caching y Memory Management)
# MAGIC * ✅ Entender particiones y paralelismo en Spark
# MAGIC * ✅ Conocimiento de groupBy y joins distribuidos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. ¿Qué es Data Skew y por qué mata el performance?
# MAGIC 2. Detección de skew con groupBy + count
# MAGIC 3. Salting: la técnica para mitigar skew
# MAGIC 4. repartition vs coalesce: cuándo usar cada uno
# MAGIC 5. Adaptive Query Execution (AQE) automático
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 💡 Por qué importa
# MAGIC
# MAGIC **Data Skew** = una partición tiene 99% de los datos, las demás casi vacías.  
# MAGIC El executor con la partición grande se vuelve el cuello de botella.  
# MAGIC Spark no puede paralelizar lo que está en una sola partición.
# MAGIC
# MAGIC **Impacto real:** Un job de 10 minutos puede tomar 2 horas por skew no detectado.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⚠️ Regla de Oro
# MAGIC
# MAGIC > **"Si una clave domina, el paralelismo muere"**
# MAGIC > 
# MAGIC > Data skew no es un error, es un patrón de datos.  
# MAGIC > La solución no es más hardware, es redistribuir la carga.
# MAGIC > 
# MAGIC > * Detectar → Salting → Repartition → Verificar

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos
from pyspark.sql.functions import col, sum as _sum, count, lit, concat, rand, floor, spark_partition_id
import time

print("💾 CARGANDO DATOS Y SIMULANDO SKEW")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Datos cargados: {df.count():,} registros")
except Exception as e:
    print(f"⚠️  Tabla no encontrada: {e}")
    print("   Ejecuta primero: 00_05_Preparacion_Datos_Empresariales.ipynb")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Data Skew y Salting
# MAGIC %md
# MAGIC ## 📚 Teoría: Data Skew y Salting
# MAGIC
# MAGIC ### ⚖️ ¿Qué es Data Skew?
# MAGIC
# MAGIC Data Skew ocurre cuando una clave de agrupación tiene una desproporcionada cantidad de registros:
# MAGIC
# MAGIC ```
# MAGIC Sin skew (ideal):           Con skew (problema):
# MAGIC Partición 1: 1,000 filas    Partición 1: 99,000 filas ← cuello de botella
# MAGIC Partición 2: 1,000 filas    Partición 2: 100 filas
# MAGIC Partición 3: 1,000 filas    Partición 3: 100 filas
# MAGIC Partición 4: 1,000 filas    Partición 4: 100 filas
# MAGIC
# MAGIC → 4 executors en paralelo   → 1 executor hace el 99% del trabajo
# MAGIC → Rápido (10 min)           → Lento (2 horas)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 Causas comunes de skew
# MAGIC
# MAGIC * **Clave dominante:** `sucursal_id = 'SUC001'` tiene 90% de las ventas
# MAGIC * **Nulos:** `NULL` se agrupa en una sola partición
# MAGIC * **Valores default:** `0` o `''` concentran muchos registros
# MAGIC * **Hot keys:** IDs de productos más vendidos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧂 Salting: la solución
# MAGIC
# MAGIC Salting añade un número aleatorio a la clave de join/groupBy para distribuir la carga:
# MAGIC
# MAGIC ```python
# MAGIC # Sin salting (skew):
# MAGIC df.groupBy("sucursal_id").agg(sum("ventas"))  # SUC001 domina
# MAGIC
# MAGIC # Con salting (distribuido):
# MAGIC df_salt = df.withColumn("salt", floor(rand() * 10))
# MAGIC df_salt = df_salt.withColumn("key_salted", concat(col("sucursal_id"), lit("_"), col("salt")))
# MAGIC df_salt.groupBy("key_salted").agg(sum("ventas"))  # 10x más particiones para SUC001
# MAGIC # Luego agregar por sucursal_id original
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📐 repartition vs coalesce
# MAGIC
# MAGIC | Método | Efecto | Shuffle | Cuándo usar |
# MAGIC |--------|--------|---------|------------|
# MAGIC | `repartition(n)` | Aumenta/redistribuye particiones | Sí (costoso) | Aumentar paralelismo o particionar por columna |
# MAGIC | `coalesce(n)` | Reduce particiones | No (barato) | Consolidar archivos pequeños después de filtrar |
# MAGIC | `repartition('col')` | Particiona por valor de columna | Sí | Joins por esa columna |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🤖 Adaptive Query Execution (AQE)
# MAGIC
# MAGIC AQE (Spark 3.0+) detecta y mitiga skew automáticamente:
# MAGIC ```python
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# MAGIC # Spark divide automáticamente particiones grandes
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,🧪 Detección y Mitigación de Skew
print("🧪 DETECCIÓN Y MITIGACIÓN DE DATA SKEW")
print("="*70)

# --- 1. DETECTAR SKEW ---
print("\n1️⃣  DETECCIÓN: Contar registros por sucursal")
print("-"*70)

distribucion = df.groupBy("sucursal_id").count().orderBy("count", ascending=False)
distribucion.show()

total = df.count()
print(f"\n📊 Total de registros: {total:,}")
max_count = distribucion.first()["count"]
skew_ratio = max_count / total * 100
print(f"   Sucursal dominante: {max_count:,} ({skew_ratio:.1f}% del total)")

if skew_ratio > 40:
    print(f"   ⚠️  SKEW DETECTADO: una sucursal tiene {skew_ratio:.1f}% de los datos")
else:
    print(f"   ✅ Distribución relativamente equilibrada")

# --- 2. VER PARTICIONES ACTUALES ---
print("\n2️⃣  PARTICIONES ACTUALES")
print("-"*70)
n_particiones = df.rdd.getNumPartitions()
print(f"   Particiones del DataFrame: {n_particiones}")

# Ver distribución por partición
part_dist = df.withColumn("partition_id", spark_partition_id())\
    .groupBy("partition_id").count().orderBy("partition_id")
print("\n   Registros por partición:")
part_dist.show()

# --- 3. SALTING: SIMULAR MITIGACIÓN ---
print("\n3️⃣  SALTING: Redistribuir la carga")
print("-"*70)

N_SALTS = 10
df_salted = df.withColumn(
    "salt",
    floor(rand() * N_SALTS)
).withColumn(
    "sucursal_salted",
    concat(col("sucursal_id"), lit("_"), col("salt"))
)

print(f"   Salting con N={N_SALTS}: cada sucursal se divide en {N_SALTS} sub-claves")
print(f"   Particiones antes: {df.rdd.getNumPartitions()}")
df_salted_rep = df_salted.repartition(N_SALTS * 5, "sucursal_salted")
print(f"   Particiones después: {df_salted_rep.rdd.getNumPartitions()}")

# Agregar por clave salted
df_agg_salted = df_salted_rep.groupBy("sucursal_salted").agg(
    _sum("ventas").alias("ventas_salt")
)

# Re-agregar por sucursal original (eliminar sal)
df_final = df_agg_salted.withColumn(
    "sucursal_id",
    col("sucursal_salted").substr(1, 6)  # extraer sucursal_id original
).groupBy("sucursal_id").agg(
    _sum("ventas_salt").alias("ventas_total")
).orderBy("ventas_total", ascending=False)

print("\n   Resultado después de salting:")
df_final.show()

# --- 4. AQE: SKEW AUTOMÁTICO ---
print("\n4️⃣  ADAPTIVE QUERY EXECUTION (AQE)")
print("-"*70)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
print("   ✅ AQE habilitado: Spark detecta skew automáticamente")
print("   ✅ Skew Join habilitado: particiones grandes se dividen solas")
print("   💡 AQE elimina la necesidad de salting manual en muchos casos")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,⚖️ Teoría: Skew aplicado a Los Andes Market
# MAGIC %md
# MAGIC ## ⚖️ Data skew aplicado a Los Andes Market
# MAGIC
# MAGIC ### 📊 ¿Hay skew en las sucursales de Mendoza?
# MAGIC
# MAGIC En **Los Andes Market**, las sucursales pueden tener volúmenes muy diferentes:
# MAGIC * Una sucursal en **Centro Comercial** puede tener muchas más transacciones que una en **Zona Residencial**
# MAGIC * Si una sucursal domina los registros, `groupBy("sucursal_id")` concentra el trabajo en un solo executor
# MAGIC
# MAGIC ```python
# MAGIC # Detectar skew en los datos reales
# MAGIC distribucion = df.groupBy("sucursal_id").count().orderBy("count", ascending=False)
# MAGIC # Si la primera sucursal tiene >40% de los registros → skew
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧂 Salting aplicado a ventas
# MAGIC
# MAGIC Si una sucursal domina, el salting redistribuye su carga:
# MAGIC
# MAGIC ```python
# MAGIC # Sin salting: SUC001 tiene 90% de los registros → 1 executor saturado
# MAGIC df.groupBy("sucursal_id").sum("ventas")
# MAGIC
# MAGIC # Con salting: SUC001 se divide en 10 sub-claves → 10 executors en paralelo
# MAGIC df_salted = df.withColumn("salt", floor(rand() * 10))
# MAGIC df_salted = df_salted.withColumn("key", concat(col("sucursal_id"), lit("_"), col("salt")))
# MAGIC df_salted.groupBy("key").sum("ventas")  # Distribuido
# MAGIC # Luego re-agregar por sucursal_id original
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué sucursal tiene más registros? ¿Hay skew?
# MAGIC * ¿El skew afecta los tiempos de groupBy?
# MAGIC * ¿AQE puede mitigar el skew automáticamente?

# COMMAND ----------

# DBTITLE 1,⚖️ Práctica: Skew aplicado a Los Andes Market
from pyspark.sql.functions import col, sum as _sum, count, lit, concat, rand, floor, spark_partition_id, year
import time

print("⚖️ DATA SKEW APLICADO A LOS ANDES MARKET")
print("="*70)

if 'df' in dir() and df is not None:
    print("\n1️⃣  DETECCIÓN REAL: Distribución por sucursal")
    print("-"*70)

    distribucion = (df.groupBy("sucursal_id")
        .agg(count("*").alias("registros"), _sum("ventas").alias("ventas_total"))
        .orderBy("registros", ascending=False))
    distribucion.show(truncate=30)

    total = df.count()
    max_reg = distribucion.first()["registros"]
    skew_ratio = max_reg / total * 100
    print(f"\n   Total registros: {total:,}")
    print(f"   Sucursal dominante: {max_reg:,} ({skew_ratio:.1f}% del total)")

    if skew_ratio > 40:
        print(f"   ⚠️  SKEW DETECTADO: una sucursal concentra {skew_ratio:.1f}% de los datos")
    elif skew_ratio > 20:
        print(f"   🟡 Skew moderado ({skew_ratio:.1f}%) — AQE puede manejarlo")
    else:
        print(f"   ✅ Distribución equilibrada (max {skew_ratio:.1f}%)")

    print("\n" + "="*70)
    print("\n2️⃣  DISTRIBUCIÓN POR ZONA")
    print("-"*70)

    dist_zona = df.groupBy("zona").count().orderBy("count", ascending=False)
    dist_zona.show(truncate=30)
    max_zona = dist_zona.first()["count"]
    skew_zona = max_zona / total * 100
    print(f"\n   Zona dominante: {skew_zona:.1f}% de los registros")

    print("\n" + "="*70)
    print("\n3️⃣  SALTING: Redistribuir carga si hay skew")
    print("-"*70)

    N_SALTS = 10
    df_salted = (df
        .withColumn("salt", floor(rand() * N_SALTS))
        .withColumn("sucursal_salted", concat(col("sucursal_id"), lit("_"), col("salt"))))

    print(f"\n   Salting con N={N_SALTS}: cada sucursal se divide en {N_SALTS} sub-claves")
    print(f"   Particiones originales: {df.rdd.getNumPartitions()}")

    df_salted_rep = df_salted.repartition(N_SALTS * 5, "sucursal_salted")
    print(f"   Particiones con salting: {df_salted_rep.rdd.getNumPartitions()}")

    # Agregar por clave salted
    agg_salted = df_salted_rep.groupBy("sucursal_salted").agg(_sum("ventas").alias("ventas_parcial"))

    # Re-agregar por sucursal_id original (quitar el salt)
    df_final = (agg_salted
        .withColumn("sucursal_id", col("sucursal_salted").substr(1, 6))
        .groupBy("sucursal_id")
        .agg(_sum("ventas_parcial").alias("ventas_total"))
        .orderBy("ventas_total", ascending=False))
    print("\n   Resultado final (mismo que sin salting, pero distribuido):")
    df_final.show(5, truncate=30)

    print("\n" + "="*70)
    print("\n4️⃣  COMPARACIÓN: groupBy con y sin salting")
    print("-"*70)

    start = time.time()
    df.groupBy("sucursal_id").agg(_sum("ventas").alias("total")).orderBy("total", ascending=False).collect()
    t_normal = time.time() - start

    start = time.time()
    df_final.collect()
    t_salted = time.time() - start

    print(f"\n   groupBy normal: {t_normal:.3f}s")
    print(f"   groupBy + salting: {t_salted:.3f}s")
    print(f"\n   💡 En datos pequeños la diferencia es mínima")
    print(f"   💡 En GB/TB con skew extremo, salting puede ser 10x más rápido")

    print("\n" + "="*70)
    print("\n5️⃣  AQE: Mitigación automática de skew")
    print("-"*70)

    # Habilitar AQE
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    print("\n   AQE habilitado (skew join automático)")
    print("   Spark dividirá automáticamente particiones grandes durante la ejecución")
    print("   💡 AQE elimina la necesidad de salting manual en muchos casos")
else:
    print("⚠️  No hay datos disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 13_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Data Skew — el asesino del paralelismo:**
# MAGIC    - Una clave domina (90% de registros en una partición)
# MAGIC    - Un executor hace todo el trabajo mientras los demás esperan
# MAGIC    - Síntomas: un task tarda 10x más que los demás en Spark UI
# MAGIC
# MAGIC 2. **Detección de skew:**
# MAGIC    - `df.groupBy('clave').count().orderBy('count', ascending=False)` — ver distribución
# MAGIC    - Si una clave tiene >40% de los registros → skew significativo
# MAGIC    - `spark_partition_id()` muestra la distribución física por partición
# MAGIC
# MAGIC 3. **Salting — la técnica de mitigación:**
# MAGIC    - Añadir `floor(rand() * N)` a la clave para dividirla en N sub-claves
# MAGIC    - Agregar por clave salted, luego re-agregar por clave original
# MAGIC    - Distribuye la carga: una partición gigante → N particiones manejables
# MAGIC
# MAGIC 4. **repartition vs coalesce:**
# MAGIC    - `repartition(n)`: aumenta/redistribuye (con shuffle, costoso)
# MAGIC    - `coalesce(n)`: reduce (sin shuffle, barato)
# MAGIC    - `repartition('col')`: particiona por valor de columna (para joins)
# MAGIC    - Regla: coalesce para reducir, repartition para aumentar o redistribuir
# MAGIC
# MAGIC 5. **Adaptive Query Execution (AQE):**
# MAGIC    - Spark 3.0+ detecta y mitiga skew automáticamente
# MAGIC    - `spark.sql.adaptive.skewJoin.enabled = true` — particiona grandes claves solo
# MAGIC    - Elimina la necesidad de salting manual en muchos casos
# MAGIC    - Recomendado: siempre habilitar AQE en producción
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Detectar skew antes de optimizar**
# MAGIC ```python
# MAGIC # MALO: aplicar salting sin verificar si hay skew
# MAGIC df_salted = df.withColumn("salt", floor(rand() * 10))  # ¿hace falta?
# MAGIC
# MAGIC # BUENO: detectar primero, mitigar solo si es necesario
# MAGIC distribucion = df.groupBy("sucursal_id").count().orderBy("count", ascending=False)
# MAGIC distribucion.show()
# MAGIC # Si max_count / total > 40% → hay skew, aplicar salting
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: coalesce para reducir, repartition para aumentar**
# MAGIC ```python
# MAGIC # MALO: repartition(4) para reducir particiones (shuffle innecesario)
# MAGIC df_small = df.repartition(4)  # costoso, mueve todos los datos
# MAGIC
# MAGIC # BUENO: coalesce para reducir (sin shuffle)
# MAGIC df_small = df.coalesce(4)  # barato, solo combina particiones adyacentes
# MAGIC # repartition solo para aumentar o redistribuir por columna
# MAGIC df_big = df.repartition(32)  # más paralelismo
# MAGIC df_by_sucursal = df.repartition("sucursal_id")  # para joins
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Habilitar AQE antes de salting manual**
# MAGIC ```python
# MAGIC # MALO: salting manual sin probar AQE primero
# MAGIC # (trabajo extra que AQE podría hacer automáticamente)
# MAGIC
# MAGIC # BUENO: AQE primero, salting solo si AQE no es suficiente
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# MAGIC # Ejecutar el job y verificar en Spark UI si el skew se resolvió
# MAGIC # Si no → aplicar salting manual
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Detectar skew | `df.groupBy('clave').count().orderBy('count', desc)` |
# MAGIC | Ver distribución física | `df.withColumn('pid', spark_partition_id()).groupBy('pid').count()` |
# MAGIC | Mitigar skew manualmente | Salting: `concat(clave, "_", floor(rand()*N))` |
# MAGIC | Reducir particiones | `df.coalesce(n)` (sin shuffle) |
# MAGIC | Aumentar particiones | `df.repartition(n)` (con shuffle) |
# MAGIC | Particionar por columna | `df.repartition('col')` (para joins) |
# MAGIC | Skew automático | `spark.sql.adaptive.skewJoin.enabled = true` |
# MAGIC | Particiones óptimas | 2-3 × número de cores del cluster |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>⚖️ ¡Data Skew y Salting dominados!</h3>
# MAGIC   <p><i>"Data skew no es un error, es un patrón. Detectarlo es la mitad de la solución; salting es la otra."</i></p>
# MAGIC </div>