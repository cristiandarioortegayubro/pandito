# Databricks notebook source
# DBTITLE 1,Portada del Módulo
# MAGIC %md
# MAGIC # Saliendo de lo Pandito v4
# MAGIC ## Módulo 00: Debugging Asistido con IA
# MAGIC
# MAGIC ### 📘 Objetivos de Este Notebook:
# MAGIC 1. Aprender a **describir errores efectivamente** a Genie Code
# MAGIC 2. Dominar la **interpretación de stacktraces** y mensajes de error
# MAGIC 3. Resolver **problemas de performance** con asistencia de IA
# MAGIC 4. Depurar **lógica de negocio** incorrecta
# MAGIC 5. Practicar con **casos reales** de debugging
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 ¿Por Qué Este Notebook?
# MAGIC
# MAGIC **La realidad del desarrollo:**
# MAGIC - 70% del tiempo se gasta en debugging, no en escribir código
# MAGIC - Los errores crípticos paralizan el aprendizaje
# MAGIC - Google/Stack Overflow no siempre tienen tu error exacto
# MAGIC
# MAGIC **Con Genie Code:**
# MAGIC - Resuelves errores 5x más rápido
# MAGIC - Entiendes la causa raíz, no solo el síntoma
# MAGIC - Aprendes patrones de prevención

# COMMAND ----------

# DBTITLE 1,Anatomía de un Error
# MAGIC %md
# MAGIC ## 🐛 Anatomía de un Error
# MAGIC
# MAGIC ### Los 3 Componentes de Todo Error
# MAGIC
# MAGIC ```
# MAGIC 1. TIPO DE ERROR (What)
# MAGIC    ↓
# MAGIC 2. MENSAJE DESCRIPTIVO (Why)
# MAGIC    ↓  
# MAGIC 3. STACKTRACE (Where)
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Real Desglosado
# MAGIC
# MAGIC ```python
# MAGIC KeyError: 'ventas_totales'
# MAGIC ^^^^^^^^^^^  ^^^^^^^^^^^^^^
# MAGIC     │              │
# MAGIC     │              └─ Mensaje: La clave que buscaste
# MAGIC     └─ Tipo: Error de clave de diccionario
# MAGIC
# MAGIC Stacktrace:
# MAGIC   File "<command-123>", line 4, in <module>
# MAGIC     total = df['ventas_totales'].sum()
# MAGIC             ^^                    ^^^^^
# MAGIC             └─ Línea exacta del error
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 Tipos de Errores Comunes
# MAGIC
# MAGIC | Error | Causa Común | Solución Típica |
# MAGIC |-------|-------------|------------------|
# MAGIC | `KeyError` | Columna no existe | Verificar `df.columns` |
# MAGIC | `TypeError` | Tipos incompatibles | Convertir tipos con `.astype()` |
# MAGIC | `ValueError` | Valor inválido | Validar input antes de operar |
# MAGIC | `IndexError` | Índice fuera de rango | Verificar longitud con `len()` |
# MAGIC | `AttributeError` | Método no existe | Verificar documentación o tipo correcto |
# MAGIC | `SyntaxError` | Código inválido | Revisar paréntesis, comillas, indentación |
# MAGIC | `NameError` | Variable no definida | Definir variable antes de usar |

# COMMAND ----------

# DBTITLE 1,Cómo Describir Errores a Genie
# MAGIC %md
# MAGIC ## 💬 Cómo Describir Errores a Genie Code
# MAGIC
# MAGIC ### ❌ Prompt Inefectivo
# MAGIC ```
# MAGIC "Tengo un error, ayúdame"
# MAGIC ```
# MAGIC **Problema:** Demasiado vago, Genie no tiene contexto.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ✅ Prompt Efectivo - Estructura CEAS
# MAGIC
# MAGIC ```
# MAGIC [C]ontexto: Qué estabas intentando hacer
# MAGIC [E]rror: Mensaje de error completo
# MAGIC [A]cción: Qué ya intentaste
# MAGIC [S]olicitud: Qué necesitas específicamente
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Completo
# MAGIC
# MAGIC ```
# MAGIC Contexto: Estoy calculando el revenue total por producto desde un DataFrame
# MAGIC          de ventas que tiene columnas: producto, cantidad, precio_unitario
# MAGIC
# MAGIC Error: KeyError: 'revenue'
# MAGIC        Traceback:
# MAGIC        Line 5: total = df['revenue'].sum()
# MAGIC
# MAGIC Acción: Verifique con df.columns y 'revenue' no aparece en la lista.
# MAGIC         Intenté df['Revenue'] con mayúscula pero sigue fallando.
# MAGIC
# MAGIC Solicitud: ¿Cómo creo la columna 'revenue' multiplicando cantidad * precio_unitario
# MAGIC            y luego calculo el total por producto?
# MAGIC ```
# MAGIC
# MAGIC **Resultado:** Genie genera código exacto que necesitas + explicación educativa.

# COMMAND ----------

# DBTITLE 1,Ejercicio 1: KeyError
# 💻 EJERCICIO 1: Debugging de KeyError

import pandas as pd

# DataFrame de ejemplo con error intencional
df = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
    'cantidad': [10, 50, 30, 15],
    'precio_unitario': [1200, 25, 80, 350]
})

# Código con error intencional
try:
    # ¡Este código va a fallar!
    total_revenue = df['revenue'].sum()  # ERROR: columna 'revenue' no existe
    print(f"Total Revenue: ${total_revenue:,.2f}")
except KeyError as e:
    print(f"❌ KeyError detectado: {e}")
    print(f"🔍 Columnas disponibles: {df.columns.tolist()}")
    print("\n👉 TAREA: Usa Genie Code para corregir este error")
    print("   Prompt sugerido: 'Crea la columna revenue como cantidad * precio_unitario'")

# COMMAND ----------

# DBTITLE 1,Debugging de Performance
# MAGIC %md
# MAGIC ## 🔍 Debugging de Performance
# MAGIC
# MAGIC ### 🐢 Consultas Lentas: El Problema Más Común
# MAGIC
# MAGIC #### 🚩 Síntomas
# MAGIC - Consulta tarda más de 30 segundos
# MAGIC - Notebook se congela
# MAGIC - "Out of Memory" errors
# MAGIC
# MAGIC #### 🔧 Estrategias de Diagnóstico con Genie
# MAGIC
# MAGIC **Prompt Pattern:**
# MAGIC ```
# MAGIC "Esta consulta [PEGAR SQL/CÓDIGO] tarda [TIEMPO].
# MAGIC La tabla tiene [N] filas y [M] columnas.
# MAGIC ¿Qué optimizaciones sugieres?"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚡ Optimizaciones Comunes que Genie Sugiere
# MAGIC
# MAGIC #### 1️⃣ Filtrar Antes de Agregar
# MAGIC ```python
# MAGIC # ❌ Lento: Agrupa todo, luego filtra
# MAGIC df.groupby('region').sum()[df['region'] == 'LATAM']
# MAGIC
# MAGIC # ✅ Rápido: Filtra primero, luego agrupa
# MAGIC df[df['region'] == 'LATAM'].groupby('region').sum()
# MAGIC ```
# MAGIC
# MAGIC #### 2️⃣ Usar Columnas Específicas (No SELECT *)
# MAGIC ```python
# MAGIC # ❌ Lento: Lee todas las columnas
# MAGIC df = spark.read.table("ventas").select("*")
# MAGIC
# MAGIC # ✅ Rápido: Solo columnas necesarias
# MAGIC df = spark.read.table("ventas").select("producto", "revenue")
# MAGIC ```
# MAGIC
# MAGIC #### 3️⃣ Particionar por Fecha
# MAGIC ```python
# MAGIC # ❌ Lento: Escanea toda la tabla
# MAGIC df = spark.read.table("logs").filter("fecha >= '2024-01-01'")
# MAGIC
# MAGIC # ✅ Rápido: Usa particiones
# MAGIC df = spark.read.table("logs").filter("year=2024 AND month=1")
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Ejercicio 2: Performance
# 💻 EJERCICIO 2: Optimización de Consulta Lenta

import pandas as pd
import time

# Crear dataset más grande para simular lentitud
df_grande = pd.DataFrame({
    'fecha': pd.date_range('2023-01-01', periods=100000, freq='1H'),
    'region': ['Norte', 'Sur', 'Este', 'Oeste'] * 25000,
    'producto': ['A', 'B', 'C', 'D', 'E'] * 20000,
    'revenue': range(100000)
})

print(f"Dataset: {len(df_grande):,} filas")

# ❌ Código ineficiente
start = time.time()
resultado_lento = df_grande.groupby(['region', 'producto']).agg({
    'revenue': ['sum', 'mean', 'count']
}).reset_index()
tiempo_lento = time.time() - start

print(f"\n❌ Tiempo sin optimizar: {tiempo_lento:.4f} segundos")
print(f"Resultado shape: {resultado_lento.shape}")

# 👉 TAREA: Usa Genie para optimizar esta consulta
print("\n👉 PROMPT SUGERIDO:")
print("   'Este código agrupa 100K filas. ¿Cómo lo optimizo?'")
print("   'Sugerencias: filtrar primero, usar columnas específicas, etc.'")

# COMMAND ----------

# DBTITLE 1,Debugging de Lógica de Negocio
# MAGIC %md
# MAGIC ## 🧠 Debugging de Lógica de Negocio
# MAGIC
# MAGIC ### 🔴 El Error Más Peligroso: Código que "Funciona" Pero Está Mal
# MAGIC
# MAGIC ```python
# MAGIC # ¿Este código calcula el revenue correcto?
# MAGIC revenue = df['cantidad'] + df['precio_unitario']  # 🚨 SUMA en vez de MULTIPLICAR
# MAGIC ```
# MAGIC
# MAGIC **Problema:** No hay error de Python, pero la lógica está mal.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 Cómo Usar Genie para Validar Lógica
# MAGIC
# MAGIC #### Prompt Pattern de Revisión
# MAGIC ```
# MAGIC "Revisa este código que calcula [DESCRIPCIÓN DE NEGOCIO]:
# MAGIC
# MAGIC [PEGAR CÓDIGO]
# MAGIC
# MAGIC ¿La lógica es correcta? ¿Hay edge cases que no considero?"
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Real
# MAGIC
# MAGIC **Prompt:**
# MAGIC ```
# MAGIC "Revisa este código que calcula el Churn Rate mensual:
# MAGIC
# MAGIC churn_rate = usuarios_cancelados / usuarios_totales * 100
# MAGIC
# MAGIC ¿La lógica es correcta?"
# MAGIC ```
# MAGIC
# MAGIC **Respuesta de Genie:**
# MAGIC ```
# MAGIC 🚨 Problema detectado:
# MAGIC
# MAGIC La fórmula es correcta, pero falta considerar:
# MAGIC 1. ¿usuarios_totales incluye nuevos usuarios del mes?
# MAGIC 2. Debería ser: cancelados / activos_al_inicio_del_mes
# MAGIC
# MAGIC Código corregido:
# MAGIC
# MAGIC activos_inicio = df[df['status'] == 'activo'].groupby('mes').first()
# MAGIC cancelados = df[df['status'] == 'cancelado'].groupby('mes').count()
# MAGIC churn_rate = (cancelados / activos_inicio * 100).fillna(0)
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Casos de Estudio Reales
# MAGIC %md
# MAGIC ## 📁 Casos de Estudio: Errores Reales y Sus Soluciones
# MAGIC
# MAGIC ### Caso 1: "SettingWithCopyWarning" en Pandas
# MAGIC
# MAGIC **Error:**
# MAGIC ```python
# MAGIC SettingWithCopyWarning: 
# MAGIC A value is trying to be set on a copy of a slice from a DataFrame
# MAGIC ```
# MAGIC
# MAGIC **Prompt a Genie:**
# MAGIC ```
# MAGIC "Tengo este warning en Pandas:
# MAGIC
# MAGIC df_filtrado = df[df['edad'] > 18]
# MAGIC df_filtrado['categoria'] = 'adulto'
# MAGIC
# MAGIC SettingWithCopyWarning...
# MAGIC
# MAGIC ¿Cómo lo corrijo?"
# MAGIC ```
# MAGIC
# MAGIC **Solución de Genie:**
# MAGIC ```python
# MAGIC # Usa .copy() explícitamente
# MAGIC df_filtrado = df[df['edad'] > 18].copy()
# MAGIC df_filtrado['categoria'] = 'adulto'
# MAGIC
# MAGIC # O usa .loc[] para modificar in-place
# MAGIC df.loc[df['edad'] > 18, 'categoria'] = 'adulto'
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Caso 2: "AnalysisException" en PySpark
# MAGIC
# MAGIC **Error:**
# MAGIC ```
# MAGIC AnalysisException: Column 'ventas_Q1' does not exist.
# MAGIC Did you mean one of the following? [ventas_q1, ventas_Q2]
# MAGIC ```
# MAGIC
# MAGIC **Prompt a Genie:**
# MAGIC ```
# MAGIC "PySpark me dice que la columna 'ventas_Q1' no existe,
# MAGIC pero la veo en df.printSchema(). ¿Por qué?"
# MAGIC ```
# MAGIC
# MAGIC **Respuesta de Genie:**
# MAGIC ```
# MAGIC PySpark es case-sensitive en columnas.
# MAGIC 'ventas_Q1' ≠ 'ventas_q1'
# MAGIC
# MAGIC Solución:
# MAGIC 1. Usa el nombre exacto: df.select('ventas_q1')
# MAGIC 2. O renombra: df = df.withColumnRenamed('ventas_q1', 'ventas_Q1')
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Caso 3: "Out of Memory" en Joins
# MAGIC
# MAGIC **Error:**
# MAGIC ```
# MAGIC java.lang.OutOfMemoryError: GC overhead limit exceeded
# MAGIC ```
# MAGIC
# MAGIC **Prompt a Genie:**
# MAGIC ```
# MAGIC "Este join me da OutOfMemory:
# MAGIC
# MAGIC df_grande = spark.read.table('ventas')  # 100M rows
# MAGIC df_pequena = spark.read.table('productos')  # 1K rows
# MAGIC resultado = df_grande.join(df_pequena, 'producto_id')
# MAGIC
# MAGIC ¿Cómo lo optimizo?"
# MAGIC ```
# MAGIC
# MAGIC **Solución de Genie:**
# MAGIC ```python
# MAGIC from pyspark.sql.functions import broadcast
# MAGIC
# MAGIC # Usa broadcast join para tabla pequeña
# MAGIC resultado = df_grande.join(
# MAGIC     broadcast(df_pequena), 
# MAGIC     'producto_id'
# MAGIC )
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Ejercicio Integrador
# MAGIC %md
# MAGIC ## 🎯 Ejercicio Integrador: Debugging Challenge
# MAGIC
# MAGIC ### 🔴 Escenario: Reporte de Ventas Mensual Roto
# MAGIC
# MAGIC Tu equipo reporta que el dashboard de ventas muestra números incorrectos.
# MAGIC El código está abajo. **Tiene 3 errores diferentes.**
# MAGIC
# MAGIC ### 📝 Tu Misión
# MAGIC
# MAGIC 1. **Identifica los 3 errores** (sin ejecutar el código)
# MAGIC 2. **Usa Genie** para verificar tu hipótesis
# MAGIC 3. **Corrige el código** con la ayuda de Genie
# MAGIC 4. **Valida** que los resultados ahora sean correctos
# MAGIC
# MAGIC ### 👉 Siguiente Celda: Código con Errores
# MAGIC
# MAGIC **Pistas:**
# MAGIC - Un error de lógica de negocio
# MAGIC - Un error de tipo de datos
# MAGIC - Un error de nombres de columnas

# COMMAND ----------

# DBTITLE 1,Código con Errores
# 🐛 CÓDIGO CON 3 ERRORES - ENCUÉNTRALOS CON GENIE

import pandas as pd

df_ventas = pd.DataFrame({
    'fecha': ['2024-01-15', '2024-01-20', '2024-02-10', '2024-02-25'],
    'producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
    'cantidad': [10, 50, 30, 15],
    'precio_unit': [1200, 25, 80, 350],
    'descuento_pct': [10, 5, 0, 15]  # Porcentaje de descuento
})

print("Dataset original:")
print(df_ventas)
print("\n" + "="*60)

# ERROR 1: Lógica incorrecta de cálculo de revenue
# El revenue debería ser: cantidad * precio_unit * (1 - descuento_pct/100)
# Pero el código hace:
df_ventas['revenue'] = df_ventas['cantidad'] + df_ventas['precio_unit']  # 🚨

# ERROR 2: Columna mal escrita (case-sensitive)
try:
    df_ventas['mes'] = pd.to_datetime(df_ventas['Fecha']).dt.month  # 🚨
except KeyError as e:
    print(f"\n❌ ERROR 2 detectado: {e}")
    # TAREA: Corrígelo con Genie

# ERROR 3: Tipo de datos incorrecto para operación numérica
try:
    revenue_total = df_ventas['revenue'].sum()
    descuento_promedio = df_ventas['descuento_pct'].mean()  # Esto funciona
    
    # Intentar calcular revenue con descuento (fallará por ERROR 1)
    print(f"\nRevenue Total (INCORRECTO): ${revenue_total:,.2f}")
    print(f"Descuento Promedio: {descuento_promedio}%")
except Exception as e:
    print(f"\n❌ ERROR 3: {type(e).__name__}: {e}")

print("\n" + "="*60)
print("👉 TAREA: Usa Genie Code para corregir los 3 errores")
print("\nPrompt sugerido:")
print("\"Revisa este código de cálculo de revenue. Hay 3 errores:")
print("1. Lógica de cálculo incorrecta")
print("2. Nombre de columna mal escrito")
print("3. [Detectar al ejecutar]")
print("\nCorrige el código completo.\"")

# COMMAND ----------

# DBTITLE 1,Conclusiones y Próximos Pasos
# MAGIC %md
# MAGIC ## 🎓 Conclusiones y Próximos Pasos
# MAGIC
# MAGIC ### ✅ Lo Que Aprendiste en Este Notebook
# MAGIC
# MAGIC 1. **Estructura CEAS** para describir errores efectivamente
# MAGIC 2. **Interpretación de stacktraces** y mensajes de error
# MAGIC 3. **Debugging de performance** con patrones de optimización
# MAGIC 4. **Validación de lógica de negocio** con IA
# MAGIC 5. **Casos reales** de errores comunes y sus soluciones
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💪 Checklist de Dominio
# MAGIC
# MAGIC ¿Puedes hacer esto sin dudar?
# MAGIC
# MAGIC * ☑️ Describir un error a Genie usando CEAS
# MAGIC * ☑️ Leer un stacktrace e identificar la línea problemática
# MAGIC * ☑️ Diagnosticar consultas lentas con Genie
# MAGIC * ☑️ Pedir a Genie que valide lógica de negocio
# MAGIC * ☑️ Resolver 3 errores distintos en < 5 minutos con IA
# MAGIC
# MAGIC Si marcaste todo, 🎉 **¡Dominas debugging asistido por IA!**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🚀 Próximo Notebook
# MAGIC
# MAGIC **➡️ [00_04_Generacion_Codigo_PySpark_SQL](#notebook-00_04)**
# MAGIC
# MAGIC Aprende a:
# MAGIC * Generar código PySpark desde cero con Genie
# MAGIC * Migrar de Pandas a PySpark automáticamente
# MAGIC * Optimizar consultas SQL complejas
# MAGIC * Dominar patrones de ETL con asistencia de IA
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📚 Recursos Adicionales
# MAGIC
# MAGIC * **Anexo de Troubleshooting:** [/anexos/troubleshooting/COMMON_ERRORS.md](#file-COMMON_ERRORS.md)
# MAGIC * **PySpark Errors:** [Documentación oficial](https://spark.apache.org/docs/latest/sql-error-conditions.html)
# MAGIC * **Pandas Warnings:** [Guía de mejores prácticas](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🔧 Debugging Ya No Es Frustrante</h3>
# MAGIC   <p><i>"Con Genie Code, cada error es una oportunidad de aprendizaje instantánea."</i></p>
# MAGIC </div>

# COMMAND ----------

