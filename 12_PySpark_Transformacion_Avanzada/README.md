# 🔄 Módulo 12: PySpark Transformación Avanzada

## 🎯 Objetivo del Módulo

**Domina técnicas avanzadas de transformación** para análisis complejos con joins, agregaciones, window functions y UDFs.

Este módulo te lleva de operaciones básicas a **transformaciones de nivel producción** que encontrarás en pipelines de datos empresariales.

**Al finalizar este módulo podrás:**
* ✅ Ejecutar joins complejos (inner, left, right, cross, anti, semi)
* ✅ Aplicar agregaciones con groupBy y funciones de agregación
* ✅ Usar window functions para cálculos por partición
* ✅ Crear y usar User Defined Functions (UDFs)
* ✅ Trabajar con arrays, structs y datos semi-estructurados
* ✅ Implementar transformaciones encadenadas eficientes

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 11 (PySpark Core) completado
* Módulos 03-06 (Pandas, Agregaciones) para comparación
* SQL intermedio (joins, group by, subqueries)

**Datasets:**
* `ventas_retail.csv`
* `transacciones_financieras.parquet`

**Tiempo estimado:** 4.5 horas

---

## 📚 Contenido del Módulo

### 12_01_Joins_Tipos_y_Estrategias
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* Tipos de joins: inner, left, right, full outer, cross
* Joins especiales: left_semi, left_anti
* Múltiples condiciones de join
* Broadcast joins para tablas pequeñas
* Join strategies: shuffle hash join vs broadcast join

**Patrones comunes:**
```python
# Inner join simple
df_result = df_ventas.join(df_clientes, 'cliente_id', 'inner')

# Left join con múltiples condiciones
df_result = df_ventas.join(
    df_productos,
    (df_ventas.producto_id == df_productos.id) & 
    (df_ventas.fecha >= df_productos.fecha_valida),
    'left'
)

# Broadcast join (tabla pequeña)
from pyspark.sql.functions import broadcast
df_result = df_large.join(broadcast(df_small), 'key')

# Left semi (solo filas que hacen match)
df_result = df_clientes.join(df_compras, 'cliente_id', 'left_semi')

# Left anti (filas sin match - clientes sin compras)
df_result = df_clientes.join(df_compras, 'cliente_id', 'left_anti')
```

**Resultado:** Dominio de joins para cualquier caso de negocio

---

### 12_02_GroupBy_y_Agregaciones_Complejas
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* `.groupBy()` con una o múltiples columnas
* Funciones de agregación: sum, avg, count, min, max, stddev
* `.agg()` con múltiples agregaciones
* Agregaciones con alias
* Agregaciones condicionales con `when()`
* Cube y rollup para subtotales

**Ejemplos:**
```python
from pyspark.sql.functions import sum, avg, count, max, min, stddev, col, when

# Agregación simple
df_agg = df.groupBy('region').agg(
    sum('monto').alias('revenue_total'),
    avg('monto').alias('ticket_promedio'),
    count('transaccion_id').alias('num_transacciones')
)

# Agregación con múltiples dimensiones
df_agg = df.groupBy('region', 'categoria').agg(
    sum('monto').alias('revenue'),
    count('*').alias('qty')
)

# Agregación condicional
df_agg = df.groupBy('cliente_id').agg(
    sum(when(col('monto') > 1000, 1).otherwise(0)).alias('compras_premium'),
    sum(when(col('categoria') == 'Electronics', col('monto')).otherwise(0)).alias('gasto_electronics')
)

# Rollup para subtotales jerárquicos
df_rollup = df.rollup('region', 'categoria').agg(sum('monto').alias('revenue'))
```

**Resultado:** Capacidad de generar métricas complejas eficientemente

---

### 12_03_Window_Functions_Particiones
**Duración:** 70 min | **Dificultad:** Avanzado

**Temas:**
* Window functions: qué son y cuándo usarlas
* `Window.partitionBy()`, `Window.orderBy()`
* Funciones de ranking: row_number, rank, dense_rank
* Funciones de analítica: lag, lead, first, last
* Funciones de agregación en ventana: sum, avg, count
* Frames: rowsBetween, rangeBetween

**Casos de uso:**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead, sum, avg

# Ranking por partición
window_spec = Window.partitionBy('categoria').orderBy(col('monto').desc())
df_ranked = df.withColumn('rank', rank().over(window_spec))

# Top N por grupo
df_top3 = df_ranked.filter(col('rank') <= 3)

# Comparación con periodo anterior (lag)
window_time = Window.partitionBy('producto_id').orderBy('fecha')
df_growth = df.withColumn(
    'monto_mes_anterior',
    lag('monto', 1).over(window_time)
).withColumn(
    'growth_pct',
    ((col('monto') - col('monto_mes_anterior')) / col('monto_mes_anterior') * 100)
)

# Running total
window_cumsum = Window.partitionBy('cliente_id').orderBy('fecha').rowsBetween(Window.unboundedPreceding, Window.currentRow)
df_cumsum = df.withColumn('revenue_acumulado', sum('monto').over(window_cumsum))

# Moving average (últimas 7 filas)
window_ma = Window.partitionBy('producto_id').orderBy('fecha').rowsBetween(-6, 0)
df_ma = df.withColumn('ma_7d', avg('cantidad').over(window_ma))
```

**Resultado:** Análisis temporales y de ranking complejos

---

### 12_04_User_Defined_Functions_UDFs
**Duración:** 60 min | **Dificultad:** Intermedio-Avanzado

**Temas:**
* Crear UDFs con decorator `@udf`
* Especificar return type
* UDFs con múltiples parámetros
* Pandas UDFs (vectorizadas, más rápidas)
* Cuándo usar UDFs vs funciones nativas

**⚠️ Importante:** UDFs son lentas, usa funciones nativas cuando sea posible.

**Ejemplos:**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, DoubleType

# UDF simple
@udf(returnType=StringType())
def categorizar_monto(monto):
    if monto > 5000:
        return 'Premium'
    elif monto > 1000:
        return 'Standard'
    else:
        return 'Basic'

df_categorized = df.withColumn('segmento', categorizar_monto(col('monto')))

# UDF con múltiples parámetros
@udf(returnType=DoubleType())
def calcular_descuento(monto, categoria):
    if categoria == 'VIP':
        return monto * 0.20
    elif categoria == 'Premium':
        return monto * 0.10
    else:
        return 0.0

df_discount = df.withColumn(
    'descuento',
    calcular_descuento(col('monto'), col('categoria_cliente'))
)

# Pandas UDF (vectorizada - MÁS RÁPIDA)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(DoubleType())
def calcular_margen_vectorized(costo: pd.Series, precio: pd.Series) -> pd.Series:
    return ((precio - costo) / precio * 100)

df_margin = df.withColumn('margen_pct', calcular_margen_vectorized(col('costo'), col('precio')))
```

**Resultado:** Capacidad de implementar lógica custom eficientemente

---

### 12_05_Arrays_Structs_y_Datos_Semiestructurados
**Duración:** 65 min | **Dificultad:** Avanzado

**Temas:**
* Trabajar con columnas de tipo array
* Funciones de array: explode, array_contains, array_distinct, size
* Structs: crear y acceder a campos anidados
* Flatten de estructuras anidadas
* Explode vs posexplode
* JSON parsing con `from_json()` y `to_json()`

**Casos de uso:**
```python
from pyspark.sql.functions import explode, array_contains, struct, col, from_json, to_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# Explode array (una fila por elemento)
df_exploded = df.withColumn('producto', explode(col('productos_array')))

# Verificar si array contiene elemento
df_filtered = df.filter(array_contains(col('categorias'), 'Electronics'))

# Crear struct (registro anidado)
df_struct = df.withColumn(
    'cliente_info',
    struct(col('cliente_id'), col('nombre'), col('email'))
)

# Acceder a campo de struct
df_extract = df.select(col('cliente_info.nombre'))

# Parsear JSON string a struct
json_schema = StructType([
    StructField('producto_id', IntegerType()),
    StructField('nombre', StringType())
])
df_parsed = df.withColumn('producto_obj', from_json(col('producto_json'), json_schema))

# Flatten nested structure
df_flat = df.select(
    'transaccion_id',
    col('cliente.nombre').alias('cliente_nombre'),
    col('cliente.email').alias('cliente_email'),
    explode(col('items')).alias('item')
).select(
    'transaccion_id',
    'cliente_nombre',
    'cliente_email',
    col('item.producto_id'),
    col('item.cantidad'),
    col('item.precio')
)
```

**Resultado:** Manejo de datos semi-estructurados y anidados

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar tipos de joins disponibles
* Nombrar funciones de agregación estándar
* Identificar diferencia entre UDF y Pandas UDF

### Nivel 2: Comprensión
* Explicar cuándo usar broadcast join
* Describir cómo funcionan window functions
* Interpretar resultados de rollup/cube

### Nivel 3: Aplicación
* Ejecutar joins complejos con múltiples condiciones
* Crear agregaciones con múltiples métricas
* Aplicar window functions para rankings y running totals
* Implementar UDFs custom

### Nivel 4: Análisis
* Decidir tipo de join óptimo según caso de uso
* Evaluar cuándo usar UDF vs funciones nativas
* Optimizar window functions con frames apropiados

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Pipeline de Agregación Multi-Nivel
```
"Tengo dos DataFrames:
- df_ventas: transaccion_id, fecha, cliente_id, producto_id, monto, cantidad
- df_productos: producto_id, nombre, categoria, costo_unitario

Genera un análisis que:
1. Haga LEFT JOIN para enriquecer ventas con info de productos
2. Calcule margen bruto: (monto - (cantidad * costo_unitario))
3. Agrupe por categoria y mes (extraer mes de fecha)
4. Calcule: revenue total, margen bruto total, margen bruto %, unidades vendidas
5. Ordene por revenue descendente
6. Agregue ranking dentro de cada mes (rank por revenue)

Muestra el código completo con nombres de columnas claros."
```

### Prompt 2: Análisis de Cohortes con Window Functions
```
"Tengo DataFrame de transacciones con: cliente_id, fecha, monto.

Calcula métricas de cohorte:
1. Para cada cliente, identifica su mes de primera compra (cohorte)
2. Calcula meses desde primera compra para cada transacción
3. Agrupa por cohorte y 'meses_desde_primera_compra'
4. Calcula: # clientes activos, revenue total, revenue promedio por cliente
5. Calcula retention rate: (clientes en mes N / clientes en mes 0) * 100

Usa window functions para:
- Identificar primera compra por cliente
- Calcular running retention

Visualiza resultado en formato cohort table."
```

### Prompt 3: Pipeline con UDFs para Segmentación
```
"Necesito segmentar clientes con lógica custom compleja:

Reglas de segmentación:
- VIP: > 10 compras Y monto_promedio > $5000 Y última_compra < 30 días
- Premium: > 5 compras Y monto_promedio > $2000 Y última_compra < 90 días
- Standard: resto de clientes con al menos 1 compra
- Inactivo: última_compra > 90 días

Genera código que:
1. Agregue métricas por cliente (num_compras, monto_promedio, días_ultima_compra)
2. Cree UDF o use when() para aplicar reglas de segmentación
3. Calcule distribución de clientes por segmento
4. Calcule revenue total y LTV promedio por segmento

¿Recomiendas UDF o when() para este caso? ¿Por qué?"
```

---

## 🔧 Solución de Problemas

### Problema 1: Ambiguous column after join
**Causa:** Ambas tablas tienen columnas con el mismo nombre  
**Solución:** Usa alias y especifica tabla
```python
# ❌ MALO
df_result = df1.join(df2, 'id')
df_result.select('id', 'nombre')  # ¿De cuál tabla?

# ✅ BUENO
df_result = df1.alias('a').join(df2.alias('b'), col('a.id') == col('b.id'))
df_result.select('a.id', 'a.nombre', 'b.nombre')
```

### Problema 2: UDF muy lenta
**Causa:** UDFs normales no son vectorizadas  
**Solución:** Usa Pandas UDF o funciones nativas
```python
# ❌ LENTO - UDF normal
@udf(returnType=DoubleType())
def calc_margin(precio, costo):
    return (precio - costo) / precio

# ✅ RÁPIDO - Pandas UDF
@pandas_udf(DoubleType())
def calc_margin_fast(precio: pd.Series, costo: pd.Series) -> pd.Series:
    return (precio - costo) / precio

# ✅ MÁS RÁPIDO - Función nativa
df.withColumn('margin', (col('precio') - col('costo')) / col('precio'))
```

### Problema 3: Window function muy lenta
**Causa:** Partición muy grande o frame mal configurado  
**Solución:** Optimiza partición y frame
```python
# ❌ LENTO - sin partición (procesa todo junto)
window = Window.orderBy('fecha')

# ✅ RÁPIDO - con partición
window = Window.partitionBy('producto_id').orderBy('fecha')

# Frame óptimo para moving average
window = Window.partitionBy('id').orderBy('fecha').rowsBetween(-6, 0)
```

### Problema 4: Explode genera demasiadas filas
**Causa:** Arrays muy grandes en cada fila  
**Solución:** Filtra antes o usa lateral view
```python
# Filtra antes de explode
df_filtered = df.filter(size(col('items_array')) < 100)
df_exploded = df_filtered.select('*', explode('items_array').alias('item'))
```

---

## 📖 Recursos Adicionales

### Documentación
* [PySpark SQL Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
* [Window Functions Guide](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-window.html)
* [PySpark UDFs](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html)

### Artículos
* [When to Use Broadcast Joins](https://databricks.com/blog/broadcast-joins)
* [Window Functions in PySpark](https://databricks.com/blog/window-functions-pyspark)

---

## ✅ Checklist

**Joins:**
- [ ] Inner, left, right, full outer
- [ ] Left semi, left anti
- [ ] Broadcast join para tablas pequeñas
- [ ] Múltiples condiciones de join

**Agregaciones:**
- [ ] groupBy con múltiples columnas
- [ ] agg() con múltiples funciones
- [ ] Agregaciones condicionales
- [ ] Rollup y cube

**Window Functions:**
- [ ] row_number, rank, dense_rank
- [ ] lag, lead
- [ ] Running totals con rowsBetween
- [ ] Moving averages

**UDFs:**
- [ ] UDF básico con @udf
- [ ] Pandas UDF vectorizado
- [ ] Comparar performance UDF vs nativo

**Semi-estructurados:**
- [ ] explode arrays
- [ ] Structs y campos anidados
- [ ] from_json y to_json

---

## 🚀 Próximo Módulo

**➡️ [Módulo 13: PySpark SQL, Window Functions y Delta Lake](../13_PySpark_SQL_Window_DeltaLake/)**

---

[📖 Volver al Índice](../README.md)
