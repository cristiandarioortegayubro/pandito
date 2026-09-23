# Databricks notebook source


# COMMAND ----------

# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🗄️ Módulo 14 - Notebook 01: SQL Editor y primeras consultas
# MAGIC
# MAGIC ## 📊 Databricks SQL: El lenguaje universal de datos
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
# MAGIC Al finalizar este notebook serás capaz de:
# MAGIC
# MAGIC ✅ **Usar** el SQL Editor de Databricks  
# MAGIC ✅ **Escribir** consultas SELECT, WHERE, ORDER BY  
# MAGIC ✅ **Filtrar** datos con operadores de comparación  
# MAGIC ✅ **Ordenar** y limitar resultados  
# MAGIC ✅ **Aplicar** funciones SQL (COUNT, SUM, AVG, MIN, MAX)  
# MAGIC ✅ **Entender** la diferencia entre SQL y PySpark DataFrame API
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Módulos 12-13 completados (PySpark Core y Transformación)
# MAGIC * ✅ Conocimiento básico de DataFrames
# MAGIC * ✅ Familiaridad con conceptos de tablas y columnas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **Databricks SQL Editor** - Interfaz y características
# MAGIC 2. **SELECT** - Extracción de columnas
# MAGIC 3. **WHERE** - Filtrado de filas
# MAGIC 4. **ORDER BY y LIMIT** - Ordenamiento y paginación
# MAGIC 5. **Funciones agregadas** - COUNT, SUM, AVG, MIN, MAX
# MAGIC 6. **DISTINCT** - Valores únicos
# MAGIC 7. **Caso integrador** - Análisis de ventas de Los Andes Market

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
# MAGIC %sql
# MAGIC -- 💾 CARGA DE DATOS PARA SQL EDITOR
# MAGIC -- Verificamos que la tabla de ventas existe en Unity Catalog
# MAGIC
# MAGIC USE CATALOG pandito_ds;
# MAGIC USE SCHEMA default;
# MAGIC
# MAGIC -- Vista previa de la tabla principal
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3 LIMIT 10;
# MAGIC
# MAGIC -- Información de la tabla
# MAGIC DESCRIBE TABLE ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Conteo total de registros
# MAGIC SELECT COUNT(*) AS total_registros FROM ventas_mensuales_mendoza_h3;

# COMMAND ----------

# DBTITLE 1,📚 Teoría: SQL Editor y Consultas
# MAGIC %md
# MAGIC ## 📚 Teoría: SQL Editor y Consultas Declarativas
# MAGIC
# MAGIC ### 🗄️ ¿Qué es el Databricks SQL Editor?
# MAGIC
# MAGIC **Databricks SQL Editor** es la interfaz dedicada para escribir y ejecutar consultas SQL sobre datos en Unity Catalog. Es diferente a ejecutar `%sql` en notebooks:
# MAGIC
# MAGIC | Característica | Notebook `%sql` | SQL Editor |
# MAGIC |----------------|----------------|------------|
# MAGIC | Interfaz | Celda de notebook | Editor dedicado |
# MAGIC | Resultados | Inline | Tabla interactiva |
# MAGIC | Visualizaciones | Con código | Widgets nativos |
# MAGIC | Dashboards | Programando | Drag-and-drop |
# MAGIC | Compartir | Notebook | Query URL |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📖 Sintaxis SQL Fundamental
# MAGIC
# MAGIC **1️⃣ SELECT: Extraer columnas**
# MAGIC ```sql
# MAGIC -- Seleccionar columnas específicas
# MAGIC SELECT fecha, sucursal_id, ventas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Seleccionar todas las columnas
# MAGIC SELECT * FROM pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Crear columnas calculadas
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_id,
# MAGIC   ventas,
# MAGIC   ventas * 1.21 AS ventas_con_iva,
# MAGIC   ventas / 12 AS ventas_promedio_diario
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC **2️⃣ WHERE: Filtrar filas**
# MAGIC ```sql
# MAGIC -- Filtro simple
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas > 50000;
# MAGIC
# MAGIC -- Filtros múltiples (AND / OR)
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas > 50000 AND sucursal_id = 'S001';
# MAGIC
# MAGIC -- BETWEEN
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas BETWEEN 30000 AND 80000;
# MAGIC
# MAGIC -- IN
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE sucursal_id IN ('S001', 'S002', 'S003');
# MAGIC
# MAGIC -- LIKE (patrones de texto)
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE sucursal_id LIKE 'S%';
# MAGIC
# MAGIC -- IS NULL / IS NOT NULL
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas IS NOT NULL;
# MAGIC ```
# MAGIC
# MAGIC **3️⃣ ORDER BY y LIMIT**
# MAGIC ```sql
# MAGIC -- Ordenar ascendente
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas ASC;
# MAGIC
# MAGIC -- Ordenar descendente
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas DESC;
# MAGIC
# MAGIC -- Top 10 ventas más altas
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 10;
# MAGIC ```
# MAGIC
# MAGIC **4️⃣ Funciones Agregadas**
# MAGIC ```sql
# MAGIC -- Estadísticas básicas
# MAGIC SELECT 
# MAGIC   COUNT(*) AS total_filas,
# MAGIC   SUM(ventas) AS ventas_totales,
# MAGIC   AVG(ventas) AS ventas_promedio,
# MAGIC   MIN(ventas) AS ventas_minimas,
# MAGIC   MAX(ventas) AS ventas_maximas
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- COUNT DISTINCT
# MAGIC SELECT COUNT(DISTINCT sucursal_id) AS sucursales_unicas
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC **5️⃣ DISTINCT: Valores únicos**
# MAGIC ```sql
# MAGIC -- Sucursales únicas
# MAGIC SELECT DISTINCT sucursal_id 
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC ORDER BY sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 SQL vs Pandas vs PySpark
# MAGIC
# MAGIC | Operación | Pandas | PySpark | SQL |
# MAGIC |-----------|--------|---------|-----|
# MAGIC | Seleccionar | `df[['col']]` | `df.select('col')` | `SELECT col` |
# MAGIC | Filtrar | `df[df.x > 5]` | `df.filter(col('x') > 5)` | `WHERE x > 5` |
# MAGIC | Agregar | `df['x'].sum()` | `df.agg({'x': 'sum'})` | `SUM(x)` |
# MAGIC | Ordenar | `df.sort_values('x')` | `df.orderBy('x')` | `ORDER BY x` |
# MAGIC | Limitar | `df.head(10)` | `df.limit(10)` | `LIMIT 10` |
# MAGIC
# MAGIC **SQL es declarativo**: describes QUÉ quieres, no CÓMO obtenerlo.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **SQL es el lenguaje más demandado en analítica:**
# MAGIC * 📊 95% de empresas usan SQL
# MAGIC * 💼 Requerido en: Data Analyst, Data Engineer, Data Scientist
# MAGIC * 🔗 Conecta con: BI Tools (Tableau, Power BI), Databricks, Snowflake
# MAGIC * 🏢 Estándar: ISO/ANSI desde 1986

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
# MAGIC %sql
# MAGIC -- 💻 SETUP INICIAL: Verificación de entorno SQL
# MAGIC
# MAGIC -- Verificar catálogo activo
# MAGIC SELECT current_catalog() AS catalog_actual, current_schema() AS schema_actual;
# MAGIC
# MAGIC -- Verificar que la tabla existe
# MAGIC SHOW TABLES IN pandito_ds.default LIKE 'ventas_mensuales_mendoza_h3';
# MAGIC
# MAGIC -- Ejercicio: Mostrar las 5 sucursales con mayores ventas promedio
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS meses_con_datos,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_totales,
# MAGIC   ROUND(MIN(ventas), 2) AS ventas_minimas,
# MAGIC   ROUND(MAX(ventas), 2) AS ventas_maximas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id
# MAGIC ORDER BY ventas_promedio DESC
# MAGIC LIMIT 5;
# MAGIC
# MAGIC -- Ejercicio: Filtrar ventas por rango de fechas
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_id,
# MAGIC   ventas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC WHERE fecha >= '2023-01-01'
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# DBTITLE 1,📊 Teoría: SQL con datos reales
# MAGIC %md
# MAGIC ## 📊 Consultas SQL con datos reales de Los Andes Market
# MAGIC
# MAGIC ### 🏪 Nuestra tabla en Unity Catalog
# MAGIC
# MAGIC `pandito_ds.default.ventas_mensuales_mendoza_h3` contiene las ventas mensuales de **Los Andes Market** en Mendoza:
# MAGIC
# MAGIC | Columna | Tipo | Descripción |
# MAGIC |---------|------|-------------|
# MAGIC | `fecha` | date | Mes de la venta |
# MAGIC | `sucursal_id` | string | ID de sucursal |
# MAGIC | `sucursal_nombre` | string | Nombre legible |
# MAGIC | `zona` | string | Zona comercial |
# MAGIC | `lat`, `lon` | double | Coordenadas GPS |
# MAGIC | `ventas` | double | Monto vendido |
# MAGIC | `h3_index`, `h3_res8`, `h3_res7` | string | Índices hexagonales |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio con SQL
# MAGIC * ¿Cuáles son las 10 ventas mensuales más altas?
# MAGIC * ¿Qué sucursales venden más de $100k/mes?
# MAGIC * ¿Cuántos registros hay por año?
# MAGIC * ¿Cómo comparar SQL con lo que ya sabemos de Pandas/PySpark?

# COMMAND ----------

# DBTITLE 1,📊 Práctica: SQL con datos reales
# MAGIC %sql
# MAGIC -- 📊 PRÁCTICA SQL CON DATOS REALES DE LOS ANDES MARKET
# MAGIC
# MAGIC -- 1️⃣  TOP 10 VENTAS MENSUALES MÁS ALTAS
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   ROUND(ventas, 0) AS ventas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 10;
# MAGIC
# MAGIC -- 2️⃣  VENTAS POR ZONA (agregación básica)
# MAGIC SELECT 
# MAGIC   zona,
# MAGIC   COUNT(*) AS registros,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 0) AS ventas_promedio,
# MAGIC   ROUND(MAX(ventas), 0) AS venta_max,
# MAGIC   ROUND(MIN(ventas), 0) AS venta_min
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY zona
# MAGIC ORDER BY ventas_totales DESC;
# MAGIC
# MAGIC -- 3️⃣  FILTROS: Ventas altas en Corredor Comercial
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_nombre,
# MAGIC   ROUND(ventas, 0) AS ventas
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC WHERE ventas > 100000 
# MAGIC   AND zona = 'Corredor Comercial'
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 15;
# MAGIC
# MAGIC -- 4️⃣  COLUMNAS CALCULADAS: IVA y margen estimado
# MAGIC SELECT 
# MAGIC   fecha,
# MAGIC   sucursal_nombre,
# MAGIC   ROUND(ventas, 0) AS ventas,
# MAGIC   ROUND(ventas * 1.21, 0) AS ventas_con_iva,
# MAGIC   ROUND(ventas * 0.15, 0) AS margen_estimado,
# MAGIC   ROUND(ventas / 30, 0) AS ventas_diarias
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ORDER BY ventas DESC
# MAGIC LIMIT 10;
# MAGIC
# MAGIC -- 5️⃣  REGISTROS POR AÑO
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   COUNT(*) AS registros,
# MAGIC   COUNT(DISTINCT sucursal_id) AS sucursales_activas,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_anuales
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha)
# MAGIC ORDER BY anio;
# MAGIC
# MAGIC -- 6️⃣  SUCURSALES ÚNICAS CON COORDENADAS
# MAGIC SELECT DISTINCT 
# MAGIC   sucursal_id,
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   lat,
# MAGIC   lon
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ORDER BY sucursal_id;

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 14_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **SELECT — extracción de columnas:**
# MAGIC    - `SELECT col1, col2 FROM tabla` — columnas específicas
# MAGIC    - `SELECT * FROM tabla` — todas las columnas
# MAGIC    - `SELECT ventas * 1.21 AS ventas_con_iva` — columnas calculadas con alias
# MAGIC
# MAGIC 2. **WHERE — filtrado de filas:**
# MAGIC    - `WHERE ventas > 50000` — comparación
# MAGIC    - `WHERE ventas BETWEEN 30000 AND 80000` — rango
# MAGIC    - `WHERE sucursal_id IN ('S001', 'S002')` — lista de valores
# MAGIC    - `WHERE sucursal_id LIKE 'S%'` — patrón de texto
# MAGIC    - `WHERE ventas IS NOT NULL` — nulos
# MAGIC
# MAGIC 3. **ORDER BY y LIMIT — ordenamiento y paginación:**
# MAGIC    - `ORDER BY ventas DESC` — descendente (mayor a menor)
# MAGIC    - `ORDER BY ventas ASC` — ascendente (menor a mayor)
# MAGIC    - `LIMIT 10` — primeros N resultados
# MAGIC    - Combinar: `ORDER BY ventas DESC LIMIT 10` → top 10
# MAGIC
# MAGIC 4. **Funciones agregadas:**
# MAGIC    - `COUNT(*)` — total de filas
# MAGIC    - `SUM(ventas)` — suma total
# MAGIC    - `AVG(ventas)` — promedio
# MAGIC    - `MIN(ventas)` / `MAX(ventas)` — extremos
# MAGIC    - `COUNT(DISTINCT sucursal_id)` — valores únicos
# MAGIC
# MAGIC 5. **SQL vs Pandas vs PySpark:**
# MAGIC    - SQL es declarativo: describes QUÉ quieres, no CÓMO obtenerlo
# MAGIC    - `df[['col']]` (Pandas) = `df.select('col')` (PySpark) = `SELECT col` (SQL)
# MAGIC    - SQL es el estándar universal: 95% de empresas lo usan
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Nunca usar SELECT * en producción**
# MAGIC ```sql
# MAGIC -- MALO: trae todas las columnas, incluyendo las innecesarias
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- BUENO: solo las columnas necesarias
# MAGIC SELECT fecha, sucursal_id, ventas
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Siempre usar alias en columnas calculadas**
# MAGIC ```sql
# MAGIC -- MALO: nombre de columna autogenerado e incomprensible
# MAGIC SELECT ventas * 1.21 FROM ventas_mensuales_mendoza_h3;
# MAGIC -- Resultado: (ventas * 1.21)
# MAGIC
# MAGIC -- BUENO: alias descriptivo
# MAGIC SELECT ventas * 1.21 AS ventas_con_iva
# MAGIC FROM ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Filtrar antes de agregar para optimizar**
# MAGIC ```sql
# MAGIC -- MALO: agregar todo y luego filtrar (escanea toda la tabla)
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas_mensuales_mendoza_h3
# MAGIC HAVING SUM(ventas) > 1000000;
# MAGIC
# MAGIC -- BUENO: filtrar antes con WHERE (reduce datos a procesar)
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas_mensuales_mendoza_h3
# MAGIC WHERE fecha >= '2023-01-01'
# MAGIC GROUP BY sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | SQL |
# MAGIC |-----------|-----|
# MAGIC | Seleccionar columnas | `SELECT col1, col2 FROM tabla` |
# MAGIC | Columna calculada | `SELECT col * 1.21 AS iva FROM tabla` |
# MAGIC | Filtrar por valor | `WHERE col > 1000` |
# MAGIC | Filtrar por rango | `WHERE col BETWEEN 100 AND 500` |
# MAGIC | Filtrar por lista | `WHERE col IN ('a', 'b', 'c')` |
# MAGIC | Filtrar por patrón | `WHERE col LIKE 'S%'` |
# MAGIC | Detectar nulos | `WHERE col IS NULL` |
# MAGIC | Ordenar resultados | `ORDER BY col DESC` |
# MAGIC | Limitar resultados | `LIMIT 10` |
# MAGIC | Contar filas | `SELECT COUNT(*) FROM tabla` |
# MAGIC | Sumar valores | `SELECT SUM(col) FROM tabla` |
# MAGIC | Valores únicos | `SELECT DISTINCT col FROM tabla` |
# MAGIC | Promedio | `SELECT AVG(col) FROM tabla` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🗄️ ¡SQL Editor y primeras consultas dominados!</h3>
# MAGIC   <p><i>"SQL es declarativo: describes qué quieres, no cómo obtenerlo. El lenguaje universal de datos."</i></p>
# MAGIC </div>