# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🏗️ Módulo 14 - Notebook 04: Vistas, Unity Catalog y permisos
# MAGIC
# MAGIC ## 🔒 Gobernanza de Datos en Databricks
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
# MAGIC ✅ **Crear** vistas SQL (CREATE VIEW)  
# MAGIC ✅ **Entender** la arquitectura de Unity Catalog  
# MAGIC ✅ **Navegar** catálogos, schemas y tablas  
# MAGIC ✅ **Aplicar** CREATE TABLE AS SELECT (CTAS)  
# MAGIC ✅ **Configurar** permisos básicos con GRANT/REVOKE  
# MAGIC ✅ **Implementar** gobernanza de datos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 14_01 al 14_03 completados
# MAGIC * ✅ Conocimiento de JOINs y CTEs
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **CREATE VIEW** - Vistas para reutilizar consultas
# MAGIC 2. **Unity Catalog** - Arquitectura de gobernanza
# MAGIC 3. **Catálogos y Schemas** - Organización de datos
# MAGIC 4. **CREATE TABLE AS SELECT** - Crear tablas desde consultas
# MAGIC 5. **GRANT/REVOKE** - Permisos y seguridad
# MAGIC 6. **Caso integrador** - Data layer empresarial

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
# MAGIC %sql
# MAGIC -- 💾 CARGA: Explorar estructura de Unity Catalog
# MAGIC
# MAGIC -- Ver catálogo actual
# MAGIC SELECT current_catalog();
# MAGIC
# MAGIC -- Listar catálogos disponibles
# MAGIC SHOW CATALOGS;
# MAGIC
# MAGIC -- Listar schemas en el catálogo del proyecto
# MAGIC SHOW SCHEMAS IN pandito_ds;
# MAGIC
# MAGIC -- Listar tablas en el schema default
# MAGIC SHOW TABLES IN pandito_ds.default;
# MAGIC
# MAGIC -- Ver estructura de la tabla principal
# MAGIC DESCRIBE TABLE pandito_ds.default.ventas_mensuales_mendoza_h3;

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Vistas y Unity Catalog
# MAGIC %md
# MAGIC ## 📚 Teoría: Vistas, Unity Catalog y Gobernanza
# MAGIC
# MAGIC ### 🏗️ CREATE VIEW: Vistas SQL
# MAGIC
# MAGIC **Vista:** Una consulta SQL guardada como objeto. Se usa como una tabla virtual.
# MAGIC
# MAGIC ```sql
# MAGIC -- Crear vista de ventas anuales
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_ventas_anuales AS
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   COUNT(*) AS meses,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id, YEAR(fecha);
# MAGIC
# MAGIC -- Usar la vista
# MAGIC SELECT * FROM pandito_ds.default.vw_ventas_anuales ORDER BY ventas_totales DESC;
# MAGIC ```
# MAGIC
# MAGIC **Ventajas de las vistas:**
# MAGIC * 🔒 Seguridad: Ocultar columnas sensibles
# MAGIC * ♻️ Reutilización: Una consulta, múltiples usos
# MAGIC * 📦 Abstracción: Simplificar consultas complejas
# MAGIC * 🔄 Actualización automática: Refleja cambios en datos base
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🗄️ Unity Catalog: Arquitectura
# MAGIC
# MAGIC **Unity Catalog** es el sistema de gobernanza de datos de Databricks:
# MAGIC
# MAGIC ```
# MAGIC Metastore (Cuenta Databricks)
# MAGIC └── Catálogo (pandito_ds)
# MAGIC     └── Schema (default)
# MAGIC         ├── Tabla: ventas_mensuales_mendoza_h3
# MAGIC         ├── Tabla: dl_sequences_lstm
# MAGIC         ├── Vista: vw_ventas_anuales
# MAGIC         └── Volume: archivos/
# MAGIC ```
# MAGIC
# MAGIC **Niveles de gobernanza:**
# MAGIC | Nivel | Qué controla | Ejemplo |
# MAGIC |-------|-------------|---------|
# MAGIC | **Catálogo** | Acceso a bases de datos | `pandito_ds` |
# MAGIC | **Schema** | Agrupación de tablas | `default`, `staging` |
# MAGIC | **Tabla** | Datos individuales | `ventas_mensuales_mendoza_h3` |
# MAGIC | **Columna** | Granularidad fina | `ventas`, `sucursal_id` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📦 CREATE TABLE AS SELECT (CTAS)
# MAGIC
# MAGIC ```sql
# MAGIC -- Crear tabla resumen desde consulta
# MAGIC CREATE TABLE IF NOT EXISTS pandito_ds.default.resumen_sucursales
# MAGIC AS SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS total_meses,
# MAGIC   ROUND(AVG(ventas), 2) AS promedio_ventas,
# MAGIC   ROUND(MIN(ventas), 2) AS venta_minima,
# MAGIC   ROUND(MAX(ventas), 2) AS venta_maxima
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id;
# MAGIC
# MAGIC -- Consultar la nueva tabla
# MAGIC SELECT * FROM pandito_ds.default.resumen_sucursales
# MAGIC ORDER BY promedio_ventas DESC;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔒 GRANT y REVOKE: Permisos
# MAGIC
# MAGIC ```sql
# MAGIC -- Otorgar permiso de lectura
# MAGIC GRANT SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3 TO `user@email.com`;
# MAGIC
# MAGIC -- Otorgar acceso a todo el schema
# MAGIC GRANT USE SCHEMA ON SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC GRANT SELECT ON ALL TABLES IN SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC
# MAGIC -- Revocar permiso
# MAGIC REVOKE SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3 FROM `user@email.com`;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Gobernanza de datos = confianza empresarial:**
# MAGIC * 🔒 **Seguridad:** Control de acceso granular
# MAGIC * 📋 **Auditoría:** Quién accedió a qué datos
# MAGIC * 🏷️ **Linaje:** Trazabilidad de transformaciones
# MAGIC * 🤝 **Colaboración:** Múltiples equipos, mismo datos
# MAGIC * 📊 **Descubrimiento:** Búsqueda y catalogación de datos

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
# MAGIC %sql
# MAGIC -- 💻 SETUP: Ejercicios de Vistas y Unity Catalog
# MAGIC
# MAGIC -- Ejercicio 1: Crear vista de KPIs por sucursal
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_kpis_sucursal AS
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   COUNT(*) AS meses_activos,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 2) AS ventas_promedio,
# MAGIC   ROUND(MIN(ventas), 2) AS venta_minima,
# MAGIC   ROUND(MAX(ventas), 2) AS venta_maxima,
# MAGIC   ROUND(STDDEV(ventas), 2) AS volatilidad
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id;
# MAGIC
# MAGIC -- Consultar la vista
# MAGIC SELECT * FROM pandito_ds.default.vw_kpis_sucursal ORDER BY ventas_promedio DESC;
# MAGIC
# MAGIC -- Ejercicio 2: Crear tabla resumen anual
# MAGIC CREATE OR REPLACE TABLE pandito_ds.default.resumen_anual_ventas
# MAGIC AS SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   sucursal_id,
# MAGIC   ROUND(SUM(ventas), 2) AS ventas_anuales,
# MAGIC   ROUND(AVG(ventas), 2) AS promedio_mensual,
# MAGIC   COUNT(*) AS meses_con_datos
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha), sucursal_id;
# MAGIC
# MAGIC -- Verificar la tabla creada
# MAGIC SELECT * FROM pandito_ds.default.resumen_anual_ventas ORDER BY anio DESC, ventas_anuales DESC;
# MAGIC
# MAGIC -- Ejercicio 3: Vista de crecimiento interanual
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_crecimiento_interanual AS
# MAGIC WITH ventas_anuales AS (
# MAGIC   SELECT sucursal_id, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC   GROUP BY sucursal_id, YEAR(fecha)
# MAGIC )
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   anio,
# MAGIC   total,
# MAGIC   LAG(total) OVER (PARTITION BY sucursal_id ORDER BY anio) AS total_anterior,
# MAGIC   ROUND((total - LAG(total) OVER (PARTITION BY sucursal_id ORDER BY anio)) 
# MAGIC     / LAG(total) OVER (PARTITION BY sucursal_id ORDER BY anio) * 100, 2) AS crecimiento_pct
# MAGIC FROM ventas_anuales;
# MAGIC
# MAGIC SELECT * FROM pandito_ds.default.vw_crecimiento_interanual ORDER BY sucursal_id, anio;

# COMMAND ----------

# DBTITLE 1,🏗️ Teoría: Vistas con datos reales
# MAGIC %md
# MAGIC ## 🏗️ Vistas y gobernanza con datos reales de Los Andes Market
# MAGIC
# MAGIC ### 📦 Data layer empresarial
# MAGIC
# MAGIC Con SQL podemos crear **vistas reutilizables** sobre `ventas_mensuales_mendoza_h3` que sirvan como capa de abstracción para diferentes consumidores:
# MAGIC
# MAGIC ```sql
# MAGIC -- Vista para el CFO: resumen anual
# MAGIC CREATE OR REPLACE VIEW vw_ventas_anuales AS
# MAGIC SELECT sucursal_id, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id, YEAR(fecha);
# MAGIC
# MAGIC -- Vista para operaciones: KPIs mensuales
# MAGIC CREATE OR REPLACE VIEW vw_kpis_mensuales AS
# MAGIC SELECT sucursal_id, MONTH(fecha) AS mes, AVG(ventas) AS promedio
# MAGIC FROM ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id, MONTH(fecha);
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué vistas necesitaría el CFO? ¿Y el equipo de operaciones?
# MAGIC * ¿Cómo crear una tabla resumen física con CTAS?
# MAGIC * ¿Qué permisos dar a un analista externo?

# COMMAND ----------

# DBTITLE 1,🏗️ Práctica: Vistas con datos reales
# MAGIC %sql
# MAGIC -- 🏗️ PRÁCTICA: VISTAS Y CTAS CON LOS ANDES MARKET
# MAGIC
# MAGIC -- 1️⃣  VISTA: Dashboard ejecutivo por sucursal
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_dashboard_sucursal AS
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   COUNT(*) AS meses_activos,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_totales,
# MAGIC   ROUND(AVG(ventas), 0) AS ventas_promedio,
# MAGIC   ROUND(MAX(ventas), 0) AS mejor_mes,
# MAGIC   ROUND(MIN(ventas), 0) AS peor_mes,
# MAGIC   ROUND(STDDEV(ventas), 0) AS volatilidad,
# MAGIC   CASE 
# MAGIC     WHEN AVG(ventas) > 100000 THEN 'Alto'
# MAGIC     WHEN AVG(ventas) > 50000 THEN 'Medio'
# MAGIC     ELSE 'Bajo'
# MAGIC   END AS rendimiento
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id, sucursal_nombre, zona;
# MAGIC
# MAGIC SELECT * FROM pandito_ds.default.vw_dashboard_sucursal
# MAGIC ORDER BY ventas_promedio DESC;
# MAGIC
# MAGIC -- 2️⃣  VISTA: Evolución mensual con lag
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_evolucion_mensual AS
# MAGIC SELECT 
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   fecha,
# MAGIC   ROUND(ventas, 0) AS ventas,
# MAGIC   ROUND(LAG(ventas) OVER (PARTITION BY sucursal_id ORDER BY fecha), 0) AS ventas_mes_anterior,
# MAGIC   ROUND(
# MAGIC     (ventas - LAG(ventas) OVER (PARTITION BY sucursal_id ORDER BY fecha)) 
# MAGIC     / LAG(ventas) OVER (PARTITION BY sucursal_id ORDER BY fecha) * 100, 1
# MAGIC   ) AS variacion_pct
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC SELECT * FROM pandito_ds.default.vw_evolucion_mensual
# MAGIC ORDER BY ABS(variacion_pct) DESC NULLS LAST
# MAGIC LIMIT 15;
# MAGIC
# MAGIC -- 3️⃣  CTAS: Tabla física resumen anual por zona
# MAGIC CREATE OR REPLACE TABLE pandito_ds.default.resumen_anual_zona AS
# MAGIC SELECT 
# MAGIC   YEAR(fecha) AS anio,
# MAGIC   zona,
# MAGIC   COUNT(DISTINCT sucursal_id) AS sucursales,
# MAGIC   ROUND(SUM(ventas), 0) AS ventas_anuales,
# MAGIC   ROUND(AVG(ventas), 0) AS promedio_mensual,
# MAGIC   ROUND(MAX(ventas), 0) AS mejor_mes,
# MAGIC   ROUND(MIN(ventas), 0) AS peor_mes
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha), zona;
# MAGIC
# MAGIC SELECT * FROM pandito_ds.default.resumen_anual_zona
# MAGIC ORDER BY anio DESC, ventas_anuales DESC;
# MAGIC
# MAGIC -- 4️⃣  CTAS: Tabla de outliers (z-score > 1.5)
# MAGIC CREATE OR REPLACE TABLE pandito_ds.default.outliers_ventas AS
# MAGIC SELECT 
# MAGIC   sucursal_nombre,
# MAGIC   zona,
# MAGIC   fecha,
# MAGIC   ROUND(ventas, 0) AS ventas,
# MAGIC   ROUND(promedio, 0) AS promedio_sucursal,
# MAGIC   ROUND(desviacion, 0) AS std_sucursal,
# MAGIC   ROUND((ventas - promedio) / desviacion, 2) AS z_score,
# MAGIC   CASE 
# MAGIC     WHEN (ventas - promedio) / desviacion > 1.5 THEN 'Outlier Superior'
# MAGIC     WHEN (ventas - promedio) / desviacion < -1.5 THEN 'Outlier Inferior'
# MAGIC   END AS tipo_outlier
# MAGIC FROM (
# MAGIC   SELECT 
# MAGIC     sucursal_nombre, zona, fecha, ventas,
# MAGIC     AVG(ventas) OVER (PARTITION BY sucursal_id) AS promedio,
# MAGIC     STDDEV(ventas) OVER (PARTITION BY sucursal_id) AS desviacion
# MAGIC   FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ) sub
# MAGIC WHERE ABS((ventas - promedio) / desviacion) > 1.5;
# MAGIC
# MAGIC SELECT * FROM pandito_ds.default.outliers_ventas
# MAGIC ORDER BY ABS(z_score) DESC;
# MAGIC
# MAGIC -- 5️⃣  VERIFICAR OBJETOS CREADOS
# MAGIC SHOW TABLES IN pandito_ds.default;

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 14_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **CREATE VIEW — vistas SQL:**
# MAGIC    ```sql
# MAGIC    CREATE OR REPLACE VIEW pandito_ds.default.vw_ventas_anuales AS
# MAGIC    SELECT sucursal_id, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC    GROUP BY sucursal_id, YEAR(fecha);
# MAGIC    
# MAGIC    -- Usar como tabla virtual
# MAGIC    SELECT * FROM pandito_ds.default.vw_ventas_anuales;
# MAGIC    ```
# MAGIC
# MAGIC 2. **Unity Catalog — arquitectura de gobernanza:**
# MAGIC    ```sql
# MAGIC    -- Jerarquía: Metastore → Catálogo → Schema → Tabla
# MAGIC    SHOW CATALOGS;                    -- Listar catálogos
# MAGIC    SHOW SCHEMAS IN pandito_ds;      -- Listar schemas
# MAGIC    SHOW TABLES IN pandito_ds.default; -- Listar tablas
# MAGIC    DESCRIBE TABLE pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC    ```
# MAGIC
# MAGIC 3. **CREATE TABLE AS SELECT (CTAS):**
# MAGIC    ```sql
# MAGIC    -- Crear tabla física desde consulta
# MAGIC    CREATE TABLE IF NOT EXISTS pandito_ds.default.resumen_sucursales
# MAGIC    AS SELECT sucursal_id, AVG(ventas) AS promedio, MAX(ventas) AS maximo
# MAGIC    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC    GROUP BY sucursal_id;
# MAGIC    ```
# MAGIC
# MAGIC 4. **GRANT y REVOKE — permisos:**
# MAGIC    ```sql
# MAGIC    -- Otorgar lectura
# MAGIC    GRANT SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC      TO `user@email.com`;
# MAGIC    
# MAGIC    -- Otorgar acceso al schema
# MAGIC    GRANT USE SCHEMA ON SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC    GRANT SELECT ON ALL TABLES IN SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC    
# MAGIC    -- Revocar
# MAGIC    REVOKE SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC      FROM `user@email.com`;
# MAGIC    ```
# MAGIC
# MAGIC 5. **Caso integrador — data layer empresarial:**
# MAGIC    - Vista de KPIs por sucursal (`vw_kpis_sucursal`)
# MAGIC    - Tabla resumen anual con CTAS (`resumen_anual_ventas`)
# MAGIC    - Vista de crecimiento interanual con LAG y window functions
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de Vistas y Unity Catalog
# MAGIC
# MAGIC **Caso 1: Crear vista reutilizable**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE VIEW pandito_ds.default.vw_kpis AS
# MAGIC SELECT sucursal_id, SUM(ventas) AS total, AVG(ventas) AS promedio
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Crear tabla física con CTAS**
# MAGIC ```sql
# MAGIC CREATE TABLE IF NOT EXISTS pandito_ds.default.resumen AS
# MAGIC SELECT YEAR(fecha) AS anio, sucursal_id, SUM(ventas) AS total
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY YEAR(fecha), sucursal_id;
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Otorgar permisos a un usuario**
# MAGIC ```sql
# MAGIC GRANT USE CATALOG ON CATALOG pandito_ds TO `user@email.com`;
# MAGIC GRANT USE SCHEMA ON SCHEMA pandito_ds.default TO `user@email.com`;
# MAGIC GRANT SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3 TO `user@email.com`;
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Revocar permisos**
# MAGIC ```sql
# MAGIC REVOKE SELECT ON TABLE pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC FROM `user@email.com`;
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Explorar la jerarquía de Unity Catalog**
# MAGIC ```sql
# MAGIC SHOW CATALOGS;
# MAGIC SHOW SCHEMAS IN pandito_ds;
# MAGIC SHOW TABLES IN pandito_ds.default;
# MAGIC DESCRIBE TABLE pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 14
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **14_01 - SQL Editor Primeras Consultas:** SELECT, WHERE, ORDER BY, LIMIT, agregaciones
# MAGIC 2. **14_02 - Agregaciones GROUP BY CASE WHEN:** GROUP BY, HAVING, CASE WHEN, window functions
# MAGIC 3. **14_03 - JOINs Subconsultas CTEs:** INNER/LEFT/RIGHT JOIN, subconsultas, CTEs, EXISTS
# MAGIC 4. **14_04 - Vistas Unity Catalog y Permisos:** CREATE VIEW, CTAS, GRANT/REVOKE, gobernanza
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Crear vistas SQL para reutilización y seguridad
# MAGIC * ✅ Navegar la jerarquía de Unity Catalog (catálogo → schema → tabla)
# MAGIC * ✅ Crear tablas físicas con CREATE TABLE AS SELECT
# MAGIC * ✅ Configurar permisos con GRANT y REVOKE
# MAGIC * ✅ Implementar gobernanza de datos profesional
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🔒 ¡Módulo 14 Completado!</h3>
# MAGIC   <p><i>"Dominas SQL Editor: desde SELECT hasta gobernanza con Unity Catalog. Ahora puedes construir capas de datos profesionales en Databricks."</i></p>
# MAGIC </div>