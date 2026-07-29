# Databricks notebook source
# DBTITLE 1,Portada del Módulo
# MAGIC %md
# MAGIC # Saliendo de lo Pandito v4
# MAGIC ## Módulo 00: Generación de Código PySpark y SQL con IA
# MAGIC
# MAGIC ### 📘 Objetivos de Este Notebook:
# MAGIC 1. Generar **código PySpark desde cero** con Genie Code
# MAGIC 2. **Migrar de Pandas a PySpark** automáticamente
# MAGIC 3. Optimizar **consultas SQL** complejas con IA
# MAGIC 4. Dominar **patrones de ETL** comunes
# MAGIC 5. Aprender a **revisar y validar** código generado por IA
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 ¿Por Qué Este Notebook?
# MAGIC
# MAGIC **El desafío de Big Data:**
# MAGIC - PySpark tiene sintaxis diferente a Pandas
# MAGIC - SQL optimizado requiere conocimiento avanzado
# MAGIC - ETL pipelines son complejos y propensos a errores
# MAGIC
# MAGIC **Con Genie Code:**
# MAGIC - Genera código distribuido sin memorizar APIs
# MAGIC - Traduce Pandas a PySpark instantáneamente
# MAGIC - Optimiza SQL automáticamente
# MAGIC - Acelera desarrollo de pipelines 10x
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Regla de Oro
# MAGIC
# MAGIC > **"Genie genera, tú validas"**
# MAGIC > 
# MAGIC > Siempre revisa el código generado:
# MAGIC > * ¿Hace lo que necesitas?
# MAGIC > * ¿Es eficiente?
# MAGIC > * ¿Entiendes cómo funciona?
# MAGIC >
# MAGIC > Genie es un copiloto, no un autopiloto.

# COMMAND ----------

# DBTITLE 1,Generación de Código PySpark
# MAGIC %md
# MAGIC ## ⚡ Generación de Código PySpark desde Cero
# MAGIC
# MAGIC ### 📝 Patrón de Prompt para PySpark
# MAGIC
# MAGIC ```
# MAGIC "Genera código PySpark que:
# MAGIC 1. [ENTRADA DE DATOS] - de dónde leer
# MAGIC 2. [TRANSFORMACIONES] - qué operaciones aplicar
# MAGIC 3. [AGREGACIONES] - qué cálculos hacer
# MAGIC 4. [SALIDA] - formato y destino del resultado
# MAGIC
# MAGIC Compatible con Databricks Serverless."
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Ejemplos de Prompts Efectivos
# MAGIC
# MAGIC #### Ejemplo 1: Lectura y Filtrado
# MAGIC ```
# MAGIC Prompt:
# MAGIC "Lee un archivo CSV desde /Volumes/main/default/ventas/ventas_2024.csv
# MAGIC Filtra filas donde region = 'LATAM' y revenue > 1000
# MAGIC Muestra las primeras 10 filas"
# MAGIC
# MAGIC Genie genera:
# MAGIC ```
# MAGIC
# MAGIC ```python
# MAGIC from pyspark.sql.functions import col
# MAGIC
# MAGIC df = (spark.read
# MAGIC     .option("header", "true")
# MAGIC     .option("inferSchema", "true")
# MAGIC     .csv("/Volumes/main/default/ventas/ventas_2024.csv")
# MAGIC )
# MAGIC
# MAGIC df_filtrado = df.filter(
# MAGIC     (col("region") == "LATAM") & 
# MAGIC     (col("revenue") > 1000)
# MAGIC )
# MAGIC
# MAGIC df_filtrado.show(10)
# MAGIC ```
# MAGIC
# MAGIC #### Ejemplo 2: Agregación y Window Functions
# MAGIC ```
# MAGIC Prompt:
# MAGIC "Desde la tabla catalog.schema.transacciones:
# MAGIC 1. Agrupa por cliente_id y fecha
# MAGIC 2. Calcula: total_compras, ticket_promedio, num_transacciones
# MAGIC 3. Añade ranking por total_compras (descendente) dentro de cada fecha
# MAGIC 4. Filtra solo top 10 clientes por día"
# MAGIC
# MAGIC Genie genera:
# MAGIC ```
# MAGIC
# MAGIC ```python
# MAGIC from pyspark.sql import Window
# MAGIC from pyspark.sql.functions import col, sum, avg, count, row_number
# MAGIC
# MAGIC df = spark.table("catalog.schema.transacciones")
# MAGIC
# MAGIC df_agg = df.groupBy("cliente_id", "fecha").agg(
# MAGIC     sum("monto").alias("total_compras"),
# MAGIC     avg("monto").alias("ticket_promedio"),
# MAGIC     count("*").alias("num_transacciones")
# MAGIC )
# MAGIC
# MAGIC window_spec = Window.partitionBy("fecha").orderBy(col("total_compras").desc())
# MAGIC
# MAGIC df_ranked = df_agg.withColumn(
# MAGIC     "ranking",
# MAGIC     row_number().over(window_spec)
# MAGIC )
# MAGIC
# MAGIC df_top10 = df_ranked.filter(col("ranking") <= 10)
# MAGIC
# MAGIC display(df_top10)
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Ejercicio 1: Generar PySpark
# 💻 EJERCICIO 1: Genera tu Primer Código PySpark

print("🎯 EJERCICIO: Genera código PySpark con Genie")
print("="*60)
print("\n👉 Prompt sugerido para Genie:")
print()
print('"Crea un DataFrame PySpark de ejemplo con:')
print('- 1000 filas')
print('- Columnas: user_id (entero), fecha (dates en enero 2024),')
print('  producto (A/B/C/D), cantidad (1-10), precio (10-1000)')
print('- Calcula revenue = cantidad * precio')
print('- Agrupa por producto y calcula:')
print('  * revenue total')
print('  * cantidad promedio')
print('  * número de transacciones')
print('- Ordena por revenue descendente')
print('- Muestra resultado')
print('"')
print("\n" + "="*60)
print("👇 Pega el código generado abajo y ejécutalo")

# COMMAND ----------

# DBTITLE 1,Migración Pandas a PySpark
# MAGIC %md
# MAGIC ## 🔄 Migración de Pandas a PySpark
# MAGIC
# MAGIC ### 🎯 El Desafío
# MAGIC
# MAGIC Tienes código Pandas que funciona en 100K filas, pero necesitas escalarlo a 100M filas.
# MAGIC
# MAGIC **Problema:** Reescribir manualmente toma horas y es propenso a errores.
# MAGIC
# MAGIC **Solución:** Genie traduce automáticamente.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Patrón de Prompt de Migración
# MAGIC
# MAGIC ```
# MAGIC "Convierte este código Pandas a PySpark:
# MAGIC
# MAGIC [PEGAR CÓDIGO PANDAS]
# MAGIC
# MAGIC Requisitos:
# MAGIC - Compatible con Databricks Serverless
# MAGIC - Optimizado para grandes volúmenes
# MAGIC - Mantener la lógica de negocio exacta
# MAGIC - Agregar comentarios explicativos"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Ejemplo de Migración
# MAGIC
# MAGIC #### 🐼 Código Pandas Original
# MAGIC ```python
# MAGIC import pandas as pd
# MAGIC
# MAGIC df = pd.read_csv('ventas.csv')
# MAGIC
# MAGIC # Filtrar
# MAGIC df_filtrado = df[df['region'] == 'LATAM']
# MAGIC
# MAGIC # Crear columna calculada
# MAGIC df_filtrado['revenue'] = df_filtrado['cantidad'] * df_filtrado['precio']
# MAGIC
# MAGIC # Agrupar
# MAGIC resumen = df_filtrado.groupby('producto').agg({
# MAGIC     'revenue': 'sum',
# MAGIC     'cantidad': 'mean',
# MAGIC     'user_id': 'count'
# MAGIC }).reset_index()
# MAGIC
# MAGIC # Renombrar columnas
# MAGIC resumen.columns = ['producto', 'revenue_total', 'cantidad_promedio', 'num_ventas']
# MAGIC
# MAGIC # Ordenar
# MAGIC resumen = resumen.sort_values('revenue_total', ascending=False)
# MAGIC ```
# MAGIC
# MAGIC #### ⚡ Código PySpark Generado por Genie
# MAGIC ```python
# MAGIC from pyspark.sql.functions import col, sum, avg, count
# MAGIC
# MAGIC # Leer datos
# MAGIC df = (spark.read
# MAGIC     .option("header", "true")
# MAGIC     .option("inferSchema", "true")
# MAGIC     .csv("/Volumes/main/default/ventas.csv")
# MAGIC )
# MAGIC
# MAGIC # Filtrar
# MAGIC df_filtrado = df.filter(col("region") == "LATAM")
# MAGIC
# MAGIC # Crear columna calculada
# MAGIC df_con_revenue = df_filtrado.withColumn(
# MAGIC     "revenue",
# MAGIC     col("cantidad") * col("precio")
# MAGIC )
# MAGIC
# MAGIC # Agrupar y agregar
# MAGIC resumen = df_con_revenue.groupBy("producto").agg(
# MAGIC     sum("revenue").alias("revenue_total"),
# MAGIC     avg("cantidad").alias("cantidad_promedio"),
# MAGIC     count("user_id").alias("num_ventas")
# MAGIC )
# MAGIC
# MAGIC # Ordenar
# MAGIC resumen_ordenado = resumen.orderBy(col("revenue_total").desc())
# MAGIC
# MAGIC # Mostrar
# MAGIC display(resumen_ordenado)
# MAGIC ```
# MAGIC
# MAGIC ### 🔍 Diferencias Clave Explicadas por Genie
# MAGIC
# MAGIC | Pandas | PySpark | Razón |
# MAGIC |--------|---------|--------|
# MAGIC | `df[df['col'] == val]` | `df.filter(col("col") == val)` | API distribuida |
# MAGIC | `df['new'] = df['a'] * df['b']` | `df.withColumn("new", col("a") * col("b"))` | Inmutabilidad |
# MAGIC | `df.groupby().agg()` | `df.groupBy().agg()` | CamelCase en Spark |
# MAGIC | `df.sort_values()` | `df.orderBy()` | Nombres de métodos |
# MAGIC | `df.reset_index()` | No necesario | Spark no tiene índices |

# COMMAND ----------

# DBTITLE 1,Ejercicio 2: Migrar a PySpark
# 💻 EJERCICIO 2: Migra Tu Código Pandas a PySpark

import pandas as pd
from datetime import datetime, timedelta
import random

print("🐼 Código Pandas Original (funciona en datos pequeños):")
print("="*60)

# Crear datos de ejemplo
fechas = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(100)]
df_pandas = pd.DataFrame({
    'fecha': random.choices(fechas, k=500),
    'cliente': [f'C{i:03d}' for i in random.choices(range(50), k=500)],
    'producto': random.choices(['Laptop', 'Mouse', 'Teclado', 'Monitor'], k=500),
    'cantidad': random.choices(range(1, 10), k=500),
    'precio': random.choices([1200, 25, 80, 350], k=500)
})

# Análisis Pandas
df_pandas['revenue'] = df_pandas['cantidad'] * df_pandas['precio']
df_pandas['mes'] = pd.to_datetime(df_pandas['fecha']).dt.month

resumen_pandas = df_pandas.groupby(['mes', 'producto']).agg({
    'revenue': ['sum', 'mean'],
    'cantidad': 'sum',
    'cliente': 'nunique'
}).reset_index()

resumen_pandas.columns = ['mes', 'producto', 'revenue_total', 'revenue_promedio', 
                          'cantidad_total', 'clientes_unicos']

print("\n✅ Resultado Pandas:")
print(resumen_pandas.head(10))
print(f"\nShape: {resumen_pandas.shape}")

print("\n" + "="*60)
print("👉 TAREA: Usa Genie para convertir esto a PySpark")
print("\nPrompt sugerido:")
print('"Convierte el código Pandas de arriba a PySpark.')
print('Crea primero un DataFrame Spark desde df_pandas usando')
print('spark.createDataFrame(df_pandas), luego aplica las mismas')
print('transformaciones usando PySpark API."')

# COMMAND ----------

# DBTITLE 1,Optimización de SQL
# MAGIC %md
# MAGIC ## 🚀 Optimización de Consultas SQL
# MAGIC
# MAGIC ### 🐢 SQL Lento vs SQL Rápido
# MAGIC
# MAGIC #### ❌ Consulta Ineficiente
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     *,
# MAGIC     (SELECT COUNT(*) FROM ordenes WHERE cliente_id = c.id) as num_ordenes
# MAGIC FROM clientes c
# MAGIC WHERE pais = 'Colombia'
# MAGIC ```
# MAGIC
# MAGIC **Problemas:**
# MAGIC - `SELECT *` trae columnas innecesarias
# MAGIC - Subconsulta correlacionada (ejecuta por cada fila)
# MAGIC - Sin índices/particiones
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### ✅ Consulta Optimizada (Generada por Genie)
# MAGIC ```sql
# MAGIC WITH ordenes_por_cliente AS (
# MAGIC     SELECT 
# MAGIC         cliente_id,
# MAGIC         COUNT(*) as num_ordenes
# MAGIC     FROM ordenes
# MAGIC     GROUP BY cliente_id
# MAGIC )
# MAGIC SELECT 
# MAGIC     c.id,
# MAGIC     c.nombre,
# MAGIC     c.email,
# MAGIC     COALESCE(o.num_ordenes, 0) as num_ordenes
# MAGIC FROM clientes c
# MAGIC LEFT JOIN ordenes_por_cliente o ON c.id = o.cliente_id
# MAGIC WHERE c.pais = 'Colombia'
# MAGIC ```
# MAGIC
# MAGIC **Mejoras:**
# MAGIC - Solo columnas necesarias
# MAGIC - CTE pre-agrega datos
# MAGIC - JOIN en vez de subconsulta
# MAGIC - 10-100x más rápido
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Prompt Pattern para Optimización SQL
# MAGIC
# MAGIC ```
# MAGIC "Optimiza esta consulta SQL:
# MAGIC
# MAGIC [PEGAR SQL]
# MAGIC
# MAGIC Contexto:
# MAGIC - Tabla X tiene N millones de filas
# MAGIC - Columna Y está indexada
# MAGIC - Necesito resultado en < 10 segundos
# MAGIC
# MAGIC Sugerencias de optimización:"
# MAGIC ```
# MAGIC
# MAGIC ### ⚡ Optimizaciones Comunes que Genie Aplica
# MAGIC
# MAGIC 1. **Usar CTEs** en vez de subconsultas repetidas
# MAGIC 2. **Filtrar early** con WHERE antes de JOIN
# MAGIC 3. **Evitar SELECT *** y especificar columnas
# MAGIC 4. **Usar UNION ALL** en vez de UNION (si no hay duplicados)
# MAGIC 5. **Particionar por fecha** cuando sea aplicable
# MAGIC 6. **Usar COALESCE** para manejar NULLs eficientemente
# MAGIC 7. **Evitar funciones en WHERE** (no usar `WHERE YEAR(fecha) = 2024`)

# COMMAND ----------

# DBTITLE 1,Patrones de ETL
# MAGIC %md
# MAGIC ## 🛠️ Patrones de ETL con Genie Code
# MAGIC
# MAGIC ### 📋 Pipeline ETL Típico
# MAGIC
# MAGIC ```
# MAGIC EXTRACT → TRANSFORM → LOAD
# MAGIC   ↓          ↓           ↓
# MAGIC Leer      Limpiar      Guardar
# MAGIC Datos     Transformar  Resultado
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Prompt Pattern para ETL
# MAGIC
# MAGIC ```
# MAGIC "Crea un pipeline ETL que:
# MAGIC
# MAGIC 1. EXTRACT:
# MAGIC    - Lee desde [SOURCE]
# MAGIC    - Formato: [CSV/Parquet/Delta/JSON]
# MAGIC
# MAGIC 2. TRANSFORM:
# MAGIC    - Limpia: [nulls, duplicados, tipos]
# MAGIC    - Calcula: [nuevas columnas]
# MAGIC    - Filtra: [condiciones]
# MAGIC    - Agrega: [agregaciones]
# MAGIC
# MAGIC 3. LOAD:
# MAGIC    - Guarda en [DESTINATION]
# MAGIC    - Formato: [Parquet/Delta]
# MAGIC    - Modo: [overwrite/append]
# MAGIC    - Particiona por: [columna]
# MAGIC
# MAGIC Compatible con Databricks Serverless."
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Ejemplo: Pipeline de Ventas Diarias
# MAGIC
# MAGIC **Prompt a Genie:**
# MAGIC ```
# MAGIC "Crea un pipeline ETL que:
# MAGIC
# MAGIC 1. Lee logs de ventas desde /Volumes/main/raw/ventas_logs.json
# MAGIC 2. Limpia:
# MAGIC    - Elimina filas con revenue null
# MAGIC    - Elimina duplicados por transaction_id
# MAGIC    - Convierte fecha a date type
# MAGIC 3. Transforma:
# MAGIC    - Calcula revenue = cantidad * precio_unitario
# MAGIC    - Agrega por día y producto
# MAGIC 4. Guarda en tabla Delta: catalog.gold.ventas_diarias
# MAGIC    - Modo: append
# MAGIC    - Particiona por fecha"
# MAGIC ```
# MAGIC
# MAGIC **Código Generado:**
# MAGIC ```python
# MAGIC from pyspark.sql.functions import col, to_date, sum as _sum, count
# MAGIC
# MAGIC # EXTRACT
# MAGIC df_raw = (spark.read
# MAGIC     .option("multiLine", "true")
# MAGIC     .json("/Volumes/main/raw/ventas_logs.json")
# MAGIC )
# MAGIC
# MAGIC # TRANSFORM
# MAGIC df_clean = (
# MAGIC     df_raw
# MAGIC     .filter(col("revenue").isNotNull())  # Eliminar nulls
# MAGIC     .dropDuplicates(["transaction_id"])  # Sin duplicados
# MAGIC     .withColumn("fecha", to_date(col("fecha")))  # Convertir tipo
# MAGIC )
# MAGIC
# MAGIC df_enriched = df_clean.withColumn(
# MAGIC     "revenue",
# MAGIC     col("cantidad") * col("precio_unitario")
# MAGIC )
# MAGIC
# MAGIC df_aggregated = (
# MAGIC     df_enriched
# MAGIC     .groupBy("fecha", "producto")
# MAGIC     .agg(
# MAGIC         _sum("revenue").alias("revenue_total"),
# MAGIC         _sum("cantidad").alias("cantidad_total"),
# MAGIC         count("*").alias("num_transacciones")
# MAGIC     )
# MAGIC )
# MAGIC
# MAGIC # LOAD
# MAGIC df_aggregated.write \
# MAGIC     .format("delta") \
# MAGIC     .mode("append") \
# MAGIC     .partitionBy("fecha") \
# MAGIC     .saveAsTable("catalog.gold.ventas_diarias")
# MAGIC
# MAGIC print("✅ Pipeline ejecutado exitosamente")
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Buenas Prácticas de Revisión
# MAGIC %md
# MAGIC ## ✅ Buenas Prácticas: Revisar Código Generado
# MAGIC
# MAGIC ### ⚠️ Genie es Poderoso, Pero No Infalible
# MAGIC
# MAGIC **Siempre revisa:**
# MAGIC
# MAGIC #### 1️⃣ Lógica de Negocio
# MAGIC ```python
# MAGIC # ¿Esta fórmula es correcta para tu caso?
# MAGIC revenue = cantidad * precio_unitario * (1 - descuento/100)
# MAGIC
# MAGIC # Verifica:
# MAGIC # - ¿Descuento es porcentaje o decimal?
# MAGIC # - ¿Hay impuestos?
# MAGIC # - ¿Hay costos adicionales?
# MAGIC ```
# MAGIC
# MAGIC #### 2️⃣ Eficiencia
# MAGIC ```python
# MAGIC # 🚨 Potencialmente lento
# MAGIC for producto in productos:
# MAGIC     df.filter(col("producto") == producto).count()
# MAGIC
# MAGIC # ✅ Más eficiente
# MAGIC df.groupBy("producto").count().collect()
# MAGIC ```
# MAGIC
# MAGIC #### 3️⃣ Manejo de Nulls
# MAGIC ```python
# MAGIC # ¿Qué pasa si hay nulls?
# MAGIC df.withColumn("revenue", col("cantidad") * col("precio"))
# MAGIC
# MAGIC # Mejor con validación:
# MAGIC df.withColumn(
# MAGIC     "revenue",
# MAGIC     when(col("cantidad").isNotNull() & col("precio").isNotNull(),
# MAGIC          col("cantidad") * col("precio"))
# MAGIC     .otherwise(0)
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC #### 4️⃣ Compatibilidad Serverless
# MAGIC ```python
# MAGIC # ❌ NO compatible con Serverless
# MAGIC df.rdd.map(lambda x: x[0])  # RDD no soportado
# MAGIC
# MAGIC # ✅ Compatible
# MAGIC df.select(col("columna")).collect()  # DataFrame API
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 Checklist de Revisión
# MAGIC
# MAGIC Antes de ejecutar código generado:
# MAGIC
# MAGIC * ☑️ ¿La lógica de negocio es correcta?
# MAGIC * ☑️ ¿Maneja casos edge (nulls, duplicados, valores extremos)?
# MAGIC * ☑️ ¿Es eficiente para el volumen de datos esperado?
# MAGIC * ☑️ ¿Es compatible con Databricks Serverless?
# MAGIC * ☑️ ¿Entiendo cómo funciona cada línea?
# MAGIC * ☑️ ¿Hay comentarios que expliquen partes complejas?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💬 Cómo Pedir a Genie que Explique
# MAGIC
# MAGIC ```
# MAGIC Prompt:
# MAGIC "Explica este código línea por línea:
# MAGIC
# MAGIC [PEGAR CÓDIGO]
# MAGIC
# MAGIC En particular, explica:
# MAGIC - ¿Qué hace la línea X?
# MAGIC - ¿Por qué se usa Y en lugar de Z?
# MAGIC - ¿Qué pasa si [edge case]?"
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Ejercicio 3: Revisar Código
# 💻 EJERCICIO 3: Revisa y Mejora Código Generado

print("🔍 EJERCICIO: Revisa este código generado por IA")
print("="*60)
print("\nCódigo generado (tiene 2 problemas):")
print()
print("```python")
print("from pyspark.sql.functions import col, sum")
print()
print("# Calcular revenue total por región")
print("df = spark.table('ventas')")
print()
print("# Problema 1: No filtra fechas, escanea toda la tabla")
print("df_revenue = df.groupBy('region').agg(")
print("    sum('cantidad' * 'precio').alias('revenue_total')  # Problema 2: sintaxis incorrecta")
print(")")
print("")
print("df_revenue.show()")
print("```")

print("\n" + "="*60)
print("👉 TAREAS:")
print("\n1. Identifica los 2 problemas en el código")
print("\n2. Usa Genie con este prompt:")
print('   "Revisa este código PySpark. Tiene 2 problemas:')
print('   - No filtra por fecha reciente (solo últimos 30 días)')
print('   - Sintaxis incorrecta en la multiplicación de columnas')
print('   Corrígelo y explica los cambios."')
print("\n3. Compara el código original vs corregido")
print("\n4. Pregunta a Genie: '¿Qué otras optimizaciones recomiendas?'")
print("\n" + "="*60)

# COMMAND ----------

# DBTITLE 1,Conclusiones y Próximos Pasos
# MAGIC %md
# MAGIC ## 🎓 Conclusiones y Próximos Pasos
# MAGIC
# MAGIC ### ✅ Lo Que Aprendiste en Este Notebook
# MAGIC
# MAGIC 1. **Generar código PySpark** desde cero con prompts estructurados
# MAGIC 2. **Migrar de Pandas a PySpark** automáticamente
# MAGIC 3. **Optimizar consultas SQL** con asistencia de IA
# MAGIC 4. **Implementar pipelines ETL** completos con Genie
# MAGIC 5. **Revisar y validar** código generado por IA
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💪 Checklist de Dominio
# MAGIC
# MAGIC ¿Puedes hacer esto con confianza?
# MAGIC
# MAGIC * ☑️ Generar un pipeline PySpark completo con un prompt
# MAGIC * ☑️ Traducir código Pandas a PySpark en < 2 minutos
# MAGIC * ☑️ Identificar consultas SQL ineficientes
# MAGIC * ☑️ Crear ETL con extract-transform-load completo
# MAGIC * ☑️ Revisar código generado por IA críticamente
# MAGIC * ☑️ Explicar por qué una solución es mejor que otra
# MAGIC
# MAGIC Si marcaste todo, 🎉 **¡Dominas generación de código Big Data con IA!**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🚀 ¿Qué Sigue?
# MAGIC
# MAGIC **Has completado el Módulo 00: Guía Rápida de Genie Code**
# MAGIC
# MAGIC Ahora estás listo para:
# MAGIC
# MAGIC 1. **Módulo 01:** [Entorno Databricks & GitHub](../01_Entorno_Databricks_Free_Edition_GitHub/)
# MAGIC    - Configurar tu workspace
# MAGIC    - Conectar con GitHub
# MAGIC    - Dominar notebooks y SQL Editor
# MAGIC
# MAGIC 2. **Módulo 02:** [Fundamentos de Pandas](../02_Fundamentos_Pandas/)
# MAGIC    - Aprendizaje acelerado con Genie Code
# MAGIC    - Ejercicios prácticos con IA como copiloto
# MAGIC
# MAGIC 3. **Módulo 11:** [Introducción a PySpark](../11_Introduccion_PySpark/)
# MAGIC    - Big Data desde día 1
# MAGIC    - Usando todo lo aprendido de Genie
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Usa Genie Durante Todo el Libro
# MAGIC
# MAGIC **En cada módulo:**
# MAGIC * 👉 Pide a Genie que genere ejercicios adicionales
# MAGIC * 👉 Usa Genie para depurar tus errores
# MAGIC * 👉 Pide a Genie que revise tu código
# MAGIC * 👉 Pregunta a Genie cuando no entiendas algo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📚 Recursos Adicionales
# MAGIC
# MAGIC * **Cheatsheet PySpark:** [/anexos/cheatsheets/PYSPARK_CHEATSHEET.md](#file-PYSPARK_CHEATSHEET.md)
# MAGIC * **Cheatsheet SQL:** [/anexos/cheatsheets/SQL_CHEATSHEET.md](#file-SQL_CHEATSHEET.md)
# MAGIC * **Troubleshooting:** [/anexos/troubleshooting/COMMON_ERRORS.md](#file-COMMON_ERRORS.md)
# MAGIC * **Documentación Genie:** [Databricks Docs](https://docs.databricks.com/en/genie/index.html)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🧞 Tu Copiloto de Big Data Está Listo</h3>
# MAGIC   <p><i>"Con Genie Code, el único límite es tu imaginación, no tu memoria de sintaxis."</i></p>
# MAGIC   <p style="margin-top: 15px; font-size: 1.2em;">
# MAGIC     <strong>➡️ <a href="../01_Entorno_Databricks_Free_Edition_GitHub/" style="color: white;">Comienza el Módulo 01</a></strong>
# MAGIC   </p>
# MAGIC </div>

# COMMAND ----------

