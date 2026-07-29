# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Portada del Módulo
# MAGIC %md
# MAGIC # Saliendo de lo Pandito v4
# MAGIC ## Módulo 00: Guía Rápida de Genie Code & Databricks Assistant
# MAGIC
# MAGIC ### 📘 Objetivos de Este Módulo:
# MAGIC 1. Comprender qué es **Genie Code** y cómo funciona la analítica agéntica
# MAGIC 2. Aprender a usar el **Databricks Assistant** como copiloto de análisis
# MAGIC 3. Integrar IA generativa en tu flujo de trabajo diario
# MAGIC 4. Dominar patrones de prompts efectivos para análisis de datos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 ¿Por Qué Este Módulo Primero?
# MAGIC
# MAGIC Antes de sumergirte en los fundamentos técnicos, queremos que conozcas tu herramienta secreta: **Genie Code**. Esta tecnología de IA te permitirá:
# MAGIC
# MAGIC ✅ Generar código automáticamente mientras aprendes  
# MAGIC ✅ Depurar errores con explicaciones claras  
# MAGIC ✅ Acelerar tu curva de aprendizaje 10x  
# MAGIC ✅ Experimentar sin miedo a "romper" cosas  
# MAGIC
# MAGIC **Piensa en Genie Code como tu mentor de datos disponible 24/7.**

# COMMAND ----------

# DBTITLE 1,¿Qué es Genie Code?
# MAGIC %md
# MAGIC ## 🤖 ¿Qué es Genie Code?
# MAGIC
# MAGIC **Genie Code** es el asistente de inteligencia artificial integrado en Databricks que te ayuda a:
# MAGIC
# MAGIC ### 1️⃣ Escribir Código
# MAGIC ```python
# MAGIC # En lugar de recordar sintaxis exacta, simplemente pides:
# MAGIC # "Crea un DataFrame con columnas nombre, edad, salario y 5 filas de ejemplo"
# MAGIC
# MAGIC # Genie genera automáticamente:
# MAGIC import pandas as pd
# MAGIC
# MAGIC df = pd.DataFrame({
# MAGIC     'nombre': ['Ana', 'Juan', 'María', 'Carlos', 'Sofía'],
# MAGIC     'edad': [28, 34, 42, 31, 29],
# MAGIC     'salario': [55000, 72000, 85000, 63000, 58000]
# MAGIC })
# MAGIC
# MAGIC df
# MAGIC ```
# MAGIC
# MAGIC ### 2️⃣ Explicar Conceptos
# MAGIC ```
# MAGIC Prompt: "Explica qué es un LEFT JOIN con ejemplo"
# MAGIC
# MAGIC → Genie responde con:
# MAGIC - Definición clara
# MAGIC - Diagrama visual
# MAGIC - Código ejecutable
# MAGIC - Casos de uso de negocio
# MAGIC ```
# MAGIC
# MAGIC ### 3️⃣ Depurar Errores
# MAGIC ```
# MAGIC Prompt: "Tengo un KeyError: 'ventas_totales', ¿cómo lo soluciono?"
# MAGIC
# MAGIC → Genie analiza:
# MAGIC - Por qué ocurre el error
# MAGIC - Qué columnas existen realmente
# MAGIC - Cómo corregir el nombre
# MAGIC - Cómo prevenir este error en el futuro
# MAGIC ```
# MAGIC
# MAGIC ### 4️⃣ Optimizar Performance
# MAGIC ```
# MAGIC Prompt: "Esta consulta tarda 2 minutos, ¿cómo la optimizo?"
# MAGIC
# MAGIC → Genie sugiere:
# MAGIC - Uso de índices
# MAGIC - Filtrado temprano
# MAGIC - Particionamiento
# MAGIC - Broadcast joins
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Diferencia entre Genie Code y ChatGPT
# MAGIC %md
# MAGIC ## 🔍 Genie Code vs ChatGPT / Claude / Copilot
# MAGIC
# MAGIC | Característica | Genie Code | ChatGPT/Claude | GitHub Copilot |
# MAGIC |----------------|------------|----------------|----------------|
# MAGIC | **Contexto de Datos** | ✅ Conoce tus tablas, esquemas y metadatos | ❌ No tiene acceso a tu workspace | ❌ No conoce tus datos |
# MAGIC | **Ejecuta Código** | ✅ Genera y ejecuta directamente | ❌ Solo genera texto | ✅ Genera en el editor |
# MAGIC | **Optimizado para Databricks** | ✅ PySpark, Delta Lake, Unity Catalog | ⚠️ Conocimiento general | ⚠️ Conocimiento general |
# MAGIC | **Debugging Contextual** | ✅ Ve tus errores y stacktraces | ❌ Necesitas copiar el error | ⚠️ Limitado al archivo actual |
# MAGIC | **Genera Dashboards** | ✅ Crea visualizaciones completas | ❌ Solo código de viz | ❌ No especializado en dashboards |
# MAGIC | **Privacidad** | ✅ Tus datos permanecen en Databricks | ⚠️ Depende del plan | ⚠️ Depende de la configuración |
# MAGIC
# MAGIC ### 💡 Cuándo Usar Cada Uno
# MAGIC
# MAGIC **Usa Genie Code para:**
# MAGIC - Trabajar con tus tablas específicas
# MAGIC - Generar consultas SQL sobre Unity Catalog
# MAGIC - Crear pipelines de ETL
# MAGIC - Debugging en tiempo real
# MAGIC - Análisis exploratorio de datos
# MAGIC
# MAGIC **Usa ChatGPT/Claude para:**
# MAGIC - Conceptos teóricos generales
# MAGIC - Algoritmos de machine learning
# MAGIC - Diseño de arquitecturas
# MAGIC - Explicaciones pedagógicas
# MAGIC
# MAGIC **Usa GitHub Copilot para:**
# MAGIC - Completar código línea por línea
# MAGIC - Funciones repetitivas
# MAGIC - Boilerplate code

# COMMAND ----------

# DBTITLE 1,Cómo Acceder a Genie Code
# MAGIC %md
# MAGIC ## 🚀 Cómo Acceder a Genie Code en Databricks
# MAGIC
# MAGIC ### Método 1: Panel Lateral (Recomendado)
# MAGIC ```
# MAGIC 1. En cualquier notebook, busca el ícono 🧞 en la esquina superior derecha
# MAGIC 2. Click para abrir el panel de Genie
# MAGIC 3. Escribe tu pregunta o solicitud
# MAGIC 4. Genie genera el código y puedes insertarlo en una celda
# MAGIC ```
# MAGIC
# MAGIC ### Método 2: Comando de Celda
# MAGIC ```python
# MAGIC # En una celda de notebook, puedes escribir:
# MAGIC # /genie tu pregunta aquí
# MAGIC
# MAGIC # Ejemplo:
# MAGIC # /genie crea un gráfico de barras con las ventas por mes
# MAGIC ```
# MAGIC
# MAGIC ### Método 3: Chat en Editor SQL
# MAGIC ```
# MAGIC 1. Abre el SQL Editor
# MAGIC 2. Click en el botón "Assistant" 
# MAGIC 3. Describe tu consulta en lenguaje natural
# MAGIC 4. Genie genera el SQL optimizado
# MAGIC ```
# MAGIC
# MAGIC ### Método 4: Genie Spaces (Avanzado)
# MAGIC ```
# MAGIC 1. Crea un "Genie Space" sobre tus tablas específicas
# MAGIC 2. Haz preguntas de negocio en lenguaje natural
# MAGIC 3. Genie responde con análisis completo + visualizaciones
# MAGIC 4. Ideal para usuarios no técnicos (C-level, gerentes)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎓 Para Este Libro
# MAGIC
# MAGIC **Te recomendamos usar el Panel Lateral** porque:
# MAGIC - Puedes ver el código generado antes de ejecutarlo (aprendizaje)
# MAGIC - Puedes modificar el código sugerido (entendimiento)
# MAGIC - Puedes comparar tu código vs el de Genie (mejora continua)

# COMMAND ----------

# DBTITLE 1,Ejemplo Práctico - Tu Primer Prompt
# MAGIC %md
# MAGIC ## 🧪 Ejercicio Práctico: Tu Primer Prompt
# MAGIC
# MAGIC ### Escenario de Negocio
# MAGIC Eres analista de ventas y necesitas crear un reporte rápido.
# MAGIC
# MAGIC ### ❌ Forma Tradicional (Sin Genie)
# MAGIC ```python
# MAGIC # Tendrías que recordar/buscar:
# MAGIC # - Sintaxis de pandas
# MAGIC # - Cómo crear DataFrames
# MAGIC # - Cómo calcular totales
# MAGIC # - Cómo formatear fechas
# MAGIC # - Cómo hacer pivot tables
# MAGIC # (10-15 minutos de coding + debugging)
# MAGIC ```
# MAGIC
# MAGIC ### ✅ Forma Agéntica (Con Genie)
# MAGIC ```
# MAGIC Prompt a Genie:
# MAGIC "Crea un DataFrame de ventas con columnas: fecha, producto, cantidad, precio_unitario.
# MAGIC Incluye 10 transacciones de ejemplo de enero 2024.
# MAGIC Calcula el ingreso total por producto.
# MAGIC Muestra el resultado ordenado de mayor a menor."
# MAGIC
# MAGIC ⏱️ Tiempo: 30 segundos
# MAGIC ```
# MAGIC
# MAGIC ### 🎯 Pruébalo Ahora
# MAGIC
# MAGIC En la siguiente celda, copia este prompt exacto en el panel de Genie y observa el código generado:

# COMMAND ----------

# DBTITLE 1,Celda para experimentar con Genie
# 🧞 EJERCICIO: Usa Genie Code para generar el siguiente DataFrame
# 
# Prompt sugerido:
# "Crea un DataFrame de ventas con columnas: fecha, producto, cantidad, precio_unitario.
# Incluye 10 transacciones de ejemplo de enero 2024.
# Calcula el ingreso total por producto.
# Muestra el resultado ordenado de mayor a menor."
#
# INSTRUCCIONES:
# 1. Abre el panel de Genie (ícono 🧞 arriba a la derecha)
# 2. Copia el prompt de arriba
# 3. Pégalo en Genie
# 4. Copia el código generado y pégalo aquí
# 5. Ejecuta esta celda

# PEGA AQUÍ EL CÓDIGO GENERADO POR GENIE:


# COMMAND ----------

# DBTITLE 1,Anatomía de un Prompt Efectivo
# MAGIC %md
# MAGIC ## 📝 Anatomía de un Prompt Efectivo
# MAGIC
# MAGIC ### 🎯 Estructura Recomendada
# MAGIC
# MAGIC ```
# MAGIC [CONTEXTO] + [ACCIÓN] + [DETALLES] + [FORMATO DE SALIDA]
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplos Comparativos
# MAGIC
# MAGIC #### ❌ Prompt Vago
# MAGIC ```
# MAGIC "Necesito analizar ventas"
# MAGIC ```
# MAGIC **Problema:** Genie no sabe qué análisis, qué periodo, qué métricas.
# MAGIC
# MAGIC #### ✅ Prompt Específico
# MAGIC ```
# MAGIC "Analiza las ventas del Q4 2023 de la tabla 'ventas_retail'.
# MAGIC Calcula: total de ingresos, ticket promedio, producto más vendido.
# MAGIC Agrupa por mes y muestra un gráfico de líneas."
# MAGIC ```
# MAGIC **Resultado:** Código preciso, ejecutable inmediatamente.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔑 Elementos Clave de un Buen Prompt
# MAGIC
# MAGIC 1. **Datos de Entrada**
# MAGIC    ```
# MAGIC    "Usando la tabla unity_catalog.schema.clientes..."
# MAGIC    "Con este DataFrame llamado 'df_ventas'..."
# MAGIC    "Crea un DataFrame de ejemplo con..."
# MAGIC    ```
# MAGIC
# MAGIC 2. **Transformaciones**
# MAGIC    ```
# MAGIC    "Filtra las filas donde estado = 'ACTIVO'"
# MAGIC    "Agrupa por región y calcula el promedio"
# MAGIC    "Combina con la tabla de productos usando LEFT JOIN"
# MAGIC    ```
# MAGIC
# MAGIC 3. **Métricas/Cálculos**
# MAGIC    ```
# MAGIC    "Calcula el ARPU (ingreso promedio por usuario)"
# MAGIC    "Determina el Churn Rate mensual"
# MAGIC    "Computa el EBITDA por sucursal"
# MAGIC    ```
# MAGIC
# MAGIC 4. **Formato de Salida**
# MAGIC    ```
# MAGIC    "Muestra los top 10 resultados"
# MAGIC    "Genera un gráfico de barras horizontal"
# MAGIC    "Exporta a formato Parquet"
# MAGIC    ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Tip Pro: Refinamiento Iterativo
# MAGIC
# MAGIC No necesitas un prompt perfecto al primer intento. Genie entiende conversaciones:
# MAGIC
# MAGIC ```
# MAGIC Prompt 1: "Crea un DataFrame de empleados"
# MAGIC → Genie genera DataFrame básico
# MAGIC
# MAGIC Prompt 2: "Agrega una columna de 'departamento'"
# MAGIC → Genie modifica el DataFrame anterior
# MAGIC
# MAGIC Prompt 3: "Calcula el salario promedio por departamento"
# MAGIC → Genie añade la agregación
# MAGIC
# MAGIC Prompt 4: "Visualízalo en un gráfico de barras"
# MAGIC → Genie agrega el código de Plotly
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Conclusiones y Próximos Pasos
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 00_01
# MAGIC
# MAGIC ### ✅ Lo Que Aprendiste
# MAGIC
# MAGIC 1. **Qué es Genie Code** y cómo se diferencia de otros asistentes de IA
# MAGIC 2. **Cómo acceder a Genie** en Databricks (4 métodos)
# MAGIC 3. **Anatomía de prompts efectivos** para análisis de datos
# MAGIC 4. **Refinamiento iterativo** de código mediante conversación
# MAGIC
# MAGIC ### 🚀 Próximos Notebooks de Este Módulo
# MAGIC
# MAGIC * **00_02** - Prompts Efectivos para Análisis de Datos
# MAGIC   - Patrones de prompts por tipo de análisis
# MAGIC   - Biblioteca de prompts reutilizables
# MAGIC   - Casos de uso empresariales específicos
# MAGIC
# MAGIC * **00_03** - Debugging Asistido con IA
# MAGIC   - Cómo describir errores a Genie
# MAGIC   - Interpretación de stacktraces
# MAGIC   - Debugging de performance
# MAGIC
# MAGIC * **00_04** - Generación de Código PySpark y SQL
# MAGIC   - Migración de Pandas a PySpark con Genie
# MAGIC   - Optimización de consultas SQL
# MAGIC   - Patrones de ETL comunes
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 💪 Reto Personal
# MAGIC
# MAGIC **Durante el resto del libro, comprométete a:**
# MAGIC
# MAGIC 1. **Antes de googlear un error** → Pregúntale a Genie
# MAGIC 2. **Antes de copiar código de Stack Overflow** → Pídele a Genie que lo explique
# MAGIC 3. **Después de cada módulo** → Usa Genie para crear 3 ejercicios adicionales
# MAGIC 4. **Al finalizar un análisis** → Pídele a Genie que revise tu código y sugiera mejoras
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📚 Continúa Tu Aprendizaje
# MAGIC
# MAGIC **Siguiente notebook:** [00_02_Prompts_Efectivos_Analisis_Datos](#notebook-00_02)
# MAGIC
# MAGIC **O salta al Módulo 01:** [01_01_Configuracion_Databricks_y_Git](#notebook-01_01) para comenzar con los fundamentos técnicos.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🧞 Tu Superpoder de Aprendizaje Está Activado</h3>
# MAGIC   <p><i>"La mejor manera de aprender es haciendo. Con Genie, puedes hacer 10x más."</i></p>
# MAGIC </div>