# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🔍 Módulo 07 - Notebook 04: Descomposición estacional y tendencias
# MAGIC
# MAGIC ## 📊 Análisis de componentes de series temporales
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 07 - Series de Tiempo Financieras  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Descomponer** una serie temporal en componentes  
# MAGIC ✅ **Identificar** tendencia, estacionalidad y residuo  
# MAGIC ✅ **Calcular** índices estacionales  
# MAGIC ✅ **Detectar** estacionalidad en ventas  
# MAGIC ✅ **Ajustar** datos por estacionalidad  
# MAGIC ✅ **Interpretar** resultados para decisiones de negocio
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Notebooks 07_01 al 07_03 completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Componentes** - Tendencia, estacionalidad, residuo
# MAGIC 2. **Descomposición aditiva** - statsmodels.seasonal_decompose
# MAGIC 3. **Índices estacionales** - Factor por mes
# MAGIC 4. **Ajuste estacional** - Eliminar estacionalidad
# MAGIC 5. **Detección automática** - Identificar patrones
# MAGIC 6. **Caso integrador** - Análisis completo de ventas

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
import numpy as np

print("💾 CARGANDO DATOS PARA DESCOMPOSICIÓN")
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

# DBTITLE 1,📚 Teoría: Descomposición
# MAGIC %md
# MAGIC ## 📚 Teoría: Descomposición de Series Temporales
# MAGIC
# MAGIC ### 🔍 Componentes de una Serie Temporal
# MAGIC
# MAGIC Toda serie temporal se puede descomponer en:
# MAGIC
# MAGIC ```
# MAGIC Serie = Tendencia + Estacionalidad + Residuo
# MAGIC         
# MAGIC         ↑              ↑              ↑
# MAGIC    Dirección      Patrón que     Lo que queda
# MAGIC    a largo        se repite      (ruido, anomalías)
# MAGIC    plazo          cada N meses
# MAGIC ```
# MAGIC
# MAGIC **Visualización:**
# MAGIC ```
# MAGIC Ventas    =    Tendencia    +    Estacionalidad    +    Residuo
# MAGIC   📈           📈                🔄                    📉
# MAGIC  (real)       (crecimiento)    (patrón anual)        (ruido)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📐 Descomposición Aditiva vs Multiplicativa
# MAGIC
# MAGIC **Aditiva:** `Ventas = Tendencia + Estacionalidad + Ruido`
# MAGIC * Útil cuando la estacionalidad es constante en magnitud
# MAGIC
# MAGIC **Multiplicativa:** `Ventas = Tendencia × Estacionalidad × Ruido`
# MAGIC * Útil cuando la estacionalidad crece con la tendencia
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Índices Estacionales
# MAGIC
# MAGIC Un índice estacional muestra cuánto above/below del promedio está cada mes:
# MAGIC
# MAGIC | Mes | Índice | Interpretación |
# MAGIC |-----|--------|----------------|
# MAGIC | Ene | 0.85 | 15% por debajo del promedio |
# MAGIC | Jul | 1.20 | 20% por encima del promedio |
# MAGIC | Dic | 1.35 | 35% por encima (alta temporada) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Ajuste Estacional
# MAGIC
# MAGIC ```python
# MAGIC # Eliminar el efecto estacional para ver la tendencia real
# MAGIC ventas_ajustadas = ventas / indice_estacional
# MAGIC # = ventas sin el patrón estacional
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Descomposición en negocios:**
# MAGIC * 📊 Separar tendencia real de estacionalidad
# MAGIC * 📈 ¿Las ventas crecen o es solo temporada alta?
# MAGIC * 📦 Planificar inventario por estacionalidad
# MAGIC * 🏪 Staffing: más personal en temporada alta
# MAGIC * 📉 Detectar anomalías (residuos grandes = algo inusual)

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

print("💻 DESCOMPOSICIÓN ESTACIONAL DE VENTAS")
print("="*70)

if USAR_DATOS_REALES:
    # Agregar ventas totales por mes
    monthly = df.groupby('fecha')['ventas'].sum().reset_index().sort_values('fecha')
    monthly = monthly.set_index('fecha')
    
    # Asegurar frecuencia mensual
    monthly = monthly.asfreq('MS')
    monthly['ventas'] = monthly['ventas'].interpolate()
    
    # Descomposición aditiva (período=12 meses)
    print("\n1️⃣ DESCOMPOSICIÓN ADITIVA (período=12):")
    decomposition = seasonal_decompose(monthly['ventas'], model='additive', period=12)
    
    # Tendencia
    trend = decomposition.trend.dropna()
    print(f"   Tendencia: ${trend.iloc[0]:,.2f} → ${trend.iloc[-1]:,.2f}")
    print(f"   Crecimiento: {(trend.iloc[-1]/trend.iloc[0]-1)*100:.2f}% en {len(trend)} meses")
    
    # Estacionalidad (índices por mes)
    seasonal = decomposition.seasonal
    print("\n2️⃣ ÍNDICES ESTACIONALES (por mes):")
    seasonal_monthly = seasonal.groupby(seasonal.index.month).mean()
    for mes, indice in seasonal_monthly.items():
        nombre_mes = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][mes-1]
        print(f"   {nombre_mes}: {indice:+,.2f}")
    
    # Mes con mayor estacionalidad
    mes_max = seasonal_monthly.idxmax()
    mes_min = seasonal_monthly.idxmin()
    print(f"\n   Pico estacional: mes {mes_max} (+{seasonal_monthly.max():,.2f})")
    print(f"   Valle estacional: mes {mes_min} ({seasonal_monthly.min():,.2f})")
    
    # Residuo
    resid = decomposition.resid.dropna()
    print(f"\n3️⃣ RESIDUO (ruido):")
    print(f"   Promedio: {resid.mean():,.2f}")
    print(f"   Desviación: {resid.std():,.2f}")
    print(f"   Mínimo: {resid.min():,.2f}")
    print(f"   Máximo: {resid.max():,.2f}")
    
    # Ventas ajustadas estacionalmente
    print("\n4️⃣ VENTAS AJUSTADAS ESTACIONALMENTE:")
    ventas_ajustadas = monthly['ventas'] - seasonal
    print(f"   Últimos 6 meses (ajustados):")
    for fecha, valor in ventas_ajustadas.tail(6).items():
        print(f"   {fecha.strftime('%Y-%m')}: ${valor:,.2f} (original: ${monthly.loc[fecha, 'ventas']:,.2f})")
    
    print(f"\n✅ Descomposición completada")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 07_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Descomposición de series temporales:**
# MAGIC    ```python
# MAGIC    from statsmodels.tsa.seasonal import seasonal_decompose
# MAGIC    
# MAGIC    decomposition = seasonal_decompose(monthly['ventas'], model='additive', period=12)
# MAGIC    trend = decomposition.trend
# MAGIC    seasonal = decomposition.seasonal
# MAGIC    resid = decomposition.resid
# MAGIC    ```
# MAGIC
# MAGIC 2. **Modelo aditivo vs multiplicativo:**
# MAGIC    ```python
# MAGIC    # Aditivo: Serie = Tendencia + Estacionalidad + Residuo
# MAGIC    # (estacionalidad constante en magnitud)
# MAGIC    seasonal_decompose(df, model='additive', period=12)
# MAGIC    
# MAGIC    # Multiplicativo: Serie = Tendencia × Estacionalidad × Residuo
# MAGIC    # (estacionalidad crece con la tendencia)
# MAGIC    seasonal_decompose(df, model='multiplicative', period=12)
# MAGIC    ```
# MAGIC
# MAGIC 3. **Índices estacionales:**
# MAGIC    ```python
# MAGIC    # Factor por mes: >1 = sobre el promedio, <1 = bajo el promedio
# MAGIC    seasonal_monthly = seasonal.groupby(seasonal.index.month).mean()
# MAGIC    # Dic: +35% (alta temporada), Ene: -15% (baja temporada)
# MAGIC    ```
# MAGIC
# MAGIC 4. **Ajuste estacional:**
# MAGIC    ```python
# MAGIC    # Eliminar el efecto estacional para ver la tendencia real
# MAGIC    ventas_ajustadas = monthly['ventas'] - seasonal  # aditivo
# MAGIC    # o
# MAGIC    ventas_ajustadas = monthly['ventas'] / seasonal  # multiplicativo
# MAGIC    ```
# MAGIC
# MAGIC 5. **Detección de anomalías:**
# MAGIC    - Residuos grandes = algo inusual ocurrió
# MAGIC    - `resid.std()` mide la magnitud típica del ruido
# MAGIC    - Valores fuera de ±2σ son candidatos a investigación
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de descomposición
# MAGIC
# MAGIC **Caso 1: Datos mensuales con estacionalidad anual**
# MAGIC ```python
# MAGIC result = seasonal_decompose(df, model='additive', period=12)
# MAGIC result.plot()
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Datos trimestrales con estacionalidad anual**
# MAGIC ```python
# MAGIC result = seasonal_decompose(df, model='additive', period=4)
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Datos diarios con estacionalidad semanal**
# MAGIC ```python
# MAGIC result = seasonal_decompose(df, model='additive', period=7)
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Ajuste estacional para comparar períodos**
# MAGIC ```python
# MAGIC # Eliminar estacionalidad y comparar tendencia real
# MAGIC ventas_ajustadas = df['ventas'] - result.seasonal
# MAGIC # Ahora enero vs diciembre son comparables
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Extraer componentes individualmente**
# MAGIC ```python
# MAGIC trend = result.trend        # dirección de largo plazo
# MAGIC seasonal = result.seasonal   # patrón repetitivo
# MAGIC resid = result.resid        # ruido y anomalías
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 07
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **07_01 - Resampling y Ventanas Móviles:** Cambio de frecuencia, promedios móviles, suavizado
# MAGIC 2. **07_02 - Deflactación IPC y CAGR:** Ajuste por inflación, crecimiento real vs nominal
# MAGIC 3. **07_03 - Forecasting y Predicción:** Naive, regresión lineal, naive seasonal, MAE/MAPE/RMSE
# MAGIC 4. **07_04 - Descomposición Estacional:** Tendencia, estacionalidad, residuo, ajuste estacional
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Manipular series temporales con DatetimeIndex y resample
# MAGIC * ✅ Deflactar series y calcular CAGR real
# MAGIC * ✅ Generar pronósticos y evaluarlos con métricas
# MAGIC * ✅ Descomponer series y ajustar por estacionalidad
# MAGIC * ✅ Detectar anomalías mediante análisis de residuos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>📈 ¡Módulo 07 Completado!</h3>
# MAGIC   <p><i>"Dominas series de tiempo: desde resampling hasta descomposición estacional. Ahora puedes analizar tendencias reales detrás del ruido."</i></p>
# MAGIC </div>