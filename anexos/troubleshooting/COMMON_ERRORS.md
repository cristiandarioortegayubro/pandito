# 🔧 Guía de Troubleshooting - Saliendo de lo Pandito v4

**Soluciones a errores comunes en Databricks, Pandas, PySpark y SQL**

---

## 📚 Índice por Categoría

1. [Errores de Pandas](#pandas-errors)
2. [Errores de PySpark](#pyspark-errors)
3. [Errores de SQL](#sql-errors)
4. [Errores de Databricks](#databricks-errors)
5. [Errores de Python](#python-errors)
6. [Errores de Performance](#performance-errors)

---

<a name="pandas-errors"></a>
## 🐼 Errores de Pandas

### KeyError: 'columna_no_existe'

**Error:**
```python
KeyError: 'ventas'
```

**Causa:** Intentas acceder a una columna que no existe en el DataFrame.

**Soluciones:**
```python
# ✅ Ver todas las columnas
print(df.columns.tolist())

# ✅ Verificar si existe antes
if 'ventas' in df.columns:
    resultado = df['ventas'].sum()

# ✅ Usar get() con valor por defecto
valor = df.get('ventas', pd.Series([0]))
```

---

### ValueError: cannot reindex from a duplicate axis

**Error:**
```python
ValueError: cannot reindex from a duplicate axis
```

**Causa:** El DataFrame tiene índices duplicados.

**Soluciones:**
```python
# ✅ Resetear índice
df = df.reset_index(drop=True)

# ✅ Eliminar duplicados
df = df[~df.index.duplicated(keep='first')]

# ✅ Verificar duplicados
print(df.index.duplicated().sum())
```

---

### TypeError: unsupported operand type(s) for +: 'int' and 'str'

**Error:**
```python
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Causa:** Intentas operar entre tipos incompatibles.

**Soluciones:**
```python
# ✅ Ver tipos de datos
print(df.dtypes)

# ✅ Convertir tipo
df['columna'] = df['columna'].astype('float')
df['columna'] = pd.to_numeric(df['columna'], errors='coerce')

# ✅ Limpiar y convertir
df['precio'] = df['precio'].str.replace('$', '').str.replace(',', '').astype('float')
```

---

### SettingWithCopyWarning

**Warning:**
```python
SettingWithCopyWarning: A value is trying to be set on a copy of a slice
```

**Causa:** Modificas una vista del DataFrame en lugar del DataFrame original.

**Soluciones:**
```python
# ❌ Incorrecto
df_filtrado = df[df['edad'] > 30]
df_filtrado['nueva_col'] = 100  # Warning!

# ✅ Correcto: Usar .copy()
df_filtrado = df[df['edad'] > 30].copy()
df_filtrado['nueva_col'] = 100

# ✅ Correcto: Usar .loc
df.loc[df['edad'] > 30, 'nueva_col'] = 100
```

---

### ValueError: Length mismatch: Expected axis has X elements, new values have Y elements

**Error:**
```python
ValueError: Length mismatch: Expected axis has 100 elements, new values have 50 elements
```

**Causa:** Intentas asignar una lista/array con tamaño diferente al DataFrame.

**Soluciones:**
```python
# ✅ Verificar longitudes
print(f"DataFrame: {len(df)}, Nueva lista: {len(nueva_lista)}")

# ✅ Usar valores escalares o alinear tamaños
df['nueva_col'] = 0  # Escalar funciona

# ✅ Para arrays, asegurarse de mismo tamaño
if len(nueva_lista) == len(df):
    df['nueva_col'] = nueva_lista
```

---

<a name="pyspark-errors"></a>
## ⚡ Errores de PySpark

### AnalysisException: cannot resolve column name

**Error:**
```python
AnalysisException: cannot resolve '`columna_incorrecta`' given input columns: [col1, col2, col3]
```

**Causa:** La columna no existe en el DataFrame.

**Soluciones:**
```python
# ✅ Ver columnas disponibles
df.printSchema()
print(df.columns)

# ✅ Usar nombres correctos (case-sensitive)
df.select("Col1")  # ❌ Falla si la columna es "col1"
df.select("col1")  # ✅ Correcto

# ✅ Verificar antes de usar
if 'columna' in df.columns:
    df.select('columna')
```

---

### Py4JJavaError: OutOfMemoryError

**Error:**
```python
Py4JJavaError: An error occurred while calling o123.showString.
: java.lang.OutOfMemoryError: Java heap space
```

**Causa:** El cluster se queda sin memoria.

**Soluciones:**
```python
# ✅ No uses .collect() en DataFrames grandes
# ❌ Incorrecto
resultado = df.collect()  # Carga TODO en memoria

# ✅ Correcto: Usar .show() o escribir a disco
df.show(20)
df.write.parquet('/output/path')

# ✅ Filtrar antes de collect()
df.filter(F.col('fecha') == '2024-01-01').collect()

# ✅ Aumentar particiones
df = df.repartition(200)

# ✅ Liberar cache
df.unpersist()
```

---

### AnalysisException: Path does not exist

**Error:**
```python
AnalysisException: Path does not exist: /path/to/file
```

**Causa:** La ruta del archivo no existe o es incorrecta.

**Soluciones:**
```python
# ✅ Verificar ruta
import os
print(os.path.exists('/path/to/file'))

# ✅ Usar rutas correctas en Databricks
# ❌ Incorrecto en Free Edition
df = spark.read.parquet('/dbfs/mnt/data/')

# ✅ Correcto: Usar workspace paths
df = spark.read.parquet('/Workspace/Users/tu_usuario/data/')

# ✅ Listar archivos
dbutils.fs.ls('/Workspace/Users/tu_usuario/')
```

---

### pyspark.sql.utils.StreamingQueryException

**Error:**
```python
StreamingQueryException: Query [id = ...] terminated with exception
```

**Causa:** Error en streaming query.

**Soluciones:**
```python
# ✅ Revisar logs
query.exception()

# ✅ Agregar checkpoint location
query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start("/output/path")

# ✅ Manejo de errores
try:
    query.awaitTermination()
except KeyboardInterrupt:
    query.stop()
```

---

### TypeError: 'Column' object is not callable

**Error:**
```python
TypeError: 'Column' object is not callable
```

**Causa:** Sintaxis incorrecta al usar funciones de columna.

**Soluciones:**
```python
# ❌ Incorrecto
df.filter(F.col('edad')(> 30))  # Paréntesis extra

# ✅ Correcto
df.filter(F.col('edad') > 30)

# ❌ Incorrecto
df.select(F.sum('ventas')())

# ✅ Correcto
df.select(F.sum('ventas'))
```

---

<a name="sql-errors"></a>
## 🗄️ Errores de SQL

### AnalysisException: Table or view not found

**Error:**
```sql
AnalysisException: Table or view not found: `tabla_no_existe`
```

**Causa:** La tabla no existe o no tienes permisos.

**Soluciones:**
```sql
-- ✅ Listar tablas disponibles
SHOW TABLES IN catalog.schema;

-- ✅ Verificar catálogo actual
SELECT current_catalog(), current_schema();

-- ✅ Usar nombre completo
SELECT * FROM catalog.schema.tabla;

-- ✅ Verificar permisos
SHOW GRANTS ON TABLE catalog.schema.tabla;
```

---

### SemanticException: Column ambiguously defined

**Error:**
```sql
SemanticException: Column 'id' is ambiguous
```

**Causa:** Dos tablas en el JOIN tienen columnas con el mismo nombre.

**Soluciones:**
```sql
-- ❌ Incorrecto
SELECT id, nombre
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id;

-- ✅ Correcto: Usar alias
SELECT v.id, c.nombre
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id;
```

---

### ParseException: mismatched input

**Error:**
```sql
ParseException: mismatched input 'GROUP' expecting <EOF>
```

**Causa:** Sintaxis SQL incorrecta.

**Soluciones:**
```sql
-- ❌ Falta FROM
SELECT categoria, SUM(ventas)
GROUP BY categoria;

-- ✅ Correcto
SELECT categoria, SUM(ventas)
FROM ventas
GROUP BY categoria;

-- ❌ Orden incorrecto
SELECT categoria
GROUP BY categoria
FROM ventas;

-- ✅ Correcto: FROM → WHERE → GROUP BY → HAVING → ORDER BY
SELECT categoria, SUM(ventas) as total
FROM ventas
WHERE fecha >= '2024-01-01'
GROUP BY categoria
HAVING SUM(ventas) > 1000
ORDER BY total DESC;
```

---

<a name="databricks-errors"></a>
## 🧱 Errores de Databricks

### RESOURCE_DOES_NOT_EXIST: Cluster does not exist

**Error:**
```
RESOURCE_DOES_NOT_EXIST: Cluster XXX does not exist
```

**Causa:** El cluster fue eliminado o está en otro workspace.

**Soluciones:**
```python
# ✅ Usar Serverless (recomendado)
# No requiere configuración de cluster

# ✅ Verificar cluster activo
%sh
databricks clusters list

# ✅ Crear nuevo cluster si es necesario
# En Free Edition, usar Serverless automáticamente
```

---

### REQUEST_LIMIT_EXCEEDED: Too many requests

**Error:**
```
REQUEST_LIMIT_EXCEEDED: Too many requests
```

**Causa:** Demasiadas peticiones simultáneas a la API.

**Soluciones:**
```python
# ✅ Agregar delays entre requests
import time
for item in items:
    procesar(item)
    time.sleep(1)  # Esperar 1 segundo

# ✅ Usar batch operations
# En lugar de 100 requests individuales, hacer 1 batch
```

---

### ImportError: No module named 'libreria'

**Error:**
```python
ImportError: No module named 'geopandas'
```

**Causa:** La librería no está instalada en el cluster.

**Soluciones:**
```python
# ✅ Instalar con pip
%pip install geopandas

# ✅ Para múltiples librerías
%pip install geopandas h3 plotly

# ✅ Reiniciar Python después de instalar
dbutils.library.restartPython()
```

---

<a name="python-errors"></a>
## 🐍 Errores de Python

### IndentationError: unexpected indent

**Error:**
```python
IndentationError: unexpected indent
```

**Causa:** Indentación incorrecta (mezcla de tabs y espacios).

**Soluciones:**
```python
# ❌ Incorrecto (mezcla tabs y espacios)
def funcion():
    if True:
        print("hola")  # 4 espacios
	print("mundo")  # Tab

# ✅ Correcto: Siempre 4 espacios
def funcion():
    if True:
        print("hola")
        print("mundo")
```

---

### NameError: name 'variable' is not defined

**Error:**
```python
NameError: name 'df' is not defined
```

**Causa:** Intentas usar una variable antes de definirla.

**Soluciones:**
```python
# ✅ Definir variables antes de usar
df = pd.DataFrame({'a': [1, 2, 3]})
print(df)

# ✅ Verificar si está definida
try:
    print(df)
except NameError:
    print("df no está definido")

# ✅ En notebooks: ejecutar celdas en orden
```

---

### AttributeError: 'NoneType' object has no attribute 'X'

**Error:**
```python
AttributeError: 'NoneType' object has no attribute 'sum'
```

**Causa:** Una variable es None en lugar del objeto esperado.

**Soluciones:**
```python
# ✅ Verificar None antes de usar
if df is not None:
    resultado = df.sum()

# ✅ Usar get() con default
resultado = getattr(df, 'sum', lambda: 0)()

# ✅ Debugging: imprimir tipo
print(type(df))  # <class 'NoneType'>
```

---

<a name="performance-errors"></a>
## ⚡ Problemas de Performance

### Query muy lenta

**Síntoma:** La consulta tarda minutos u horas.

**Soluciones:**

```python
# ✅ 1. Filtrar temprano (pushdown predicates)
# ❌ Lento
df = spark.table('tabla_gigante')
df_filtrado = df.filter(F.col('fecha') == '2024-01-01')

# ✅ Rápido: Filtrar primero
df = spark.table('tabla_gigante').filter(F.col('fecha') == '2024-01-01')

# ✅ 2. Seleccionar solo columnas necesarias
# ❌ Lento
df = spark.table('tabla').filter(...).select('col1', 'col2')

# ✅ Rápido
df = spark.table('tabla').select('col1', 'col2').filter(...)

# ✅ 3. Usar broadcast para tablas pequeñas
from pyspark.sql.functions import broadcast
df_grande.join(broadcast(df_pequeña), 'id')

# ✅ 4. Particionar datos
df.write.partitionBy('año', 'mes').parquet('/output')

# ✅ 5. Cachear si se reutiliza múltiples veces
df.cache()
df.count()  # Materializar cache
```

---

### Out of Memory

**Síntoma:** El notebook/cluster se queda sin memoria.

**Soluciones:**

```python
# ✅ 1. No uses .collect() en DataFrames grandes
# ❌ Malo
all_data = df.collect()  # Carga TODO en memoria

# ✅ Bueno: Procesar en chunks
df.write.parquet('/output')

# ✅ 2. Liberar memoria
import gc
del df_gigante
gc.collect()

# ✅ 3. Aumentar particiones
df = df.repartition(200)

# ✅ 4. Evitar Pandas para datasets grandes
# Usar PySpark en lugar de pandas_df = spark_df.toPandas()

# ✅ 5. Limpiar cache
spark.catalog.clearCache()
df.unpersist()
```

---

## 🔍 Técnicas de Debugging

### Ver plan de ejecución (PySpark)
```python
# Ver plan lógico y físico
df.explain(True)

# Ver solo plan físico
df.explain()
```

### Inspeccionar datos intermedios
```python
# Tomar muestra pequeña
df.show(5)
df.limit(10).toPandas()

# Contar sin traer datos
df.count()

# Ver esquema
df.printSchema()
```

### Logging de errores
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    resultado = procesar_datos(df)
except Exception as e:
    logger.error(f"Error procesando datos: {e}")
    raise
```

---

## 📚 Recursos Adicionales

* **Databricks KB:** https://kb.databricks.com/
* **Stack Overflow:** https://stackoverflow.com/questions/tagged/databricks
* **Pandas Docs:** https://pandas.pydata.org/docs/user_guide/index.html
* **PySpark Docs:** https://spark.apache.org/docs/latest/api/python/

---

## 💡 Tips Generales

1. **Lee el mensaje de error completo** - La última línea suele tener la causa
2. **Google el error exacto** - Entre comillas para búsqueda exacta
3. **Usa Genie Code** - Pégale el error y te dará soluciones
4. **Simplifica el problema** - Prueba con datos pequeños primero
5. **Revisa la documentación** - Muchos errores son por sintaxis incorrecta

---

**🧞 Recuerda:** Cuando tengas un error, ¡pregúntale a Genie Code! Es tu debugging assistant 24/7.

_Última actualización: 2026-07-29_
