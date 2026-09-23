# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 📊 Módulo 14 - Notebook 02: Agregaciones, GROUP BY y CASE WHEN
# MAGIC
# MAGIC ## 📈 Análisis agregado con SQL declarativo
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 14 - SQL Editor y Databricks SQL  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Agrupar** datos con GROUP BY  
# MAGIC ✅ **Filtrar** grupos con HAVING  
# MAGIC ✅ **Crear** lógica condicional con CASE WHEN  
# MAGIC ✅ **Combinar** múltiples agregaciones  
# MAGIC ✅ **Aplicar** funciones de ventana básicas  
# MAGIC ✅ **Resolver** casos de negocio con SQL agregado
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebook 14_01 completado (SELECT, WHERE, ORDER BY)
# MAGIC * ✅ Conocimiento de funciones agregadas básicas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **GROUP BY** - Agrupación de filas
# MAGIC 2. **HAVING** - Filtrado de grupos
# MAGIC 3. **CASE WHEN** - Lógica condicional
# MAGIC 4. **Múltiples agregaciones** - SUM, COUNT, AVG juntas
# MAGIC 5. **YEAR/MONTH/DATE_TRUNC** - Agrupación temporal
# MAGIC 6. **Caso integrador** - Dashboard de KPIs por sucursal

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
# MAGIC %sql
# MAGIC -- 💾 CARGA: Verificar datos disponibles
# MAGIC USE CATALOG pandito_ds;
# MAGIC USE SCHEMA default;
# MAGIC
# MAGIC -- Vista previa con información temporal
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_id,
# MAGIC   ventas,
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   MONTH(fecha) AS mes
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC ORDER BY fecha DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,📚 Teoría: GROUP BY y CASE WHEN
# MAGIC %md
# MAGIC ## 📚 Teoría: GROUP BY, HAVING y CASE WHEN
# MAGIC
# MAGIC ### 📊 GROUP BY: Agrupar y Agregar
# MAGIC
# MAGIC **GROUP BY** agrupa filas que comparten valores en una o más columnas, permitiendo calcular agregaciones por grupo.
# MAGIC
# MAGIC ```sql
# MAGIC -- Ventas totales por sucursal
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS meses_activos,
# MAGIC   SUM(ventas) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio,
# MAGIC   MIN(ventas) AS venta_minima,
# MAGIC   MAX(ventas) AS venta_maxima
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id
# MAGIC ORDER BY ventas_totales DESC;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 HAVING: Filtrar Grupos
# MAGIC
# MAGIC **HAVING** filtra grupos después de GROUP BY (como WHERE pero para agregaciones).
# MAGIC
# MAGIC ```sql
# MAGIC -- Solo sucursales con ventas promedio > 50000
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id
# MAGIC HAVING AVG(ventas) > 50000
# MAGIC ORDER BY ventas_promedio DESC;
# MAGIC ```
# MAGIC
# MAGIC **WHERE vs HAVING:**
# MAGIC * `WHERE` filtra filas ANTES de agrupar
# MAGIC * `HAVING` filtra grupos DESPUÉS de agrupar
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 CASE WHEN: Lógica Condicional
# MAGIC
# MAGIC **CASE WHEN** crea columnas basadas en condiciones (como if/elif/else de Python).
# MAGIC
# MAGIC ```sql
# MAGIC -- Clasificar sucursales por nivel de ventas
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   ventas,
# MAGIC   CASE 
# MAGIC     WHEN ventas > 80000 THEN 'Alto'
# MAGIC     WHEN ventas > 50000 THEN 'Medio'
# MAGIC     WHEN ventas > 30000 THEN 'Bajo'
# MAGIC     ELSE 'Muy Bajo'
# MAGIC   END AS nivel_ventas,
# MAGIC   CASE 
# MAGIC     WHEN ventas > 80000 THEN 1
# MAGIC     WHEN ventas > 50000 THEN 2
# MAGIC     WHEN ventas > 30000 THEN 3
# MAGIC     ELSE 4
# MAGIC   END AS ranking
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas DESC;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📅 Agrupación Temporal
# MAGIC
# MAGIC ```sql
# MAGIC -- Ventas por año
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   COUNT(*) AS registros,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_anuales,
# MAGIC   ROUND(AVG(ventas), 2) AS promedio_mensual
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha)
# MAGIC ORDER BY anio;
# MAGIC
# MAGIC -- Ventas por año y mes (pivot-like)
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   MONTH(fecha) AS mes,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha), MONTH(fecha)
# MAGIC ORDER BY anio, mes;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **GROUP BY + CASE WHEN = Análisis empresarial completo:**
# MAGIC * 📊 Segmentación de clientes/ventas
# MAGIC * 📈 KPIs por categoría/región/período
# MAGIC * 🎯 Clasificación automática de datos
# MAGIC * 📋 Reportes agregados para dashboards

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
# MAGIC %sql
# MAGIC -- 💻 SETUP: Ejercicios de GROUP BY y CASE WHEN
# MAGIC
# MAGIC -- Ejercicio 1: KPIs por sucursal con clasificación
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS meses_con_datos,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio,
# MAGIC   ROUND(MIN(ventas), 2) AS venta_minima,
# MAGIC   ROUND(MAX(ventas), 2) AS venta_maxima,
# MAGIC   CASE 
# MAGIC     WHEN AVG(ventas) > 80000 THEN 'Alto'
# MAGIC     WHEN AVG(ventas) > 50000 THEN 'Medio'
# MAGIC     ELSE 'Bajo'
# MAGIC   END AS rendimiento
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id
# MAGIC ORDER BY ventas_promedio DESC;
# MAGIC
# MAGIC -- Ejercicio 2: Análisis anual con tendencia
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   COUNT(*) AS meses,
# MAGIC   ROUND(SUM(ventas), 2) AS total_anual,
# MAGIC   ROUND(AVG(ventas), 2) AS promedio_mensual,
# MAGIC   ROUND((MAX(ventas) - MIN(ventas)) / AVG(ventas) * 100, 2) AS variabilidad_pct
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha)
# MAGIC ORDER BY anio;
# MAGIC
# MAGIC -- Ejercicio 3: Top 3 meses con mejores ventas por sucursal
# MAGIC WITH ranked_ventas AS (
# MAGIC   SELECT 
# MAGIC     sucursal_id,
# MAGIC     fecha,
# MAGIC     ventas,
# MAGIC     ROW_NUMBER() OVER (PARTITION BY sucursal_id ORDER BY ventas DESC) AS ranking
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC )
# MAGIC SELECT sucursal_id, fecha, ventas, ranking
# MAGIC FROM ranked_ventas
# MAGIC WHERE ranking <= 3
# MAGIC ORDER BY sucursal_id, ranking;

# COMMAND ----------

# DBTITLE 1,📈 Teoría: Agregaciones con datos reales
# MAGIC %md
# MAGIC ## 📈 Agregaciones y CASE WHEN con datos reales de Los Andes Market
# MAGIC
# MAGIC ### 📊 KPIs de negocio con GROUP BY
# MAGIC
# MAGIC Con SQL podemos calcular métricas ejecutivas sobre las ventas reales de **Los Andes Market**:
# MAGIC
# MAGIC ```sql
# MAGIC -- KPI: Ventas por zona con clasificación
# MAGIC SELECT 
# MAGIC   zona,
# MAGIC   SUM(ventas) AS total,
# MAGIC   CASE WHEN AVG(ventas) > 80000 THEN 'Alto' ELSE 'Bajo' END AS nivel
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC GROUP BY zona;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué zona genera más ventas? ¿Y por sucursal?
# MAGIC * ¿Cómo clasificar sucursales en Alto/Medio/Bajo?
# MAGIC * ¿Cuál es la variabilidad mensual de cada sucursal?
# MAGIC * ¿Qué meses del año tienen mejores ventas?

# COMMAND ----------

# DBTITLE 1,📈 Práctica: Agregaciones con datos reales
# MAGIC %sql
# MAGIC -- 📈 PRÁCTICA: AGREGACIONES Y CASE WHEN CON LOS ANDES MARKET
# MAGIC
# MAGIC -- 1️⃣  DASHBOARD DE KPIs POR ZONA
# MAGIC SELECT 
# MAGIC   zona,
# MAGIC   COUNT(*) AS meses_con_datos,
# MAGIC   COUNT(DISTINCT sucursal_id) AS num_sucursales,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 0) AS ventas_promedio,
# MAGIC   ROUND(MAX(ventas), 0) AS venta_max,
# MAGIC   ROUND(MIN(ventas), 0) AS venta_min,
# MAGIC   CASE 
# MAGIC     WHEN AVG(ventas) > 100000 THEN 'Alto'
# MAGIC     WHEN AVG(ventas) > 50000 THEN 'Medio'
# MAGIC     ELSE 'Bajo'
# MAGIC   END AS rendimiento
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY zona
# MAGIC ORDER BY ventas_totales DESC;
# MAGIC
# MAGIC -- 2️⃣  RANKING DE SUCURSALES CON CASE WHEN
# MAGIC SELECT 
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   COUNT(*) AS meses_activos,
# MAGIC   ROUND(AVG(ventas), 0) AS ventas_promedio,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_totales,
# MAGIC   CASE 
# MAGIC     WHEN SUM(ventas) > 2000000 THEN 'Estrella'
# MAGIC     WHEN SUM(ventas) > 1000000 THEN 'Sólida'
# MAGIC     WHEN SUM(ventas) > 500000 THEN 'Estable'
# MAGIC     ELSE 'Emergente'
# MAGIC   END AS categoria_sucursal
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_nombre, zona
# MAGIC ORDER BY ventas_totales DESC;
# MAGIC
# MAGIC -- 3️⃣  VENTAS POR AÑO Y MES (estacionalidad)
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   MONTH(fecha) AS mes,
# MAGIC   COUNT(*) AS registros,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_mes,
# MAGIC   ROUND(AVG(ventas), 0) AS promedio_sucursal
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha), MONTH(fecha)
# MAGIC ORDER BY anio, mes;
# MAGIC
# MAGIC -- 4️⃣  HAVING: Solo sucursales con ventas promedio altas
# MAGIC SELECT 
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   ROUND(AVG(ventas), 0) AS ventas_promedio,
# MAGIC   ROUND(STDDEV(ventas), 0) AS volatilidad
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_nombre, zona
# MAGIC HAVING AVG(ventas) > 80000
# MAGIC ORDER BY ventas_promedio DESC;
# MAGIC
# MAGIC -- 5️⃣  VENTAS TRIMESTRALES CON DATE_TRUNC
# MAGIC SELECT 
# MAGIC   DATE_TRUNC('quarter', fecha) AS trimestre,
# MAGIC   zona,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_trimestrales,
# MAGIC   ROUND(AVG(ventas), 0) AS promedio_mensual
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY DATE_TRUNC('quarter', fecha), zona
# MAGIC ORDER BY trimestre, zona;

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 14_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **GROUP BY — agrupación y agregación:**
# MAGIC    - `GROUP BY sucursal_id` agrupa filas por valor de columna
# MAGIC    - Combina con `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`
# MAGIC    - Todas las columnas en SELECT (no agregadas) deben estar en GROUP BY
# MAGIC
# MAGIC 2. **HAVING — filtrado de grupos:**
# MAGIC    - `HAVING AVG(ventas) > 50000` filtra grupos después de agregar
# MAGIC    - WHERE filtra filas ANTES de agrupar, HAVING filtra grupos DESPUÉS
# MAGIC    - Se pueden combinar WHERE + GROUP BY + HAVING en la misma consulta
# MAGIC
# MAGIC 3. **CASE WHEN — lógica condicional:**
# MAGIC    - `CASE WHEN cond THEN val1 WHEN cond2 THEN val2 ELSE val3 END`
# MAGIC    - Equivalente a if/elif/else de Python o F.when() de PySpark
# MAGIC    - Crea columnas categóricas o numéricas basadas en condiciones
# MAGIC
# MAGIC 4. **Agrupación temporal:**
# MAGIC    - `GROUP BY YEAR(fecha)` — agregación anual
# MAGIC    - `GROUP BY YEAR(fecha), MONTH(fecha)` — agregación mensual por año
# MAGIC    - `DATE_TRUNC('month', fecha)` — truncar a inicio de mes
# MAGIC
# MAGIC 5. **Window functions básicas:**
# MAGIC    - `ROW_NUMBER() OVER (PARTITION BY sucursal ORDER BY ventas DESC)`
# MAGIC    - Ranking dentro de cada grupo (partición)
# MAGIC    - CTEs (`WITH ... AS`) para filtrar sobre resultados rankeados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Toda columna no agregada en SELECT debe estar en GROUP BY**
# MAGIC ```sql
# MAGIC -- MALO: sucursal_id en SELECT pero no en GROUP BY
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas GROUP BY fecha; -- 💥 Error
# MAGIC
# MAGIC -- BUENO: todas las columnas no agregadas en GROUP BY
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas GROUP BY sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: WHERE antes, HAVING después de GROUP BY**
# MAGIC ```sql
# MAGIC -- MALO: usar HAVING para filtrar filas (no grupos)
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas
# MAGIC HAVING fecha >= '2023-01-01'  -- 💥 fecha no es agregación
# MAGIC GROUP BY sucursal_id;
# MAGIC
# MAGIC -- BUENO: WHERE para filas, HAVING para grupos
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas
# MAGIC WHERE fecha >= '2023-01-01'   -- filtra filas antes
# MAGIC GROUP BY sucursal_id
# MAGIC HAVING SUM(ventas) > 1000000;  -- filtra grupos después
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: CASE WHEN evalúa en orden, el primer match gana**
# MAGIC ```sql
# MAGIC -- MALO: condiciones solapadas, siempre cae en la primera
# MAGIC CASE WHEN ventas > 30000 THEN 'Bajo'    -- 100000 > 30000 → 'Bajo' 💥
# MAGIC      WHEN ventas > 50000 THEN 'Medio'
# MAGIC      WHEN ventas > 80000 THEN 'Alto'
# MAGIC END
# MAGIC
# MAGIC -- BUENO: de mayor a menor, el primer match gana
# MAGIC CASE WHEN ventas > 80000 THEN 'Alto'
# MAGIC      WHEN ventas > 50000 THEN 'Medio'
# MAGIC      WHEN ventas > 30000 THEN 'Bajo'
# MAGIC      ELSE 'Muy Bajo'
# MAGIC END
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | SQL |
# MAGIC |-----------|-----|
# MAGIC | Agregar por categoría | `GROUP BY col` + `SUM/AVG/COUNT` |
# MAGIC | Filtrar filas antes de agrupar | `WHERE cond` |
# MAGIC | Filtrar grupos después de agrupar | `HAVING agg_cond` |
# MAGIC | Clasificar por rangos | `CASE WHEN ... THEN ... END` |
# MAGIC | Agregar por año | `GROUP BY YEAR(fecha)` |
# MAGIC | Agregar por año y mes | `GROUP BY YEAR(fecha), MONTH(fecha)` |
# MAGIC | Ranking por grupo | `ROW_NUMBER() OVER (PARTITION BY ...)` |
# MAGIC | Top N por grupo | CTE + `ROW_NUMBER()` + `WHERE ranking <= N` |
# MAGIC | Múltiples agregaciones | `SUM() AS total, AVG() AS prom, COUNT() AS n` |
# MAGIC | Redondear resultados | `ROUND(SUM(ventas), 2) AS total` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>📊 ¡Agregaciones, GROUP BY y CASE WHEN dominados!</h3>
# MAGIC   <p><i>"GROUP BY segmenta, CASE WHEN clasifica, HAVING filtra: la trinidad del análisis SQL agregado."</i></p>
# MAGIC </div>