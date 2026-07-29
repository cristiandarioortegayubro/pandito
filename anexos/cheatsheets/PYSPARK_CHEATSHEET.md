# ⚡ PySpark Cheatsheet - Saliendo de lo Pandito v4

**Referencia rápida de PySpark para procesamiento distribuido de datos**

---

## 🚀 Inicialización y SparkSession

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

# SparkSession ya disponible en Databricks como 'spark'
# Para inicializar manualmente:
spark = SparkSession.builder \
    .appName("MiApp") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Ver configuración
spark.conf.get("spark.sql.shuffle.partitions")
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Ver versión
spark.version
```

---

## 📂 Lectura de Datos

```python
# CSV
df = spark.read.csv("ruta/archivo.csv", header=True, inferSchema=True)
df = spark.read.option("header", "true") \
              .option("inferSchema", "true") \
              .option("sep", ";") \
              .csv("archivo.csv")

# Parquet (recomendado)
df = spark.read.parquet("ruta/datos.parquet")

# JSON
df = spark.read.json("ruta/datos.json")

# Delta Lake
df = spark.read.format("delta").load("ruta/delta_table")
df = spark.table("catalog.schema.table")  # Unity Catalog

# Múltiples archivos
df = spark.read.parquet("ruta/*.parquet")
df = spark.read.csv("ruta/datos_202*.csv")

# Con esquema explícito
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("nombre", StringType(), True),
    StructField("fecha", DateType(), True),
    StructField("monto", DoubleType(), True)
])
df = spark.read.schema(schema).csv("datos.csv")

# Desde Pandas
pandas_df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
spark_df = spark.createDataFrame(pandas_df)
```

---

## 💾 Escritura de Datos

```python
# Parquet
df.write.mode("overwrite").parquet("ruta/salida.parquet")

# CSV
df.write.mode("overwrite") \
    .option("header", "true") \
    .csv("ruta/salida.csv")

# Delta Lake
df.write.format("delta") \
    .mode("overwrite") \
    .save("ruta/delta_table")

# Unity Catalog
df.write.mode("overwrite") \
    .saveAsTable("catalog.schema.table")

# Particionar por columna
df.write.partitionBy("año", "mes") \
    .parquet("ruta/salida")

# Modos de escritura
.mode("overwrite")    # Reemplazar
.mode("append")       # Agregar
.mode("ignore")       # No escribir si existe
.mode("error")        # Error si existe (default)
```

---

## 🔍 Inspección de Datos

```python
# Ver datos
df.show()              # Primeras 20 filas
df.show(5)             # Primeras 5 filas
df.show(truncate=False) # Sin truncar columnas
df.head(5)             # Primeras 5 filas como lista

# Esquema
df.printSchema()       # Árbol de esquema
df.schema              # StructType
df.columns             # Lista de columnas
df.dtypes              # Lista de (columna, tipo)

# Estadísticas
df.count()             # Número de filas
df.describe().show()   # Estadísticas descriptivas
df.summary().show()    # Estadísticas + cuartiles

# Muestra aleatoria
df.sample(fraction=0.1, seed=42).show()

# Convertir a Pandas (¡CUIDADO con tamaño!)
pandas_df = df.toPandas()
```

---

## 🎯 Selección de Columnas

```python
# Seleccionar columnas
df.select("col1", "col2")
df.select(F.col("col1"), F.col("col2"))
df.select(df.col1, df.col2)

# Todas las columnas excepto algunas
df.drop("col_a_eliminar")
df.drop("col1", "col2")

# Renombrar columnas
df.withColumnRenamed("old_name", "new_name")
df.select(F.col("old").alias("new"))

# Seleccionar con expresiones
df.select(
    F.col("ventas") * 1.21,
    F.upper(F.col("nombre")),
    F.year(F.col("fecha"))
)
```

---

## 🔎 Filtrado (WHERE)

```python
# Filtrado simple
df.filter(F.col("edad") > 30)
df.filter(df.edad > 30)
df.where(F.col("ciudad") == "Madrid")

# Múltiples condiciones
df.filter((F.col("edad") > 30) & (F.col("ciudad") == "Madrid"))
df.filter((F.col("edad") < 25) | (F.col("edad") > 65))

# NOT IN
df.filter(~F.col("estado").isin(["INACTIVO", "SUSPENDIDO"]))

# BETWEEN
df.filter(F.col("precio").between(100, 500))

# IS NULL / IS NOT NULL
df.filter(F.col("columna").isNull())
df.filter(F.col("columna").isNotNull())

# LIKE / RLIKE (regex)
df.filter(F.col("nombre").like("%Ana%"))
df.filter(F.col("email").rlike(".*@gmail\\.com$"))

# SQL WHERE (también válido)
df.filter("edad > 30 AND ciudad = 'Madrid'")
```

---

## 🔧 Transformaciones de Columnas

```python
# Crear nueva columna
df.withColumn("nueva", F.col("col1") + F.col("col2"))
df.withColumn("doble", F.col("valor") * 2)

# Modificar columna existente
df.withColumn("precio", F.col("precio") * 1.21)

# Condicionales con when/otherwise
df.withColumn(
    "categoria",
    F.when(F.col("edad") < 30, "Joven")
     .when(F.col("edad") < 60, "Adulto")
     .otherwise("Senior")
)

# Operaciones de strings
df.withColumn("mayuscula", F.upper(F.col("nombre")))
df.withColumn("minuscula", F.lower(F.col("nombre")))
df.withColumn("sin_espacios", F.trim(F.col("texto")))
df.withColumn("concat", F.concat(F.col("col1"), F.lit(" - "), F.col("col2")))

# Extracción de substring
df.withColumn("primeros_3", F.substring(F.col("codigo"), 1, 3))

# Split
df.withColumn("array_partes", F.split(F.col("email"), "@"))
df.withColumn("usuario", F.split(F.col("email"), "@")[0])

# Cast (cambiar tipo)
df.withColumn("entero", F.col("string_col").cast("int"))
df.withColumn("fecha", F.col("string_date").cast("date"))

# Reemplazar valores
df.withColumn("estado", 
    F.when(F.col("estado") == "ACT", "ACTIVO")
     .when(F.col("estado") == "INA", "INACTIVO")
     .otherwise(F.col("estado"))
)
```

---

## 📅 Funciones de Fecha

```python
# Fecha/hora actual
df.withColumn("ahora", F.current_timestamp())
df.withColumn("hoy", F.current_date())

# Extraer componentes
df.withColumn("año", F.year(F.col("fecha")))
df.withColumn("mes", F.month(F.col("fecha")))
df.withColumn("dia", F.dayofmonth(F.col("fecha")))
df.withColumn("dia_semana", F.dayofweek(F.col("fecha")))
df.withColumn("trimestre", F.quarter(F.col("fecha")))

# Diferencia entre fechas
df.withColumn("dias_diff", F.datediff(F.col("fecha_fin"), F.col("fecha_inicio")))
df.withColumn("meses_diff", F.months_between(F.col("fecha_fin"), F.col("fecha_inicio")))

# Sumar/restar días
df.withColumn("fecha_futura", F.date_add(F.col("fecha"), 30))
df.withColumn("fecha_pasada", F.date_sub(F.col("fecha"), 30))

# Formato de fecha
df.withColumn("fecha_str", F.date_format(F.col("fecha"), "yyyy-MM-dd"))

# Parsear string a fecha
df.withColumn("fecha", F.to_date(F.col("fecha_str"), "yyyy-MM-dd"))
df.withColumn("timestamp", F.to_timestamp(F.col("ts_str"), "yyyy-MM-dd HH:mm:ss"))
```

---

## 📊 Agregaciones y GroupBy

```python
# Agregaciones simples
df.agg(
    F.sum("ventas").alias("total_ventas"),
    F.avg("precio").alias("precio_promedio"),
    F.min("fecha").alias("fecha_min"),
    F.max("fecha").alias("fecha_max"),
    F.count("*").alias("total_registros")
)

# GroupBy
df.groupBy("categoria") \
  .agg(F.sum("ventas").alias("total_ventas"))

# Múltiples agregaciones
df.groupBy("categoria") \
  .agg(
      F.sum("ventas").alias("total_ventas"),
      F.avg("precio").alias("precio_promedio"),
      F.count("*").alias("num_transacciones"),
      F.countDistinct("cliente_id").alias("clientes_unicos")
  )

# GroupBy múltiples columnas
df.groupBy("categoria", "subcategoria") \
  .agg(F.sum("ventas").alias("total"))

# Aggregate con dict (pandas-style)
df.groupBy("categoria").agg({
    "ventas": "sum",
    "precio": "mean",
    "cantidad": "max"
})

# Agregaciones estadísticas
df.groupBy("categoria").agg(
    F.stddev("precio").alias("desv_std"),
    F.variance("precio").alias("varianza"),
    F.approx_count_distinct("cliente_id").alias("aprox_clientes")
)
```

---

## 🔄 Joins

```python
# INNER JOIN (default)
df1.join(df2, on="id")
df1.join(df2, df1.id == df2.cliente_id)

# LEFT JOIN
df1.join(df2, on="id", how="left")

# RIGHT JOIN
df1.join(df2, on="id", how="right")

# FULL OUTER JOIN
df1.join(df2, on="id", how="outer")

# LEFT ANTI JOIN (filas de df1 que NO están en df2)
df1.join(df2, on="id", how="left_anti")

# LEFT SEMI JOIN (filas de df1 que SÍ están en df2, pero solo columnas de df1)
df1.join(df2, on="id", how="left_semi")

# Join en múltiples columnas
df1.join(df2, on=["id", "fecha"], how="left")

# Join con broadcast (optimización para tabla pequeña)
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), on="id")
```

---

## 📐 Window Functions

```python
from pyspark.sql.window import Window

# Definir ventana
window_spec = Window.partitionBy("categoria").orderBy("fecha")

# Ranking
df.withColumn("rank", F.rank().over(window_spec))
df.withColumn("dense_rank", F.dense_rank().over(window_spec))
df.withColumn("row_number", F.row_number().over(window_spec))

# Agregaciones sobre ventana
window_agg = Window.partitionBy("categoria")
df.withColumn("total_categoria", F.sum("ventas").over(window_agg))
df.withColumn("promedio_categoria", F.avg("precio").over(window_agg))

# Lead/Lag (valores anterior/siguiente)
df.withColumn("venta_anterior", F.lag("ventas", 1).over(window_spec))
df.withColumn("venta_siguiente", F.lead("ventas", 1).over(window_spec))

# First/Last
df.withColumn("primera_venta", F.first("ventas").over(window_spec))
df.withColumn("ultima_venta", F.last("ventas").over(window_spec))

# Ventana con rango de filas
window_range = Window.partitionBy("categoria") \
                     .orderBy("fecha") \
                     .rowsBetween(-3, 0)  # 3 filas anteriores + actual

df.withColumn("promedio_movil_4", F.avg("ventas").over(window_range))

# Percentiles
window_all = Window.partitionBy("categoria") \
                   .orderBy("ventas") \
                   .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

df.withColumn("percentil", F.percent_rank().over(window_all))
```

---

## 🔀 Union y Deduplicación

```python
# Union (apilar verticalmente)
df_union = df1.union(df2)
df_union = df1.unionByName(df2)  # Por nombre de columna

# Eliminar duplicados
df.distinct()
df.dropDuplicates()
df.dropDuplicates(["col1", "col2"])  # Por columnas específicas
```

---

## 🔢 Ordenamiento

```python
# Ordenar ascendente
df.orderBy("columna")
df.orderBy(F.col("columna").asc())

# Ordenar descendente
df.orderBy(F.col("columna").desc())

# Múltiples columnas
df.orderBy(F.col("col1").desc(), F.col("col2").asc())

# sort (alias de orderBy)
df.sort("columna")
```

---

## 🧹 Limpieza de Datos

```python
# Eliminar nulls
df.na.drop()                        # Eliminar filas con cualquier null
df.na.drop(subset=["col1", "col2"]) # Solo si nulls en estas columnas
df.na.drop(how="all")               # Solo si todas las columnas son null

# Rellenar nulls
df.na.fill(0)                       # Rellenar con 0
df.na.fill({"col1": 0, "col2": "N/A"})  # Diferentes valores por columna
df.na.fill({"numeric_col": df.select(F.mean("numeric_col")).first()[0]})  # Media

# Reemplazar valores
df.na.replace(["ACTIVO", "ACT"], "ACTIVE")
df.replace({"old_value": "new_value"}, subset=["columna"])
```

---

## 🔍 SQL en PySpark

```python
# Registrar DataFrame como vista temporal
df.createOrReplaceTempView("mi_tabla")

# Ejecutar SQL
resultado = spark.sql("""
    SELECT categoria, SUM(ventas) as total
    FROM mi_tabla
    WHERE fecha >= '2024-01-01'
    GROUP BY categoria
    ORDER BY total DESC
""")

# SQL directo en Unity Catalog
spark.sql("SELECT * FROM catalog.schema.table").show()
```

---

## 🎯 UDFs (User Defined Functions)

```python
from pyspark.sql.types import StringType, IntegerType

# UDF simple
def categorizar_edad(edad):
    if edad < 30:
        return "Joven"
    elif edad < 60:
        return "Adulto"
    else:
        return "Senior"

udf_categoria = F.udf(categorizar_edad, StringType())
df.withColumn("categoria_edad", udf_categoria(F.col("edad")))

# UDF con decorador
@F.udf(returnType=StringType())
def upper_case(text):
    return text.upper() if text else None

df.withColumn("upper", upper_case(F.col("nombre")))

# Pandas UDF (más eficiente)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(StringType())
def pandas_upper(series: pd.Series) -> pd.Series:
    return series.str.upper()

df.withColumn("upper", pandas_upper(F.col("nombre")))
```

---

## ⚡ Delta Lake

```python
# Crear tabla Delta
df.write.format("delta").mode("overwrite") \
  .saveAsTable("catalog.schema.tabla_delta")

# Leer tabla Delta
df = spark.read.format("delta").load("/path/to/delta")
df = spark.table("catalog.schema.tabla_delta")

# MERGE (UPSERT)
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "catalog.schema.tabla")

delta_table.alias("target") \
  .merge(
      source_df.alias("source"),
      "target.id = source.id"
  ) \
  .whenMatchedUpdate(set={
      "nombre": "source.nombre",
      "fecha_actualizacion": F.current_timestamp()
  }) \
  .whenNotMatchedInsert(values={
      "id": "source.id",
      "nombre": "source.nombre",
      "fecha_creacion": F.current_timestamp()
  }) \
  .execute()

# Time Travel
df_historico = spark.read.format("delta") \
  .option("versionAsOf", 3) \
  .load("/path/to/delta")

df_fecha = spark.read.format("delta") \
  .option("timestampAsOf", "2024-01-01") \
  .load("/path/to/delta")

# Ver historial de versiones
delta_table.history().show()

# Vacuum (limpiar archivos antiguos)
delta_table.vacuum(168)  # Mantener 7 días (168 horas)

# Optimize (compactar archivos pequeños)
delta_table.optimize().executeCompaction()

# Z-ORDER (optimizar para queries)
delta_table.optimize().executeZOrderBy("columna1", "columna2")
```

---

## 📈 Optimización y Performance

```python
# Cache (almacenar en memoria)
df.cache()
df.persist()

# Liberar cache
df.unpersist()

# Reparticionamiento
df.repartition(10)                    # 10 particiones
df.repartition(10, "columna")         # Particionar por columna
df.coalesce(5)                        # Reducir particiones (sin shuffle)

# Ver plan de ejecución
df.explain()
df.explain(True)    # Plan detallado

# Ver particiones
df.rdd.getNumPartitions()

# Broadcast join (para tablas pequeñas)
from pyspark.sql.functions import broadcast
df_grande.join(broadcast(df_pequeña), on="id")

# Pushdown predicates (filtrar antes de join)
# ✅ Bueno
df.filter(F.col("fecha") > "2024-01-01").join(df2, on="id")

# ❌ Malo
df.join(df2, on="id").filter(F.col("fecha") > "2024-01-01")

# Columnar pruning (seleccionar solo columnas necesarias)
# ✅ Bueno
df.select("col1", "col2").filter(...)

# ❌ Malo
df.filter(...).select("col1", "col2")
```

---

## 🎯 Patrones Comunes

### ETL Pipeline Bronze → Silver → Gold

```python
# Bronze (raw data)
df_bronze = spark.read.csv("/raw/data.csv")
df_bronze.write.format("delta").mode("overwrite") \
    .save("/bronze/tabla")

# Silver (cleaned)
df_silver = spark.read.format("delta").load("/bronze/tabla") \
    .filter(F.col("valor").isNotNull()) \
    .dropDuplicates(["id"]) \
    .withColumn("fecha", F.to_date(F.col("fecha_str")))

df_silver.write.format("delta").mode("overwrite") \
    .save("/silver/tabla")

# Gold (business logic)
df_gold = spark.read.format("delta").load("/silver/tabla") \
    .groupBy("categoria", F.year("fecha").alias("año")) \
    .agg(
        F.sum("ventas").alias("total_ventas"),
        F.avg("precio").alias("precio_promedio")
    )

df_gold.write.format("delta").mode("overwrite") \
    .save("/gold/ventas_resumen")
```

### Window Function - Running Total

```python
window_spec = Window.partitionBy("categoria") \
                    .orderBy("fecha") \
                    .rowsBetween(Window.unboundedPreceding, 0)

df.withColumn("total_acumulado", F.sum("ventas").over(window_spec))
```

### Pivot Table

```python
df.groupBy("categoria") \
  .pivot("mes") \
  .agg(F.sum("ventas")) \
  .show()
```

---

## ⚠️ Errores Comunes y Soluciones

### Error: Analysis Exception - Column not found
```python
# ❌ Problema
df.select("columna_incorrecta")

# ✅ Solución
df.columns  # Ver columnas disponibles
df.printSchema()  # Ver esquema
```

### Error: Py4JJavaError - OutOfMemoryError
```python
# ❌ Problema: DataFrame muy grande en memoria
df.cache().count()

# ✅ Solución: No cachear todo, usar particiones
df.repartition(200).write.parquet("salida")
```

### Performance lenta en UDFs
```python
# ❌ Problema: UDF Python lenta
@F.udf(StringType())
def slow_udf(x):
    return x.upper()

# ✅ Solución: Usar funciones nativas de Spark
F.upper(F.col("columna"))

# O usar Pandas UDF si necesitas lógica custom
@pandas_udf(StringType())
def fast_udf(series):
    return series.str.upper()
```

---

## 📚 Recursos Adicionales

* **Documentación oficial:** https://spark.apache.org/docs/latest/api/python/
* **Databricks Docs:** https://docs.databricks.com/spark/
* **Delta Lake:** https://docs.delta.io/latest/delta-intro.html

---

**💡 Tip de Serverless:** Databricks Serverless escala automáticamente según tu carga. No necesitas preocuparte por configurar el cluster.

_Última actualización: 2026-07-29_
