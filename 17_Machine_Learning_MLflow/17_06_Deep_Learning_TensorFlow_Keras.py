# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🧠 Módulo 17 - Notebook 06: Deep Learning con TensorFlow y Keras
# MAGIC
# MAGIC ## 🤖 Redes neuronales para series temporales
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 17 - Machine Learning con MLflow  
# MAGIC **Duración estimada:** 80 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition  
# MAGIC **Nota:** Notebook opcional - Deep Learning requiere recursos adicionales
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Evaluar** viabilidad de TensorFlow/Keras en Databricks Free Edition  
# MAGIC ✅ **Entender** qué son las redes neuronales y LSTM  
# MAGIC ✅ **Preparar** secuencias temporales para deep learning  
# MAGIC ✅ **Construir** un modelo LSTM básico con Keras  
# MAGIC ✅ **Comparar** deep learning vs modelos tradicionales  
# MAGIC ✅ **Trackear** con MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Notebooks 17_01 al 17_05 completados
# MAGIC * ✅ Conocimiento de series de tiempo (Módulo 08)
# MAGIC * ✅ Conceptos básicos de redes neuronales (recomendado)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **TensorFlow y Keras** - Framework de deep learning
# MAGIC 2. **Redes Neuronales** - Concepto básico
# MAGIC 3. **LSTM** - Long Short-Term Memory para series temporales
# MAGIC 4. **Preparación de secuencias** - Usar `dl_sequences_lstm` de UC
# MAGIC 5. **Modelo LSTM básico** - Arquitectura y entrenamiento
# MAGIC 6. **Evaluación** - LSTM vs RandomForest vs LinearRegression
# MAGIC 7. **Viabilidad** - Análisis de limitaciones en Free Edition

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import mlflow
import pandas as pd
import numpy as np

print("💾 VERIFICACIÓN DE ENTORNO PARA DEEP LEARNING")
print("="*70)

# Verificar si TensorFlow está disponible
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TF_AVAILABLE = True
    print(f"✅ TensorFlow {tf.__version__} disponible")
    print(f"   Keras {keras.__version__}")
    print(f"   GPU disponible: {len(tf.config.list_physical_devices('GPU')) > 0}")
except ImportError:
    TF_AVAILABLE = False
    print("⚠️  TensorFlow no disponible en este entorno")
    print("   En Databricks Free Edition, TensorFlow puede no estar preinstalado")
    print("   Para instalarlo: %pip install tensorflow")
    print("\n   ℹ️  Este notebook es OPCIONAL y puede requerir configuración adicional")

# Cargar secuencias LSTM de Unity Catalog si existen
CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df_seq = spark.table(f"{CATALOG}.{SCHEMA}.dl_sequences_lstm").toPandas()
    print(f"\n✅ Secuencias LSTM cargadas: {len(df_seq)} secuencias")
    print(f"   Columnas: {list(df_seq.columns)}")
    SEQUENCES_AVAILABLE = True
except Exception as e:
    print(f"\n⚠️  Tabla dl_sequences_lstm no disponible: {e}")
    print("   Las secuencias se generan en 02_05_Preparacion_Datos_Empresariales")
    SEQUENCES_AVAILABLE = False

# Cargar datos de ventas para versión simplificada
try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"\n✅ Datos de ventas cargados: {len(df)} registros")
except Exception as e:
    np.random.seed(42)
    df = pd.DataFrame({
        'fecha': pd.date_range('2019-01-01', periods=300, freq='ME'),
        'sucursal_id': np.random.choice(['S001','S002','S003','S004','S005'], 300),
        'ventas': np.random.normal(50000, 15000, 300).round(2)
    })
    print(f"\n⚠️  Usando datos sintéticos: {len(df)} registros")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Deep Learning
# MAGIC %md
# MAGIC ## 📚 Teoría: Deep Learning y LSTM
# MAGIC
# MAGIC ### 🧠 ¿Qué es Deep Learning?
# MAGIC
# MAGIC **Deep Learning** es una rama del Machine Learning que usa redes neuronales artificiales con múltiples capas.
# MAGIC
# MAGIC ```
# MAGIC Entrada → [Capa 1] → [Capa 2] → [Capa 3] → Salida
# MAGIC   (features)   (ReLU)     (ReLU)    (Linear)   (predicción)
# MAGIC ```
# MAGIC
# MAGIC **vs Machine Learning tradicional:**
# MAGIC
# MAGIC | Aspecto | ML Tradicional (sklearn) | Deep Learning (TensorFlow) |
# MAGIC |---------|------------------------|---------------------------|
# MAGIC | Features | Manuales (feature engineering) | Automáticas (aprende representaciones) |
# MAGIC | Datos | Funciona con pocos | Necesita muchos |
# MAGIC | Hardware | CPU suficiente | GPU recomendada |
# MAGIC | Interpretabilidad | Alta | Baja (caja negra) |
# MAGIC | Mejor para | Tabular data | Imágenes, texto, series temporales |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 LSTM: Long Short-Term Memory
# MAGIC
# MAGIC **LSTM** es un tipo de red neuronal recurrente (RNN) diseñada para secuencias temporales.
# MAGIC
# MAGIC ```
# MAGIC Entrada: [Mes 1, Mes 2, ..., Mes 12]
# MAGIC            ↓     ↓          ↓
# MAGIC         [LSTM→LSTM→...→LSTM]  ← Memoria a largo plazo
# MAGIC            ↓
# MAGIC         [Dense Layer]
# MAGIC            ↓
# MAGIC Salida: Predicción Mes 13
# MAGIC ```
# MAGIC **Por qué LSTM para series temporales:**
# MAGIC * 📅 **Memoria:** Recuerda patrones de hace muchos períodos
# MAGIC * 🔄 **Secuencias:** Diseñada para datos ordenados temporalmente
# MAGIC * 📈 **Tendencias:** Captura tendencias y estacionalidad
# MAGIC * 🎯 **Forecasting:** Predice valores futuros basados en el pasado
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏗️ Arquitectura del Modelo
# MAGIC
# MAGIC ```python
# MAGIC model = Sequential([
# MAGIC     LSTM(50, activation='relu', input_shape=(12, 1)),  # 12 meses de historial
# MAGIC     Dropout(0.2),           # Regularización
# MAGIC     Dense(25, activation='relu'),  # Capa oculta
# MAGIC     Dense(1)                # Salida: 1 valor predictivo
# MAGIC ])
# MAGIC
# MAGIC model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# MAGIC model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Viabilidad en Databricks Free Edition
# MAGIC
# MAGIC **Limitaciones:**
# MAGIC * ❌ **Sin GPU:** TensorFlow funciona en CPU pero más lento
# MAGIC * ❌ **Memoria limitada:** Modelos grandes pueden agotar recursos
# MAGIC * ⚠️ **No preinstalado:** Puede requerir `%pip install tensorflow`
# MAGIC * ✅ **Funciona para:** Modelos pequeños, experimentación, aprendizaje
# MAGIC
# MAGIC **Recomendación:**
# MAGIC * Usar TensorFlow para experimentación y aprendizaje
# MAGIC * Para producción, considerar modelos más simples (RandomForest, XGBoost)
# MAGIC * El notebook es OPCIONAL y puede requerir ajustes según el entorno
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Deep Learning en negocios:**
# MAGIC * 📈 **Forecasting avanzado:** Predicción de ventas con mayor precisión
# MAGIC * 🤖 **NLP:** Análisis de sentimientos, chatbots
# MAGIC * 🖼️ **Visión:** Clasificación de imágenes, OCR
# MAGIC * 🎯 **Recomendaciones:** Sistemas de recomendación personalizados
# MAGIC * 📊 **Detección de anomalías:** Fraude, outliers complejos

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import mlflow
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("💻 EXPERIMENTO: DEEP LEARNING CON TENSORFLOW/KERAS")
print("="*70)

# Verificar TensorFlow
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from sklearn.preprocessing import MinMaxScaler
    TF_AVAILABLE = True
    print(f"✅ TensorFlow {tf.__version__} disponible")
except ImportError:
    TF_AVAILABLE = False
    print("⚠️  TensorFlow no disponible")
    print("   Para instalar: %pip install tensorflow")
    print("   Este notebook es OPCIONAL")
    print("\n" + "="*70)
    print("✅ Teoría de Deep Learning revisada - Notebook opcional")
    raise SystemExit

# Preparar datos para LSTM (versión simplificada)
df_sorted = df.sort_values('fecha').copy()
ventas = df_sorted['ventas'].values.reshape(-1, 1)

# Normalizar
scaler = MinMaxScaler(feature_range=(0, 1))
ventas_scaled = scaler.fit_transform(ventas)

# Crear secuencias (12 meses de historial → predecir mes 13)
def create_sequences(data, seq_length=12):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length), 0])
        y.append(data[i + seq_length, 0])
    return np.array(X), np.array(y)

X, y = create_sequences(ventas_scaled, seq_length=12)
X = X.reshape((X.shape[0], X.shape[1], 1))  # [samples, timesteps, features]

# Split train/test
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"\n📊 Datos preparados para LSTM:")
print(f"   Secuencias totales: {len(X)}")
print(f"   Train: {len(X_train)}, Test: {len(X_test)}")
print(f"   Forma X_train: {X_train.shape}")

mlflow.set_experiment("deep_learning_lstm_los_andes")

# Entrenar modelo LSTM
with mlflow.start_run(run_name="lstm_v1"):
    mlflow.log_param("model", "LSTM")
    mlflow.log_param("seq_length", 12)
    mlflow.log_param("epochs", 30)
    mlflow.log_param("batch_size", 16)
    
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(12, 1)),
        Dropout(0.2),
        Dense(25, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    history = model.fit(
        X_train, y_train,
        epochs=30,
        batch_size=16,
        validation_split=0.2,
        verbose=0
    )
    
    # Evaluar
    predictions = model.predict(X_test, verbose=0)
    predictions = scaler.inverse_transform(predictions)
    y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    rmse = np.sqrt(np.mean((y_test_real - predictions) ** 2))
    mae = np.mean(np.abs(y_test_real - predictions))
    
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)
    mlflow.set_tag("model_type", "LSTM")
    mlflow.set_tag("framework", "TensorFlow/Keras")
    
    print(f"\n✅ LSTM entrenado (30 epochs)")
    print(f"   RMSE: {rmse:,.2f}")
    print(f"   MAE:  {mae:,.2f}")
    print(f"   Loss final: {history.history['loss'][-1]:.6f}")
    
    print(f"\n🔮 Predicciones vs Real (primeros 5):")
    for i in range(min(5, len(y_test_real))):
        print(f"   Real: ${y_test_real[i][0]:,.2f} → Predicho: ${predictions[i][0]:,.2f}")

print("\n" + "="*70)
print("✅ Deep Learning con TensorFlow/Keras completado")
print("   📌 Notebook OPCIONAL - Requiere TensorFlow instalado")
print("   📌 Compare estos resultados con RandomForest del Notebook 17_02")

# COMMAND ----------

# DBTITLE 1,🧠 Teoría: Deep Learning con datos reales
# MAGIC %md
# MAGIC ## 🧠 Deep Learning aplicado a Los Andes Market
# MAGIC
# MAGIC ### 📈 LSTM para forecasting de ventas
# MAGIC
# MAGIC Con una red LSTM podemos intentar predecir las ventas mensuales de **Los Andes Market** usando los últimos 12 meses como ventana:
# MAGIC
# MAGIC ```python
# MAGIC # Formato LSTM: (samples, timesteps=12, features=1)
# MAGIC # Entrada: [ventas mes 1, mes 2, ..., mes 12]
# MAGIC # Salida: predicción mes 13
# MAGIC model = Sequential([LSTM(50, input_shape=(12, 1)), Dense(1)])
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Consideraciones
# MAGIC * LSTM requiere normalización (`MinMaxScaler`)
# MAGIC * Si TensorFlow no está disponible → `%pip install tensorflow`
# MAGIC * En Free Edition puede ser lento (CPU sin GPU)
# MAGIC * Comparar LSTM vs RandomForest para justificar complejidad

# COMMAND ----------

# DBTITLE 1,🧠 Práctica: Deep Learning con datos reales
import mlflow
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("🧠 DEEP LEARNING CON DATOS REALES DE LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and df is not None:
    # Verificar TensorFlow
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        TF_OK = True
        print(f"✅ TensorFlow {tf.__version__} disponible")
    except ImportError:
        TF_OK = False
        print("⚠️  TensorFlow no disponible. Instalar con: %pip install tensorflow")

    print("\n1️⃣  PREPARAR SECUENCIAS DESDE VENTAS REALES")
    print("-"*70)

    # Agregar ventas totales mensuales
    ventas_mensuales = df.groupby('fecha')['ventas'].sum().sort_index()
    print(f"   Período: {ventas_mensuales.index[0].strftime('%Y-%m')} a {ventas_mensuales.index[-1].strftime('%Y-%m')}")
    print(f"   Total de meses: {len(ventas_mensuales)}")

    # Normalizar
    scaler = MinMaxScaler(feature_range=(0, 1))
    ventas_scaled = scaler.fit_transform(ventas_mensuales.values.reshape(-1, 1))

    # Crear secuencias (12 meses → predecir mes 13)
    SEQ_LEN = 12
    X, y = [], []
    for i in range(len(ventas_scaled) - SEQ_LEN):
        X.append(ventas_scaled[i:i+SEQ_LEN, 0])
        y.append(ventas_scaled[i+SEQ_LEN, 0])
    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    print(f"   Secuencias: {len(X)} (train={len(X_train)}, test={len(X_test)})")
    print(f"   Forma X: {X.shape} (samples, timesteps=12, features=1)")

    print("\n" + "="*70)
    print("\n2️⃣  ENTRENAR LSTM CON MLFLOW TRACKING")
    print("-"*70)

    if TF_OK:
        mlflow.set_experiment("lstm_ventas_los_andes")

        with mlflow.start_run(run_name="lstm_v1"):
            mlflow.log_param("model", "LSTM")
            mlflow.log_param("seq_len", SEQ_LEN)
            mlflow.log_param("layers", "LSTM(50)+Dense(25)+Dense(1)")
            mlflow.log_param("epochs", 30)
            mlflow.log_param("batch_size", 16)

            model = Sequential([
                LSTM(50, activation='relu', input_shape=(SEQ_LEN, 1)),
                Dropout(0.2),
                Dense(25, activation='relu'),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])

            history = model.fit(X_train, y_train, epochs=30, batch_size=16,
                               validation_split=0.2, verbose=0)

            preds_scaled = model.predict(X_test, verbose=0)
            preds = scaler.inverse_transform(preds_scaled).flatten()
            y_real = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

            rmse = np.sqrt(mean_squared_error(y_real, preds))
            r2 = r2_score(y_real, preds)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)

            print(f"   ✅ LSTM entrenado (30 epochs)")
            print(f"   RMSE: ${rmse:,.0f}")
            print(f"   R²: {r2:.4f}")
            print(f"\n   Predicciones vs Reales (últimos {len(y_real)} meses):")
            for i in range(min(len(y_real), 6)):
                print(f"      Real: ${y_real[i]:,.0f} | Predicho: ${preds[i]:,.0f}")
    else:
        print("   ⏭️  TensorFlow no disponible — saltando entrenamiento LSTM")
        print("   💡 Instalar con: %pip install tensorflow")

    print("\n" + "="*70)
    print("\n3️⃣  COMPARACIÓN: LSTM vs Modelos Tradicionales")
    print("-"*70)
    print("\n   | Modelo          | Ventajas                    | Complejidad |")
    print("   |-----------------|----------------------------|-------------|")
    print("   | LinearRegression| Simple, interpretable       | Baja        |")
    print("   | RandomForest    | Robusto, no lineal          | Media       |")
    print("   | LSTM            | Memoria temporal, secuencias| Alta        |")
    print("\n   💡 Para datasets pequeños, RandomForest puede superar a LSTM")
    print("   💡 LSTM brilla con grandes volúmenes de datos temporales")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 17_06
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Deep Learning vs ML tradicional:**
# MAGIC    ```python
# MAGIC    # ML tradicional (sklearn): feature engineering manual
# MAGIC    model = RandomForestRegressor(n_estimators=100)
# MAGIC    model.fit(X_train, y_train)  # Features pre-calculadas
# MAGIC    
# MAGIC    # Deep Learning (TensorFlow): aprende representaciones
# MAGIC    model = Sequential([LSTM(50, input_shape=(12, 1)), Dense(1)])
# MAGIC    model.fit(X_train, y_train)  # Aprende features automaticamente
# MAGIC    ```
# MAGIC
# MAGIC 2. **Arquitectura LSTM para series temporales:**
# MAGIC    ```python
# MAGIC    model = Sequential([
# MAGIC        LSTM(50, activation='relu', input_shape=(12, 1)),  # 12 meses de historial
# MAGIC        Dropout(0.2),           # Regularizacion (evita overfitting)
# MAGIC        Dense(25, activation='relu'),  # Capa oculta
# MAGIC        Dense(1)                # Salida: 1 valor predictivo
# MAGIC    ])
# MAGIC    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# MAGIC    model.fit(X_train, y_train, epochs=30, batch_size=16, validation_split=0.2)
# MAGIC    ```
# MAGIC
# MAGIC 3. **Preparacion de secuencias 3D para LSTM:**
# MAGIC    ```python
# MAGIC    # Formato requerido: (samples, timesteps, features)
# MAGIC    X = X.reshape((X.shape[0], X.shape[1], 1))  # [samples, 12, 1]
# MAGIC    
# MAGIC    # MinMaxScaler obligatorio antes de LSTM
# MAGIC    scaler = MinMaxScaler(feature_range=(0, 1))
# MAGIC    ventas_scaled = scaler.fit_transform(ventas)
# MAGIC    
# MAGIC    # Desnormalizar predicciones al evaluar
# MAGIC    predictions = scaler.inverse_transform(predictions)
# MAGIC    ```
# MAGIC
# MAGIC 4. **MLflow tracking para deep learning:**
# MAGIC    ```python
# MAGIC    with mlflow.start_run(run_name="lstm_v1"):
# MAGIC        mlflow.log_param("model", "LSTM")
# MAGIC        mlflow.log_param("seq_length", 12)
# MAGIC        mlflow.log_param("epochs", 30)
# MAGIC        mlflow.log_metric("rmse", rmse)
# MAGIC        mlflow.log_metric("mae", mae)
# MAGIC        mlflow.set_tag("framework", "TensorFlow/Keras")
# MAGIC    ```
# MAGIC
# MAGIC 5. **Viabilidad en Databricks Free Edition:**
# MAGIC    - Sin GPU: TensorFlow funciona en CPU pero mas lento
# MAGIC    - Memoria limitada: modelos pequenos si, grandes no
# MAGIC    - No preinstalado: requiere `%pip install tensorflow`
# MAGIC    - Recomendacion: experimentacion si, produccion usar RandomForest/XGBoost
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de LSTM con Keras
# MAGIC
# MAGIC **Caso 1: Arquitectura basica LSTM**
# MAGIC ```python
# MAGIC model = Sequential([
# MAGIC     LSTM(50, activation='relu', input_shape=(12, 1)),
# MAGIC     Dropout(0.2),
# MAGIC     Dense(1)
# MAGIC ])
# MAGIC model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: Preparar secuencias 3D**
# MAGIC ```python
# MAGIC def create_sequences(data, seq_length=12):
# MAGIC     X, y = [], []
# MAGIC     for i in range(len(data) - seq_length):
# MAGIC         X.append(data[i:(i + seq_length), 0])
# MAGIC         y.append(data[i + seq_length, 0])
# MAGIC     return np.array(X), np.array(y)
# MAGIC
# MAGIC X = X.reshape((X.shape[0], X.shape[1], 1))  # (samples, 12, 1)
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: Entrenar con EarlyStopping**
# MAGIC ```python
# MAGIC from tensorflow.keras.callbacks import EarlyStopping
# MAGIC early = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
# MAGIC model.fit(X_train, y_train, epochs=50, batch_size=16,
# MAGIC          validation_split=0.2, callbacks=[early], verbose=0)
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Evaluar y desnormalizar**
# MAGIC ```python
# MAGIC predictions = model.predict(X_test, verbose=0)
# MAGIC predictions = scaler.inverse_transform(predictions)
# MAGIC y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))
# MAGIC rmse = np.sqrt(np.mean((y_test_real - predictions) ** 2))
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Comparar LSTM vs RandomForest**
# MAGIC ```python
# MAGIC # LSTM: mejor para patrones temporales complejos (estacionalidad, memoria larga)
# MAGIC # RandomForest: mejor para datos tabulares con features pre-calculadas
# MAGIC # Linea base: LinearRegression (todo modelo debe superarla)
# MAGIC # Ordenar por RMSE en MLflow Experiments y seleccionar el mejor
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 Resumen del Módulo 17
# MAGIC
# MAGIC **Aprendiste:**
# MAGIC
# MAGIC 1. **17_01 - MLflow y Experimentos:** Tracking, parametros, metricas, autolog
# MAGIC 2. **17_02 - Regresion Prediccion Ventas:** LinearRegression, RandomForest, GradientBoosting, RMSE/MAE/R2
# MAGIC 3. **17_03 - Clasificacion Churn Clientes:** LogisticRegression, DecisionTree, RandomForest, Precision/Recall/F1/ROC-AUC
# MAGIC 4. **17_04 - Clustering Segmentacion Clientes:** KMeans, Elbow, Silhouette, StandardScaler
# MAGIC 5. **17_05 - Model Registry y Serving:** register_model, stages, batch scoring, Unity Catalog
# MAGIC 6. **17_06 - Deep Learning TensorFlow Keras:** LSTM, secuencias 3D, Keras, viabilidad Free Edition
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Trackear experimentos ML con MLflow
# MAGIC * ✅ Entrenar y comparar modelos de regresion y clasificacion
# MAGIC * ✅ Segmentar clientes con clustering no supervisado
# MAGIC * ✅ Versionar y desplegar modelos con Model Registry
# MAGIC * ✅ Construir redes neuronales LSTM para series temporales
# MAGIC * ✅ Evaluar viabilidad de deep learning segun entorno
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🧠 ¡Módulo 17 Completado!</h3>
# MAGIC   <p><i>"Dominas Machine Learning con MLflow: desde experimentos basicos hasta deep learning con LSTM. Ahora puedes construir, trackear y desplegar modelos profesionales."</i></p>
# MAGIC </div>