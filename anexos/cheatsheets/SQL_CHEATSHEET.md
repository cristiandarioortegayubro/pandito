# 🗄️ SQL Cheatsheet - Databricks SQL - Saliendo de lo Pandito v4

**Referencia rápida de Databricks SQL para análisis de datos**

---

## 🎯 Consultas Básicas

```sql
-- SELECT básico
SELECT * FROM tabla;
SELECT columna1, columna2 FROM tabla;
SELECT DISTINCT categoria FROM productos;

-- Alias
SELECT nombre AS cliente, precio * cantidad AS total
FROM ventas;

-- LIMIT
SELECT * FROM tabla LIMIT 10;

-- WHERE
SELECT * FROM ventas
WHERE fecha >= '2024-01-01'
  AND categoria = 'Electrónica'
  AND precio > 100;
```

---

## 🔎 Filtrado (WHERE)

```sql
-- Operadores de comparación
SELECT * FROM tabla WHERE edad > 30;
SELECT * FROM tabla WHERE edad >= 18 AND edad <= 65;
SELECT * FROM tabla WHERE estado = 'ACTIVO';
SELECT * FROM tabla WHERE estado != 'INACTIVO';

-- BETWEEN
SELECT * FROM ventas
WHERE fecha BETWEEN '2024-01-01' AND '2024-12-31';

-- IN
SELECT * FROM clientes
WHERE ciudad IN ('Madrid', 'Barcelona', 'Valencia');

-- NOT IN
SELECT * FROM productos
WHERE categoria NOT IN ('Descontinuado', 'Agotado');

-- LIKE (patrones de texto)
SELECT * FROM clientes WHERE nombre LIKE 'Ana%';     -- Empieza con Ana
SELECT * FROM clientes WHERE email LIKE '%@gmail.com'; -- Termina con @gmail.com
SELECT * FROM productos WHERE codigo LIKE 'PROD_____'; -- Exactamente 9 caracteres

-- IS NULL / IS NOT NULL
SELECT * FROM tabla WHERE columna IS NULL;
SELECT * FROM tabla WHERE columna IS NOT NULL;

-- Múltiples condiciones
SELECT * FROM ventas
WHERE (categoria = 'Electrónica' OR categoria = 'Computadoras')
  AND precio > 500
  AND fecha >= '2024-01-01';
```

---

## 📊 Agregaciones

```sql
-- Funciones de agregación básicas
SELECT COUNT(*) FROM ventas;
SELECT COUNT(DISTINCT cliente_id) FROM ventas;
SELECT SUM(monto) FROM ventas;
SELECT AVG(precio) FROM productos;
SELECT MIN(fecha) FROM transacciones;
SELECT MAX(precio) FROM productos;

-- GROUP BY
SELECT categoria, SUM(ventas) as total_ventas
FROM ventas
GROUP BY categoria;

-- GROUP BY múltiples columnas
SELECT categoria, subcategoria, SUM(ventas) as total
FROM ventas
GROUP BY categoria, subcategoria;

-- HAVING (filtrar después de agrupar)
SELECT categoria, SUM(ventas) as total
FROM ventas
GROUP BY categoria
HAVING SUM(ventas) > 10000;

-- Múltiples agregaciones
SELECT 
    categoria,
    COUNT(*) as num_productos,
    SUM(ventas) as total_ventas,
    AVG(precio) as precio_promedio,
    MIN(precio) as precio_min,
    MAX(precio) as precio_max
FROM ventas
GROUP BY categoria;
```

---

## 🔄 JOINS

```sql
-- INNER JOIN
SELECT a.*, b.nombre_categoria
FROM ventas a
INNER JOIN categorias b ON a.categoria_id = b.id;

-- LEFT JOIN
SELECT a.*, b.nombre
FROM clientes a
LEFT JOIN pedidos b ON a.cliente_id = b.cliente_id;

-- RIGHT JOIN
SELECT a.*, b.nombre
FROM pedidos a
RIGHT JOIN clientes b ON a.cliente_id = b.cliente_id;

-- FULL OUTER JOIN
SELECT a.*, b.*
FROM tabla1 a
FULL OUTER JOIN tabla2 b ON a.id = b.id;

-- CROSS JOIN (producto cartesiano)
SELECT a.producto, b.region
FROM productos a
CROSS JOIN regiones b;

-- SELF JOIN
SELECT 
    a.empleado_nombre,
    b.empleado_nombre as jefe_nombre
FROM empleados a
LEFT JOIN empleados b ON a.jefe_id = b.empleado_id;

-- JOIN en múltiples columnas
SELECT *
FROM ventas a
JOIN productos b 
  ON a.producto_id = b.id 
 AND a.año = b.año;
```

---

## 🔀 UNION y Combinaciones

```sql
-- UNION (elimina duplicados)
SELECT producto FROM ventas_2023
UNION
SELECT producto FROM ventas_2024;

-- UNION ALL (mantiene duplicados, más rápido)
SELECT producto FROM ventas_2023
UNION ALL
SELECT producto FROM ventas_2024;

-- INTERSECT (valores en ambas)
SELECT producto FROM ventas_2023
INTERSECT
SELECT producto FROM ventas_2024;

-- EXCEPT (valores en primera pero no en segunda)
SELECT producto FROM ventas_2023
EXCEPT
SELECT producto FROM ventas_2024;
```

---

## 📐 Subconsultas

```sql
-- Subconsulta en WHERE
SELECT * FROM productos
WHERE precio > (SELECT AVG(precio) FROM productos);

-- Subconsulta con IN
SELECT * FROM ventas
WHERE cliente_id IN (
    SELECT cliente_id FROM clientes WHERE ciudad = 'Madrid'
);

-- Subconsulta correlacionada
SELECT 
    producto,
    precio,
    (SELECT AVG(precio) 
     FROM productos p2 
     WHERE p2.categoria = p1.categoria) as precio_promedio_categoria
FROM productos p1;

-- Subconsulta en FROM (tabla derivada)
SELECT categoria, promedio_ventas
FROM (
    SELECT categoria, AVG(ventas) as promedio_ventas
    FROM productos
    GROUP BY categoria
) subconsulta
WHERE promedio_ventas > 1000;

-- EXISTS / NOT EXISTS
SELECT * FROM clientes c
WHERE EXISTS (
    SELECT 1 FROM pedidos p 
    WHERE p.cliente_id = c.id
);
```

---

## 🪟 Window Functions

```sql
-- ROW_NUMBER (número de fila)
SELECT 
    producto,
    ventas,
    ROW_NUMBER() OVER (ORDER BY ventas DESC) as ranking
FROM productos;

-- RANK (con empates)
SELECT 
    producto,
    ventas,
    RANK() OVER (ORDER BY ventas DESC) as rank
FROM productos;

-- DENSE_RANK (ranking sin saltos)
SELECT 
    producto,
    ventas,
    DENSE_RANK() OVER (ORDER BY ventas DESC) as dense_rank
FROM productos;

-- PARTITION BY (agrupar dentro de la ventana)
SELECT 
    categoria,
    producto,
    ventas,
    RANK() OVER (PARTITION BY categoria ORDER BY ventas DESC) as rank_en_categoria
FROM productos;

-- SUM OVER (total acumulado)
SELECT 
    fecha,
    ventas,
    SUM(ventas) OVER (ORDER BY fecha ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as ventas_acumuladas
FROM ventas_diarias;

-- AVG OVER (promedio móvil)
SELECT 
    fecha,
    ventas,
    AVG(ventas) OVER (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as promedio_7dias
FROM ventas_diarias;

-- LAG / LEAD (valores anteriores/siguientes)
SELECT 
    fecha,
    ventas,
    LAG(ventas, 1) OVER (ORDER BY fecha) as ventas_dia_anterior,
    LEAD(ventas, 1) OVER (ORDER BY fecha) as ventas_dia_siguiente
FROM ventas_diarias;

-- FIRST_VALUE / LAST_VALUE
SELECT 
    categoria,
    producto,
    precio,
    FIRST_VALUE(precio) OVER (PARTITION BY categoria ORDER BY precio) as precio_mas_bajo,
    LAST_VALUE(precio) OVER (PARTITION BY categoria ORDER BY precio RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as precio_mas_alto
FROM productos;
```

---

## 📅 Funciones de Fecha

```sql
-- Fecha/hora actual
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;
SELECT NOW();

-- Extraer componentes
SELECT 
    fecha,
    YEAR(fecha) as año,
    MONTH(fecha) as mes,
    DAY(fecha) as dia,
    DAYOFWEEK(fecha) as dia_semana,  -- 1=Domingo, 7=Sábado
    QUARTER(fecha) as trimestre,
    WEEKOFYEAR(fecha) as semana
FROM ventas;

-- Diferencia entre fechas
SELECT DATEDIFF('2024-12-31', '2024-01-01') as dias_diferencia;
SELECT MONTHS_BETWEEN('2024-12-31', '2024-01-01') as meses_diferencia;

-- Sumar/restar días
SELECT DATE_ADD('2024-01-01', 30) as fecha_futura;
SELECT DATE_SUB('2024-01-01', 30) as fecha_pasada;

-- Formato de fecha
SELECT DATE_FORMAT(fecha, 'yyyy-MM-dd') FROM ventas;
SELECT DATE_FORMAT(fecha, 'dd/MM/yyyy') FROM ventas;

-- Convertir string a fecha
SELECT TO_DATE('2024-01-15', 'yyyy-MM-dd');
SELECT TO_TIMESTAMP('2024-01-15 14:30:00', 'yyyy-MM-dd HH:mm:ss');

-- Truncar fecha (inicio de periodo)
SELECT DATE_TRUNC('MONTH', fecha) as inicio_mes FROM ventas;
SELECT DATE_TRUNC('YEAR', fecha) as inicio_año FROM ventas;
SELECT DATE_TRUNC('QUARTER', fecha) as inicio_trimestre FROM ventas;

-- Último día del mes
SELECT LAST_DAY(fecha) FROM ventas;
```

---

## 🔤 Funciones de String

```python
-- Mayúsculas/minúsculas
SELECT UPPER(nombre), LOWER(apellido) FROM clientes;

-- Concatenación
SELECT CONCAT(nombre, ' ', apellido) as nombre_completo FROM clientes;
SELECT nombre || ' ' || apellido as nombre_completo FROM clientes;

-- Substring
SELECT SUBSTRING(codigo, 1, 3) as prefijo FROM productos;

-- Longitud
SELECT LENGTH(descripcion) FROM productos;

-- Trim (quitar espacios)
SELECT TRIM(nombre) FROM clientes;
SELECT LTRIM(texto) as sin_espacios_izq FROM tabla;
SELECT RTRIM(texto) as sin_espacios_der FROM tabla;

-- Replace
SELECT REPLACE(email, '@gmail.com', '@empresa.com') FROM clientes;

-- Split
SELECT SPLIT(email, '@')[0] as usuario FROM clientes;

-- LIKE patrones
SELECT * FROM productos WHERE nombre LIKE '%laptop%';
SELECT * FROM clientes WHERE email LIKE '%@gmail.com';

-- Regex
SELECT REGEXP_EXTRACT(texto, '\\d+', 0) as numero FROM tabla;
SELECT REGEXP_REPLACE(texto, '[^0-9]', '') as solo_numeros FROM tabla;
```

---

## 🔢 Funciones Matemáticas

```sql
-- Redondeo
SELECT ROUND(precio, 2) FROM productos;  -- 2 decimales
SELECT CEILING(precio) FROM productos;    -- Redondear arriba
SELECT FLOOR(precio) FROM productos;      -- Redondear abajo

-- Valor absoluto
SELECT ABS(diferencia) FROM tabla;

-- Potencia y raíz
SELECT POWER(valor, 2) as cuadrado FROM tabla;
SELECT SQRT(valor) as raiz_cuadrada FROM tabla;

-- Logaritmo
SELECT LOG(valor) FROM tabla;
SELECT LOG10(valor) FROM tabla;

-- Módulo
SELECT MOD(numero, 10) as ultimo_digito FROM tabla;

-- Números aleatorios
SELECT RAND() as numero_aleatorio;
SELECT RAND(42) as numero_aleatorio_seed;  -- Con seed fijo
```

---

## 🎯 CASE WHEN (Condicionales)

```sql
-- CASE WHEN básico
SELECT 
    producto,
    precio,
    CASE
        WHEN precio < 50 THEN 'Económico'
        WHEN precio < 200 THEN 'Medio'
        ELSE 'Premium'
    END as rango_precio
FROM productos;

-- CASE con múltiples condiciones
SELECT 
    cliente,
    edad,
    genero,
    CASE
        WHEN edad < 18 THEN 'Menor'
        WHEN edad >= 18 AND edad < 30 THEN 'Joven'
        WHEN edad >= 30 AND edad < 60 THEN 'Adulto'
        ELSE 'Senior'
    END as grupo_edad
FROM clientes;

-- CASE en agregaciones
SELECT 
    categoria,
    SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) as activos,
    SUM(CASE WHEN estado = 'INACTIVO' THEN 1 ELSE 0 END) as inactivos
FROM productos
GROUP BY categoria;
```

---

## 🏗️ Creación y Modificación de Tablas

```sql
-- Crear tabla
CREATE TABLE ventas (
    id BIGINT,
    fecha DATE,
    producto STRING,
    cantidad INT,
    precio DOUBLE,
    cliente_id BIGINT
)
USING DELTA
PARTITIONED BY (fecha);

-- Crear tabla desde consulta
CREATE TABLE ventas_resumen AS
SELECT 
    categoria,
    SUM(ventas) as total
FROM ventas
GROUP BY categoria;

-- Insertar datos
INSERT INTO ventas VALUES 
    (1, '2024-01-01', 'Laptop', 2, 1200.00, 101),
    (2, '2024-01-02', 'Mouse', 5, 25.00, 102);

-- Insertar desde SELECT
INSERT INTO ventas_2024
SELECT * FROM ventas WHERE YEAR(fecha) = 2024;

-- Actualizar registros
UPDATE ventas
SET precio = precio * 1.10
WHERE categoria = 'Electrónica';

-- Eliminar registros
DELETE FROM ventas WHERE fecha < '2020-01-01';

-- Eliminar tabla
DROP TABLE IF EXISTS tabla_temporal;

-- Truncar tabla (eliminar todos los datos)
TRUNCATE TABLE tabla_temporal;
```

---

## ⚡ Delta Lake - Operaciones Avanzadas

```sql
-- MERGE (UPSERT)
MERGE INTO clientes_target t
USING clientes_source s
ON t.id = s.id
WHEN MATCHED THEN
    UPDATE SET t.nombre = s.nombre, t.email = s.email
WHEN NOT MATCHED THEN
    INSERT (id, nombre, email) VALUES (s.id, s.nombre, s.email);

-- Time Travel (versiones anteriores)
SELECT * FROM ventas VERSION AS OF 5;
SELECT * FROM ventas TIMESTAMP AS OF '2024-01-01';

-- Ver historial de tabla
DESCRIBE HISTORY ventas;

-- Optimizar tabla
OPTIMIZE ventas;

-- Optimizar con Z-ORDER
OPTIMIZE ventas ZORDER BY (categoria, fecha);

-- Vacuum (limpiar archivos antiguos)
VACUUM ventas RETAIN 168 HOURS;  -- 7 días

-- Ver detalles de tabla
DESCRIBE DETAIL ventas;
DESCRIBE EXTENDED ventas;

-- Ver propiedades de tabla
SHOW TBLPROPERTIES ventas;
```

---

## 🔍 Análisis de Performance

```sql
-- EXPLAIN (ver plan de ejecución)
EXPLAIN SELECT * FROM ventas WHERE categoria = 'Electrónica';

-- Estadísticas de tabla
ANALYZE TABLE ventas COMPUTE STATISTICS;
ANALYZE TABLE ventas COMPUTE STATISTICS FOR COLUMNS categoria, fecha;

-- Ver tamaño de tabla
SELECT 
    table_name,
    SUM(size_in_bytes) / (1024*1024*1024) as size_gb
FROM system.information_schema.table_storage
WHERE table_catalog = 'main'
  AND table_schema = 'default'
GROUP BY table_name;
```

---

## 📊 CTEs (Common Table Expressions)

```sql
-- CTE simple
WITH ventas_2024 AS (
    SELECT * FROM ventas WHERE YEAR(fecha) = 2024
)
SELECT categoria, SUM(monto) as total
FROM ventas_2024
GROUP BY categoria;

-- Múltiples CTEs
WITH 
ventas_electronica AS (
    SELECT * FROM ventas WHERE categoria = 'Electrónica'
),
ventas_por_mes AS (
    SELECT 
        MONTH(fecha) as mes,
        SUM(monto) as total
    FROM ventas_electronica
    GROUP BY MONTH(fecha)
)
SELECT * FROM ventas_por_mes ORDER BY mes;

-- CTE recursivo
WITH RECURSIVE numeros(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM numeros WHERE n < 10
)
SELECT * FROM numeros;
```

---

## 🎯 Patrones Comunes de Análisis

### Top N por Grupo
```sql
SELECT * FROM (
    SELECT 
        categoria,
        producto,
        ventas,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY ventas DESC) as rank
    FROM productos
)
WHERE rank <= 5;
```

### Tasa de Crecimiento
```sql
SELECT 
    mes,
    ventas,
    LAG(ventas) OVER (ORDER BY mes) as ventas_mes_anterior,
    (ventas - LAG(ventas) OVER (ORDER BY mes)) / LAG(ventas) OVER (ORDER BY mes) * 100 as crecimiento_porcentual
FROM ventas_mensuales;
```

### Detección de Duplicados
```sql
SELECT 
    *,
    COUNT(*) OVER (PARTITION BY id) as cuenta
FROM tabla
WHERE cuenta > 1;
```

### Pivot Manual (sin PIVOT syntax)
```sql
SELECT 
    categoria,
    SUM(CASE WHEN mes = 'Enero' THEN ventas ELSE 0 END) as Enero,
    SUM(CASE WHEN mes = 'Febrero' THEN ventas ELSE 0 END) as Febrero,
    SUM(CASE WHEN mes = 'Marzo' THEN ventas ELSE 0 END) as Marzo
FROM ventas
GROUP BY categoria;
```

### Calcular Percentiles
```sql
SELECT 
    PERCENTILE(precio, 0.25) as p25,
    PERCENTILE(precio, 0.50) as mediana,
    PERCENTILE(precio, 0.75) as p75,
    PERCENTILE(precio, 0.95) as p95
FROM productos;
```

---

## 🎯 Unity Catalog

```sql
-- Crear catálogo
CREATE CATALOG IF NOT EXISTS mi_catalogo;

-- Crear schema
CREATE SCHEMA IF NOT EXISTS mi_catalogo.mi_schema;

-- Usar catálogo y schema
USE CATALOG mi_catalogo;
USE SCHEMA mi_schema;

-- Consultar con nombre completo
SELECT * FROM mi_catalogo.mi_schema.mi_tabla;

-- Listar catálogos
SHOW CATALOGS;

-- Listar schemas
SHOW SCHEMAS IN mi_catalogo;

-- Listar tablas
SHOW TABLES IN mi_catalogo.mi_schema;

-- Permisos
GRANT SELECT ON TABLE mi_catalogo.mi_schema.mi_tabla TO `usuario@empresa.com`;
GRANT ALL PRIVILEGES ON SCHEMA mi_catalogo.mi_schema TO `grupo_usuarios`;
```

---

## ⚠️ Errores Comunes y Soluciones

### Error: Column ambiguously defined
```sql
-- ❌ Problema
SELECT id, nombre
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id;  -- Ambiguo: ¿id de qué tabla?

-- ✅ Solución
SELECT v.id, c.nombre
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id;
```

### Error: Cannot resolve column name
```sql
-- ❌ Problema
SELECT columna_incorrecta FROM tabla;

-- ✅ Solución
DESCRIBE tabla;  -- Ver columnas disponibles
SELECT * FROM tabla LIMIT 1;  -- Ver estructura
```

### Performance lento en agregaciones
```sql
-- ❌ Lento
SELECT categoria, SUM(ventas)
FROM ventas_gigante
GROUP BY categoria;

-- ✅ Mejor: Filtrar primero
SELECT categoria, SUM(ventas)
FROM ventas_gigante
WHERE fecha >= '2024-01-01'  -- Reducir datos
GROUP BY categoria;
```

---

## 📚 Recursos Adicionales

* **Databricks SQL Reference:** https://docs.databricks.com/sql/language-manual/
* **Delta Lake SQL:** https://docs.delta.io/latest/delta-batch.html
* **Unity Catalog:** https://docs.databricks.com/data-governance/unity-catalog/

---

**💡 Tip:** En Databricks SQL Editor, usa Ctrl+Space para autocompletar nombres de tablas y columnas.

_Última actualización: 2026-07-29_
