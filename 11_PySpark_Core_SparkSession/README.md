# ⚡ Módulo 11: PySpark Core y SparkSession

## 🎯 Objetivo del Módulo

**Domina los fundamentos de PySpark** para procesar Big Data de manera distribuida y escalable en Databricks.

Este es tu salto de **Pandas (single-node)** a **PySpark (distributed)**. Aprende a pensar en paralelo y a escalar análisis de GB a TB sin cambiar tu código.

**Al finalizar este módulo podrás:**
* ✅ Entender la arquitectura distribuida de Spark (driver, executors, particiones)
* ✅ Crear y configurar SparkSession en serverless
* ✅ Leer datos desde múltiples fuentes (CSV, Parquet, Delta, JSON)
* ✅ Crear DataFrames de Spark desde Pandas, listas, RDDs
* ✅ Aplicar transformaciones básicas: select, filter, withColumn
* ✅ Entender lazy evaluation y cómo optimiza Spark
* ✅ Escribir datos en formatos optimizados para Big Data

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 01-06 completados (especialmente Pandas)
* Familiaridad con SQL básico
* Conceptos de DataFrames (filas, columnas, schemas)

**Datasets:**
* `ventas_retail.csv`
* `transacciones_financieras.parquet`

**Entorno:**
* Databricks Serverless Compute (CPU) ✅
* Python 3.10+
* PySpark 3.5+

**Tiempo estimado:** 4 horas

---

## 📚 Contenido del Módulo

### 11_01_Arquitectura_Spark_y_Computacion_Distribuida
**Duración:** 50 min | **Dificultad:** Principiante

**Temas:**
* Arquitectura Spark: Driver, Executors, Cluster Manager
* Lazy evaluation vs Eager execution
* Transformaciones vs Acciones
* Particiones y paralelismo
* DAG (Directed Acyclic Graph) de ejecución
* Plan físico vs plan lógico

**Conceptos clave:**
```python
# Transformación (lazy): no ejecuta nada
df_filtered = df.filter(df.edad > 25)

# Acción (eager): ejecuta todo el DAG
count = df_filtered.count()
```

**Resultado:** Comprensión de cómo Spark procesa datos distribuidos

---

### 11_02_SparkSession_Configuracion_Serverless
**Duración:** 45 min | **Dificultad:** Principiante

**Temas:**
* Crear SparkSession (ya disponible en Databricks como `spark`)
* Configuraciones importantes: shuffle, partitions, memory
* Serverless vs Classic Clusters
* Limitaciones de DBFS en Serverless
* Verificar versión y configuración actual

**Código esencial:**
```python
# SparkSession ya disponible
print(spark.version)  # 3.5.x
print(spark.sparkContext.defaultParallelism)

# Acceder a configuración
spark.conf.get("spark.sql.shuffle.partitions")

# Modificar configuración (sesión actual)
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

**Nota Serverless:** No puedes instalar librerías Scala ni acceder a `/dbfs/` directamente. Usa `/Workspace/` o Unity Catalog Volumes.

---

### 11_03_Creacion_DataFrames_Multiples_Fuentes
**Duración:** 55 min | **Dificultad:** Principiante-Intermedio

**Temas:**
* Leer CSV: `spark.read.csv()` con opciones (header, inferSchema, delimiter)
* Leer Parquet: `spark.read.parquet()` (formato preferido)
* Leer JSON: `spark.read.json()` (incluyendo JSON Lines)
* Leer Delta Lake: `spark.read.format("delta").load()`
* Crear desde Pandas: `spark.createDataFrame(pandas_df)`
* Crear desde listas: `spark.createDataFrame(data, schema)`

**Comparación de formatos:**
```python
# CSV (lento, sin schema)
df_csv = spark.read.csv('ventas.csv', header=True, inferSchema=True)

# Parquet (rápido, con schema, comprimido)
df_parquet = spark.read.parquet('ventas.parquet')

# Delta (Parquet + ACID + time travel)
df_delta = spark.read.format('delta').load('ventas_delta')
```

**Resultado:** Dominio de ingestión de datos desde cualquier fuente

---

### 11_04_Transformaciones_Basicas_Select_Filter
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* `.select()`: seleccionar columnas
* `.filter()` / `.where()`: filtrar filas
* `.withColumn()`: crear/modificar columnas
* `.withColumnRenamed()`: renombrar columnas
* `.drop()`: eliminar columnas
* Funciones de columna: `col()`, `lit()`, `when()`
* Operadores: `&`, `|`, `~` para AND, OR, NOT

**Patrones comunes:**
```python
from pyspark.sql.functions import col, lit, when

# Selección y filtrado
df_filtered = (df
    .select('cliente_id', 'fecha', 'monto')
    .filter(col('monto') > 1000)
)

# Crear columna derivada
df_with_segment = df.withColumn(
    'segmento',
    when(col('monto') > 5000, 'Premium')
    .when(col('monto') > 1000, 'Standard')
    .otherwise('Basic')
)

# Renombrar
df_renamed = df.withColumnRenamed('monto', 'revenue')
```

**Resultado:** Capacidad de transformar DataFrames con código legible

---

### 11_05_Acciones_Show_Count_Collect
**Duración:** 50 min | **Dificultad:** Principiante

**Temas:**
* `.show()`: vista previa (10 filas por defecto)
* `.count()`: contar filas (acción costosa)
* `.collect()`: traer todo a driver (⚠️ peligroso con big data)
* `.take(n)`: primeras n filas
* `.first()`: primera fila
* `.display()`: visualización en Databricks (recomendado)
* `.write.format().save()`: escribir resultados

**⚠️ Cuidado con Collect:**
```python
# ❌ NUNCA hagas esto con big data
all_rows = df.collect()  # Puede crashear el driver si df tiene GB/TB

# ✅ Usa límites
sample = df.limit(100).collect()  # Seguro

# ✅ O agrega primero
aggregated = df.groupBy('region').count()  # Resultado pequeño
result = aggregated.collect()  # Seguro
```

**Resultado:** Uso responsable de acciones según tamaño de datos

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Nombrar componentes de arquitectura Spark (driver, executor, partition)
* Listar diferencia entre transformación y acción
* Identificar formatos de datos optimizados (Parquet, Delta)

### Nivel 2: Comprensión
* Explicar qué es lazy evaluation y sus beneficios
* Describir cuándo usar `.show()` vs `.collect()` vs `.display()`
* Interpretar un plan de ejecución de Spark

### Nivel 3: Aplicación
* Crear DataFrames desde CSV, Parquet, Delta
* Aplicar transformaciones: select, filter, withColumn
* Leer y escribir datos en múltiples formatos
* Configurar SparkSession para casos específicos

### Nivel 4: Análisis
* Evaluar performance de diferentes formatos (CSV vs Parquet)
* Decidir número óptimo de particiones para un dataset
* Comparar cuándo usar Pandas vs PySpark según tamaño de datos

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Migración de Pandas a PySpark
```
"Tengo este código en Pandas:

df = pd.read_csv('ventas.csv')
df_filtered = df[df['monto'] > 1000]
df_grouped = df_filtered.groupby('region').agg({'monto': 'sum'})
df_sorted = df_grouped.sort_values('monto', ascending=False)

Migra este código a PySpark manteniendo la misma lógica.
Explica las diferencias clave entre ambas versiones.
Sugiere optimizaciones específicas de PySpark."
```

### Prompt 2: Pipeline de Lectura Multi-Formato
```
"Crea un pipeline PySpark que:
1. Lee 'ventas.csv' (con header, infiere schema)
2. Lee 'clientes.parquet'
3. Lee 'productos.json'
4. Une las 3 fuentes en un solo DataFrame
5. Filtra transacciones del último mes
6. Calcula revenue total por cliente
7. Escribe resultado en formato Delta en 'output/ventas_consolidadas'

Muestra schema de cada DataFrame intermedio.
Explica por qué Delta es mejor que Parquet para este caso."
```

### Prompt 3: Análisis de Performance
```
"Tengo un DataFrame de 500M filas con columnas:
- fecha (date)
- cliente_id (int)
- monto (double)
- region (string)

Necesito:
1. Filtrar últimos 90 días
2. Agrupar por región y calcular sum(monto)
3. Ordenar por monto descendente

Genera el código PySpark optimizado.
Explica:
- Por qué es importante el orden de operaciones (filter antes de agg)
- Cuántas particiones recomiendas
- Si debería cachear algún DataFrame intermedio
- Cómo verificar el plan de ejecución (explain())"
```

---

## 🔧 Solución de Problemas

### Problema 1: AnalysisException - tabla o columna no encontrada
**Causa:** Typo en nombre de columna o tabla  
**Solución:** Verifica schema exacto
```python
# Ver schema completo
df.printSchema()

# Ver nombres de columnas
print(df.columns)

# Buscar columna por patrón
[col for col in df.columns if 'fecha' in col.lower()]
```

### Problema 2: Py4JJavaError al leer archivo
**Causa:** Ruta incorrecta o formato incompatible  
**Solución:** Verifica ruta y formato
```python
# Listar archivos en directorio
dbutils.fs.ls('/path/to/data/')

# Probar lectura con manejo de errores
try:
    df = spark.read.parquet('/path/to/file.parquet')
except Exception as e:
    print(f"Error: {e}")
```

### Problema 3: OutOfMemoryError al hacer collect()
**Causa:** Intentando traer demasiados datos al driver  
**Solución:** Usa límites o agregaciones
```python
# ❌ MALO
df.collect()  # 10GB de datos

# ✅ BUENO - opción 1: límite
df.limit(1000).collect()

# ✅ BUENO - opción 2: agregación
df.groupBy('categoria').count().collect()
```

### Problema 4: Performance lenta en joins
**Causa:** Particiones mal distribuidas o skew  
**Solución:** Repartition o broadcast
```python
# Para DataFrames grandes
df_large.repartition(200, 'join_key')

# Para DataFrame pequeño (< 10MB)
from pyspark.sql.functions import broadcast
df_result = df_large.join(broadcast(df_small), 'join_key')
```

### Problema 5: Schema inference toma mucho tiempo en CSV
**Causa:** Spark lee todo el archivo para inferir tipos  
**Solución:** Define schema explícitamente
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

schema = StructType([
    StructField("cliente_id", IntegerType(), True),
    StructField("nombre", StringType(), True),
    StructField("monto", DoubleType(), True)
])

df = spark.read.csv('ventas.csv', header=True, schema=schema)
```

---

## 📖 Recursos Adicionales

### Documentación Oficial
* [PySpark API](https://spark.apache.org/docs/latest/api/python/)
* [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
* [Databricks PySpark Guide](https://docs.databricks.com/pyspark/index.html)

### Libros Recomendados
* "Learning Spark" (2nd Edition) - Databricks
* "Spark: The Definitive Guide" - Matei Zaharia
* "High Performance Spark" - Holden Karau

### Artículos
* [When to use Pandas vs PySpark](https://databricks.com/blog/2023/pandas-pyspark)
* [PySpark Best Practices](https://databricks.com/blog/pyspark-best-practices)

---

## ✅ Checklist de Completitud

**Arquitectura Spark:**
- [ ] Entender driver vs executors
- [ ] Diferenciar transformación vs acción
- [ ] Explicar lazy evaluation
- [ ] Interpretar DAG de ejecución

**SparkSession:**
- [ ] Verificar versión de Spark
- [ ] Acceder a configuración
- [ ] Modificar configuración de sesión
- [ ] Entender limitaciones serverless

**Lectura de Datos:**
- [ ] Leer CSV con opciones
- [ ] Leer Parquet
- [ ] Leer Delta Lake
- [ ] Crear desde Pandas
- [ ] Definir schema explícito

**Transformaciones:**
- [ ] select() columnas
- [ ] filter() con condiciones complejas
- [ ] withColumn() crear columnas derivadas
- [ ] withColumnRenamed() renombrar
- [ ] Usar when() para lógica condicional

**Acciones:**
- [ ] show() vs display()
- [ ] count() filas
- [ ] take(n) vs collect()
- [ ] write() en múltiples formatos

**Ejercicios:**
- [ ] Migrar código Pandas → PySpark
- [ ] Pipeline multi-formato
- [ ] Optimizar query con explain()

---

## 🚀 Próximo Módulo

**➡️ [Módulo 12: PySpark Transformación Avanzada](../12_PySpark_Transformacion_Avanzada/)**

Aprende joins, agregaciones, window functions y UDFs.

---

[📖 Volver al Índice](../README.md)
