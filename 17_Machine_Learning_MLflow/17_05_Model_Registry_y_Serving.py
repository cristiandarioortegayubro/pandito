# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 📦 Módulo 17 - Notebook 05: Model registry y serving
# MAGIC
# MAGIC ## 🚀 De Notebook a Producción
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 17 - Machine Learning con MLflow  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio-Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** el Model Registry de MLflow  
# MAGIC ✅ **Registrar** modelos en Unity Catalog  
# MAGIC ✅ **Versionar** modelos (staging, production, archived)  
# MAGIC ✅ **Cargar** modelos registrados para inferencia  
# MAGIC ✅ **Entender** el concepto de Model Serving  
# MAGIC ✅ **Crear** un pipeline de scoring batch
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 17_01 al 17_04 completados
# MAGIC * ✅ Modelos entrenados en experimentos previos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **Model Registry** - Centralización de modelos
# MAGIC 2. **Registro de modelos** - create_registered_model, log_model
# MAGIC 3. **Versiones y stages** - Staging, Production, Archived
# MAGIC 4. **Cargar modelos** - mlflow.pyfunc.load_model
# MAGIC 5. **Batch scoring** - Inferencia sobre nuevos datos
# MAGIC 6. **Pipeline ML completo** - De entrenamiento a producción

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("💾 PREPARANDO MODELO PARA REGISTRY")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter
    print(f"✅ Datos cargados: {len(df)} registros")except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    np.random.seed(42)
    df = pd.DataFrame({
        'fecha': pd.date_range('2019-01-01', periods=300, freq='ME'),
        'sucursal_id': np.random.choice(['S001','S002','S003','S004','S005'], 300),
        'ventas': np.random.normal(50000, 15000, 300).round(2)
    })
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter

print(f"   Features: mes, anio, trimestre")
print(f"   Target: ventas")
print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Model Registry
# MAGIC %md
# MAGIC ## 📚 Teoría: Model Registry y Serving
# MAGIC
# MAGIC ### 📦 ¿Qué es el Model Registry?
# MAGIC
# MAGIC **Model Registry** es el sistema centralizado de MLflow para gestionar el ciclo de vida de modelos.
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────────┐
# MAGIC │              MODEL REGISTRY                   │
# MAGIC ├──────────┬──────────────┬───────────────────┤
# MAGIC │ Staging  │  Production  │    Archived       │
# MAGIC │          │              │                   │
# MAGIC │ En       │  En uso      │  Versiones        │
# MAGIC │ prueba   │  activo      │  anteriores       │
# MAGIC └──────────┴──────────────┴───────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏷️ Registro de Modelos en Unity Catalog
# MAGIC
# MAGIC ```python
# MAGIC # Registrar modelo en Unity Catalog
# MAGIC mlflow.register_model(
# MAGIC     model_uri="runs:/<run_id>/model",
# MAGIC     name="pandito_ds.default.modelo_ventas"
# MAGIC )
# MAGIC
# MAGIC # En Databricks, los modelos se registran en Unity Catalog
# MAGIC # Formato: catalog.schema.model_name
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Stages del Modelo
# MAGIC
# MAGIC | Stage | Significado | Cuándo usar |
# MAGIC |-------|-------------|------------|
# MAGIC | **None** | Recién registrado | Versión nueva |
# MAGIC | **Staging** | En pruebas | Validación/QA |
# MAGIC | **Production** | En uso activo | Inferencia real |
# MAGIC | **Archived** | Retirado | Versiones antiguas |
# MAGIC
# MAGIC ```python
# MAGIC # Promover modelo a Production
# MAGIC client = mlflow.tracking.MlflowClient()
# MAGIC client.transition_model_version_stage(
# MAGIC     name="pandito_ds.default.modelo_ventas",
# MAGIC     version=1,
# MAGIC     stage="Production"
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔮 Inferencia: Usar el Modelo
# MAGIC
# MAGIC ```python
# MAGIC # Cargar modelo desde registry
# MAGIC model = mlflow.pyfunc.load_model(
# MAGIC     model_uri="models:/pandito_ds.default.modelo_ventas/Production"
# MAGIC )
# MAGIC
# MAGIC # Predecir
# MAGIC predictions = model.predict(new_data)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🚀 Model Serving (Concepto)
# MAGIC
# MAGIC En Databricks Free Edition, el serving puede tener limitaciones, pero el concepto es:
# MAGIC
# MAGIC ```
# MAGIC Modelo en Registry → Endpoint REST → Predicciones en tiempo real
# MAGIC
# MAGIC POST /invocations
# MAGIC {"inputs": [{"mes": 12, "anio": 2024, "trimestre": 4}]}
# MAGIC →
# MAGIC {"predictions": [85000.0]}
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Model Registry = control y orden en ML:**
# MAGIC * 🔄 **Versionado:** Cada modelo tiene versión
# MAGIC * 🏷️ **Stages:** Control de qué modelo está en producción
# MAGIC * 🔙 **Rollback:** Volver a versión anterior si algo falla
# MAGIC * 👥 **Colaboración:** Todo el equipo ve los modelos
# MAGIC * 📊 **Auditoría:** Quién, cuándo, qué modelo

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import mlflow.sklearn
import mlflow.pyfunc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("💻 REGISTRO Y SERVING DE MODELO")
print("="*70)

# Preparar datos (usar variables de celda anterior)
feature_cols = ['mes', 'anio', 'trimestre']
X = df[feature_cols].values
y = df['ventas'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("model_registry_los_andes")

# Entrenar y registrar modelo
MODEL_NAME = "pandito_ds.default.modelo_ventas_rf"

with mlflow.start_run(run_name="rf_for_registry_v1") as run:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.sklearn.log_model(model, "model")
    
    run_id = run.info.run_id
    print(f"✅ Modelo entrenado")
    print(f"   Run ID: {run_id}")
    print(f"   RMSE: {rmse:,.2f}")
    print(f"   R²: {r2:.4f}")

# Registrar en Model Registry
try:
    model_uri = f"runs:/{run_id}/model"
    registered = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
    print(f"\n📦 Modelo registrado: {MODEL_NAME}")
    print(f"   Versión: {registered.version}")
except Exception as e:
    print(f"\n⚠️  No se pudo registrar (puede requerir permisos): {e}")
    print(f"   El modelo está en el run: {run_id}")

# Cargar modelo para inferencia (batch scoring)
try:
    loaded_model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")
    
    # Batch scoring: predecir sobre datos nuevos
    new_data = pd.DataFrame({
        'mes': [1, 2, 3, 4, 5, 6],
        'anio': [2025, 2025, 2025, 2025, 2025, 2025],
        'trimestre': [1, 1, 1, 2, 2, 2]
    })
    
    predictions_new = loaded_model.predict(new_data)
    
    print(f"\n🔮 BATCH SCORING - Predicciones 2025:")
    for i, row in new_data.iterrows():
        print(f"   Mes {int(row['mes'])}/2025: ${predictions_new[i]:,.2f}")
except Exception as e:
    print(f"\n⚠️  Carga del modelo: {e}")

print("\n" + "="*70)
print("✅ Pipeline ML completo: Entrenamiento → Registry → Inferencia")

# COMMAND ----------

# DBTITLE 1,📦 Teoría: Registry con datos reales
# MAGIC %md
# MAGIC ## 📦 Model Registry aplicado a Los Andes Market
# MAGIC
# MAGIC ### 🚀 Pipeline completo: entrenar → registrar → scoring
# MAGIC
# MAGIC Con MLflow Model Registry podemos llevar un modelo de predicción de ventas de **Los Andes Market** a producción:
# MAGIC
# MAGIC ```python
# MAGIC # 1. Entrenar y registrar
# MAGIC mlflow.sklearn.log_model(model, "model")
# MAGIC mlflow.register_model(f"runs:/{run_id}/model", "pandito_ds.default.modelo_ventas")
# MAGIC
# MAGIC # 2. Cargar modelo de producción
# MAGIC model = mlflow.pyfunc.load_model("models:/pandito_ds.default.modelo_ventas/Production")
# MAGIC
# MAGIC # 3. Batch scoring
# MAGIC predicciones = model.predict(nuevos_datos)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Cómo versionar modelos de predicción de ventas?
# MAGIC * ¿Cómo hacer batch scoring sobre datos nuevos?
# MAGIC * ¿Cómo comparar versión Staging vs Production?

# COMMAND ----------

# DBTITLE 1,📦 Práctica: Registry con datos reales
import mlflow
import mlflow.sklearn
import mlflow.pyfunc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("📦 MODEL REGISTRY APLICADO A LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and df is not None:
    print("\n1️⃣  ENTRENAR Y REGISTRAR MODELO DE VENTAS")
    print("-"*70)

    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter

    feature_cols = ['mes', 'anio', 'trimestre']
    X = df[feature_cols].values
    y = df['ventas'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("registry_ventas_los_andes")

    MODEL_NAME = "pandito_ds.default.modelo_ventas_rf"

    with mlflow.start_run(run_name="rf_registry_v1") as run:
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        preds = rf.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("features", ", ".join(feature_cols))
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(rf, "model")
        run_id = run.info.run_id

        print(f"   Modelo entrenado: RMSE=${rmse:,.0f}, R²={r2:.4f}")
        print(f"   Run ID: {run_id}")

    print("\n" + "="*70)
    print("\n2️⃣  REGISTRAR EN MODEL REGISTRY")
    print("-"*70)

    try:
        result = mlflow.register_model(
            model_uri=f"runs:/{run_id}/model",
            name=MODEL_NAME
        )
        print(f"   ✅ Modelo registrado: {MODEL_NAME}")
        print(f"   Versión: {result.version}")
    except Exception as e:
        print(f"   ⚠️  No se pudo registrar (permisos): {e}")
        print(f"   El modelo está disponible en el run: {run_id}")

    print("\n" + "="*70)
    print("\n3️⃣  CARGAR MODELO Y BATCH SCORING")
    print("-"*70)

    # Cargar modelo desde el run
    loaded_model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

    # Simular datos nuevos (próximos 3 meses de 2025)
    nuevos_datos = pd.DataFrame({
        'mes': [1, 2, 3],
        'anio': [2025, 2025, 2025],
        'trimestre': [1, 1, 1],
    })

    predicciones = loaded_model.predict(nuevos_datos)
    print(f"\n   Batch scoring — Predicción de ventas para Q1 2025:")
    for i, row in nuevos_datos.iterrows():
        print(f"      {row['anio']}-{row['mes']:02d}: ${predicciones[i]:,.0f}")

    print("\n" + "="*70)
    print("\n4️⃣  SCORING POR SUCURSAL")
    print("-"*70)

    # Predecir para cada sucursal
    sucursales = df[['sucursal_id', 'sucursal_nombre']].drop_duplicates().head(5)
    for _, suc in sucursales.iterrows():
        datos_suc = pd.DataFrame({
            'mes': [1, 2, 3],
            'anio': [2025, 2025, 2025],
            'trimestre': [1, 1, 1],
        })
        preds_suc = loaded_model.predict(datos_suc)
        print(f"   {suc['sucursal_nombre']}:")
        print(f"      Ene: ${preds_suc[0]:,.0f} | Feb: ${preds_suc[1]:,.0f} | Mar: ${preds_suc[2]:,.0f}")

    print("\n" + "="*70)
    print("\n5️⃣  PIPELINE COMPLETO: Entrenar → Registrar → Scoring")
    print("-"*70)
    print("\n   ✅ Pipeline ML completo:")
    print(f"      1. Entrenar RandomForest → Run ID: {run_id}")
    print(f"      2. Registrar en Model Registry: {MODEL_NAME}")
    print(f"      3. Cargar modelo: mlflow.pyfunc.load_model()")
    print(f"      4. Batch scoring: predicciones para Q1 2025")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 17_05
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Model Registry — ciclo de vida de modelos:**
# MAGIC    - Centraliza modelos entrenados en Unity Catalog
# MAGIC    - `mlflow.register_model(model_uri, name)` registra desde un run
# MAGIC    - Formato: `catalog.schema.model_name` (ej: `pandito_ds.default.modelo_ventas`)
# MAGIC    - Cada registro crea una versión incremental (v1, v2, v3...)
# MAGIC
# MAGIC 2. **Stages — control de versiones:**
# MAGIC    - `None`: recién registrado, sin asignar
# MAGIC    - `Staging`: en pruebas/QA antes de producción
# MAGIC    - `Production`: en uso activo para inferencia
# MAGIC    - `Archived`: retirado, versión anterior conservada
# MAGIC    - `transition_model_version_stage()` mueve entre stages
# MAGIC
# MAGIC 3. **Cargar modelos registrados:**
# MAGIC    - `mlflow.pyfunc.load_model("models:/nombre/Production")` — cargar por stage
# MAGIC    - `mlflow.pyfunc.load_model("models:/nombre/1")` — cargar por versión
# MAGIC    - El modelo cargado funciona como cualquier predictor: `model.predict(data)`
# MAGIC
# MAGIC 4. **Batch Scoring — inferencia sobre nuevos datos:**
# MAGIC    - Cargar modelo desde registry → predecir sobre DataFrame nuevo
# MAGIC    - Sin re-entrenar: usar el modelo guardado directamente
# MAGIC    - Ideal para scoring periódico (mensual, semanal) sobre datos frescos
# MAGIC
# MAGIC 5. **Pipeline ML completo:**
# MAGIC    - Entrenamiento → log_model → register_model → transition to Production → load_model → batch scoring
# MAGIC    - MLflow tracking + registry + serving = ciclo de vida profesional
# MAGIC    - Reproducible, versionado y auditable de extremo a extremo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Registrar en Unity Catalog, no en el metastore local**
# MAGIC ```python
# MAGIC # MALO: registrar sin catalog (no portable, sin gobernanza)
# MAGIC mlflow.register_model(model_uri=f"runs:/{run_id}/model", name="modelo_ventas")
# MAGIC
# MAGIC # BUENO: registrar en Unity Catalog con formato catalog.schema.model
# MAGIC mlflow.register_model(
# MAGIC     model_uri=f"runs:/{run_id}/model",
# MAGIC     name="pandito_ds.default.modelo_ventas_rf"
# MAGIC )
# MAGIC # Gobernanza, permisos y acceso desde cualquier notebook
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Promover a Production solo después de validar en Staging**
# MAGIC ```python
# MAGIC # MALO: registrar y mandar a Production sin validar
# MAGIC mlflow.register_model(model_uri, name=MODEL_NAME)
# MAGIC client.transition_model_version_stage(name=MODEL_NAME, version=1, stage="Production")
# MAGIC # Sin QA → riesgo en producción
# MAGIC
# MAGIC # BUENO: Staging → validar métricas → Production
# MAGIC client.transition_model_version_stage(name=MODEL_NAME, version=1, stage="Staging")
# MAGIC # Validar: cargar modelo, predecir sobre test, comparar métricas
# MAGIC loaded = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/Staging")
# MAGIC # Si pasa validación → promover
# MAGIC client.transition_model_version_stage(name=MODEL_NAME, version=1, stage="Production")
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Cargar por stage, no por versión**
# MAGIC ```python
# MAGIC # MALO: hardcodear versión (se rompe al actualizar)
# MAGIC model = mlflow.pyfunc.load_model("models:/pandito_ds.default.modelo_ventas/1")
# MAGIC # Si se promueve v2 a Production, este código sigue usando v1
# MAGIC
# MAGIC # BUENO: cargar por stage (siempre la versión actual en Production)
# MAGIC model = mlflow.pyfunc.load_model("models:/pandito_ds.default.modelo_ventas/Production")
# MAGIC # Al promover v2 a Production, este código usa v2 automáticamente
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Registrar modelo desde un run | `mlflow.register_model(model_uri, name)` |
# MAGIC | Promover a staging | `client.transition_model_version_stage(..., stage="Staging")` |
# MAGIC | Promover a production | `client.transition_model_version_stage(..., stage="Production")` |
# MAGIC | Archivar versión antigua | `client.transition_model_version_stage(..., stage="Archived")` |
# MAGIC | Cargar modelo en producción | `mlflow.pyfunc.load_model("models:/name/Production")` |
# MAGIC | Cargar versión específica | `mlflow.pyfunc.load_model("models:/name/1")` |
# MAGIC | Batch scoring sobre datos nuevos | `model.predict(new_data)` |
# MAGIC | Ver versiones disponibles | `client.search_model_versions("name='...'"`)
# MAGIC | Rollback a versión anterior | Archivar actual + promover la anterior a Production |
# MAGIC | Registro en Unity Catalog | `name="catalog.schema.model_name"` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🚀 ¡Model Registry y Serving dominados!</h3>
# MAGIC   <p><i>"Model Registry convierte experimentos en producción: versionado, stages y rollback para ML profesional."</i></p>
# MAGIC </div>