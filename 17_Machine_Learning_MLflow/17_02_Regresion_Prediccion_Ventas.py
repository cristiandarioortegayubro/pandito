# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 📈 Módulo 17 - Notebook 02: Regresión - Predicción de Ventas
# MAGIC
# MAGIC ## 🎯 Machine Learning para Forecasting
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 17 - Machine Learning con MLflow  
# MAGIC **Duración estimada:** 75 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** el problema de regresión  
# MAGIC ✅ **Preparar** datos para ML (features, target, splits)  
# MAGIC ✅ **Entrenar** LinearRegression, RandomForest, GradientBoosting  
# MAGIC ✅ **Evaluar** con RMSE, MAE, R²  
# MAGIC ✅ **Comparar** modelos con MLflow  
# MAGIC ✅ **Seleccionar** el mejor modelo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebook 17_01 completado (MLflow y Experimentos)
# MAGIC * ✅ Conocimiento de Pandas y estadística básica
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **Preparación de datos** - Features, target, train/test split
# MAGIC 2. **Linear Regression** - Línea base
# MAGIC 3. **Random Forest Regressor** - Modelo de ensemble
# MAGIC 4. **Gradient Boosting** - Modelo avanzado
# MAGIC 5. **Evaluación y comparación** - RMSE, MAE, R²
# MAGIC 6. **Selección de modelo** - Mejor modelo con MLflow

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("💾 CARGANDO DATOS PARA REGRESIÓN")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter
    print(f"✅ Datos cargados: {len(df)} registros")
    print(f"   Columnas: {list(df.columns)}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    np.random.seed(42)
    df = pd.DataFrame({
        'fecha': pd.date_range('2019-01-01', periods=300, freq='ME'),
        'sucursal_id': np.random.choice(['S001','S002','S003','S004','S005'], 300),
        'ventas': np.random.normal(50000, 15000, 300).round(2),
        'lat': np.random.uniform(-32.9, -32.8, 300),
        'lon': np.random.uniform(-68.9, -68.8, 300)
    })
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter
    USAR_DATOS_REALES = False

print(f"\n📊 Dataset para ML:")
print(f"   • Filas: {len(df)}")
print(f"   • Features: mes, anio, trimestre")
print(f"   • Target: ventas")
print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Regresión
# MAGIC %md
# MAGIC ## 📚 Teoría: Regresión y Predicción
# MAGIC
# MAGIC ### 📈 ¿Qué es la Regresión?
# MAGIC
# MAGIC **Regresión** es un tipo de Machine Learning que predice un valor numérico continuo.
# MAGIC
# MAGIC ```
# MAGIC Entradas (Features)        Modelo         Salida (Target)
# MAGIC ┌─────────────┐         ┌──────────┐      ┌─────────┐
# MAGIC │ mes: 12    │         │          │      │ ventas: │
# MAGIC │ anio: 2024 │ ──────► │  Modelo  │ ───► │ 85000  │
# MAGIC │ trimestre:4│         │  ML      │      │         │
# MAGIC └─────────────┘         └──────────┘      └─────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Tipos de Modelos de Regresión
# MAGIC
# MAGIC | Modelo | Pros | Contras | Cuándo usar |
# MAGIC |--------|------|---------|-------------|
# MAGIC | **Linear Regression** | Simple, interpretable | Asume relación lineal | Línea base |
# MAGIC | **Random Forest** | Robusto, no lineal | Menos interpretable | Datos complejos |
# MAGIC | **Gradient Boosting** | Alto rendimiento | Requiere tuning | Competencia |
# MAGIC | **Ridge/Lasso** | Regularización | Requiere tuning | Muchas features |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Métricas de Evaluación
# MAGIC
# MAGIC | Métrica | Qué mide | Fórmula | Interpretación |
# MAGIC |---------|----------|---------|----------------|
# MAGIC | **RMSE** | Error en unidades del target | √(mean((y-ŷ)²)) | Menor = mejor |
# MAGIC | **MAE** | Error absoluto promedio | mean(|y-ŷ|) | Menor = mejor |
# MAGIC | **R²** | Varianza explicada | 1 - SS_res/SS_tot | 0-1, mayor = mejor |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Flujo de Trabajo
# MAGIC
# MAGIC ```python
# MAGIC # 1. Preparar features y target
# MAGIC X = df[['mes', 'anio', 'trimestre']]
# MAGIC y = df['ventas']
# MAGIC
# MAGIC # 2. Split train/test
# MAGIC X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# MAGIC
# MAGIC # 3. Entrenar con MLflow tracking
# MAGIC with mlflow.start_run(run_name="random_forest_v1"):
# MAGIC     model = RandomForestRegressor(n_estimators=100, random_state=42)
# MAGIC     model.fit(X_train, y_train)
# MAGIC     predictions = model.predict(X_test)
# MAGIC     
# MAGIC     mlflow.log_metric("rmse", np.sqrt(mean_squared_error(y_test, predictions)))
# MAGIC     mlflow.sklearn.log_model(model, "model")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Regresión en negocios:**
# MAGIC * 📈 Predecir ventas futuras
# MAGIC * 💰 Estimar ingresos trimestrales
# MAGIC * 📦 Forecasting de inventario
# MAGIC * 👥 Proyección de headcount
# MAGIC * 🏠 Predicción de precios

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("💻 EXPERIMENTO: COMPARACIÓN DE MODELOS DE REGRESIÓN")
print("="*70)

# Preparar datos (usar variables de la celda anterior)
feature_cols = ['mes', 'anio', 'trimestre']
X = df[feature_cols].values
y = df['ventas'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("regresion_ventas_los_andes")

models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    with mlflow.start_run(run_name=f"{name}_v1"):
        # Parámetros
        mlflow.log_param("model", name)
        mlflow.log_param("features", ", ".join(feature_cols))
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        
        # Entrenar
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Métricas
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.set_tag("dataset", "ventas_mensuales_mendoza_h3")
        mlflow.sklearn.log_model(model, "model")
        
        results.append({"Modelo": name, "RMSE": rmse, "MAE": mae, "R2": r2})
        print(f"\n  {name}:")
        print(f"    RMSE: {rmse:,.2f}")
        print(f"    MAE:  {mae:,.2f}")
        print(f"    R²:   {r2:.4f}")

print(f"\n📊 COMPARACIÓN DE MODELOS:")
results_df = pd.DataFrame(results).sort_values('RMSE')
print(results_df.to_string(index=False))
print(f"\n🏆 Mejor modelo: {results_df.iloc[0]['Modelo']}")
print("\n" + "="*70)
print("✅ Experimentos de regresión completados")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 17_02
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Preparación de datos para ML:**
# MAGIC    - Features (X): mes, anio, trimestre — variables predictoras
# MAGIC    - Target (y): ventas — variable a predecir
# MAGIC    - `train_test_split(X, y, test_size=0.2)` — división entrenamiento/test
# MAGIC    - `random_state=42` para reproducibilidad
# MAGIC
# MAGIC 2. **Linear Regression — línea base:**
# MAGIC    - `LinearRegression().fit(X_train, y_train)` — modelo más simple
# MAGIC    - Asume relación lineal entre features y target
# MAGIC    - Interpretable: coeficientes indican impacto de cada feature
# MAGIC    - Punto de partida: todo modelo debe superarlo
# MAGIC
# MAGIC 3. **Random Forest y Gradient Boosting — ensembles:**
# MAGIC    - `RandomForestRegressor(n_estimators=100)` — bagging, robusto
# MAGIC    - `GradientBoostingRegressor(n_estimators=100)` — boosting, alto rendimiento
# MAGIC    - Capturan relaciones no lineales sin transformación manual
# MAGIC    - Más complejos pero generalmente más precisos
# MAGIC
# MAGIC 4. **Métricas de evaluación:**
# MAGIC    - `RMSE` — error en unidades del target ($), penaliza errores grandes
# MAGIC    - `MAE` — error absoluto promedio, más interpretable
# MAGIC    - `R²` — varianza explicada (0-1), mayor = mejor
# MAGIC    - Comparar las tres métricas juntas para una evaluación completa
# MAGIC
# MAGIC 5. **Comparación con MLflow:**
# MAGIC    - Cada modelo en un `mlflow.start_run()` con su nombre
# MAGIC    - `log_param` para configuración, `log_metric` para resultados
# MAGIC    - `mlflow.sklearn.log_model()` guarda el modelo entrenado
# MAGIC    - Pestaña Experiments: comparar side-by-side y seleccionar el mejor
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Siempre empezar con Linear Regression como baseline**
# MAGIC ```python
# MAGIC # MALO: saltar a GradientBoosting sin baseline
# MAGIC model = GradientBoostingRegressor()
# MAGIC model.fit(X_train, y_train)
# MAGIC rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
# MAGIC # ¿Es bueno? No hay referencia para comparar
# MAGIC
# MAGIC # BUENO: baseline primero, luego complejos
# MAGIC models = {
# MAGIC     'LinearRegression': LinearRegression(),
# MAGIC     'RandomForest': RandomForestRegressor(n_estimators=100),
# MAGIC     'GradientBoosting': GradientBoostingRegressor(n_estimators=100)
# MAGIC }
# MAGIC for name, model in models.items():
# MAGIC     model.fit(X_train, y_train)
# MAGIC     rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
# MAGIC     print(f"{name}: RMSE = {rmse:,.2f}")
# MAGIC # Solo si GradientBoosting supera LinearRegression → vale la pena
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: RMSE en unidades del target para interpretabilidad**
# MAGIC ```python
# MAGIC # MALO: reportar R² solo (¿qué significa 0.65 en términos de $?)
# MAGIC print(f"R² = {r2:.4f}")  # No comunica el error en pesos
# MAGIC
# MAGIC # BUENO: RMSE en unidades del target ($)
# MAGIC rmse = np.sqrt(mean_squared_error(y_test, predictions))
# MAGIC print(f"RMSE = ${rmse:,.2f}")  # Error promedio de $15,000
# MAGIC # Combinar con R² para contexto: R²=0.65, RMSE=$15,000
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Registrar todo en MLflow para reproducibilidad**
# MAGIC ```python
# MAGIC # MALO: entrenar sin tracking, no se puede reproducir
# MAGIC model = RandomForestRegressor(n_estimators=100)
# MAGIC model.fit(X_train, y_train)
# MAGIC # ¿Qué features? ¿Qué test_size? → se pierde
# MAGIC
# MAGIC # BUENO: MLflow tracking completo
# MAGIC with mlflow.start_run(run_name="random_forest_v1"):
# MAGIC     mlflow.log_param("model", "RandomForest")
# MAGIC     mlflow.log_param("n_estimators", 100)
# MAGIC     mlflow.log_param("features", "mes, anio, trimestre")
# MAGIC     mlflow.log_param("test_size", 0.2)
# MAGIC     mlflow.log_metric("rmse", rmse)
# MAGIC     mlflow.log_metric("mae", mae)
# MAGIC     mlflow.log_metric("r2", r2)
# MAGIC     mlflow.sklearn.log_model(model, "model")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Modelo |
# MAGIC |-----------|--------|
# MAGIC | Línea base / primer modelo | `LinearRegression()` |
# MAGIC | Datos con relaciones no lineales | `RandomForestRegressor(n_estimators=100)` |
# MAGIC | Máximo rendimiento (con tuning) | `GradientBoostingRegressor(n_estimators=100)` |
# MAGIC | Muchas features correlacionadas | `Ridge()` o `Lasso()` (regularización) |
# MAGIC | Interpretabilidad prioritaria | `LinearRegression()` (coeficientes claros) |
# MAGIC | Evaluar error en $ | `RMSE` (unidades del target) |
# MAGIC | Evaluar error promedio simple | `MAE` (absoluto, sin penalizar grandes) |
# MAGIC | Evaluar varianza explicada | `R²` (0-1, mayor = mejor) |
# MAGIC | Comparar múltiples modelos | `mlflow.start_run()` por cada modelo |
# MAGIC | Seleccionar el mejor | Pestaña Experiments → ordenar por RMSE asc |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>📈 ¡Regresión y predicción de ventas dominadas!</h3>
# MAGIC   <p><i>"El mejor modelo no es el más complejo: es el que supera el baseline con el menor RMSE y mayor reproducibilidad."</i></p>
# MAGIC </div>