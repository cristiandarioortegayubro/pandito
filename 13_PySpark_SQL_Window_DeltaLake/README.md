# 🗄️ Módulo 13: PySpark SQL, Window Functions y Delta Lake

## 🎯 Objetivo del Módulo

**Domina SQL en PySpark y Delta Lake** para análisis avanzados con ACID transactions, time travel y optimizaciones de lakehouse.

Delta Lake es el **formato estándar de Databricks** que combina la simplicidad de data lakes con la confiabilidad de data warehouses.

**Al finalizar este módulo podrás:**
* ✅ Escribir queries SQL complejas en PySpark
* ✅ Usar CTEs, subqueries y consultas anidadas
* ✅ Aplicar window functions avanzadas en SQL
* ✅ Crear, leer y actualizar tablas Delta Lake
* ✅ Usar time travel para auditoría y rollback
* ✅ Optimizar tablas Delta con OPTIMIZE y Z-ORDER
* ✅ Implementar CDC (Change Data Capture) con MERGE

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 11-12 completados
* SQL intermedio-avanzado
* Conceptos de ACID transactions

**Datasets:**
* Todos los datasets previos
* Se crearán tablas Delta durante el módulo

**Tiempo estimado:** 5 horas

---

## 📚 Contenido del Módulo

### 13_01_SQL_en_PySpark_spark_sql
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* `spark.sql()` para ejecutar queries SQL
* Registrar DataFrames como temp views
* CTEs (Common Table Expressions)
* Subqueries correlacionadas
* Integración DataFrame API ↔ SQL

**Ejemplos:**
```python
# Registrar DataFrame como vista temporal
df.createOrReplaceTempView('ventas')

# Ejecutar SQL
result = spark.sql("""
    SELECT 
        region,
        DATE_TRUNC('month', fecha) as mes,
        SUM(monto) as revenue,
        COUNT(*) as transacciones,
        AVG(monto) as ticket_promedio
    FROM ventas
    WHERE fecha >= '2024-01-01'
    GROUP BY region, DATE_TRUNC('month', fecha)
    ORDER BY mes, revenue DESC
""")

# CTE (WITH clause)
result = spark.sql("""
    WITH ventas_mes AS (
        SELECT 
            cliente_id,
            DATE_TRUNC('month', fecha) as mes,
            SUM(monto) as revenue_mes
        FROM ventas
        GROUP BY cliente_id, mes
    ),
    clientes_activos AS (
        SELECT 
            cliente_id,
            COUNT(DISTINCT mes) as meses_activos,
            SUM(revenue_mes) as revenue_total
        FROM ventas_mes
        GROUP BY cliente_id
    )
    SELECT * FROM clientes_activos
    WHERE meses_activos >= 3
    ORDER BY revenue_total DESC
""")
```

---

### 13_02_Window_Functions_SQL_Avanzado
**Duración:** 60 min | **Dificultad:** Avanzado

**Temas:**
* PARTITION BY, ORDER BY en SQL
* ROW_NUMBER, RANK, DENSE_RANK
* LAG, LEAD para comparaciones temporales
* FIRST_VALUE, LAST_VALUE
* Frames: ROWS BETWEEN, RANGE BETWEEN
* Percentiles con PERCENTILE_CONT

**Casos de uso:**
```sql
-- Top 3 productos por categoría
SELECT *
FROM (
    SELECT 
        producto_id,
        nombre,
        categoria,
        revenue,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY revenue DESC) as rank
    FROM productos_revenue
)
WHERE rank <= 3;

-- Growth MoM con LAG
SELECT 
    mes,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY mes) as revenue_mes_anterior,
    ((revenue - LAG(revenue, 1) OVER (ORDER BY mes)) / 
     LAG(revenue, 1) OVER (ORDER BY mes) * 100) as growth_pct
FROM ventas_mensuales
ORDER BY mes;

-- Running total
SELECT 
    fecha,
    monto,
    SUM(monto) OVER (ORDER BY fecha ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as monto_acumulado
FROM transacciones
ORDER BY fecha;

-- Moving average últimos 7 días
SELECT 
    fecha,
    monto,
    AVG(monto) OVER (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma_7d
FROM ventas_diarias
ORDER BY fecha;
```

---

### 13_03_Introduccion_Delta_Lake_ACID
**Duración:** 65 min | **Dificultad:** Intermedio

**Temas:**
* ¿Qué es Delta Lake? Arquitectura
* ACID transactions en data lakes
* Crear tablas Delta managed y external
* Lectura optimizada con pruning
* Versioning automático
* Transaction log

**Operaciones básicas:**
```python
# Escribir Delta table
df.write.format('delta').mode('overwrite').save('/path/to/delta/ventas')

# Crear tabla managed
df.write.format('delta').saveAsTable('mi_catalogo.mi_schema.ventas')

# Leer Delta table
df_delta = spark.read.format('delta').load('/path/to/delta/ventas')

# Append (INSERT)
df_new.write.format('delta').mode('append').save('/path/to/delta/ventas')

# Overwrite
df_updated.write.format('delta').mode('overwrite').save('/path/to/delta/ventas')

# Overwrite partición específica
df_updated.write.format('delta') \
    .mode('overwrite') \
    .option('replaceWhere', 'fecha >= "2024-01-01" AND fecha < "2024-02-01"') \
    .save('/path/to/delta/ventas')
```

**Ventajas Delta vs Parquet:**
* ✅ ACID transactions
* ✅ Time travel
* ✅ Schema evolution
* ✅ MERGE/UPDATE/DELETE
* ✅ Optimizaciones automáticas

---

### 13_04_Time_Travel_y_Auditoria
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* Consultar versiones históricas
* `VERSION AS OF` y `TIMESTAMP AS OF`
* Restaurar versiones anteriores (RESTORE)
* Ver historial con DESCRIBE HISTORY
* Vacuum para limpiar old versions
* Casos de uso: auditoría, rollback, reproducibilidad

**Ejemplos:**
```sql
-- Ver versión específica
SELECT * FROM ventas VERSION AS OF 5;

-- Ver en timestamp específico
SELECT * FROM ventas TIMESTAMP AS OF '2024-01-15 10:00:00';

-- Comparar versiones
WITH version_actual AS (
    SELECT COUNT(*) as cnt_actual FROM ventas
),
version_anterior AS (
    SELECT COUNT(*) as cnt_anterior FROM ventas VERSION AS OF 10
)
SELECT 
    cnt_actual,
    cnt_anterior,
    (cnt_actual - cnt_anterior) as diff
FROM version_actual CROSS JOIN version_anterior;

-- Restaurar versión anterior
RESTORE TABLE ventas TO VERSION AS OF 5;

-- Ver historial completo
DESCRIBE HISTORY ventas;

-- Limpiar versiones antiguas (retener últimos 7 días)
VACUUM ventas RETAIN 168 HOURS;
```

**Caso de uso:** Rollback después de carga errónea
```python
# Oops, cargaste datos incorrectos
df_bad.write.format('delta').mode('append').saveAsTable('ventas')

# Ver qué versión era la buena
spark.sql("DESCRIBE HISTORY ventas").show()

# Restaurar
spark.sql("RESTORE TABLE ventas TO VERSION AS OF 42")
```

---

### 13_05_MERGE_CDC_y_Upserts
**Duración:** 70 min | **Dificultad:** Avanzado

**Temas:**
* MERGE INTO para upserts (UPDATE + INSERT)
* CDC (Change Data Capture) patterns
* SCD Type 1 y Type 2
* Deduplicación con MERGE
* Performance de MERGE

**Upsert básico:**
```sql
MERGE INTO clientes_target t
USING clientes_updates s
ON t.cliente_id = s.cliente_id
WHEN MATCHED THEN 
    UPDATE SET 
        t.nombre = s.nombre,
        t.email = s.email,
        t.fecha_actualizacion = current_timestamp()
WHEN NOT MATCHED THEN
    INSERT (cliente_id, nombre, email, fecha_creacion)
    VALUES (s.cliente_id, s.nombre, s.email, current_timestamp());
```

**CDC con flags:**
```sql
MERGE INTO tabla_target t
USING tabla_cdc s
ON t.id = s.id
WHEN MATCHED AND s.operation = 'DELETE' THEN
    DELETE
WHEN MATCHED AND s.operation = 'UPDATE' THEN
    UPDATE SET t.columna = s.columna, t.updated_at = s.timestamp
WHEN NOT MATCHED AND s.operation = 'INSERT' THEN
    INSERT *;
```

**SCD Type 2 (historificación):**
```sql
-- Cerrar registros actuales que cambiaron
MERGE INTO dim_clientes t
USING clientes_nuevos s
ON t.cliente_id = s.cliente_id AND t.is_current = true
WHEN MATCHED AND (t.nombre != s.nombre OR t.email != s.email) THEN
    UPDATE SET 
        t.is_current = false,
        t.end_date = current_date();

-- Insertar nuevas versiones
INSERT INTO dim_clientes
SELECT 
    cliente_id,
    nombre,
    email,
    current_date() as start_date,
    null as end_date,
    true as is_current
FROM clientes_nuevos;
```

---

### 13_06_Optimizacion_OPTIMIZE_ZORDER
**Duración:** 60 min | **Dificultad:** Avanzado

**Temas:**
* OPTIMIZE para compactar small files
* Z-ORDER para co-locality de datos
* Particionamiento óptimo
* Estadísticas y data skipping
* Cuándo ejecutar optimizaciones

**Comandos:**
```sql
-- Compactar archivos pequeños
OPTIMIZE ventas;

-- OPTIMIZE con filtro (solo partición específica)
OPTIMIZE ventas WHERE fecha >= '2024-01-01';

-- Z-ORDER por columnas frecuentes en WHERE
OPTIMIZE ventas ZORDER BY (cliente_id, producto_id);

-- Ver stats de tabla
DESCRIBE DETAIL ventas;

-- Analizar tabla para estadísticas
ANALYZE TABLE ventas COMPUTE STATISTICS;
```

**Estrategia de optimización:**
```python
# Después de muchos appends pequeños
spark.sql("OPTIMIZE mi_tabla")

# Para queries que filtran por cliente_id y region
spark.sql("OPTIMIZE mi_tabla ZORDER BY (cliente_id, region)")

# Limpiar versiones antiguas (liberar storage)
spark.sql("VACUUM mi_tabla RETAIN 168 HOURS")
```

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar ventajas de Delta Lake sobre Parquet
* Nombrar operaciones DML disponibles (MERGE, UPDATE, DELETE)
* Identificar comandos de optimización

### Nivel 2: Comprensión
* Explicar qué es time travel y sus casos de uso
* Describir cómo funciona Z-ORDER
* Interpretar output de DESCRIBE HISTORY

### Nivel 3: Aplicación
* Escribir queries SQL complejas con CTEs
* Implementar MERGE para upserts
* Usar time travel para rollback
* Ejecutar OPTIMIZE y VACUUM

### Nivel 4: Análisis
* Decidir cuándo usar Z-ORDER vs partitioning
* Evaluar estrategia de retención con VACUUM
* Diseñar esquema SCD Type 2 con Delta

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Pipeline CDC Completo
```
"Tengo tabla Delta 'clientes_master' y recibo updates diarios en 'clientes_updates'.

El DF de updates tiene columnas:
- cliente_id
- nombre
- email
- direccion
- operation (INSERT, UPDATE, DELETE)
- timestamp

Genera código que:
1. Implemente MERGE INTO para aplicar CDC
2. Maneje INSERT, UPDATE, DELETE según flag 'operation'
3. Mantenga audit trail (created_at, updated_at)
4. Ejecute OPTIMIZE si hay > 10 archivos
5. Muestre resumen: # inserts, # updates, # deletes aplicados

Explica por qué Delta Lake es ideal para CDC vs Parquet."
```

### Prompt 2: Análisis con Time Travel
```
"Tengo tabla Delta 'ventas' con 30 versiones acumuladas.

Necesito analizar:
1. Growth de registros versión a versión (últimas 10 versiones)
2. Comparar revenue total entre versión actual y hace 7 días
3. Identificar qué versión tuvo el mayor spike de inserts
4. Calcular storage usado por todas las versiones

Genera queries SQL usando:
- VERSION AS OF
- DESCRIBE HISTORY
- CTEs para comparaciones

Recomienda si debería hacer VACUUM y con qué retención."
```

### Prompt 3: Optimización de Performance
```
"Tabla Delta 'transacciones' tiene:
- 500M filas
- 2000 archivos pequeños (< 10MB cada uno)
- Queries típicas filtran por: cliente_id, fecha, region

Genera estrategia de optimización:
1. OPTIMIZE para compactar archivos
2. Z-ORDER óptimo según queries
3. ¿Debería particionar? ¿Por qué columna?
4. Comandos para ejecutar optimización incremental

Compara performance antes/después con EXPLAIN."
```

---

## 🔧 Solución de Problemas

### Problema 1: ConcurrentAppendException en MERGE
**Causa:** Escrituras concurrentes en misma tabla  
**Solución:** Delta maneja automáticamente, retries
```python
# Delta Lake maneja conflictos automáticamente
# Si ves este error, simplemente reintenta
try:
    spark.sql("MERGE INTO ...")
except Exception as e:
    if "ConcurrentAppendException" in str(e):
        # Reintentar
        spark.sql("MERGE INTO ...")
```

### Problema 2: VACUUM elimina archivos necesarios
**Causa:** VACUUM con retención muy corta  
**Solución:** Usa 7+ días de retención
```sql
-- ❌ PELIGROSO
VACUUM tabla RETAIN 0 HOURS;

-- ✅ SEGURO - 7 días mínimo
VACUUM tabla RETAIN 168 HOURS;
```

### Problema 3: Z-ORDER en columnas incorrectas
**Causa:** Z-ORDER en columnas no usadas en WHERE  
**Solución:** Analiza tus queries primero
```sql
-- Identifica columnas frecuentes en WHERE
-- Luego ZORDER por esas
OPTIMIZE tabla ZORDER BY (col1, col2, col3);
```

---

## 📖 Recursos Adicionales

### Documentación
* [Delta Lake Guide](https://docs.delta.io/)
* [Databricks Delta Lake](https://docs.databricks.com/delta/index.html)
* [PySpark SQL Reference](https://spark.apache.org/docs/latest/sql-ref.html)

### Artículos
* [Delta Lake Internals](https://databricks.com/blog/delta-lake-internals)
* [Z-ORDER Optimization](https://databricks.com/blog/z-ordering)

---

## ✅ Checklist

**PySpark SQL:**
- [ ] spark.sql() y temp views
- [ ] CTEs complejas
- [ ] Subqueries

**Window Functions SQL:**
- [ ] ROW_NUMBER, RANK
- [ ] LAG, LEAD
- [ ] Running totals
- [ ] Moving averages

**Delta Lake Basics:**
- [ ] Crear tablas Delta
- [ ] Leer/escribir Delta
- [ ] Append vs overwrite

**Time Travel:**
- [ ] VERSION AS OF
- [ ] TIMESTAMP AS OF
- [ ] RESTORE TABLE
- [ ] DESCRIBE HISTORY

**MERGE:**
- [ ] Upserts básicos
- [ ] CDC con flags
- [ ] SCD Type 2

**Optimización:**
- [ ] OPTIMIZE
- [ ] Z-ORDER
- [ ] VACUUM

---

## 🚀 Próximo Módulo

**➡️ [Módulo 14: PySpark Optimización, ETL y Pipelines](../14_PySpark_Optimizacion_ETL_Pipelines/)**

---

[📖 Volver al Índice](../README.md)
