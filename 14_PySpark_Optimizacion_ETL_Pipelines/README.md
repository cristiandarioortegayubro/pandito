# 🚀 Módulo 14: PySpark Optimización, ETL y Pipelines

## 🎯 Objetivo del Módulo

**Construye pipelines de datos de nivel producción** con técnicas de optimización, paralelización y orquestación.

Este módulo te convierte en **Data Engineer de clase mundial** capaz de procesar TB de datos eficientemente.

**Al finalizar este módulo podrás:**
* ✅ Optimizar queries PySpark con explain() y caching
* ✅ Diseñar particionamiento óptimo para performance
* ✅ Implementar ETL pipelines escalables
* ✅ Manejar errores y bad data en producción
* ✅ Paralelizar procesamiento con broadcast y repartition
* ✅ Monitorear y debuggear jobs de Spark

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 11-13 completados
* Conceptos de data engineering
* SQL avanzado

**Tiempo estimado:** 5 horas

---

## 📚 Contenido del Módulo

### 14_01_explain_y_Analisis_Query_Plans
**Duración:** 55 min | **Dificultad:** Avanzado

**Temas:**
* `.explain()` para ver plan de ejecución
* Plan físico vs plan lógico
* Identificar shuffle operations
* Broadcast joins vs shuffle joins
* Catalyst optimizer
* Adaptive Query Execution (AQE)

**Análisis de planes:**
```python
# Ver plan completo
df.explain(True)

# Solo plan físico
df.explain()

# Identificar problemas
df_result = df_large.join(df_small, 'key')
df_result.explain()
# Busca: Exchange (shuffle) - costoso
# Busca: BroadcastExchange - eficiente para tabla pequeña
```

---

### 14_02_Caching_y_Persistence_Strategies
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* `.cache()` vs `.persist()`
* Storage levels: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY
* Cuándo hacer cache
* `.unpersist()` para liberar memoria
* Checkpointing

**Patrones:**
```python
# Cache DF usado múltiples veces
df_filtrado = df.filter(col('monto') > 1000)
df_filtrado.cache()

# Usar múltiples veces (no recalcula)
count = df_filtrado.count()
avg_monto = df_filtrado.agg({'monto': 'avg'}).collect()

# Liberar cuando termine
df_filtrado.unpersist()
```

---

### 14_03_Particionamiento_y_Bucketing
**Duración:** 60 min | **Dificultad:** Avanzado

**Temas:**
* Particionamiento de tablas Delta
* Repartition vs coalesce
* Optimal partition size (128-256MB)
* Bucketing para joins frecuentes
* Data skew y cómo resolverlo

**Estrategias:**
```python
# Particionar tabla por fecha
df.write.format('delta') \
    .partitionBy('fecha_año', 'fecha_mes') \
    .save('/delta/ventas')

# Repartition en memoria (distribución uniforme)
df_repartitioned = df.repartition(200, 'cliente_id')

# Coalesce para reducir particiones (no shuffle)
df_small = df.coalesce(10)

# Resolver data skew con salting
df_salted = df.withColumn('salt', (rand() * 10).cast('int'))
df_result = df_salted.repartition(200, 'cliente_id', 'salt')
```

---

### 14_04_Diseno_ETL_Pipelines_Bronze_Silver_Gold
**Duración:** 75 min | **Dificultad:** Avanzado

**Temas:**
* Arquitectura Medallion (Bronze, Silver, Gold)
* Bronze: raw data, schema on read
* Silver: cleaned, validated, conformed
* Gold: aggregated, business-level
* Idempotencia y reprocessing

**Pipeline completo:**
```python
# BRONZE - raw ingestion
def bronze_layer():
    df_raw = (spark.read
        .format('json')
        .option('multiLine', 'true')
        .load('/raw/events/')
    )
    
    df_raw.write \
        .format('delta') \
        .mode('append') \
        .option('mergeSchema', 'true') \
        .save('/delta/bronze/events')

# SILVER - cleaning & validation
def silver_layer():
    df_bronze = spark.read.format('delta').load('/delta/bronze/events')
    
    df_clean = (df_bronze
        .filter(col('timestamp').isNotNull())
        .filter(col('user_id').isNotNull())
        .withColumn('fecha', to_date(col('timestamp')))
        .withColumn('hora', hour(col('timestamp')))
        .dropDuplicates(['event_id'])
    )
    
    df_clean.write \
        .format('delta') \
        .mode('append') \
        .partitionBy('fecha') \
        .save('/delta/silver/events')

# GOLD - business metrics
def gold_layer():
    df_silver = spark.read.format('delta').load('/delta/silver/events')
    
    df_metrics = (df_silver
        .groupBy('fecha', 'event_type')
        .agg(
            count('*').alias('event_count'),
            countDistinct('user_id').alias('unique_users')
        )
    )
    
    df_metrics.write \
        .format('delta') \
        .mode('overwrite') \
        .option('replaceWhere', f"fecha = '{current_date()}'") \
        .save('/delta/gold/daily_metrics')
```

---

### 14_05_Error_Handling_y_Bad_Data
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* Manejo de bad records con badRecordsPath
* Schemas estrictos vs permissivos
* Data validation con assert
* Quarantine patterns
* Monitoring y alerting

**Patrones robustos:**
```python
# Leer con manejo de errores
df = (spark.read
    .format('csv')
    .option('header', 'true')
    .option('mode', 'PERMISSIVE')  # DROPMALFORMED, FAILFAST
    .option('badRecordsPath', '/bad_records/')
    .load('/data/input')
)

# Validación de calidad
def validate_data(df):
    # Assert críticos
    assert df.filter(col('id').isNull()).count() == 0, "IDs nulos encontrados"
    assert df.filter(col('monto') < 0).count() == 0, "Montos negativos"
    
    # Quarantine registros malos
    df_valid = df.filter(col('monto') >= 0)
    df_invalid = df.filter(col('monto') < 0)
    
    if df_invalid.count() > 0:
        df_invalid.write.format('delta').mode('append').save('/quarantine/')
        
    return df_valid

df_clean = validate_data(df)
```

---

### 14_06_Monitoring_y_Debugging_Spark_Jobs
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* Spark UI para debugging
* Identificar stages lentos
* Memory y storage metrics
* Logging efectivo
* Spark event logs

**Debugging checklist:**
```python
# Logging estructurado
import logging
logger = logging.getLogger(__name__)

def process_data(df):
    logger.info(f"Inicio procesamiento: {df.count()} filas")
    
    df_result = df.filter(col('monto') > 0)
    logger.info(f"Después filtro: {df_result.count()} filas")
    
    return df_result

# Métricas custom
from pyspark import AccumulatorParam

valid_records = spark.sparkContext.accumulator(0)
invalid_records = spark.sparkContext.accumulator(0)

def process_with_metrics(row):
    if row['monto'] > 0:
        valid_records.add(1)
        return row
    else:
        invalid_records.add(1)
        return None

# Al final del job
print(f"Valid: {valid_records.value}, Invalid: {invalid_records.value}")
```

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar tipos de storage levels
* Nombrar capas de Medallion architecture
* Identificar operaciones que causan shuffle

### Nivel 2: Comprensión
* Explicar diferencia entre cache y persist
* Describir cuándo usar repartition vs coalesce
* Interpretar planes de ejecución con explain()

### Nivel 3: Aplicación
* Optimizar queries con broadcast joins
* Diseñar pipelines Bronze-Silver-Gold
* Implementar manejo de bad records
* Cachear DataFrames estratégicamente

### Nivel 4: Análisis
* Evaluar trade-offs de particionamiento
* Decidir estrategia de caching según workload
* Diagnosticar bottlenecks con Spark UI

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Pipeline Medallion Completo
```
"Diseña pipeline ETL completo con arquitectura Medallion:

BRONZE:
- Ingesta logs JSON de /raw/events/ (multiline)
- Schema: event_id, user_id, event_type, timestamp, payload (json string)
- Escribir en /delta/bronze/events particionado por fecha

SILVER:
- Leer bronze
- Validar: no nulls en event_id, user_id, timestamp
- Parsear payload JSON a columnas
- Deduplicar por event_id
- Escribir en /delta/silver/events

GOLD:
- Agregar métricas diarias: eventos por tipo, usuarios únicos
- Calcular conversion funnel: signup → profile_complete → first_purchase
- Escribir en /delta/gold/daily_metrics

Implementa idempotencia y manejo de errores en cada capa."
```

### Prompt 2: Optimización de Join Lento
```
"Tengo query lenta:

df_large (500M filas): transaccion_id, cliente_id, monto, fecha
df_small (1000 filas): cliente_id, segmento, region

Query:
result = df_large.join(df_small, 'cliente_id')

Tarda 15 minutos. Optimiza:
1. Identifica problema con explain()
2. Aplica broadcast join si aplica
3. Si hay data skew en cliente_id, resuelve con salting
4. Cachea si se reutiliza
5. Ajusta particiones óptimas

Muestra código antes/después y explica mejora esperada."
```

### Prompt 3: Sistema de Monitoring
```
"Implementa sistema de monitoring para pipeline ETL:

1. Loggear métricas por stage:
   - Filas input
   - Filas output
   - Filas rechazadas
   - Duración (segundos)
   
2. Capturar bad records en quarantine

3. Calcular data quality score:
   - % completitud (no nulls)
   - % validez (pasa validaciones)
   - % unicidad (no duplicados)

4. Escribir métricas en tabla Delta 'etl_metrics'

5. Función para generar alerta si:
   - Data quality < 95%
   - > 1% filas rechazadas
   - Duración > 2x promedio histórico

Genera código production-ready."
```

---

## 🔧 Solución de Problemas

### Problema 1: OutOfMemoryError
**Causa:** DataFrames muy grandes sin particionamiento  
**Solución:** Repartition o reduce datos
```python
df_large.repartition(200).write.format('delta').save('/path')
```

### Problema 2: Join muy lento (shuffle)
**Causa:** No usa broadcast para tabla pequeña  
**Solución:** Broadcast join
```python
from pyspark.sql.functions import broadcast
result = df_large.join(broadcast(df_small), 'key')
```

### Problema 3: Data skew en particiones
**Causa:** Una partition key tiene muchos más datos  
**Solución:** Salting
```python
df_salted = df.withColumn('salt', (rand() * 10).cast('int'))
df.repartition(200, 'key', 'salt')
```

---

## 📖 Recursos Adicionales

### Documentación
* [Spark Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
* [Databricks ETL Best Practices](https://docs.databricks.com/etl/index.html)

---

## ✅ Checklist

- [ ] explain() y análisis de planes
- [ ] Cache estratégico
- [ ] Repartition óptimo
- [ ] Pipeline Bronze-Silver-Gold
- [ ] Bad records handling
- [ ] Monitoring y logging

---

## 🚀 Próximo Módulo

**➡️ [Módulo 15: Analítica Agéntica con Databricks Genie Code](../15_Analitica_Agentica_Databricks_Genie_Code/)**

---

[📖 Volver al Índice](../README.md)
