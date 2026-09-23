# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 📈 Módulo 07 - Notebook 03: Forecasting y predicción de ventas
# MAGIC
# MAGIC ## 🎯 Modelos de predicción para series temporales
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 07 - Series de Tiempo Financieras  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué es el forecasting  
# MAGIC ✅ **Aplicar** promedios móviles para predicción  
# MAGIC ✅ **Usar** regresión lineal para tendencia  
# MAGIC ✅ **Implementar** naive seasonal forecast  
# MAGIC ✅ **Evaluar** precisión de pronósticos (MAE, MAPE)  
# MAGIC ✅ **Visualizar** predicciones vs realidad
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Notebooks 07_01 y 07_02 completados (Resampling, IPC/CAGR)
# MAGIC * ✅ Conocimiento de Pandas y estadística básica
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Forecasting** - Conceptos y tipos
# MAGIC 2. **Promedio móvil** - Predicción simple
# MAGIC 3. **Regresión lineal** - Tendencia temporal
# MAGIC 4. **Naive seasonal** - Estacionalidad simple
# MAGIC 5. **Evaluación** - MAE, MAPE, RMSE
# MAGIC 6. **Caso integrador** - Predicción de ventas 2025

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
import numpy as np

print("💾 CARGANDO DATOS PARA FORECASTING")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Datos cargados: {len(df)} registros")
    print(f"   Período: {df['fecha'].min().strftime('%Y-%m')} a {df['fecha'].max().strftime('%Y-%m')}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Forecasting
# MAGIC %md
# MAGIC ## 📚 Teoría: Forecasting de Series Temporales
# MAGIC
# MAGIC ### 📈 ¿Qué es el Forecasting?
# MAGIC
# MAGIC **Forecasting (Pronóstico)** es predecir valores futuros basándose en patrones históricos.
# MAGIC
# MAGIC ```
# MAGIC Pasado: 2020-2024 → Modelo → Futuro: 2025
# MAGIC [Ene, Feb, Mar, ...]   →   [Predicción Ene, Feb, Mar, ...]
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Métodos de Forecasting
# MAGIC
# MAGIC | Método | Complejidad | Cuándo usar |
# MAGIC |--------|-------------|------------|
# MAGIC | **Naive** | Baja | Línea base (último valor) |
# MAGIC | **Promedio móvil** | Baja | Datos sin tendencia clara |
# MAGIC | **Regresión lineal** | Media | Tendencia lineal |
# MAGIC | **Naive seasonal** | Media | Estacionalidad fuerte |
# MAGIC | **ARIMA/SARIMA** | Alta | Series complejas |
# MAGIC | **Prophet** | Alta | Series con holidays |
# MAGIC | **LSTM** | Muy alta | Patrones no lineales |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📏 Métricas de Evaluación
# MAGIC
# MAGIC | Métrica | Qué mide | Fórmula |
# MAGIC |---------|----------|---------|
# MAGIC | **MAE** | Error absoluto promedio | mean(|y - yhat|) |
# MAGIC | **MAPE** | Error porcentual promedio | mean(|y-yhat|/y) * 100 |
# MAGIC | **RMSE** | Penaliza grandes errores | sqrt(mean((y-yhat)^2)) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Forecasting en negocios:**
# MAGIC * 📈 Predecir ingresos del próximo trimestre
# MAGIC * 📦 Estimar demanda de inventario
# MAGIC * 👥 Proyectar headcount necesario
# MAGIC * 💰 Presupuesto de ventas anual
# MAGIC * 🏪 Estacionalidad de sucursales

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

print("💻 FORECASTING DE VENTAS")
print("="*70)

if USAR_DATOS_REALES:
    # Agregar ventas totales por mes
    monthly = df.groupby('fecha')['ventas'].sum().reset_index()
    monthly = monthly.sort_values('fecha')
    
    # 1. NAIVE: último valor
    print("\n1️⃣ NAIVE FORECAST (último valor):")
    naive_forecast = monthly['ventas'].iloc[-1]
    print(f"   Predicción próximo mes: ${naive_forecast:,.2f}")
    
    # 2. PROMEDIO MÓVIL (3 meses)
    print("\n2️⃣ PROMEDIO MÓVIL (3 meses):")
    ma3 = monthly['ventas'].rolling(3).mean().iloc[-1]
    print(f"   Predicción: ${ma3:,.2f}")
    
    # 3. REGRESIÓN LINEAL
    print("\n3️⃣ REGRESIÓN LINEAL (tendencia):")
    monthly['mes_num'] = range(len(monthly))
    X = monthly[['mes_num']].values
    y = monthly['ventas'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predecir próximos 6 meses
    future_months = np.array(range(len(monthly), len(monthly) + 6)).reshape(-1, 1)
    predictions = model.predict(future_months)
    
    last_date = monthly['fecha'].iloc[-1]
    future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=6, freq='MS')
    
    print(f"   Predicciones 2025:")
    for date, pred in zip(future_dates, predictions):
        print(f"   {date.strftime('%Y-%m')}: ${pred:,.2f}")
    
    # 4. EVALUACIÓN (usar últimos 12 meses como test)
    train = monthly.iloc[:-12]
    test = monthly.iloc[-12:]
    
    model_eval = LinearRegression()
    model_eval.fit(train[['mes_num']].values, train['ventas'].values)
    test_predictions = model_eval.predict(test[['mes_num']].values)
    
    mae = mean_absolute_error(test['ventas'], test_predictions)
    rmse = np.sqrt(mean_squared_error(test['ventas'], test_predictions))
    mape = np.mean(np.abs((test['ventas'] - test_predictions) / test['ventas']) * 100)
    
    print(f"\n4️⃣ EVALUACIÓN (últimos 12 meses como test):")
    print(f"   MAE: ${mae:,.2f}")
    print(f"   RMSE: ${rmse:,.2f}")
    print(f"   MAPE: {mape:.2f}%")
    
    print(f"\n✅ Forecasting completado")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 07_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Naive Forecast:**
# MAGIC    - Predicción = último valor observado
# MAGIC    - Línea base mínima: cualquier modelo debe superar este umbral
# MAGIC    - Útil como benchmark de comparación
# MAGIC
# MAGIC 2. **Promedio móvil:**
# MAGIC    - `df['col'].rolling(window=3).mean().iloc[-1]`
# MAGIC    - Suaviza fluctuaciones para predecir el siguiente período
# MAGIC    - Ventanas mayores = más estables pero con más rezago
# MAGIC
# MAGIC 3. **Regresión lineal para tendencia:**
# MAGIC    - `LinearRegression().fit(X_meses, y_ventas)`
# MAGIC    - Captura la tendencia temporal subyacente
# MAGIC    - Extrapolación simple para horizontes cortos (6-12 meses)
# MAGIC
# MAGIC 4. **Naive seasonal:**
# MAGIC    - Predicción = valor del mismo mes del año anterior
# MAGIC    - Aprovecha estacionalidad sin modelarla explícitamente
# MAGIC    - Funciona bien cuando los patrones estacionales son estables
# MAGIC
# MAGIC 5. **Evaluación de pronósticos:**
# MAGIC    - **MAE:** error absoluto promedio (interpretable en $)
# MAGIC    - **MAPE:** error porcentual (comparable entre series)
# MAGIC    - **RMSE:** penaliza grandes errores (sensible a outliers)
# MAGIC    - Train/test split temporal: últimos 12 meses como test
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Siempre comparar contra naive**
# MAGIC ```python
# MAGIC # MALO: aceptar un modelo sin benchmark
# MAGIC modelo_rmse = 50000  # ¿Es bueno o malo?
# MAGIC
# MAGIC # BUENO: comparar contra naive
# MAGIC naive_rmse = 45000
# MAGIC modelo_rmse = 50000
# MAGIC print(f"El modelo es PEOR que naive ({modelo_rmse} > {naive_rmse})")
# MAGIC # Si no superas naive, usa naive
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Split temporal, NUNCA aleatorio**
# MAGIC ```python
# MAGIC # MALO: train_test_split aleatorio (data leakage temporal)
# MAGIC from sklearn.model_selection import train_test_split
# MAGIC X_train, X_test = train_test_split(X, y, test_size=0.2)
# MAGIC
# MAGIC # BUENO: split cronológico (respeta el tiempo)
# MAGIC train = monthly.iloc[:-12]
# MAGIC test = monthly.iloc[-12:]
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: MAPE puede ser engañoso con valores cercanos a cero**
# MAGIC ```python
# MAGIC # MALO: confiar en MAPE cuando hay valores pequeños
# MAGIC mape = np.mean(np.abs((y - yhat) / y) * 100)  # y=0 → división por cero
# MAGIC
# MAGIC # BUENO: complementar MAPE con MAE y RMSE
# MAGIC mae = mean_absolute_error(y, yhat)   # magnitud del error en $
# MAGIC rmse = np.sqrt(mean_squared_error(y, yhat))  # penaliza errores grandes
# MAGIC # Usar las 3 métricas juntas para una evaluación completa
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Línea base mínima | Naive (último valor) |
# MAGIC | Datos sin tendencia clara | Promedio móvil (window=3) |
# MAGIC | Tendencia lineal estable | Regresión lineal |
# MAGIC | Estacionalidad fuerte y estable | Naive seasonal (mismo mes año anterior) |
# MAGIC | Series complejas con tendencia + estacionalidad | SARIMA / Prophet |
# MAGIC | Patrones no lineales | LSTM / Redes neuronales |
# MAGIC | Evaluar precisión en $ | MAE |
# MAGIC | Evaluar precisión en % | MAPE |
# MAGIC | Penalizar errores grandes | RMSE |
# MAGIC | Horizonte corto (1-6 meses) | Regresión lineal o promedio móvil |
# MAGIC | Horizonte largo (>12 meses) | Prophet con intervalos de confianza |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>📈 ¡Forecasting de ventas dominado!</h3>
# MAGIC   <p><i>"Un buen pronóstico no adivina el futuro: aprende del pasado para reducir la incertidumbre."</i></p>
# MAGIC </div>