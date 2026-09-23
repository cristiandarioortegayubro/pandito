# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 13 - Notebook 03: Adaptive query execution y broadcast joins
# MAGIC
# MAGIC ## 🤖 Optimización automática y joins sin shuffle
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 13 - Performance Spark y Optimización  
# MAGIC **Duración estimada:** 55 minutos  
# MAGIC **Dificultad:** 🟠 Intermedio-Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC Al finalizar este notebook serás capaz de:
# MAGIC
# MAGIC ✅ **Entender** Adaptive Query Execution (AQE) y sus beneficios  
# MAGIC ✅ **Aplicar** Broadcast Joins para tablas pequeñas  
# MAGIC ✅ **Configurar** AQE en Spark para optimización automática  
# MAGIC ✅ **Diagnosticar** joins con EXPLAIN y Spark UI  
# MAGIC ✅ **Integrar** todas las técnicas de optimización en un pipeline
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 13_01 y 13_02 completados
# MAGIC * ✅ Entender joins distribuidos y shuffle
# MAGIC * ✅ Conocimiento de Data Skew y salting
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. Adaptive Query Execution (AQE) — Spark que se optimiza solo
# MAGIC 2. Broadcast Joins — eliminar shuffle en joins
# MAGIC 3. Configuración de AQE y auto-broadcast
# MAGIC 4. Diagnóstico con EXPLAIN y Spark UI
# MAGIC 5. Pipeline optimizado integrador
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 💡 Por qué importa
# MAGIC
# MAGIC **AQE** = Spark ajusta el plan de ejecución DURANTE la ejecución, no solo antes.  
# MAGIC **Broadcast** = envía la tabla pequeña a todos los executors, sin shuffle.  
# MAGIC
# MAGIC Juntos: joins 10-100x más rápidos sin código manual.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⚠️ Regla de Oro
# MAGIC
# MAGIC > **"AQE + Broadcast = el 80% de la optimización con 2 líneas de config"**
# MAGIC > 
# MAGIC > Antes de optimizar manualmente, habilita AQE y usa broadcast.  
# MAGIC > Solo si no es suficiente, aplica salting y cache manualmente.

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos
from pyspark.sql.functions import col, broadcast, sum as _sum, count
import time

print("💾 CARGANDO DATOS DESDE UNITY CATALOG")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df_ventas = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"✅ Ventas cargadas: {df_ventas.count():,} registros")
    
    # Crear tabla pequeña de sucursales (para broadcast join)
    df_sucursales = df_ventas.select("sucursal_id", "sucursal_nombre", "zona").dropDuplicates()
    print(f"✅ Sucursales: {df_sucursales.count()} registros (tabla pequeña para broadcast)")
except Exception as e:
    print(f"⚠️  Tabla no encontrada: {e}")
    print("   Ejecuta primero: 00_05_Preparacion_Datos_Empresariales.ipynb")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: AQE y Broadcast
# MAGIC %md
# MAGIC ## 📚 Teoría: AQE y Broadcast Joins
# MAGIC
# MAGIC ### 🤖 Adaptive Query Execution (AQE)
# MAGIC
# MAGIC AQE (Spark 3.0+) reoptimiza el plan DURANTE la ejecución, basándose en estadísticas reales:
# MAGIC
# MAGIC | Feature | Qué hace |
# MAGIC |---------|----------|
# MAGIC | **Skew Join** | Divide particiones grandes automáticamente |
# MAGIC | **Auto Coalesce** | Fusiona particiones pequeñas después de shuffle |
# MAGIC | **Dynamic Partition Pruning** | Filtra particiones en runtime con datos del join |
# MAGIC | **Auto Broadcast** | Convierte Sort-Merge a Broadcast si detecta tabla pequeña |
# MAGIC
# MAGIC ```python
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📡 Broadcast Joins
# MAGIC
# MAGIC **El problema:** Sort-Merge Join hace shuffle de ambas tablas (costoso).
# MAGIC
# MAGIC **La solución:** Si una tabla es pequeña (< 10 MB), enviarla a todos los executors:
# MAGIC
# MAGIC ```
# MAGIC Sort-Merge Join (sin broadcast):          Broadcast Join (con broadcast):
# MAGIC Tabla A → Shuffle → Merge                 Tabla B (pequeña) → Copia a TODOS
# MAGIC Tabla B → Shuffle → Merge                 Tabla A → Sin shuffle → Join local
# MAGIC
# MAGIC 2 shuffles, lento                          0 shuffles, 10-100x más rápido
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📐 Auto-Broadcast Threshold
# MAGIC
# MAGIC ```python
# MAGIC # Tablas menores a este tamaño se auto-broadcastean
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10m")  # default: 10 MB
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 Diagnóstico con EXPLAIN
# MAGIC
# MAGIC ```python
# MAGIC df.explain()           # Plan físico
# MAGIC # Buscar "BroadcastHashJoin" = broadcast funcionando
# MAGIC # Buscar "SortMergeJoin" = shuffle (no broadcast)
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,🤖 AQE y Broadcast en Acción
print("🤖 AQE Y BROADCAST JOINS EN ACCIÓN")
print("="*70)

# --- 1. HABILITAR AQE ---
print("\n1️⃣  HABILITAR ADAPTIVE QUERY EXECUTION")
print("-"*70)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10m")
print("   ✅ AQE habilitado")
print("   ✅ Coalesce automático habilitado")
print("   ✅ Skew join automático habilitado")
print("   ✅ Auto-broadcast threshold: 10 MB")

# --- 2. BROADCAST JOIN EXPLÍCITO ---
print("\n2️⃣  BROADCAST JOIN EXPLÍCITO")
print("-"*70)

start = time.time()
df_result_broadcast = df_ventas.join(
    broadcast(df_sucursales),
    on="sucursal_id",
    how="inner"
)
count_broadcast = df_result_broadcast.count()
tiempo_broadcast = time.time() - start
print(f"   Tiempo con broadcast: {tiempo_broadcast:.2f}s")
print(f"   Registros: {count_broadcast:,}")

# Ver el plan de ejecución
print("\n   📋 Plan de ejecución (explain):")
df_result_broadcast.explain()

# --- 3. SORT-MERGE JOIN (SIN BROADCAST) ---
print("\n3️⃣  SORT-MERGE JOIN (sin broadcast explícito)")
print("-"*70)

# Deshabilitar auto-broadcast temporalmente
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

start = time.time()
df_result_merge = df_ventas.join(
    df_sucursales,
    on="sucursal_id",
    how="inner"
)
count_merge = df_result_merge.count()
tiempo_merge = time.time() - start
print(f"   Tiempo sin broadcast: {tiempo_merge:.2f}s")
print(f"   Registros: {count_merge:,}")

# Restaurar auto-broadcast
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10m")

# --- 4. COMPARACIÓN ---
print("\n4️⃣  COMPARACIÓN")
print("-"*70)
print(f"   Broadcast Join: {tiempo_broadcast:.2f}s")
print(f"   Sort-Merge Join: {tiempo_merge:.2f}s")
if tiempo_merge > 0:
    speedup = tiempo_merge / tiempo_broadcast if tiempo_broadcast > 0 else 0
    print(f"   Speedup: {speedup:.1f}x")

# --- 5. PIPELINE OPTIMIZADO INTEGRADOR ---
print("\n5️⃣  PIPELINE OPTIMIZADO INTEGRADOR")
print("-"*70)

# Configuración óptima
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10m")

start = time.time()

# ETL optimizado: filtrar → enriquecer con broadcast → agregar → escribir
df_pipeline = (
    df_ventas
    .filter(col("ventas") > 50000)                    # filtrar early
    .join(broadcast(df_sucursales), "sucursal_id")      # broadcast join
    .withColumn("categoria",                           # CASE WHEN
        when(col("ventas") > 80000, lit("Alto"))
        .when(col("ventas") > 50000, lit("Medio"))
        .otherwise(lit("Bajo")))
    .groupBy("zona", "categoria")
    .agg(
        _sum("ventas").alias("ventas_total"),
        count("*").alias("num_registros")
    )
    .orderBy("ventas_total", ascending=False)
)

df_pipeline.show()
tiempo_pipeline = time.time() - start
print(f"\n   ⏱️  Pipeline completo: {tiempo_pipeline:.2f}s")
print("   ✅ AQE + Broadcast + Filter early + Caching = pipeline óptimo")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 13_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Adaptive Query Execution (AQE):**
# MAGIC    ```python
# MAGIC    spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# MAGIC    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
# MAGIC    # Spark se optimiza solo: skew, coalesce, partition pruning, auto-broadcast
# MAGIC    ```
# MAGIC
# MAGIC 2. **Broadcast Joins:**
# MAGIC    ```python
# MAGIC    from pyspark.sql.functions import broadcast
# MAGIC    # Tabla grande + tabla pequeña → sin shuffle, 10-100x más rápido
# MAGIC df_result = df_grande.join(broadcast(df_pequeno), on="clave")
# MAGIC    ```
# MAGIC
# MAGIC 3. **Auto-Broadcast Threshold:**
# MAGIC    ```python
# MAGIC    # Tablas < 10 MB se auto-broadcastean sin código manual
# MAGIC    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10m")
# MAGIC    # Deshabilitar: set to -1 (fuerza Sort-Merge)
# MAGIC    ```
# MAGIC
# MAGIC 4. **Diagnóstico con EXPLAIN:**
# MAGIC    ```python
# MAGIC    df.explain()
# MAGIC    # BroadcastHashJoin = broadcast funcionando (óptimo)
# MAGIC    # SortMergeJoin = shuffle (no broadcast, más lento)
# MAGIC    # Exchange = shuffle entre particiones (costoso)
# MAGIC    ```
# MAGIC
# MAGIC 5. **Pipeline optimizado integrador:**
# MAGIC    - AQE habilitado + auto-broadcast + filter early + broadcast join
# MAGIC    - Filtrar antes de join reduce datos a shufflear
# MAGIC    - Combinar todas las técnicas del módulo en un solo flujo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de optimización
# MAGIC
# MAGIC **Caso 1: Habilitar AQE (siempre en producción)**
# MAGIC ```python
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# MAGIC spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Broadcast join explícito**
# MAGIC ```python
# MAGIC df_result = df_grande.join(broadcast(df_pequeno), on="clave", how="inner")
# MAGIC # Sin shuffle, tabla pequeña copiada a todos los executors
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Verificar si broadcast está funcionando**
# MAGIC ```python
# MAGIC df.explain()
# MAGIC # Buscar "BroadcastHashJoin" → funciona
# MAGIC # Buscar "SortMergeJoin" → no broadcast, revisar tamaño de tabla
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Pipeline optimizado completo**
# MAGIC ```python
# MAGIC df = (df_raw
# MAGIC     .filter(col("ventas") > 50000)           # filter early
# MAGIC     .join(broadcast(df_dim), "clave")         # broadcast join
# MAGIC     .groupBy("zona").agg(sum("ventas"))      # agregación
# MAGIC     .cache())                                # cachear resultado
# MAGIC df.count()  # materializar
# MAGIC df.show()
# MAGIC df.unpersist()  # liberar
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Deshabilitar auto-broadcast para debug**
# MAGIC ```python
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
# MAGIC # Fuerza Sort-Merge en todos los joins (para comparar performance)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 13
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **13_01 - Caching, Persist y Memory Management:** cache/persist, StorageLevel, unpersist, cuándo cachear
# MAGIC 2. **13_02 - Data Skew y Salting:** detección de skew, salting, repartition vs coalesce, AQE skew
# MAGIC 3. **13_03 - Adaptive Query Execution y Broadcast:** AQE, broadcast joins, auto-broadcast, EXPLAIN, pipeline integrador
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Cachear DataFrames estratégicamente con cache/persist
# MAGIC * ✅ Detectar y mitigar Data Skew con salting
# MAGIC * ✅ Habilitar AQE para optimización automática
# MAGIC * ✅ Aplicar Broadcast Joins para eliminar shuffle
# MAGIC * ✅ Diagnosticar performance con EXPLAIN y Spark UI
# MAGIC * ✅ Construir pipelines Spark optimizados de extremo a extremo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🚀 ¡Módulo 13 Completado!</h3>
# MAGIC   <p><i>"Dominas Performance Spark: caching, skew, AQE y broadcast. Ahora tus pipelines son 10x más rápidos con 2 líneas de configuración."</i></p>
# MAGIC </div>