# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🎲 Módulo 17 - Notebook 04: Clustering - Segmentación de Clientes
# MAGIC
# MAGIC ## 📊 Machine Learning no Supervisado
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 17 - Machine Learning con MLflow  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** aprendizaje no supervisado  
# MAGIC ✅ **Aplicar** KMeans para segmentación  
# MAGIC ✅ **Determinar** número óptimo de clusters (Elbow, Silhouette)  
# MAGIC ✅ **Interpretar** perfiles de segmentos  
# MAGIC ✅ **Visualizar** clusters  
# MAGIC ✅ **Trackear** experimentos con MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 17_01 al 17_03 completados
# MAGIC * ✅ Conocimiento de Pandas y ML básico
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **Aprendizaje no supervisado** - Concepto de clustering
# MAGIC 2. **KMeans** - Algoritmo de segmentación
# MAGIC 3. **Método del Codo** - Número óptimo de K
# MAGIC 4. **Silhouette Score** - Calidad de clusters
# MAGIC 5. **Perfiles de segmentos** - Interpretación de negocio
# MAGIC 6. **Visualización** - Scatter plots de clusters

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

print("💾 PREPARANDO DATOS PARA SEGMENTACIÓN")
print("="*70)

# Generar dataset de clientes basado en patrones de Los Andes Market
np.random.seed(42)
n = 500

# 3 segmentos naturales de clientes
segment_a = pd.DataFrame({
    'frecuencia_compra': np.random.normal(25, 5, n//3),
    'ticket_promedio': np.random.normal(800, 100, n//3),
    'antiguedad_meses': np.random.normal(36, 10, n//3),
    'reclamos_mes': np.random.poisson(0.5, n//3)
})

segment_b = pd.DataFrame({
    'frecuencia_compra': np.random.normal(12, 4, n//3),
    'ticket_promedio': np.random.normal(450, 80, n//3),
    'antiguedad_meses': np.random.normal(18, 8, n//3),
    'reclamos_mes': np.random.poisson(1.5, n//3)
})

segment_c = pd.DataFrame({
    'frecuencia_compra': np.random.normal(5, 2, n//3 + n%3),
    'ticket_promedio': np.random.normal(250, 50, n//3 + n%3),
    'antiguedad_meses': np.random.normal(6, 4, n//3 + n%3),
    'reclamos_mes': np.random.poisson(3, n//3 + n%3)
})

df = pd.concat([segment_a, segment_b, segment_c], ignore_index=True)
df['frecuencia_compra'] = df['frecuencia_compra'].clip(lower=1).round(0)
df['ticket_promedio'] = df['ticket_promedio'].clip(lower=10).round(2)
df['antiguedad_meses'] = df['antiguedad_meses'].clip(lower=1).round(0)
df['reclamos_mes'] = df['reclamos_mes'].clip(lower=0)

print(f"✅ Dataset generado: {len(df)} clientes")
print(f"   Features: {list(df.columns)}")
print(f"\n📊 Estadísticas:")
print(df.describe().round(2))
print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Clustering
# MAGIC %md
# MAGIC ## 📚 Teoría: Clustering y Segmentación
# MAGIC
# MAGIC ### 🎲 ¿Qué es el Aprendizaje No Supervisado?
# MAGIC
# MAGIC **Aprendizaje No Supervisado** encuentra patrones en datos SIN etiquetas predefinidas.
# MAGIC
# MAGIC ```
# MAGIC Aprendizaje Supervisado (Regresión/Clasificación):
# MAGIC   Datos + Etiquetas → Modelo → Predicción
# MAGIC
# MAGIC Aprendizaje No Supervisado (Clustering):
# MAGIC   Datos (sin etiquetas) → Modelo → Grupos/Segmentos
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 KMeans: El Algoritmo de Clustering
# MAGIC
# MAGIC **KMeans** agrupa datos en K clusters minimizando la distancia intra-cluster.
# MAGIC
# MAGIC ```
# MAGIC 1. Elegir K (número de clusters)
# MAGIC 2. Inicializar K centroides aleatoriamente
# MAGIC 3. Asignar cada punto al centroide más cercano
# MAGIC 4. Recalcular centroides como promedio del cluster
# MAGIC 5. Repetir 3-4 hasta convergencia
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📏 ¿Cuántos Clusters? Método del Codo
# MAGIC
# MAGIC ```python
# MAGIC inertias = []
# MAGIC for k in range(1, 11):
# MAGIC     kmeans = KMeans(n_clusters=k, random_state=42)
# MAGIC     kmeans.fit(X_scaled)
# MAGIC     inertias.append(kmeans.inertia_)
# MAGIC
# MAGIC # Graficar inertia vs K
# MAGIC # El "codo" indica el K óptimo
# MAGIC ```
# MAGIC
# MAGIC ### 📐 Silhouette Score
# MAGIC
# MAGIC Mide qué tan bien separados están los clusters:
# MAGIC * **-1 a 1**: 1 = clusters bien separados, 0 = solapados, -1 = asignación incorrecta
# MAGIC * **Fórmula:** (b - a) / max(a, b) donde a = distancia intra-cluster, b = distancia inter-cluster
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏷️ Interpretación de Segmentos
# MAGIC
# MAGIC | Segmento | Frecuencia | Ticket | Antigüedad | Reclamos | Perfil |
# MAGIC |----------|-----------|--------|------------|----------|--------|
# MAGIC | A | Alta | Alto | Larga | Bajos | VIP/Premium |
# MAGIC | B | Media | Medio | Media | Medios | Regular |
# MAGIC | C | Baja | Bajo | Corta | Altos | En riesgo |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Importancia del Escalado
# MAGIC
# MAGIC ```python
# MAGIC # KMeans usa distancias → features con mayor escala dominan
# MAGIC scaler = StandardScaler()
# MAGIC X_scaled = scaler.fit_transform(df[features])
# MAGIC # Ahora todas las features tienen media=0, std=1
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Segmentación en negocios:**
# MAGIC * 🎯 Marketing personalizado por segmento
# MAGIC * 💰 Pricing diferenciado por grupo
# MAGIC * 📧 Campañas dirigidas (email, SMS, push)
# MAGIC * 🏆 Programas de fidelización por nivel
# MAGIC * 📊 Análisis RFM (Recency, Frequency, Monetary)

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

print("💻 EXPERIMENTO: SEGMENTACIÓN CON KMEANS")
print("="*70)

# Usar dataset de la celda anterior
feature_cols = ['frecuencia_compra', 'ticket_promedio', 'antiguedad_meses', 'reclamos_mes']
X = df[feature_cols].values

# Escalar datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

mlflow.set_experiment("clustering_segmentacion_los_andes")

# Método del codo y silhouette
print("\n📊 Evaluando K de 2 a 8:")
scores = []
for k in range(2, 9):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    inertia = kmeans.inertia_
    sil = silhouette_score(X_scaled, labels)
    scores.append({'K': k, 'Inertia': inertia, 'Silhouette': sil})
    print(f"   K={k}: Inertia={inertia:.0f}, Silhouette={sil:.4f}")

# Entrenar modelo final con K óptimo (asumimos 3)
k_optimo = 3
with mlflow.start_run(run_name=f"kmeans_k{k_optimo}_v1"):
    mlflow.log_param("algorithm", "KMeans")
    mlflow.log_param("k", k_optimo)
    mlflow.log_param("features", ", ".join(feature_cols))
    
    kmeans_final = KMeans(n_clusters=k_optimo, random_state=42, n_init=10)
    df['segmento'] = kmeans_final.fit_predict(X_scaled)
    
    sil_final = silhouette_score(X_scaled, df['segmento'])
    mlflow.log_metric("silhouette", sil_final)
    mlflow.log_metric("inertia", kmeans_final.inertia_)
    mlflow.set_tag("dataset", "clientes_sinteticos")
    mlflow.sklearn.log_model(kmeans_final, "model")
    
    print(f"\n✅ Modelo KMeans entrenado (K={k_optimo})")
    print(f"   Silhouette: {sil_final:.4f}")
    
    # Perfiles de segmentos
    print(f"\n📊 PERFILES DE SEGMENTOS:")
    perfiles = df.groupby('segmento')[feature_cols].mean().round(2)
    perfiles['cantidad'] = df.groupby('segmento').size()
    print(perfiles)
    
    # Nombres de segmentos
    nombres = {0: 'VIP/Premium', 1: 'Regular', 2: 'En Riesgo'}
    df['nombre_segmento'] = df['segmento'].map(nombres)
    print(f"\n🏷️ Distribución:")
    for nombre in sorted(df['nombre_segmento'].unique()):
        count = (df['nombre_segmento'] == nombre).sum()
        print(f"   {nombre}: {count} clientes ({count/len(df)*100:.1f}%)")

print("\n" + "="*70)
print("✅ Segmentación completada con MLflow")

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 17_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Aprendizaje no supervisado (clustering):**
# MAGIC    - Sin etiquetas: el algoritmo encuentra patrones por si mismo
# MAGIC    - Agrupa datos similares en clusters sin supervisión
# MAGIC    - Útil para segmentación, anomaly detection y reducción de dimensionalidad
# MAGIC
# MAGIC 2. **KMeans — el algoritmo de clustering:**
# MAGIC    - `KMeans(n_clusters=K, random_state=42).fit(X_scaled)`
# MAGIC    - Minimiza distancia intra-cluster (puntos cercanos a su centroide)
# MAGIC    - Requiere escalar datos: `StandardScaler().fit_transform(X)`
# MAGIC    - K (número de clusters) debe definirse antes de entrenar
# MAGIC
# MAGIC 3. **Método del Codo y Silhouette:**
# MAGIC    - Elbow: graficar inertia vs K, el "codo" indica K óptimo
# MAGIC    - `silhouette_score(X, labels)` mide separación entre clusters (-1 a 1)
# MAGIC    - Silhouette > 0.5 = buena separación, < 0.2 = solapados
# MAGIC    - Combinar ambos métodos para validar la elección de K
# MAGIC
# MAGIC 4. **Interpretación de segmentos:**
# MAGIC    - `df.groupby('segmento')[features].mean()` — perfil de cada cluster
# MAGIC    - Nombrar segmentos por características dominantes (VIP, Regular, En Riesgo)
# MAGIC    - Traducir números a lenguaje de negocio para stakeholders
# MAGIC
# MAGIC 5. **Trackeo con MLflow:**
# MAGIC    - `mlflow.log_param("k", K)` — número de clusters
# MAGIC    - `mlflow.log_metric("silhouette", score)` — calidad del clustering
# MAGIC    - `mlflow.sklearn.log_model(kmeans, "model")` — guardar el modelo
# MAGIC    - Comparar diferentes K en la pestaña Experiments
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: SIEMPRE escalar antes de KMeans**
# MAGIC ```python
# MAGIC # MALO: sin escalar, features con mayor escala dominan las distancias
# MAGIC kmeans = KMeans(n_clusters=3)
# MAGIC kmeans.fit(df[['frecuencia', 'ticket_promedio', 'antiguedad']])
# MAGIC # ticket_promedio (25-800) domina sobre frecuencia (5-25)
# MAGIC
# MAGIC # BUENO: escalar todas las features a media=0, std=1
# MAGIC scaler = StandardScaler()
# MAGIC X_scaled = scaler.fit_transform(df[features])
# MAGIC kmeans = KMeans(n_clusters=3, random_state=42)
# MAGIC labels = kmeans.fit_predict(X_scaled)
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Validar K con Elbow Y Silhouette**
# MAGIC ```python
# MAGIC # MALO: elegir K arbitrariamente
# MAGIC kmeans = KMeans(n_clusters=5)  # ¿Por qué 5?
# MAGIC
# MAGIC # BUENO: evaluar multiples K y elegir el óptimo
# MAGIC for k in range(2, 9):
# MAGIC     kmeans = KMeans(n_clusters=k, random_state=42)
# MAGIC     labels = kmeans.fit_predict(X_scaled)
# MAGIC     sil = silhouette_score(X_scaled, labels)
# MAGIC     print(f"K={k}: Silhouette={sil:.4f}")
# MAGIC # Elegir K donde Silhouette es maximo y Elbow confirma
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Nombrar segmentos en lenguaje de negocio**
# MAGIC ```python
# MAGIC # MALO: entregar "Cluster 0, Cluster 1, Cluster 2" a stakeholders
# MAGIC print(df.groupby('segmento')[features].mean())
# MAGIC # Nadie entiende qué significa Cluster 0
# MAGIC
# MAGIC # BUENO: traducir a perfiles de negocio
# MAGIC nombres = {0: 'VIP/Premium', 1: 'Regular', 2: 'En Riesgo'}
# MAGIC df['nombre_segmento'] = df['segmento'].map(nombres)
# MAGIC print(df.groupby('nombre_segmento')[features].mean())
# MAGIC # "VIP/Premium: alta frecuencia, ticket alto, baja reclamos"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Escalar features antes de clustering | `StandardScaler().fit_transform(X)` |
# MAGIC | Determinar K óptimo | Elbow (inertia) + Silhouette Score |
# MAGIC | Entrenar KMeans | `KMeans(n_clusters=K, random_state=42).fit(X_scaled)` |
# MAGIC | Calidad del clustering | `silhouette_score(X, labels)` (> 0.5 = bueno) |
# MAGIC | Perfil de cada segmento | `df.groupby('segmento')[features].mean()` |
# MAGIC | Nombrar segmentos | `df['segmento'].map({0: 'VIP', 1: 'Regular', 2: 'Riesgo'})` |
# MAGIC | Comparar diferentes K | Loop + `mlflow.log_metric("silhouette", sil)` |
# MAGIC | Guardar modelo | `mlflow.sklearn.log_model(kmeans, "model")` |
# MAGIC | Datos no esféricos | DBSCAN o Gaussian Mixture (no KMeans) |
# MAGIC | Muchas dimensiones (> 20) | PCA antes de KMeans |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🎯 ¡Clustering y segmentación de clientes dominados!</h3>
# MAGIC   <p><i>"KMeans sin escalar es como comparar peras con manzanas: StandardScaler es el primer paso, no el opcional."</i></p>
# MAGIC </div>