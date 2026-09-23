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

# DBTITLE 1,🔍 Teoría: Descomposición avanzada con datos reales
# MAGIC %md
# MAGIC ## 🔍 Descomposición avanzada con datos reales de Los Andes Market
# MAGIC
# MAGIC ### 📊 Profundizando el análisis estacional
# MAGIC
# MAGIC El Setup Inicial ya cubrió descomposición aditiva básica. Ahora profundizamos con:
# MAGIC
# MAGIC 1. **Modelo multiplicativo:** La estacionalidad crece con la tendencia
# MAGIC ```python
# MAGIC result = seasonal_decompose(monthly['ventas'], model='multiplicative', period=12)
# MAGIC # Útil cuando los picos estacionales son mayores en años con más ventas
# MAGIC ```
# MAGIC
# MAGIC 2. **Descomposición por sucursal:** Cada sucursal tiene su propio patrón
# MAGIC ```python
# MAGIC for sucursal in df['sucursal_nombre'].unique():
# MAGIC     datos = df[df['sucursal_nombre'] == sucursal]
# MAGIC     result = seasonal_decompose(datos['ventas'], period=12)
# MAGIC ```
# MAGIC
# MAGIC 3. **Comparación aditivo vs multiplicativo:**
# MAGIC * Aditivo: estacionalidad constante ($10K arriba/bajo del promedio)
# MAGIC * Multiplicativo: estacionalidad proporcional (10% arriba/bajo del promedio)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué meses son consistentemente altos/bajos en todas las sucursales?
# MAGIC * ¿La estacionalidad es constante (aditivo) o proporcional (multiplicativo)?
# MAGIC * ¿Qué sucursal tiene la mayor estacionalidad (más volátil)?
# MAGIC * ¿Hay sucursales sin estacionalidad (ventas planas todo el año)?

# COMMAND ----------

# DBTITLE 1,🔍 Práctica: Descomposición avanzada con datos reales
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

print("🔍 DESCOMPOSICIÓN AVANZADA CON DATOS REALES DE LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES:
    # Serie agregada
    monthly = df.groupby('fecha')['ventas'].sum().sort_index()
    monthly = monthly.asfreq('MS').interpolate()

    print("\n1️⃣  COMPARACIÓN: ADITIVO VS MULTIPLICATIVO")
    print("-"*70)

    # Aditivo
    decomp_adit = seasonal_decompose(monthly, model='additive', period=12)
    # Multiplicativo
    decomp_mult = seasonal_decompose(monthly, model='multiplicative', period=12)

    print("\n   Tendencia (aditivo):")
    trend_adit = decomp_adit.trend.dropna()
    print(f"      Inicio: ${trend_adit.iloc[0]:,.0f} → Fin: ${trend_adit.iloc[-1]:,.0f}")
    print(f"      Crecimiento: {(trend_adit.iloc[-1]/trend_adit.iloc[0]-1)*100:.1f}%")

    print("\n   Tendencia (multiplicativo):")
    trend_mult = decomp_mult.trend.dropna()
    print(f"      Inicio: ${trend_mult.iloc[0]:,.0f} → Fin: ${trend_mult.iloc[-1]:,.0f}")
    print(f"      Crecimiento: {(trend_mult.iloc[-1]/trend_mult.iloc[0]-1)*100:.1f}%")

    print("\n   Índices estacionales (comparación):")
    nombres_mes = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    seasonal_adit = decomp_adit.seasonal.groupby(decomp_adit.seasonal.index.month).mean()
    seasonal_mult = decomp_mult.seasonal.groupby(decomp_mult.seasonal.index.month).mean()

    for mes in range(1, 13):
        print(f"      {nombres_mes[mes-1]}: aditivo {seasonal_adit[mes]:+,.0f} | multiplicativo {seasonal_mult[mes]:.3f}")

    print("\n   💡 Aditivo: desviación en $ | Multiplicativo: factor (1.0 = promedio)")

    print("\n" + "="*70)
    print("\n2️⃣  DESCOMPOSICIÓN POR SUCURSAL (top 5)")
    print("-"*70)

    sucursales = df['sucursal_nombre'].unique()[:5]
    resultados_sucursal = []

    for suc in sucursales:
        datos = df[df['sucursal_nombre'] == suc].groupby('fecha')['ventas'].sum().sort_index()
        datos = datos.asfreq('MS').interpolate()
        if len(datos) >= 24:
            result = seasonal_decompose(datos, model='additive', period=12)
            seasonal_vals = result.seasonal.groupby(result.seasonal.index.month).mean()
            amplitud = seasonal_vals.max() - seasonal_vals.min()
            resultados_sucursal.append({
                'sucursal': suc,
                'amplitud_estacional': amplitud,
                'mes_pico': nombres_mes[int(seasonal_vals.idxmax())-1],
                'mes_valle': nombres_mes[int(seasonal_vals.idxmin())-1],
                'tendencia': (result.trend.dropna().iloc[-1] / result.trend.dropna().iloc[0] - 1) * 100
            })

    if resultados_sucursal:
        df_sucursal_decomp = pd.DataFrame(resultados_sucursal).sort_values('amplitud_estacional', ascending=False)
        print("\n   Estacionalidad por sucursal:")
        print(df_sucursal_decomp.round(2))
        print("\n   💡 Amplitud alta = estacionalidad marcada (ventas varían mucho por mes)")

    print("\n" + "="*70)
    print("\n3️⃣  AJUSTE ESTACIONAL: Ventas sin estacionalidad")
    print("-"*70)

    ventas_ajustadas = monthly - decomp_adit.seasonal
    print("\n   Ventas originales vs ajustadas (últimos 12 meses):")
    comparacion = pd.DataFrame({
        'ventas_originales': monthly.tail(12).round(0),
        'ventas_ajustadas': ventas_ajustadas.tail(12).round(0)
    })
    comparacion['diferencia'] = (comparacion['ventas_originales'] - comparacion['ventas_ajustadas']).round(0)
    print(comparacion)
    print("\n   💡 Ventas ajustadas eliminan el patrón estacional → tendencia limpia")

    print("\n" + "="*70)
    print("\n4️⃣  DETECCIÓN DE ANOMALÍAS (residuos)")
    print("-"*70)

    resid = decomp_adit.resid.dropna()
    umbral = 2 * resid.std()
    anomalias = resid[np.abs(resid) > umbral]

    print(f"\n   Residuo: media={resid.mean():,.0f}, std={resid.std():,.0f}")
    print(f"   Umbral anomalía: ±${umbral:,.0f}")
    print(f"   Anomalías detectadas: {len(anomalias)} de {len(resid)}")
    if len(anomalias) > 0:
        print("\n   Meses anómalos:")
        for fecha, valor in anomalias.items():
            print(f"      {fecha.strftime('%Y-%m')}: residuo {valor:+,.0f}")
    print("\n   💡 Residuos > 2σ indican eventos inusuales (promociones, crisis, etc.)")
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