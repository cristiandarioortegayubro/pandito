# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🎯 Módulo 17 - Notebook 03: Clasificación - Churn de Clientes
# MAGIC
# MAGIC ## 🤖 Machine Learning para retención de clientes
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
# MAGIC ✅ **Entender** el problema de clasificación binaria  
# MAGIC ✅ **Preparar** datos sintéticos de churn  
# MAGIC ✅ **Entrenar** LogisticRegression, DecisionTree, RandomForest  
# MAGIC ✅ **Evaluar** con Precision, Recall, F1, ROC-AUC  
# MAGIC ✅ **Interpretar** matriz de confusión  
# MAGIC ✅ **Trackear** con MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebook 17_02 completado (Regresión)
# MAGIC * ✅ Conceptos básicos de MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **Clasificación binaria** - Concepto de churn
# MAGIC 2. **Preparación de datos** - Features, target binario
# MAGIC 3. **Logistic Regression** - Línea base
# MAGIC 4. **Decision Tree y Random Forest** - Modelos más complejos
# MAGIC 5. **Evaluación** - Precision, Recall, F1, ROC-AUC
# MAGIC 6. **Matriz de confusión** - Interpretación de errores

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

print("💾 PREPARANDO DATOS DE CHURN")
print("="*70)

# Generar dataset sintético de churn basado en patrones reales
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'antiguedad_meses': np.random.randint(1, 60, n),
    'frecuencia_compra': np.random.randint(1, 30, n),
    'ticket_promedio': np.random.normal(500, 150, n).round(2),
    'reclamos_mes': np.random.poisson(1.5, n),
    'dias_sin_compra': np.random.randint(0, 90, n),
    'satisfaccion': np.random.randint(1, 6, n)
})

# Target: churn (1 = abandonó, 0 = activo) - basado en patrones
df['churn'] = (
    (df['dias_sin_compra'] > 45) | 
    (df['satisfaccion'] <= 2) | 
    (df['reclamos_mes'] > 3)
).astype(int)

# Agregar algo de ruido (no perfecto)
noise = np.random.random(n) < 0.1
df.loc[noise, 'churn'] = 1 - df.loc[noise, 'churn']

print(f"✅ Dataset generado: {len(df)} clientes")
print(f"   Churn rate: {df['churn'].mean()*100:.1f}%")
print(f"   Activos: {(df['churn']==0).sum()}")
print(f"   Churn: {(df['churn']==1).sum()}")
print(f"\n📊 Features: {list(df.columns[:-1])}")
print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Clasificación
# MAGIC %md
# MAGIC ## 📚 Teoría: Clasificación y Churn
# MAGIC
# MAGIC ### 🎯 ¿Qué es la Clasificación?
# MAGIC
# MAGIC **Clasificación** predice a qué categoría pertenece una observación.
# MAGIC
# MAGIC ```
# MAGIC Cliente: antiguedad=3, frecuencia=2, satisfaccion=2
# MAGIC         ↓
# MAGIC    Modelo de Clasificación
# MAGIC         ↓
# MAGIC Predicción: churn = 1 (abandonará)
# MAGIC ```
# MAGIC
# MAGIC **Tipos:**
# MAGIC * **Binaria:** 2 categorías (churn/no-churn, aprobar/rechazar)
# MAGIC * **Multiclase:** 3+ categorías (segmentos: alto/medio/bajo)
# MAGIC * **Multilabel:** Múltiples categorías simultaneas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Métricas de Clasificación
# MAGIC
# MAGIC | Métrica | Qué mide | Fórmula | Interpretación |
# MAGIC |---------|----------|---------|----------------|
# MAGIC | **Precision** | De los predichos positivos, cuántos son reales | TP/(TP+FP) | Minimiza falsos positivos |
# MAGIC | **Recall** | De los reales positivos, cuántos detecta | TP/(TP+FN) | Minimiza falsos negativos |
# MAGIC | **F1-Score** | Balance precision/recall | 2*P*R/(P+R) | Media armónica |
# MAGIC | **ROC-AUC** | Capacidad discriminativa general | Área bajo curva ROC | 0.5-1.0, mayor = mejor |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔲 Matriz de Confusión
# MAGIC
# MAGIC ```
# MAGIC               Predicho: No Churn | Predicho: Churn
# MAGIC Real: No Churn     TN (✓)        |    FP (✗)
# MAGIC Real: Churn        FN (✗)        |    TP (✓)
# MAGIC
# MAGIC TN = True Negative (correctamente identificado como activo)
# MAGIC FP = False Positive (activo predicho como churn - alarma innecesaria)
# MAGIC FN = False Negative (churn no detectado - cliente perdido!)
# MAGIC TP = True Positive (churn correctamente detectado)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🤖 Modelos de Clasificación
# MAGIC
# MAGIC | Modelo | Pros | Contras |
# MAGIC |--------|------|---------|
# MAGIC | **Logistic Regression** | Interpretable, rápido | Asume relación lineal |
# MAGIC | **Decision Tree** | Interpretable, no lineal | Propenso a overfitting |
# MAGIC | **Random Forest** | Robusto, no lineal | Menos interpretable |
# MAGIC | **Gradient Boosting** | Alto rendimiento | Requiere tuning |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Churn prediction en negocios:**
# MAGIC * 💰 Retener un cliente cuesta 5x menos que adquirir uno nuevo
# MAGIC * 🎯 Identificar clientes en riesgo antes de que se vayan
# MAGIC * 📧 Campañas de retención dirigidas
# MAGIC * 📊 ROI: $ invertidos en retención vs $ perdidos en churn

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("💻 EXPERIMENTO: CLASIFICACIÓN DE CHURN")
print("="*70)

# Usar dataset generado en la celda anterior
feature_cols = ['antiguedad_meses', 'frecuencia_compra', 'ticket_promedio', 'reclamos_mes', 'dias_sin_compra', 'satisfaccion']
X = df[feature_cols].values
y = df['churn'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

mlflow.set_experiment("churn_prediction_los_andes")

models = {
    "LogisticRegression": LogisticRegression(random_state=42, max_iter=1000),
    "DecisionTree": DecisionTreeClassifier(random_state=42, max_depth=5),
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    with mlflow.start_run(run_name=f"{name}_churn_v1"):
        mlflow.log_param("model", name)
        mlflow.log_param("features", len(feature_cols))
        mlflow.log_param("test_size", 0.2)
        
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]
        
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)
        roc = roc_auc_score(y_test, proba)
        
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("roc_auc", roc)
        mlflow.set_tag("dataset", "churn_sintetico")
        mlflow.sklearn.log_model(model, "model")
        
        results.append({"Modelo": name, "Precision": precision, "Recall": recall, "F1": f1, "ROC-AUC": roc})
        
        cm = confusion_matrix(y_test, predictions)
        print(f"\n  {name}:")
        print(f"    Precision: {precision:.4f}")
        print(f"    Recall:    {recall:.4f}")
        print(f"    F1-Score:  {f1:.4f}")
        print(f"    ROC-AUC:   {roc:.4f}")
        print(f"    Confusion: TN={cm[0][0]}, FP={cm[0][1]}, FN={cm[1][0]}, TP={cm[1][1]}")

print(f"\n📊 COMPARACIÓN:")
results_df = pd.DataFrame(results).sort_values('F1', ascending=False)
print(results_df.to_string(index=False))
print(f"\n🏆 Mejor modelo: {results_df.iloc[0]['Modelo']}")
print("\n" + "="*70)
print("✅ Experimentos de clasificación completados")

# COMMAND ----------

# DBTITLE 1,🎯 Teoría: Churn con datos reales
# MAGIC %md
# MAGIC ## 🎯 Clasificación de churn aplicada a Los Andes Market
# MAGIC
# MAGIC ### 🤖 Simular churn desde datos de ventas reales
# MAGIC
# MAGIC El dataset `ventas_mensuales_mendoza_h3` no tiene un target de churn explícito, pero podemos **simularlo** desde los patrones de ventas reales:
# MAGIC
# MAGIC ```python
# MAGIC # Si las ventas de una sucursal bajaron > 30% vs el año anterior → churn_risk = 1
# MAGIC df['ventas_anio_anterior'] = df.groupby('sucursal_id')['ventas'].shift(12)
# MAGIC df['variacion_pct'] = (df['ventas'] - df['ventas_anio_anterior']) / df['ventas_anio_anterior']
# MAGIC df['churn_risk'] = (df['variacion_pct'] < -0.30).astype(int)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Preguntas de negocio
# MAGIC * ¿Qué sucursales tienen mayor riesgo de churn?
# MAGIC * ¿La caída de ventas es predecible?
# MAGIC * ¿Qué features anticipan el decline de una sucursal?

# COMMAND ----------

# DBTITLE 1,🎯 Práctica: Churn con datos reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("🎯 CLASIFICACIÓN DE CHURN CON DATOS REALES DE LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and df is not None:
    print("\n1️⃣  SIMULAR TARGET DE CHURN DESDE VENTAS REALES")
    print("-"*70)

    df = df.sort_values(['sucursal_id', 'fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter

    # Ventas mes anterior y año anterior
    df['ventas_mes_anterior'] = df.groupby('sucursal_id')['ventas'].shift(1)
    df['ventas_anio_anterior'] = df.groupby('sucursal_id')['ventas'].shift(12)

    # Variaciones
    df['var_mensual_pct'] = (df['ventas'] - df['ventas_mes_anterior']) / df['ventas_mes_anterior']
    df['var_anual_pct'] = (df['ventas'] - df['ventas_anio_anterior']) / df['ventas_anio_anterior']

    # Target: churn_risk = 1 si caída > 30% vs año anterior
    df['churn_risk'] = ((df['var_anual_pct'] < -0.30) & df['var_anual_pct'].notna()).astype(int)

    # Features
    df_ml = df.dropna(subset=['var_mensual_pct', 'var_anual_pct'])
    feature_cols = ['mes', 'anio', 'trimestre', 'ventas', 'ventas_mes_anterior', 'var_mensual_pct', 'var_anual_pct']
    X = df_ml[feature_cols].values
    y = df_ml['churn_risk'].values

    churn_rate = y.mean() * 100
    print(f"   Registros con features completas: {len(df_ml):,}")
    print(f"   Churn rate: {churn_rate:.1f}% ({y.sum()} casos de {len(y)})")

    print("\n" + "="*70)
    print("\n2️⃣  ENTRENAR 2 MODELOS CON MLFLOW")
    print("-"*70)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    mlflow.set_experiment("churn_los_andes_ventas")

    models = {
        "LogisticRegression": LogisticRegression(random_state=42, max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    for name, model in models.items():
        with mlflow.start_run(run_name=f"{name}_churn"):
            mlflow.log_param("model", name)
            mlflow.log_param("features", len(feature_cols))
            mlflow.log_param("churn_rate", round(churn_rate, 1))

            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1]

            p = precision_score(y_test, preds, zero_division=0)
            r = recall_score(y_test, preds, zero_division=0)
            f1 = f1_score(y_test, preds, zero_division=0)
            try:
                roc = roc_auc_score(y_test, proba)
            except:
                roc = 0.0

            mlflow.log_metric("precision", p)
            mlflow.log_metric("recall", r)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("roc_auc", roc)
            mlflow.sklearn.log_model(model, "model")

            print(f"\n   {name}:")
            print(f"      Precision: {p:.3f} | Recall: {r:.3f} | F1: {f1:.3f} | ROC-AUC: {roc:.3f}")

    print("\n" + "="*70)
    print("\n3️⃣  MATRIZ DE CONFUSIÓN (RandomForest)")
    print("-"*70)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    preds_rf = rf.predict(X_test)
    cm = confusion_matrix(y_test, preds_rf)

    print(f"\n   Matriz de confusión:")
    print(f"   TN={cm[0,0]}  FP={cm[0,1]}")
    print(f"   FN={cm[1,0]}  TP={cm[1,1]}")
    print(f"\n   💡 FN = sucursales en riesgo no detectadas (más costoso)")
    print(f"   💡 FP = falsas alarmas (costo de retención innecesaria)")

    print("\n" + "="*70)
    print("\n4️⃣  FEATURE IMPORTANCE")
    print("-"*70)

    importances = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
    importances = importances.sort_values("importance", ascending=False)
    print("\n   Importancia de features para predecir churn:")
    print(importances.round(4).to_string(index=False))
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 17_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Clasificación binaria — el problema de churn:**
# MAGIC    - Target binario: 1 = churn (abandonó), 0 = activo
# MAGIC    - `train_test_split(X, y, stratify=y)` — división respetando proporción de clases
# MAGIC    - Churn rate desbalanceado requiere métricas más allá de accuracy
# MAGIC
# MAGIC 2. **Logistic Regression — línea base interpretable:**
# MAGIC    - `LogisticRegression(max_iter=1000)` — modelo lineal para clasificación
# MAGIC    - Coeficientes indican impacto de cada feature en la probabilidad de churn
# MAGIC    - Todo modelo de clasificación debe superarlo como baseline
# MAGIC
# MAGIC 3. **Decision Tree y Random Forest — modelos no lineales:**
# MAGIC    - `DecisionTreeClassifier(max_depth=5)` — interpretable, capta no linealidad
# MAGIC    - `RandomForestClassifier(n_estimators=100)` — robusto, reduce overfitting
# MAGIC    - Random Forest generalmente supera a Decision Tree individual
# MAGIC
# MAGIC 4. **Métricas de clasificación:**
# MAGIC    - `Precision` — de los predichos como churn, cuántos realmente lo son (minimiza falsos positivos)
# MAGIC    - `Recall` — de los que realmente churnean, cuántos detecta (minimiza falsos negativos)
# MAGIC    - `F1-Score` — balance entre Precision y Recall (media armónica)
# MAGIC    - `ROC-AUC` — capacidad discriminativa general (0.5 = azar, 1.0 = perfecto)
# MAGIC
# MAGIC 5. **Matriz de confusión — interpretación de errores:**
# MAGIC    - TN: activos correctamente identificados (no molestar)
# MAGIC    - FP: activos predichos como churn (alarma innecesaria, costo de retención)
# MAGIC    - FN: churn no detectado (cliente perdido, el error más costoso)
# MAGIC    - TP: churn correctamente detectado (oportunidad de retención)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Elegir métrica según costo de negocio**
# MAGIC ```python
# MAGIC # MALO: optimizar accuracy cuando churn es 5% (predecir "activo" = 95% accuracy)
# MAGIC model.score(X_test, y_test)  # 95% — engañoso
# MAGIC
# MAGIC # BUENO: optimizar según costo de error
# MAGIC # Si perder un cliente cuesta $1000 y retener cuesta $50:
# MAGIC # → Maximizar Recall (detectar TODOS los churn posibles)
# MAGIC # F1-Score balancea ambos, ROC-AUC mide discriminación general
# MAGIC recall = recall_score(y_test, predictions)
# MAGIC f1 = f1_score(y_test, predictions)
# MAGIC roc = roc_auc_score(y_test, proba)
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Usar stratify=y con datos desbalanceados**
# MAGIC ```python
# MAGIC # MALO: sin stratify, el split puede dejar muy pocos churn en test
# MAGIC X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# MAGIC # Si churn rate es 10%, test podría tener 0% por azar
# MAGIC
# MAGIC # BUENO: stratify mantiene la proporción de clases en ambos splits
# MAGIC X_train, X_test, y_train, y_test = train_test_split(
# MAGIC     X, y, test_size=0.2, random_state=42, stratify=y
# MAGIC )
# MAGIC # Train y test mantienen ~10% churn cada uno
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: predict_proba para ROC-AUC, predict para F1**
# MAGIC ```python
# MAGIC # MALO: usar predict() para ROC-AUC (solo 0/1, pierde información de probabilidad)
# MAGIC roc = roc_auc_score(y_test, model.predict(X_test))  # subóptimo
# MAGIC
# MAGIC # BUENO: predict_proba para probabilidades continuas
# MAGIC proba = model.predict_proba(X_test)[:, 1]  # probabilidad de churn
# MAGIC roc = roc_auc_score(y_test, proba)  # correcto, usa scores continuos
# MAGIC predictions = model.predict(X_test)  # 0/1 para Precision/Recall/F1
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Modelo / Métrica |
# MAGIC |-----------|-----------------|
# MAGIC | Línea base interpretable | `LogisticRegression(max_iter=1000)` |
# MAGIC | No lineal, interpretable | `DecisionTreeClassifier(max_depth=5)` |
# MAGIC | Robusto, máximo rendimiento | `RandomForestClassifier(n_estimators=100)` |
# MAGIC | Datos desbalanceados | `stratify=y` en train_test_split |
# MAGIC | Minimizar falsos positivos | Optimizar `Precision` |
# MAGIC | Minimizar falsos negativos (perder clientes) | Optimizar `Recall` |
# MAGIC | Balance Precision/Recall | Optimizar `F1-Score` |
# MAGIC | Capacidad discriminativa general | `ROC-AUC` (0.5-1.0) |
# MAGIC | Datos extremadamente desbalanceados | `class_weight='balanced'` o SMOTE |
# MAGIC | Interpretar errores de modelo | Matriz de confusión (TN, FP, FN, TP) |
# MAGIC | Trackear experimentos | `mlflow.start_run()` + `log_metric` por cada métrica |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🎯 ¡Clasificación y Churn de clientes dominados!</h3>
# MAGIC   <p><i>"En churn prediction, Recall es rey: detectar a tiempo al cliente en riesgo vale 20x más que una alarma falsa."</i></p>
# MAGIC </div>