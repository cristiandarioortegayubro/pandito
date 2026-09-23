# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 📊 Módulo 16 - Notebook 02: Dashboards AI/BI (Lakeview)
# MAGIC
# MAGIC ## 📈 Visualización ejecutiva con Databricks AI/BI Dashboards
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 16 - Genie Spaces, Dashboards AI/BI y ETL  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué son los AI/BI Dashboards (Lakeview)  
# MAGIC ✅ **Crear** dashboards desde consultas SQL  
# MAGIC ✅ **Diseñar** widgets: tablas, gráficos, KPIs  
# MAGIC ✅ **Aplicar** filtros interactivos  
# MAGIC ✅ **Compartir** dashboards con el equipo  
# MAGIC ✅ **Diferenciar** Lakeview de Plotly notebooks
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 14 (SQL Editor) y 09 (Plotly) completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **AI/BI Dashboards** - Qué son y cómo funcionan
# MAGIC 2. **Crear dashboard** - Desde SQL query
# MAGIC 3. **Widgets** - Tablas, barras, líneas, KPIs
# MAGIC 4. **Filtros** - Interactividad con parámetros
# MAGIC 5. **Diseño** - Layout y publicación

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd

print("💾 DATOS PARA DASHBOARDS AI/BI")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Datos cargados: {len(df)} registros")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n📌 Para crear un AI/BI Dashboard:")
print("   1. Escribe una SQL query en SQL Editor")
print("   2. Click en 'Create Dashboard' > 'AI/BI Dashboard'")
print("   3. Agrega widgets (tablas, gráficos, KPIs)")
print("   4. Configura filtros interactivos")
print("   5. Publica y comparte")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Dashboards AI/BI
# MAGIC %md
# MAGIC ## 📚 Teoría: AI/BI Dashboards (Lakeview)
# MAGIC
# MAGIC ### 📊 ¿Qué son los AI/BI Dashboards?
# MAGIC
# MAGIC **AI/BI Dashboards** (antes Lakeview) son dashboards nativos de Databricks que permiten crear visualizaciones interactivas desde consultas SQL sin programar.
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────┐
# MAGIC │         AI/BI DASHBOARD                   │
# MAGIC ├─────────────────────────────────────────┤
# MAGIC │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
# MAGIC │  │   KPI   │  │  Chart  │  │  Table  │  │
# MAGIC │  │ $1.2M   │  │  Bar    │  │  Data   │  │
# MAGIC │  └─────────┘  └─────────┘  └─────────┘  │
# MAGIC │  ┌────────────────────────────────────┐  │
# MAGIC │  │        Filtros interactivos        │  │
# MAGIC │  └────────────────────────────────────┘  │
# MAGIC └─────────────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Lakeview vs Plotly en Notebooks
# MAGIC
# MAGIC | Aspecto | Plotly (Notebook) | AI/BI Dashboard (Lakeview) |
# MAGIC |---------|------------------|---------------------------|
# MAGIC | **Dónde** | Dentro del notebook | Aplicación dedicada |
# MAGIC | **Filtros** | Programando | Drag-and-drop |
# MAGIC | **Compartir** | Compartir notebook | URL pública/interna |
# MAGIC | **Actualización** | Re-ejecutar notebook | Auto-refresh |
# MAGIC | **Interactividad** | Limitada | Total (filtros, drill-down) |
# MAGIC | **Para quién** | Data Scientists | Ejecutivos, gerentes |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📐 Tipos de Widgets
# MAGIC
# MAGIC | Widget | Uso | Ejemplo |
# MAGIC |--------|-----|--------|
# MAGIC | **KPI** | Métrica única | Ventas totales: $1.2M |
# MAGIC | **Bar Chart** | Comparación | Ventas por sucursal |
# MAGIC | **Line Chart** | Tendencia temporal | Ventas mensuales |
# MAGIC | **Table** | Datos detallados | Detalle por sucursal y mes |
# MAGIC | **Heatmap** | Correlación | Correlación entre variables |
# MAGIC | **Scatter** | Relación | Ventas vs periodo |
# MAGIC | **Pie/Donut** | Proporción | Participación por sucursal |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 SQL para Dashboards
# MAGIC
# MAGIC ```sql
# MAGIC -- Query base para dashboard de ventas
# MAGIC SELECT 
# MAGIC   sucursal_id,
# MAGIC   fecha,
# MAGIC   ventas,
# MAGIC   YEAR(fecha) as anio,
# MAGIC   MONTH(fecha) as mes
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC ORDER BY fecha;
# MAGIC
# MAGIC -- KPI: Total de ventas
# MAGIC SELECT SUM(ventas) as total_ventas,
# MAGIC        AVG(ventas) as promedio_ventas,
# MAGIC        COUNT(*) as total_registros
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Bar chart: Ventas por sucursal
# MAGIC SELECT sucursal_id, SUM(ventas) as ventas_totales
# MAGIC FROM pandito_ds.default.ventas_mensuales_mendoza_h3
# MAGIC GROUP BY sucursal_id
# MAGIC ORDER BY ventas_totales DESC;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Dashboards AI/BI = decisiones data-driven:**
# MAGIC * 📊 Visualización profesional sin programar
# MAGIC * 🔄 Datos siempre actualizados (auto-refresh)
# MAGIC * 📱 Accesible desde cualquier dispositivo
# MAGIC * 👥 Compartible con stakeholders no técnicos
# MAGIC * 🎯 Filtros interactivos para exploración

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd

print("💻 PREPARACIÓN DE DATOS PARA DASHBOARD")
print("="*70)

if USAR_DATOS_REALES:
    df['anio'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month
    
    # KPIs principales
    print("\n📊 KPIs PARA DASHBOARD:")
    print(f"   Total ventas: ${df['ventas'].sum():,.2f}")
    print(f"   Promedio mensual: ${df['ventas'].mean():,.2f}")
    print(f"   Sucursales activas: {df['sucursal_id'].nunique()}")
    print(f"   Período: {df['fecha'].min().strftime('%Y-%m')} a {df['fecha'].max().strftime('%Y-%m')}")
    
    # Datos para bar chart
    print("\n📈 DATOS PARA BAR CHART (Ventas por sucursal):")
    bar_data = df.groupby('sucursal_id')['ventas'].sum().sort_values(ascending=False)
    for sucursal, ventas in bar_data.items():
        print(f"   {sucursal}: ${ventas:,.2f}")
    
    # Datos para line chart
    print("\n📈 DATOS PARA LINE CHART (Tendencia mensual):")
    monthly = df.groupby('fecha')['ventas'].sum().tail(12)
    for fecha, ventas in monthly.items():
        print(f"   {fecha.strftime('%Y-%m')}: ${ventas:,.2f}")
    
    print("\n📌 PASOS PARA CREAR EL DASHBOARD:")
    print("   1. Ejecuta estas SQL queries en Databricks SQL Editor")
    print("   2. Click en '+ Create' > 'AI/BI Dashboard'")
    print("   3. Agrega cada query como dataset")
    print("   4. Crea widgets: KPI, bar chart, line chart, table")
    print("   5. Agrega filtros por año y sucursal")
    print("   6. Publica y comparte con tu equipo")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Datos preparados para AI/BI Dashboard")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 16_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **AI/BI Dashboards (Lakeview) — dashboards nativos de Databricks:**
# MAGIC    - Aplicación dedicada, separada del notebook
# MAGIC    - Creados desde consultas SQL sin programar
# MAGIC    - Auto-refresh: datos siempre actualizados sin re-ejecutar
# MAGIC    - URL compartible con stakeholders no técnicos
# MAGIC
# MAGIC 2. **Tipos de widgets:**
# MAGIC    - KPI: métrica única (ventas totales, ticket promedio)
# MAGIC    - Bar Chart: comparación entre categorías (ventas por sucursal)
# MAGIC    - Line Chart: tendencia temporal (evolución mensual)
# MAGIC    - Table: datos detallados con ordenamiento y paginación
# MAGIC    - Heatmap: correlación entre variables
# MAGIC    - Scatter: relación entre dos variables
# MAGIC    - Pie/Donut: proporción o participación
# MAGIC
# MAGIC 3. **Filtros interactivos:**
# MAGIC    - Drag-and-drop, sin código
# MAGIC    - Filtrar por año, sucursal, zona con un clic
# MAGIC    - Todos los widgets se actualizan en cascada al cambiar un filtro
# MAGIC    - Parámetros dinámicos conectados a las SQL queries
# MAGIC
# MAGIC 4. **Lakeview vs Plotly en Notebooks:**
# MAGIC    - Plotly: dentro del notebook, requiere programar filtros, re-ejecutar para actualizar
# MAGIC    - Lakeview: aplicación dedicada, filtros drag-and-drop, auto-refresh, URL compartible
# MAGIC    - Plotly → Data Scientists; Lakeview → Ejecutivos y gerentes
# MAGIC
# MAGIC 5. **Flujo de creación:**
# MAGIC    - SQL Editor → escribir query → Create Dashboard → AI/BI Dashboard
# MAGIC    - Agregar cada query como dataset
# MAGIC    - Crear widgets (KPI, bar, line, table) sobre los datasets
# MAGIC    - Configurar filtros por año y sucursal
# MAGIC    - Publicar y compartir con el equipo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Una SQL query por dataset, sin complejidad innecesaria**
# MAGIC ```sql
# MAGIC -- MALO: query gigante con JOINs, CTEs y window functions en un solo dataset
# MAGIC SELECT *, RANK() OVER (...), ...
# MAGIC FROM (SELECT ... FROM ... JOIN ...) WHERE ...
# MAGIC
# MAGIC -- BUENO: una query simple y enfocada por widget
# MAGIC -- Dataset 1: KPI
# MAGIC SELECT SUM(ventas) AS total FROM ventas;
# MAGIC -- Dataset 2: Bar chart
# MAGIC SELECT sucursal_id, SUM(ventas) AS total FROM ventas GROUP BY sucursal_id;
# MAGIC -- Dataset 3: Line chart
# MAGIC SELECT fecha, SUM(ventas) AS total FROM ventas GROUP BY fecha;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Agregar filtros desde el diseño, no en el SQL**
# MAGIC ```sql
# MAGIC -- MALO: filtrar por anio en el SQL (filtro fijo, no interactivo)
# MAGIC SELECT sucursal_id, SUM(ventas) FROM ventas
# MAGIC WHERE YEAR(fecha) = 2023 GROUP BY sucursal_id;
# MAGIC
# MAGIC -- BUENO: SQL sin filtro fijo, agregar filtro interactivo en el dashboard
# MAGIC SELECT sucursal_id, YEAR(fecha) AS anio, SUM(ventas) AS total
# MAGIC FROM ventas GROUP BY sucursal_id, YEAR(fecha);
# MAGIC -- Filtro interactivo: anio → usuario selecciona en el dashboard
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: KPIs arriba, gráficos al medio, tablas abajo**
# MAGIC ```python
# MAGIC # Layout profesional de dashboards:
# MAGIC # Fila 1: KPIs (ventas totales, promedio, sucursales activas)
# MAGIC # Fila 2: Gráfico de líneas (tendencia) + Bar chart (comparación)
# MAGIC # Fila 3: Tabla detallada (drill-down para investigación)
# MAGIC # Filtros: barra superior o lateral, siempre visibles
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Herramienta |
# MAGIC |-----------|-------------|
# MAGIC | Dashboard para ejecutivos | AI/BI Dashboard (Lakeview) |
# MAGIC | Visualización dentro de notebook | Plotly |
# MAGIC | Filtros drag-and-drop sin código | AI/BI Dashboard |
# MAGIC | Gráfico personalizado complejo | Plotly (Graph Objects) |
# MAGIC | Compartir URL con stakeholders | AI/BI Dashboard |
# MAGIC | Auto-refresh de datos | AI/BI Dashboard |
# MAGIC | Exploración interactiva en notebook | Plotly + ipywidgets |
# MAGIC | KPI card con métrica única | Widget KPI de Lakeview |
# MAGIC | Comparación entre categorías | Widget Bar Chart |
# MAGIC | Tendencia temporal | Widget Line Chart |
# MAGIC | Datos detallados con paginación | Widget Table |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>📊 ¡Dashboards AI/BI Lakeview dominados!</h3>
# MAGIC   <p><i>"Lakeview democratiza los dashboards: SQL + drag-and-drop = visualización ejecutiva sin programar."</i></p>
# MAGIC </div>