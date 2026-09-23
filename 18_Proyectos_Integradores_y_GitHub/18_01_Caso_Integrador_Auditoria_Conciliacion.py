# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # ⚡ Módulo 18 - Notebook 01: Caso Integrador - Auditoría y conciliación
# MAGIC
# MAGIC ## 📊 Proyecto End-to-End de auditoría automatizada
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 18 - Proyectos Integradores y GitHub  
# MAGIC **Duración estimada:** 90 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Desarrollar** un proyecto completo de auditoría  
# MAGIC ✅ **Aplicar** técnicas de conciliación automatizada  
# MAGIC ✅ **Detectar** inconsistencias y anomalías  
# MAGIC ✅ **Generar** reportes ejecutivos  
# MAGIC ✅ **Integrar** Pandas, SQL, PySpark y MLflow
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Todos los módulos 01-17 completados
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. Caso de Negocio: Auditoría de Ventas
# MAGIC 2. Carga y Validación de Datos
# MAGIC 3. Conciliación de Registros
# MAGIC 4. Detección de Anomalías (Z-score, IQR)
# MAGIC 5. Ley de Benford para Fraude
# MAGIC 6. Reporte de Hallazgos con Dashboards

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd
import numpy as np
from datetime import datetime

print("💾 CARGANDO DATOS PARA AUDITORÍA")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Datos cargados: {len(df)} registros")
    print(f"   Sucursales: {df['sucursal_id'].nunique()}")
    print(f"   Ventas totales: ${df['ventas'].sum():,.2f}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Auditoría
# MAGIC %md
# MAGIC ## 📚 Teoría: Auditoría Automatizada
# MAGIC
# MAGIC ### 🔍 ¿Qué es Auditoría Automatizada?
# MAGIC
# MAGIC Uso de herramientas de análisis de datos para verificar registros y detectar inconsistencias con cobertura 100%.
# MAGIC
# MAGIC | Manual | Automatizada |
# MAGIC |--------|-------------|
# MAGIC | Muestreo (5-10%) | Cobertura 100% |
# MAGIC | Días/Semanas | Horas |
# MAGIC | Propenso a errores | Preciso y reproducible |
# MAGIC | Reactivo | Proactivo |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Técnicas de Auditoría
# MAGIC
# MAGIC **1. Conciliación:** Comparar dos fuentes que deberían coincidir (pd.merge con indicator)
# MAGIC
# MAGIC **2. Detección de Anomalías:** Z-score > 3 o IQR para encontrar outliers
# MAGIC
# MAGIC **3. Ley de Benford:** En datos naturales, el primer dígito sigue una distribución predecible. Desviaciones indican posible fraude.
# MAGIC
# MAGIC **4. Duplicados:** Transacciones idénticas o similares (posible fraude)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC * ⏱️ Tiempo: de semanas a horas
# MAGIC * 🎯 Precisión: 100% de cobertura
# MAGIC * 🔍 Detección: patrones imposibles manualmente
# MAGIC * 💰 ROI: fraudes detectados valen millones

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("💻 PROYECTO: AUDITORÍA AUTOMATIZADA")
print("="*70)

if USAR_DATOS_REALES:
    # 1. Verificación de integridad
    print("\n1️⃣ INTEGRIDAD DE DATOS:")
    print(f"   Nulos en ventas: {df['ventas'].isnull().sum()}")
    print(f"   Duplicados: {df.duplicated().sum()}")
    print(f"   Registros: {len(df)}")

    # 2. Detección de outliers (Z-score)
    print("\n2️⃣ DETECCIÓN DE ANOMALÍAS (Z-score > 2):")
    z_scores = np.abs(stats.zscore(df['ventas']))
    outliers_z = df[z_scores > 2]
    print(f"   Outliers encontrados: {len(outliers_z)}")
    if len(outliers_z) > 0:
        print(outliers_z[['sucursal_id', 'fecha', 'ventas']].to_string())

    # 3. Detección de outliers (IQR)
    print("\n3️⃣ DETECCIÓN IQR:")
    Q1, Q3 = df['ventas'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    outliers_iqr = df[(df['ventas'] < Q1 - 1.5*IQR) | (df['ventas'] > Q3 + 1.5*IQR)]
    print(f"   Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
    print(f"   Outliers IQR: {len(outliers_iqr)}")

    # 4. Estadísticas por sucursal
    print("\n4️⃣ RESUMEN POR SUCURSAL:")
    resumen = df.groupby('sucursal_id')['ventas'].agg(['count', 'sum', 'mean', 'std']).round(2)
    print(resumen)

    # 5. Análisis de tendencias sospechosas
    print("\n5️⃣ VARIACIONES MENSUALES SOSPECHOSAS:")
    df_sorted = df.sort_values(['sucursal_id', 'fecha'])
    df_sorted['crecimiento_pct'] = df_sorted.groupby('sucursal_id')['ventas'].pct_change() * 100
    sospechosas = df_sorted[abs(df_sorted['crecimiento_pct']) > 50]
    if len(sospechosas) > 0:
        print(f"   Variaciones > 50%: {len(sospechosas)} casos")
        print(sospechosas[['sucursal_id', 'fecha', 'ventas', 'crecimiento_pct']].to_string())
    else:
        print("   No se detectaron variaciones sospechosas")

    print(f"\n✅ Auditoría completada: {len(df)} registros analizados")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 18_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Auditoría automatizada — cobertura 100%:**
# MAGIC    - De muestreo manual (5-10%) a análisis completo de todos los registros
# MAGIC    - Reproducible: mismo dataset → mismos hallazgos, sin sesgo humano
# MAGIC    - Tiempo: de semanas a horas con código automatizado
# MAGIC
# MAGIC 2. **Conciliación de registros:**
# MAGIC    - `pd.merge(df_libro, df_banco, how='outer', indicator=True)` — detectar diferencias
# MAGIC    - `_merge` column: `both` (coinciden), `left_only` (solo libro), `right_only` (solo banco)
# MAGIC    - Tolerancia de diferencias: absoluta ($1) y porcentual (0.5%)
# MAGIC
# MAGIC 3. **Detección de anomalías:**
# MAGIC    - **Z-score:** `np.abs(stats.zscore(df['ventas'])) > 2` — desviaciones estándar
# MAGIC    - **IQR:** `Q1 - 1.5×IQR` a `Q3 + 1.5×IQR` — rango intercuartílico
# MAGIC    - **Variaciones sospechosas:** `pct_change() > 50%` — saltos mensuales atípicos
# MAGIC
# MAGIC 4. **Ley de Benford para fraude:**
# MAGIC    - En datos naturales, el primer dígito sigue una distribución predecible
# MAGIC    - 1 aparece ~30% de las veces, 9 solo ~5%
# MAGIC    - Desviaciones significativas = posible manipulación o fraude
# MAGIC
# MAGIC 5. **Reporte ejecutivo integrado:**
# MAGIC    - KPIs de auditoría: registros analizados, anomalías detectadas, tasa de conciliación
# MAGIC    - Dashboard con hallazgos clasificados por severidad
# MAGIC    - Exportar partidas no conciliadas para investigación manual
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Auditoría 100% de cobertura, no muestreo**
# MAGIC ```python
# MAGIC # MALO: auditar solo una muestra aleatoria
# MAGIC muestra = df.sample(frac=0.1)  # 10% de los registros
# MAGIC auditar(muestra)  # 90% sin revisar
# MAGIC
# MAGIC # BUENO: analizar todos los registros
# MAGIC z_scores = np.abs(stats.zscore(df['ventas']))
# MAGIC outliers = df[z_scores > 2]  # 100% de cobertura
# MAGIC print(f"Outliers: {len(outliers)} de {len(df)} registros")
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Combinar Z-score e IQR para detectar outliers**
# MAGIC ```python
# MAGIC # MALO: solo Z-score (sensible a valores extremos que distorsionan media)
# MAGIC outliers = df[np.abs(stats.zscore(df['ventas'])) > 2]
# MAGIC
# MAGIC # BUENO: combinar ambos métodos para mayor robustez
# MAGIC outliers_z = df[np.abs(stats.zscore(df['ventas'])) > 2]
# MAGIC Q1, Q3 = df['ventas'].quantile([0.25, 0.75])
# MAGIC IQR = Q3 - Q1
# MAGIC outliers_iqr = df[(df['ventas'] < Q1 - 1.5*IQR) | (df['ventas'] > Q3 + 1.5*IQR)]
# MAGIC outliers_total = pd.concat([outliers_z, outliers_iqr]).drop_duplicates()
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Documentar hallazgos con severidad clasificada**
# MAGIC ```python
# MAGIC # MALO: lista de anomalías sin contexto ni prioridad
# MAGIC print(outliers[['sucursal_id', 'ventas']])  # No accionable
# MAGIC
# MAGIC # BUENO: clasificar por severidad para priorizar investigación
# MAGIC df['severidad'] = 'Normal'
# MAGIC df.loc[np.abs(stats.zscore(df['ventas'])) > 2, 'severidad'] = '⚠️ Moderada'
# MAGIC df.loc[np.abs(stats.zscore(df['ventas'])) > 3, 'severidad'] = '🔴 Crítica'
# MAGIC hallazgos = df[df['severidad'] != 'Normal'].sort_values('ventas', ascending=False)
# MAGIC print(hallazgos[['sucursal_id', 'fecha', 'ventas', 'severidad']])
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Conciliar dos fuentes | `pd.merge(df1, df2, how='outer', indicator=True)` |
# MAGIC | Detectar outliers estadísticos | `np.abs(stats.zscore(df['col'])) > 2` |
# MAGIC | Detectar outliers robustos | IQR: `Q1 - 1.5×IQR` a `Q3 + 1.5×IQR` |
# MAGIC | Variaciones sospechosas mensuales | `df.groupby('sucursal')['ventas'].pct_change() > 50%` |
# MAGIC | Posible fraude (primer dígito) | Ley de Benford: comparar frecuencia observada vs esperada |
# MAGIC | Duplicados exactos | `df.duplicated().sum()` |
# MAGIC | Duplicados por clave | `df.duplicated(subset=['fecha', 'sucursal_id']).sum()` |
# MAGIC | Nulos por columna | `df.isnull().sum()` |
# MAGIC | Reporte de hallazgos | Clasificar por severidad (Normal/Moderada/Crítica) |
# MAGIC | Exportar partidas no conciliadas | `df_no_conciliado.to_csv('hallazgos.csv')` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🔍 ¡Auditoría y conciliación automatizada dominada!</h3>
# MAGIC   <p><i>"La auditoría automatizada no reemplaza al auditor: le da superpoderes para ver lo que ningún ojo humano podría."</i></p>
# MAGIC </div>