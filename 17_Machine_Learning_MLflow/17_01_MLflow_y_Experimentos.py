# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🧪 Módulo 17 - Notebook 01: MLflow y experimentos
# MAGIC
# MAGIC ## 📊 Tracking de modelos de Machine Learning
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 17 - Machine Learning con MLflow  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué es MLflow y su arquitectura  
# MAGIC ✅ **Crear** experimentos y registrar runs  
# MAGIC ✅ **Trackear** parámetros, métricas y artifacts  
# MAGIC ✅ **Comparar** runs visualmente  
# MAGIC ✅ **Organizar** el ciclo de vida de experimentos  
# MAGIC ✅ **Integrar** MLflow con scikit-learn
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Módulos 05-15 completados (Pandas, SQL, PySpark)
# MAGIC * ✅ Conocimiento básico de estadística
# MAGIC * ✅ Familiaridad con DataFrames
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **¿Qué es MLflow?** - Plataforma de ciclo de vida ML
# MAGIC 2. **Experimentos y Runs** - Estructura de tracking
# MAGIC 3. **Parámetros, Métricas y Artifacts** - Qué registrar
# MAGIC 4. **Autologging** - Tracking automático
# MAGIC 5. **Comparación de runs** - Análisis visual
# MAGIC 6. **Caso integrador** - Primer experimento completo

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

print("🧪 MLFLOW Y EXPERIMENTOS")
print("="*70)

# Cargar datos reales de Unity Catalog
CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Datos cargados: {len(df)} registros")
    print(f"   Período: {df['fecha'].min().strftime('%Y-%m')} a {df['fecha'].max().strftime('%Y-%m')}")
    print(f"   Sucursales: {df['sucursal_id'].nunique()}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar la tabla: {e}")
    print("   Continuando con datos sintéticos...")
    np.random.seed(42)
    df = pd.DataFrame({
        'fecha': pd.date_range('2019-01-01', periods=60, freq='ME'),
        'sucursal_id': np.random.choice(['S001','S002','S003','S004','S005'], 60),
        'ventas': np.random.normal(50000, 15000, 60).round(2)
    })
    USAR_DATOS_REALES = False

print(f"\n📊 Resumen de datos:")
print(f"   • Ventas totales: ${df['ventas'].sum():,.2f}")
print(f"   • Promedio: ${df['ventas'].mean():,.2f}")
print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: MLflow y Experimentos
# MAGIC %md
# MAGIC ## 📚 Teoría: MLflow y Ciclo de Vida ML
# MAGIC
# MAGIC ### 🧪 ¿Qué es MLflow?
# MAGIC
# MAGIC **MLflow** es una plataforma open-source para gestionar el ciclo de vida completo de Machine Learning:
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────────────┐
# MAGIC │                 CICLO DE VIDA ML                  │
# MAGIC ├──────────┬──────────┬──────────┬───────────────┤
# MAGIC │ Tracking │ Models   │ Registry │ Serving       │
# MAGIC │          │          │          │               │
# MAGIC │ Registrar│ Empaquetar│ Versionar│ Desplegar     │
# MAGIC │ params,  │ modelos  │ modelos  │ en producción  │
# MAGIC │ métricas │ reusable |          │               │
# MAGIC │ artifacts│          │          │               │
# MAGIC └──────────┴──────────┴──────────┴───────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Conceptos Clave
# MAGIC
# MAGIC | Concepto | Descripción | Analogía |
# MAGIC |----------|-------------|----------|
# MAGIC | **Experiment** | Contenedor de runs relacionados | Como un proyecto de investigación |
# MAGIC | **Run** | Una ejecución individual | Como un ensayo de laboratorio |
# MAGIC | **Parameters** | Inputs configurables | Como ingredientes de una receta |
# MAGIC | **Metrics** | Valores numéricos a optimizar | Como notas de un examen |
# MAGIC | **Artifacts** | Archivos generados (modelos, gráficos) | Como el producto final |
# MAGIC | **Tags** | Metadatos descriptivos | Como etiquetas de organizacion |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Flujo de Trabajo MLflow
# MAGIC
# MAGIC ```python
# MAGIC import mlflow
# MAGIC import mlflow.sklearn
# MAGIC
# MAGIC # 1. Crear o seleccionar experimento
# MAGIC mlflow.set_experiment("ventas_prediction")
# MAGIC
# MAGIC # 2. Iniciar un run
# MAGIC with mlflow.start_run(run_name="linear_regression_v1"):
# MAGIC     
# MAGIC     # 3. Registrar parámetros
# MAGIC     mlflow.log_param("model_type", "LinearRegression")
# MAGIC     mlflow.log_param("test_size", 0.2)
# MAGIC     mlflow.log_param("random_state", 42)
# MAGIC     
# MAGIC     # 4. Entrenar modelo
# MAGIC     model = LinearRegression()
# MAGIC     model.fit(X_train, y_train)
# MAGIC     
# MAGIC     # 5. Evaluar y registrar métricas
# MAGIC     predictions = model.predict(X_test)
# MAGIC     mlflow.log_metric("rmse", np.sqrt(mean_squared_error(y_test, predictions)))
# MAGIC     mlflow.log_metric("r2", r2_score(y_test, predictions))
# MAGIC     
# MAGIC     # 6. Registrar el modelo como artifact
# MAGIC     mlflow.sklearn.log_model(model, "model")
# MAGIC     
# MAGIC     # 7. Tags para organización
# MAGIC     mlflow.set_tag("author", "cristian")
# MAGIC     mlflow.set_tag("dataset", "ventas_mensuales_mendoza_h3")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚡ Autologging: Tracking Automático
# MAGIC
# MAGIC ```python
# MAGIC # Habilitar autolog para sklearn
# MAGIC mlflow.autolog()
# MAGIC
# MAGIC # Entrenar - MLflow registra todo automáticamente
# MAGIC model = LinearRegression()
# MAGIC model.fit(X_train, y_train)
# MAGIC # → Parámetros, métricas, modelo, todo se registra solo
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **MLflow resuelve problemas reales de ML:**
# MAGIC * 🔬 **Reproducibilidad:** Misma config → mismo resultado
# MAGIC * 📊 **Comparación:** ¿Qué modelo es mejor? Side-by-side
# MAGIC * 🔄 **Versionado:** Cada iteración queda registrada
# MAGIC * 🚀 **Producción:** Del notebook al serving sin fricción
# MAGIC * 👥 **Colaboración:** El equipo ve tus experimentos

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("💻 SETUP: PRIMER EXPERIMENTO CON MLFLOW")
print("="*70)

# Preparar datos (usar variables cargadas de la celda anterior)
df_features = df.copy()
df_features['mes'] = df_features['fecha'].dt.month
df_features['anio'] = df_features['fecha'].dt.year

# Features simples: mes como feature numérica
X = df_features[['mes', 'anio']].values
y = df_features['ventas'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear experimento
mlflow.set_experiment("ventas_prediction_los_andes")

# Ejecutar experimento con tracking manual
with mlflow.start_run(run_name="linear_regression_v1"):
    # Parámetros
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("features", "mes, anio")
    
    # Entrenar
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predecir
    predictions = model.predict(X_test)
    
    # Métricas
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", np.mean(np.abs(y_test - predictions)))
    
    # Tags
    mlflow.set_tag("dataset", "ventas_mensuales_mendoza_h3")
    mlflow.set_tag("author", "saliendo_de_lo_pandito")
    
    # Registrar modelo
    mlflow.sklearn.log_model(model, "model")
    
    print(f"✅ Experimento completado")
    print(f"   RMSE: {rmse:,.2f}")
    print(f"   R²: {r2:.4f}")
    print(f"   MAE: {np.mean(np.abs(y_test - predictions)):,.2f}")
    print(f"\n📌 Revisa el experimento en la pestaña 'Experiments' de Databricks")

print("\n" + "="*70)
print("✅ Listo para Machine Learning con MLflow")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 17_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **MLflow — plataforma de ciclo de vida ML:**
# MAGIC    - Tracking: registrar parámetros, métricas y artifacts
# MAGIC    - Models: empaquetar modelos reutilizables
# MAGIC    - Registry: versionar modelos en producción
# MAGIC    - Serving: desplegar modelos sin fricción
# MAGIC
# MAGIC 2. **Experimentos y Runs:**
# MAGIC    - `mlflow.set_experiment("nombre")` — crear o seleccionar experimento
# MAGIC    - `with mlflow.start_run(run_name="...")` — una ejecución individual
# MAGIC    - Cada run registra config + resultados para comparación posterior
# MAGIC
# MAGIC 3. **Parámetros, Métricas y Artifacts:**
# MAGIC    - `mlflow.log_param("key", value)` — inputs configurables (test_size, model_type)
# MAGIC    - `mlflow.log_metric("rmse", value)` — valores numéricos a optimizar
# MAGIC    - `mlflow.sklearn.log_model(model, "model")` — guardar el modelo entrenado
# MAGIC    - `mlflow.set_tag("author", "nombre")` — metadatos descriptivos
# MAGIC
# MAGIC 4. **Autologging — tracking automático:**
# MAGIC    - `mlflow.autolog()` registra todo sin código manual
# MAGIC    - Parámetros, métricas, modelo y artifacts automáticamente
# MAGIC    - Una línea reemplaza 10+ llamadas manuales
# MAGIC
# MAGIC 5. **Comparación de runs:**
# MAGIC    - Pestaña Experiments en Databricks: vista side-by-side
# MAGIC    - Filtrar por métrica, comparar parámetros
# MAGIC    - Identificar el mejor modelo por RMSE, R² o MAE
# MAGIC    - Reproducibilidad: misma config → mismo resultado
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Siempre registrar parámetros y métricas**
# MAGIC ```python
# MAGIC # MALO: entrenar sin tracking, no hay forma de comparar
# MAGIC model = LinearRegression()
# MAGIC model.fit(X_train, y_train)
# MAGIC # ¿Cuál era la config? ¿Cuál fue el resultado? → se pierde
# MAGIC
# MAGIC # BUENO: registrar todo en MLflow
# MAGIC with mlflow.start_run(run_name="lr_v1"):
# MAGIC     mlflow.log_param("test_size", 0.2)
# MAGIC     mlflow.log_param("features", "mes, anio")
# MAGIC     model.fit(X_train, y_train)
# MAGIC     mlflow.log_metric("rmse", rmse)
# MAGIC     mlflow.log_metric("r2", r2)
# MAGIC     mlflow.sklearn.log_model(model, "model")
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Usar autolog para experiments rápidos, manual para producción**
# MAGIC ```python
# MAGIC # Exploración: autolog (rápido, sin código extra)
# MAGIC mlflow.autolog()
# MAGIC model = LinearRegression()
# MAGIC model.fit(X_train, y_train)  # todo se registra solo
# MAGIC
# MAGIC # Producción: tracking manual (control total)
# MAGIC with mlflow.start_run(run_name="prod_v1"):
# MAGIC     mlflow.log_param("model", "LinearRegression")
# MAGIC     mlflow.log_param("features", "mes, anio, sucursal_id")
# MAGIC     mlflow.log_metric("rmse", rmse)
# MAGIC     mlflow.set_tag("stage", "production")
# MAGIC     mlflow.sklearn.log_model(model, "model")
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Nombrar runs descriptivamente**
# MAGIC ```python
# MAGIC # MALO: nombre genérico, no distinguible
# MAGIC with mlflow.start_run(run_name="run_1"):
# MAGIC
# MAGIC # BUENO: nombre descriptivo con modelo y versión
# MAGIC with mlflow.start_run(run_name="linear_regression_v1"):
# MAGIC with mlflow.start_run(run_name="random_forest_tuned_v3"):
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Registrar un parámetro | `mlflow.log_param("key", value)` |
# MAGIC | Registrar una métrica | `mlflow.log_metric("rmse", value)` |
# MAGIC | Guardar el modelo | `mlflow.sklearn.log_model(model, "model")` |
# MAGIC | Agregar metadata | `mlflow.set_tag("author", "nombre")` |
# MAGIC | Tracking automático | `mlflow.autolog()` antes de entrenar |
# MAGIC | Crear experimento | `mlflow.set_experiment("nombre")` |
# MAGIC | Iniciar un run | `with mlflow.start_run(run_name="...")` |
# MAGIC | Comparar runs | Pestaña Experiments en Databricks |
# MAGIC | Exploración rápida | `mlflow.autolog()` |
# MAGIC | Producción controlada | Tracking manual con log_param/log_metric |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🧪 ¡MLflow y experimentos dominados!</h3>
# MAGIC   <p><i>"MLflow convierte el caos de experimentos ML en ciencia reproducible: cada run queda registrado, cada modelo es comparable."</i></p>
# MAGIC </div>