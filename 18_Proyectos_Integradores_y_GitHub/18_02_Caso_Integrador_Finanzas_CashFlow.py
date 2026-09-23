# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 💰 Módulo 18 - Notebook 02: Caso Integrador - Finanzas y Cash Flow
# MAGIC
# MAGIC ## 📊 Análisis Financiero End-to-End
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 18 - Proyectos Integradores y GitHub  
# MAGIC **Duración estimada:** 90 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos
# MAGIC
# MAGIC ✅ **Construir** un modelo de cash flow  
# MAGIC ✅ **Calcular** EBITDA, márgenes y ratios financieros  
# MAGIC ✅ **Proyectar** escenarios con forecasting  
# MAGIC ✅ **Visualizar** con Plotly y AI/BI Dashboards  
# MAGIC ✅ **Integrar** SQL, Pandas, PySpark y MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Módulos 01-17 completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. Modelo de Cash Flow
# MAGIC 2. Cálculo de EBITDA y márgenes
# MAGIC 3. Análisis de liquidez
# MAGIC 4. Forecasting de ventas
# MAGIC 5. Dashboard ejecutivo

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
import numpy as np

print("💾 CARGANDO DATOS PARA CASH FLOW")
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

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Cash Flow
# MAGIC %md
# MAGIC ## 📚 Teoría: Cash Flow y Análisis Financiero
# MAGIC
# MAGIC ### 💰 ¿Qué es el Cash Flow?
# MAGIC
# MAGIC **Cash Flow (Flujo de Caja)** muestra las entradas y salidas de dinero en un período.
# MAGIC
# MAGIC ```
# MAGIC Ingresos por Ventas
# MAGIC - Costos Operativos
# MAGIC = EBITDA
# MAGIC - Impuestos
# MAGIC - Inversiones
# MAGIC = Cash Flow Neto
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Ratios Financieros Clave
# MAGIC
# MAGIC | Ratio | Fórmula | Interpretación |
# MAGIC |-------|---------|----------------|
# MAGIC | **Margen Bruto** | (Ventas - COGS) / Ventas | Rentabilidad |
# MAGIC | **EBITDA** | Ventas - COGS - Gastos Op | Rentabilidad operativa |
# MAGIC | **Margen Neto** | Utilidad / Ventas | Rentabilidad final |
# MAGIC | **Liquidez** | Activo Corriente / Pasivo Corriente | Capacidad de pago |
# MAGIC | **ROE** | Utilidad / Patrimonio | Retorno sobre equity |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC * 💰 **Supervivencia:** Sin cash, no hay negocio
# MAGIC * 📊 **Decisiones:** Invertir o no invertir
# MAGIC * 📈 **Crecimiento:** Capacidad de expansión
# MAGIC * 🏦 **Financiación:** Capacidad de préstamos

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("💻 PROYECTO: ANÁLISIS FINANCIERO Y CASH FLOW")
print("="*70)

if USAR_DATOS_REALES:
    # Simular estructura financiera
    df['anio'] = df['fecha'].dt.year
    
    # Asumir costos: COGS = 60% de ventas, Gastos Op = 15%
    df['cogs'] = df['ventas'] * 0.60
    df['gastos_op'] = df['ventas'] * 0.15
    df['ebitda'] = df['ventas'] - df['cogs'] - df['gastos_op']
    df['impuestos'] = df['ebitda'] * 0.21  # IVA/Impuestos
    df['cash_flow_neto'] = df['ebitda'] - df['impuestos']
    df['margen_ebitda'] = (df['ebitda'] / df['ventas'] * 100).round(2)
    
    # Resumen anual
    print("\n📊 ESTADOS FINANCIEROS ANUALES:")
    resumen = df.groupby('anio').agg({
        'ventas': 'sum',
        'cogs': 'sum',
        'ebitda': 'sum',
        'cash_flow_neto': 'sum',
    }).round(2)
    resumen['margen_ebitda_pct'] = (resumen['ebitda'] / resumen['ventas'] * 100).round(2)
    print(resumen)
    
    # Análisis por sucursal
    print("\n🏪 EBITDA POR SUCURSAL:")
    sucursal_fin = df.groupby('sucursal_id').agg({
        'ventas': 'sum',
        'ebitda': 'sum',
        'cash_flow_neto': 'sum',
    }).round(2)
    sucursal_fin['margen_pct'] = (sucursal_fin['ebitda'] / sucursal_fin['ventas'] * 100).round(2)
    print(sucursal_fin.sort_values('ebitda', ascending=False))
    
    # Tendencia de cash flow
    print("\n📈 TENDENCIA DE CASH FLOW (últimos 12 meses):")
    monthly_cf = df.groupby('fecha')['cash_flow_neto'].sum().tail(12)
    for fecha, cf in monthly_cf.items():
        print(f"   {fecha.strftime('%Y-%m')}: ${cf:,.2f}")
    
    print(f"\n✅ Cash Flow total: ${df['cash_flow_neto'].sum():,.2f}")
    print(f"   Margen EBITDA promedio: {df['margen_ebitda'].mean():.2f}%")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 18_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Modelo de Cash Flow end-to-end:**
# MAGIC    - Ventas → COGS → EBITDA → Impuestos → Cash Flow Neto
# MAGIC    - `df['ebitda'] = df['ventas'] - df['cogs'] - df['gastos_op']`
# MAGIC    - Estructura financiera reproducible con datos reales de Unity Catalog
# MAGIC
# MAGIC 2. **Ratios financieros clave:**
# MAGIC    - Margen Bruto: `(ventas - COGS) / ventas` — rentabilidad sobre ventas
# MAGIC    - Margen EBITDA: `EBITDA / ventas` — rentabilidad operativa
# MAGIC    - Margen Neto: `utilidad / ventas` — rentabilidad final
# MAGIC    - Liquidez: `activo corriente / pasivo corriente` — capacidad de pago
# MAGIC
# MAGIC 3. **Análisis por sucursal y anual:**
# MAGIC    - `df.groupby('anio').agg({...})` — estados financieros anuales
# MAGIC    - `df.groupby('sucursal_id').agg({...})` — comparación entre sucursales
# MAGIC    - Identificar sucursales más rentables por EBITDA y margen
# MAGIC
# MAGIC 4. **Forecasting de cash flow:**
# MAGIC    - Proyectar ventas futuras con regresión lineal o naive seasonal
# MAGIC    - Calcular EBITDA proyectado aplicando la estructura de costos
# MAGIC    - Escenarios: optimista, base, pesimista con diferentes supuestos
# MAGIC
# MAGIC 5. **Dashboard ejecutivo integrado:**
# MAGIC    - KPIs: ventas totales, EBITDA, margen, cash flow neto
# MAGIC    - Gráfico de líneas: evolución mensual del cash flow
# MAGIC    - Bar chart: EBITDA por sucursal con filtro por año
# MAGIC    - Tabla: estado de resultados detallado por período
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Construir el P&L desde ventas hasta cash flow neto**
# MAGIC ```python
# MAGIC # MALO: calcular EBITDA sin estructura clara
# MAGIC df['ebitda'] = df['ventas'] * 0.25  # porcentaje arbitrario sin fundamento
# MAGIC
# MAGIC # BUENO: construir paso a paso con supuestos documentados
# MAGIC df['cogs'] = df['ventas'] * 0.60        # 60% costo de ventas
# MAGIC df['gastos_op'] = df['ventas'] * 0.15   # 15% gastos operativos
# MAGIC df['ebitda'] = df['ventas'] - df['cogs'] - df['gastos_op']
# MAGIC df['impuestos'] = df['ebitda'] * 0.21   # 21% tasa impositiva
# MAGIC df['cash_flow_neto'] = df['ebitda'] - df['impuestos']
# MAGIC # Cada supuesto está documentado y es modificable
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Siempre calcular márgenes, no solo absolutos**
# MAGIC ```python
# MAGIC # MALO: comparar solo valores absolutos entre sucursales
# MAGIC print(df.groupby('sucursal_id')['ebitda'].sum())
# MAGIC # Sucursal A: $500,000 vs Sucursal B: $300,000 → A es mejor? No necesariamente
# MAGIC
# MAGIC # BUENO: agregar márgenes para comparación justa
# MAGIC resumen = df.groupby('sucursal_id').agg(
# MAGIC     ventas=('ventas', 'sum'),
# MAGIC     ebitda=('ebitda', 'sum')
# MAGIC )
# MAGIC resumen['margen_pct'] = (resumen['ebitda'] / resumen['ventas'] * 100).round(2)
# MAGIC # A: $500K con 20% margen vs B: $300K con 35% margen → B es más eficiente
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Proyectar con escenarios múltiples**
# MAGIC ```python
# MAGIC # MALO: un solo pronóstico sin rango de incertidumbre
# MAGIC forecast = model.predict(X_future)
# MAGIC print(f"Ventas próximas: ${forecast:,.2f}")  # Un solo número, sin contexto
# MAGIC
# MAGIC # BUENO: escenarios optimista, base y pesimista
# MAGIC base = model.predict(X_future)
# MAGIC optimista = base * 1.15   # +15%
# MAGIC pesimista = base * 0.85   # -15%
# MAGIC print(f"Escenarios: Pesimista ${pesimista:,.0f} | Base ${base:,.0f} | Optimista ${optimista:,.0f}")
# MAGIC # Stakeholders ven el rango de posibilidades
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Calcular EBITDA | `ventas - COGS - gastos_op` |
# MAGIC | Calcular cash flow neto | `EBITDA - impuestos` |
# MAGIC | Margen EBITDA | `(EBITDA / ventas) * 100` |
# MAGIC | Resumen anual | `df.groupby('anio').agg({...})` |
# MAGIC | Comparar sucursales | `df.groupby('sucursal_id').agg(...)` con margen_pct |
# MAGIC | Proyectar ventas | `LinearRegression().fit(X, y)` o naive seasonal |
# MAGIC | Escenarios de forecast | Base × 1.15 (optimista), × 0.85 (pesimista) |
# MAGIC | Detectar sucursales en riesgo | EBITDA negativo o margen < 10% |
# MAGIC | Dashboard de cash flow | Plotly line chart (evolución) + bar chart (sucursales) |
# MAGIC | Exportar estado de resultados | `resumen.to_csv('pnl.csv')` o Delta table |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>💰 ¡Análisis financiero y Cash Flow dominados!</h3>
# MAGIC   <p><i>"El cash flow es el oxígeno del negocio: medirlo, proyectarlo y visualizarlo es la diferencia entre sobrevivir y crecer."</i></p>
# MAGIC </div>