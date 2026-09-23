# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🔗 Módulo 14 - Notebook 03: JOINs, Subconsultas y CTEs
# MAGIC
# MAGIC ## 📊 Combinación de Datos con SQL Avanzado
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 14 - SQL Editor y Databricks SQL  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio-Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Combinar** tablas con INNER, LEFT, RIGHT, FULL JOIN  
# MAGIC ✅ **Escribir** subconsultas correlacionadas y no correlacionadas  
# MAGIC ✅ **Crear** Common Table Expressions (CTEs)  
# MAGIC ✅ **Usar** EXISTS y IN con subconsultas  
# MAGIC ✅ **Resolver** conciliaciones bancarias con SQL  
# MAGIC ✅ **Optimizar** consultas con múltiples tablas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 14_01 y 14_02 completados
# MAGIC * ✅ Comprensión de GROUP BY y CASE WHEN
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **INNER JOIN** - Intersección de tablas
# MAGIC 2. **LEFT/RIGHT/FULL JOIN** - Preservación de filas
# MAGIC 3. **Subconsultas** - Consultas anidadas
# MAGIC 4. **CTEs (WITH)** - Tablas temporales nombradas
# MAGIC 5. **EXISTS / NOT EXISTS** - Verificación de existencia
# MAGIC 6. **Caso integrador** - Conciliación bancaria con SQL

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
# MAGIC %sql
# MAGIC -- 💾 CARGA: Verificar tablas disponibles
# MAGIC USE CATALOG pandito_ds;
# MAGIC USE SCHEMA default;
# MAGIC
# MAGIC -- Listar tablas disponibles
# MAGIC SHOW TABLES IN pandito_ds.default;
# MAGIC
# MAGIC -- Vista previa de la tabla principal
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3 LIMIT 5;

# COMMAND ----------

# DBTITLE 1,📚 Teoría: JOINs y CTEs
# MAGIC %md
# MAGIC ## 📚 Teoría: JOINs, Subconsultas y CTEs
# MAGIC
# MAGIC ### 🔗 JOINs: Combinar Tablas
# MAGIC
# MAGIC **JOIN** combina filas de dos o más tablas basándose en una columna común.
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────┐       ┌─────────────┐
# MAGIC │  Tabla A    │       │  Tabla B    │
# MAGIC │  (ventas)   │       │  (sucursales)│
# MAGIC └──────┬──────┘       └──────┬──────┘
# MAGIC        │                     │
# MAGIC        └────── JOIN ────────┘
# MAGIC               on sucursal_id
# MAGIC ```
# MAGIC
# MAGIC **Tipos de JOIN:**
# MAGIC
# MAGIC | Tipo | Descripción | Visual |
# MAGIC |------|-------------|--------|
# MAGIC | INNER | Solo filas que coinciden en ambas | ⭕ Intersección |
# MAGIC | LEFT | Todas las de izquierda + coincidencias | ◀━━ Intersección |
# MAGIC | RIGHT | Todas las de derecha + coincidencias | Intersección ━━▶ |
# MAGIC | FULL | Todas las filas de ambas tablas | ◀━━━━━━━━━━▶ |
# MAGIC
# MAGIC ```sql
# MAGIC -- INNER JOIN: Solo sucursales con datos de ventas
# MAGIC SELECT v.sucursal_id, v.fecha, v.ventas
# MAGIC FROM ventas_mensuales_mendoza_h3 v
# MAGIC INNER JOIN otra_tabla s ON v.sucursal_id = s.sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Subconsultas
# MAGIC
# MAGIC **Subconsulta:** Una consulta dentro de otra consulta.
# MAGIC
# MAGIC ```sql
# MAGIC -- Subconsulta en WHERE: Ventas por encima del promedio
# MAGIC SELECT sucursal_id, fecha, ventas
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas > (SELECT AVG(ventas) FROM ventas_mensuales_mendoza_h3)
# MAGIC ORDER BY ventas DESC;
# MAGIC
# MAGIC -- Subconsulta en SELECT: Ranking relativo
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   ventas,
# MAGIC   ventas - (SELECT AVG(ventas) FROM ventas_mensuales_mendoza_h3) AS diferencia_promedio
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏗️ CTEs (Common Table Expressions)
# MAGIC
# MAGIC **CTE:** Consulta temporal nombrada con `WITH`. Más legible que subconsultas.
# MAGIC
# MAGIC ```sql
# MAGIC -- CTE para calcular promedios por sucursal
# MAGIC WITH promedios_sucursal AS (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     AVG(ventas) AS promedio
# MAGIC   FROM ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY sucursal_id
# MAGIC )
# MAGIC SELECT 
# MAGIC   v.sucursal_id,
# MAGIC   v.fecha,
# MAGIC   v.ventas,
# MAGIC   p.promedio,
# MAGIC   v.ventas - p.promedio AS desviacion
# MAGIC FROM ventas_mensuales_mendoza_h3 v
# MAGIC JOIN promedios_sucursal p ON v.sucursal_id = p.sucursal_id
# MAGIC ORDER BY ABS(v.ventas - p.promedio) DESC;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 EXISTS y NOT EXISTS
# MAGIC
# MAGIC ```sql
# MAGIC -- Sucursales que tuvieron ventas superiores a 100000
# MAGIC SELECT DISTINCT sucursal_id
# MAGIC FROM ventas_mensuales_mendoza_h3 v1
# MAGIC WHERE EXISTS (
# MAGIC   SELECT 1 FROM ventas_mensuales_mendoza_h3 v2
# MAGIC   WHERE v2.sucursal_id = v1.sucursal_id
# MAGIC   AND v2.ventas > 100000
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **JOINs y CTEs son fundamentales para:**
# MAGIC * 🏦 Conciliaciones bancarias (comparar dos fuentes)
# MAGIC * 📊 Reportes multi-tabla (ventas + clientes + productos)
# MAGIC * 📈 Análisis comparativos (presupuesto vs real)
# MAGIC * 🎯 Detección de anomalías (datos que no coinciden)

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
# MAGIC %sql
# MAGIC -- 💻 SETUP: Ejercicios con JOINs y CTEs
# MAGIC
# MAGIC -- Ejercicio 1: CTE para ranking de ventas por sucursal
# MAGIC WITH ventas_ranking AS (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     fecha,
# MAGIC     ventas,
# MAGIC     RANK() OVER (PARTITION BY sucursal_id ORDER BY ventas DESC) AS ranking
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC )
# MAGIC SELECT sucursal_id, fecha, ventas, ranking
# MAGIC FROM ventas_ranking
# MAGIC WHERE ranking <= 3
# MAGIC ORDER BY sucursal_id, ranking;
# MAGIC
# MAGIC -- Ejercicio 2: Subconsulta para identificar outliers
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   fecha,
# MAGIC   ventas,
# MAGIC   ROUND((ventas - promedio) / desviacion, 2) AS z_score
# MAGIC FROM (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     fecha,
# MAGIC     ventas,
# MAGIC     AVG(ventas) OVER (PARTITION BY sucursal_id) AS promedio,
# MAGIC     STDDEV(ventas) OVER (PARTITION BY sucursal_id) AS desviacion
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ) sub
# MAGIC WHERE ABS((ventas - promedio) / desviacion) > 1.5
# MAGIC ORDER BY ABS((ventas - promedio) / desviacion) DESC;
# MAGIC
# MAGIC -- Ejercicio 3: CTE múltiple para análisis comparativo
# MAGIC WITH ventas_anuales AS (
# MAGIC   SELECT sucursal_id, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY sucursal_id, YEAR(fecha)
# MAGIC ),
# MAGIC crecimiento AS (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     anio,
# MAGIC     total,
# MAGIC     LAG(total) OVER (PARTITION BY sucursal_id ORDER BY anio) AS total_anio_anterior
# MAGIC   FROM ventas_anuales
# MAGIC )
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   anio,
# MAGIC   total,
# MAGIC   total_anio_anterior,
# MAGIC   ROUND((total - total_anio_anterior) / total_anio_anterior * 100, 2) AS crecimiento_pct
# MAGIC FROM crecimiento
# MAGIC WHERE total_anio_anterior IS NOT NULL
# MAGIC ORDER BY sucursal_id, anio;

# COMMAND ----------

# DBTITLE 1,🔗 Teoría: JOINs y CTEs con datos reales
# MAGIC %md
# MAGIC ## 🔗 JOINs y CTEs con datos reales de Los Andes Market
# MAGIC
# MAGIC ### 🏪 Self-join y CTEs sobre una sola tabla
# MAGIC
# MAGIC En **Los Andes Market** tenemos una sola tabla (`ventas_mensuales_mendoza_h3`), pero podemos crear tablas derivadas con CTEs y hacer joins sobre ellas:
# MAGIC
# MAGIC ```sql
# MAGIC -- CTE: promedios por sucursal
# MAGIC WITH promedios AS (
# MAGIC   SELECT sucursal_id, AVG(ventas) AS promedio
# MAGIC   FROM ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY sucursal_id
# MAGIC )
# MAGIC -- Self-join: comparar cada mes contra el promedio
# MAGIC SELECT v.*, p.promedio, v.ventas - p.promedio AS desviacion
# MAGIC FROM ventas_mensuales_mendoza_h3 v
# MAGIC JOIN promedios p ON v.sucursal_id = p.sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué meses se desvían más del promedio de cada sucursal?
# MAGIC * ¿Cuál es el crecimiento interanual por zona?
# MAGIC * ¿Qué sucursales están por encima/debajo del promedio de su zona?
# MAGIC * ¿Hay outliers (z-score > 2) en las ventas?

# COMMAND ----------

# DBTITLE 1,🔗 Práctica: JOINs y CTEs con datos reales
# MAGIC %sql
# MAGIC -- 🔗 PRÁCTICA: JOINS Y CTEs CON LOS ANDES MARKET
# MAGIC
# MAGIC -- 1️⃣  CTE: Desviación de cada mes contra el promedio de la sucursal
# MAGIC WITH promedios_sucursal AS (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     AVG(ventas) AS promedio,
# MAGIC     STDDEV(ventas) AS desviacion_std
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY sucursal_id
# MAGIC )
# MAGIC SELECT 
# MAGIC   v.sucursal_nombre,
# MAGIC   v.zona,
# MAGIC   v.fecha,
# MAGIC   ROUND(v.ventas, 0) AS ventas,
# MAGIC   ROUND(p.promedio, 0) AS promedio_sucursal,
# MAGIC   ROUND(v.ventas - p.promedio, 0) AS desviacion,
# MAGIC   CASE 
# MAGIC     WHEN v.ventas > p.promedio + p.desviacion_std THEN 'Above Normal'
# MAGIC     WHEN v.ventas < p.promedio - p.desviacion_std THEN 'Below Normal'
# MAGIC     ELSE 'Normal'
# MAGIC   END AS categoria
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3 v
# MAGIC JOIN promedios_sucursal p ON v.sucursal_id = p.sucursal_id
# MAGIC ORDER BY ABS(v.ventas - p.promedio) DESC
# MAGIC LIMIT 20;
# MAGIC
# MAGIC -- 2️⃣  CTE MÚLTIPLE: Crecimiento interanual por zona
# MAGIC WITH ventas_anuales AS (
# MAGIC   SELECT zona, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY zona, YEAR(fecha)
# MAGIC ),
# MAGIC crecimiento AS (
# MAGIC   SELECT 
# MAGIC     zona, anio, total,
# MAGIC     LAG(total) OVER (PARTITION BY zona ORDER BY anio) AS total_anterior
# MAGIC   FROM ventas_anuales
# MAGIC )
# MAGIC SELECT 
# MAGIC   zona,
# MAGIC   anio,
# MAGIC   ROUND(total, 0) AS ventas_anuales,
# MAGIC   ROUND(total_anterior, 0) AS ventas_anio_anterior,
# MAGIC   ROUND((total - total_anterior) / total_anterior * 100, 1) AS crecimiento_pct,
# MAGIC   CASE 
# MAGIC     WHEN total > total_anterior THEN '📈 Crecimiento'
# MAGIC     WHEN total < total_anterior THEN '📉 Decrecimiento'
# MAGIC     ELSE '➡️ Estable'
# MAGIC   END AS tendencia
# MAGIC FROM crecimiento
# MAGIC WHERE total_anterior IS NOT NULL
# MAGIC ORDER BY zona, anio;
# MAGIC
# MAGIC -- 3️⃣  SUBCONSULTA: Ventas por encima del promedio general
# MAGIC SELECT 
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   fecha,
# MAGIC   ROUND(ventas, 0) AS ventas,
# MAGIC   ROUND((SELECT AVG(ventas) FROM pandito_ds.default.ventas_mensuales_mendoza_h3), 0) AS promedio_global,
# MAGIC   ROUND(ventas - (SELECT AVG(ventas) FROM pandito_ds.default.ventas_mensuales_mendoza_h3), 0) AS diferencia
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas > (SELECT AVG(ventas) FROM pandito_ds.default.ventas_mensuales_mendoza_h3)
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 15;
# MAGIC
# MAGIC -- 4️⃣  EXISTS: Sucursales que tuvieron al menos un mes sobre $150k
# MAGIC SELECT DISTINCT sucursal_nombre, zona
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3 v1
# MAGIC WHERE EXISTS (
# MAGIC   SELECT 1 FROM pandito_ds.default.ventas_mensuales_mendoza_h3 v2
# MAGIC   WHERE v2.sucursal_id = v1.sucursal_id
# MAGIC   AND v2.ventas > 150000
# MAGIC )
# MAGIC ORDER BY sucursal_nombre;
# MAGIC
# MAGIC -- 5️⃣  CTE + WINDOW: Ranking mensual por zona
# MAGIC WITH ranking_mensual AS (
# MAGIC   SELECT 
# MAGIC     zona,
# MAGIC     sucursal_nombre,
# MAGIC     fecha,
# MAGIC     ventas,
# MAGIC     RANK() OVER (PARTITION BY zona, MONTH(fecha) ORDER BY ventas DESC) AS rank_zona_mes
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC )
# MAGIC SELECT 
# MAGIC   zona,
# MAGIC   sucursal_nombre,
# MAGIC   fecha,
# MAGIC   ROUND(ventas, 0) AS ventas,
# MAGIC   rank_zona_mes
# MAGIC FROM ranking_mensual
# MAGIC WHERE rank_zona_mes <= 2
# MAGIC ORDER BY zona, fecha, rank_zona_mes;

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 14_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **INNER JOIN — intersección de tablas:**
# MAGIC    - `SELECT ... FROM a INNER JOIN b ON a.clave = b.clave`
# MAGIC    - Solo filas que coinciden en ambas tablas
# MAGIC    - El más usado cuando ambas tablas tienen datos completos
# MAGIC
# MAGIC 2. **LEFT / RIGHT / FULL JOIN:**
# MAGIC    - LEFT: todas las filas de la izquierda + coincidencias (NULL si no hay)
# MAGIC    - RIGHT: todas las filas de la derecha + coincidencias
# MAGIC    - FULL: todas las filas de ambas tablas (incluso sin coincidencia)
# MAGIC    - LEFT JOIN es el más común para detectar faltantes
# MAGIC
# MAGIC 3. **Subconsultas (consultas anidadas):**
# MAGIC    - `WHERE ventas > (SELECT AVG(ventas) FROM ...)` — en WHERE
# MAGIC    - `SELECT ..., (SELECT ... FROM ...) AS col` — en SELECT
# MAGIC    - `FROM (SELECT ... FROM ...) sub` — en FROM (tabla derivada)
# MAGIC    - Correlacionadas: la subconsulta referencia la consulta externa
# MAGIC
# MAGIC 4. **CTEs (WITH) — tablas temporales nombradas:**
# MAGIC    - `WITH nombre AS (SELECT ...) SELECT ... FROM nombre`
# MAGIC    - Más legible que subconsultas anidadas profundas
# MAGIC    - Múltiples CTEs encadenados: `WITH a AS (...), b AS (...) ...`
# MAGIC    - Se pueden reutilizar dentro de la misma consulta
# MAGIC
# MAGIC 5. **EXISTS / NOT EXISTS — verificación de existencia:**
# MAGIC    - `WHERE EXISTS (SELECT 1 FROM ... WHERE ...)` — existe al menos una fila
# MAGIC    - `WHERE NOT EXISTS (...)` — no existe ninguna fila
# MAGIC    - Equivalente a left_semi / left_anti en PySpark
# MAGIC    - Más eficiente que IN cuando solo importa si existe
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Preferir CTEs sobre subconsultas anidadas**
# MAGIC ```sql
# MAGIC -- MALO: subconsulta anidada profunda, difícil de leer
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC   SELECT *
# MAGIC   FROM (
# MAGIC     SELECT sucursal_id, SUM(ventas) AS total
# MAGIC     FROM ventas GROUP BY sucursal_id
# MAGIC   ) inner_q
# MAGIC   WHERE total > 100000
# MAGIC ) outer_q;
# MAGIC
# MAGIC -- BUENO: CTE legible, paso a paso
# MAGIC WITH ventas_totales AS (
# MAGIC   SELECT sucursal_id, SUM(ventas) AS total
# MAGIC   FROM ventas GROUP BY sucursal_id
# MAGIC )
# MAGIC SELECT * FROM ventas_totales WHERE total > 100000;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: LEFT JOIN para detectar faltantes**
# MAGIC ```sql
# MAGIC -- MALO: INNER JOIN oculta filas sin coincidencia
# MAGIC SELECT v.* FROM ventas v
# MAGIC INNER JOIN sucursales s ON v.sucursal_id = s.sucursal_id;
# MAGIC -- Pierde ventas cuya sucursal no existe en la tabla de sucursales
# MAGIC
# MAGIC -- BUENO: LEFT JOIN preserva todas las ventas y revela faltantes
# MAGIC SELECT v.*, s.sucursal_id AS existe_sucursal
# MAGIC FROM ventas v
# MAGIC LEFT JOIN sucursales s ON v.sucursal_id = s.sucursal_id
# MAGIC WHERE s.sucursal_id IS NULL;  -- Solo los faltantes
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: EXISTS es más eficiente que IN para verificar existencia**
# MAGIC ```sql
# MAGIC -- MALO: IN con subconsulta grande puede ser lento
# MAGIC SELECT * FROM ventas v
# MAGIC WHERE v.sucursal_id IN (
# MAGIC   SELECT sucursal_id FROM sucursales WHERE zona = 'Centro'
# MAGIC );
# MAGIC
# MAGIC -- BUENO: EXISTS se detiene al primer match (short-circuit)
# MAGIC SELECT * FROM ventas v
# MAGIC WHERE EXISTS (
# MAGIC   SELECT 1 FROM sucursales s
# MAGIC   WHERE s.sucursal_id = v.sucursal_id AND s.zona = 'Centro'
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | SQL |
# MAGIC |-----------|-----|
# MAGIC | Coincidencia exacta entre tablas | `INNER JOIN` |
# MAGIC | Preservar filas de la izquierda | `LEFT JOIN` |
# MAGIC | Preservar filas de la derecha | `RIGHT JOIN` |
# MAGIC | Todas las filas de ambas tablas | `FULL OUTER JOIN` |
# MAGIC | Detectar filas sin coincidencia | `LEFT JOIN ... WHERE b.clave IS NULL` |
# MAGIC | Comparar contra promedio/total | Subconsulta en WHERE |
# MAGIC | Consulta legible paso a paso | `WITH cte AS (...) SELECT ...` |
# MAGIC | Múltiples pasos encadenados | `WITH a AS (...), b AS (...) SELECT ...` |
# MAGIC | Verificar si existe al menos una fila | `WHERE EXISTS (SELECT 1 FROM ...)` |
# MAGIC | Verificar que no existe ninguna fila | `WHERE NOT EXISTS (...)` |
# MAGIC | Ranking + filtrar top N | CTE + `ROW_NUMBER()` + `WHERE ranking <= N` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🔗 ¡JOINs, subconsultas y CTEs dominados!</h3>
# MAGIC   <p><i>"CTEs hacen legible lo complejo, JOINs combinan lo separado, EXISTS verifica lo incierto."</i></p>
# MAGIC </div>