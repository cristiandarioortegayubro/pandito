# 🧞 Módulo 15: Analítica Agéntica con Databricks Genie Code

## 🎯 Objetivo del Módulo

**Domina el futuro de la analítica:** combina tus habilidades técnicas con IA generativa para 10x tu productividad como analista de datos.

Este módulo cierra el círculo iniciado en el módulo 00, aplicando **Genie Code** a casos reales de negocio con toda la profundidad técnica que adquiriste.

**Al finalizar este módulo podrás:**
* ✅ Diseñar workflows analíticos asistidos por IA
* ✅ Usar Genie Code para generación de código PySpark/SQL
* ✅ Implementar debugging agéntico de pipelines
* ✅ Crear dashboards con prompts en lenguaje natural
* ✅ Automatizar análisis exploratorio con IA
* ✅ Escalar tu impacto como analista 10x

---

## 🏁 Pre-requisitos

**Conocimientos:**
* TODOS los módulos anteriores (01-14) completados
* Dominio de Pandas, PySpark, SQL, Delta Lake
* Módulo 00 (Guía Rápida Genie Code) revisado

**Tiempo estimado:** 4 horas

---

## 📚 Contenido del Módulo

### 15_01_Prompting_Avanzado_para_Analisis
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* Anatomía de prompts efectivos (contexto + acción + formato)
* Chain-of-thought prompting para problemas complejos
* Refinamiento iterativo con Genie
* Context injection: alimentar metadata, schemas
* Biblioteca de prompts reutilizables

**Patrones de prompting:**
```
# Patrón 1: Exploración de datos
"Tengo tabla Delta `ventas_retail` en catalog.schema.
Genera análisis exploratorio:
1. Schema completo con tipos
2. Estadísticas descriptivas (count, mean, std, percentiles)
3. Top 10 valores por columna categórica
4. Identificar valores faltantes (% por columna)
5. Detectar outliers en columnas numéricas (método IQR)
6. Recomendaciones de limpieza

Output: Markdown report + código ejecutable"

# Patrón 2: Pipeline completo
"Diseña pipeline ETL:
INPUT: logs JSON en /raw/events/ con schema {...}
TRANSFORMACIONES:
  - Validar timestamps
  - Parsear JSON anidado
  - Calcular métricas: eventos por usuario, conversion rate
  - Detectar anomalías (> 2σ de la media móvil 7d)
OUTPUT: Tabla Delta Gold con particionamiento por fecha
REQUISITOS: Idempotente, manejo de bad records, logging

Genera código production-ready con tests"

# Patrón 3: Optimización
"Optimiza esta query que tarda 10min:
[código actual]

CONTEXTO:
- df_large: 500M filas, 200 particiones
- df_small: 1K filas
- Join en cliente_id (alta cardinalidad)

Identifica:
1. Bottlenecks con explain()
2. Aplica optimizaciones (broadcast, repartition, cache)
3. Estima mejora de performance
4. Código refactorizado

Explica cada optimización y su impacto"
```

**Resultado:** Biblioteca de prompts para cualquier caso de uso

---

### 15_02_Generacion_Codigo_PySpark_SQL_Asistida
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* Migración Pandas → PySpark con Genie
* Generación de queries SQL complejas
* Traducción de requisitos de negocio → código
* Review y mejora de código con IA
* Testing asistido por IA

**Workflows:**
```
# Workflow 1: Migración
USER: "Tengo este código Pandas:
[código pandas]
Migra a PySpark optimizado para 100M filas"

GENIE: Genera código PySpark + explica cambios clave

USER: "Añade particionamiento por fecha y caching estratégico"

GENIE: Refina código con optimizaciones

# Workflow 2: SQL generation
USER: "Necesito query que calcule:
- Revenue por producto, región, mes (últimos 12 meses)
- Growth % MoM por producto
- Ranking de productos por región (top 5)
- Identificar productos con caída > 20% vs mes anterior

Tablas: ventas (id, fecha, producto_id, region, monto)
        productos (id, nombre, categoria)"

GENIE: Genera SQL con CTEs, window functions, joins

USER: "Convierte a PySpark DataFrame API"

GENIE: Traduce SQL → PySpark equivalente

# Workflow 3: Code review
USER: "Revisa este código de producción:
[código pyspark]

Identifica:
- Problemas de performance
- Riesgos (OOM, data skew)
- Bad practices
- Falta de error handling
- Sugerencias de mejora

Genera versión mejorada"

GENIE: Análisis detallado + código refactorizado
```

**Resultado:** Velocidad de desarrollo 5-10x

---

### 15_03_Debugging_Agentico_y_Error_Resolution
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* Describir errores efectivamente a Genie
* Debugging de AnalysisException
* Resolución de OutOfMemoryError
* Interpretar Spark UI con ayuda de IA
* Root cause analysis asistido

**Workflow de debugging:**
```
# Error típico: AnalysisException
[ERROR] AnalysisException: cannot resolve 'cliente_id' 
given input columns: [CLIENTE_ID, nombre, email]

USER: "Tengo este error al ejecutar:
df.filter(col('cliente_id') == 123)

Error completo: [stacktrace]

DataFrame df tiene columnas: ['CLIENTE_ID', 'nombre', 'email']"

GENIE: 
"El error es case-sensitivity. Spark es case-insensitive 
en SQL pero case-sensitive en DataFrame API.

Solución:
df.filter(col('CLIENTE_ID') == 123)

O configura:
spark.conf.set('spark.sql.caseSensitive', 'false')

Recomendación: Estandariza nombres de columnas en 
lowercase_underscore al inicio del pipeline."

# Error de performance
USER: "Job lleva 2 horas y no termina.
Spark UI muestra:
- Stage 42: 1 task (de 200) tarda 90% del tiempo
- Shuffle read: 500GB
- Spill to disk: 100GB

Código:
df_result = df_large.join(df_large_2, 'cliente_id')

¿Qué está pasando y cómo lo soluciono?"

GENIE: 
"Diagnóstico: Data skew severo en cliente_id.

1 cliente tiene millones de registros, causando que 
1 partition procese la mayoría de datos.

Soluciones:

Opción A (Salting):
df_salted = df_large.withColumn('salt', 
    (rand() * 10).cast('int'))
df_result = df_salted.join(
    df_large_2,
    (df_salted.cliente_id == df_large_2.cliente_id) &
    (df_salted.salt == df_large_2.salt)
)

Opción B (Filtrar outlier cliente):
# Si 1 cliente es el problema, procesa separado
df_normal = df.filter(col('cliente_id') != outlier_id)
df_outlier = df.filter(col('cliente_id') == outlier_id)
result = df_normal.union(df_outlier)

Recomiendo Opción A + aumentar memoria de executor."
```

**Resultado:** Resolución de errores en minutos en vez de horas

---

### 15_04_EDA_Automatizado_con_Genie_Spaces
**Duración:** 55 min | **Dificultad:** Principiante-Intermedio

**Temas:**
* Crear Genie Spaces sobre tablas Unity Catalog
* Análisis exploratorio en lenguaje natural
* Generación automática de visualizaciones
* Exportar análisis a notebooks
* Compartir insights con stakeholders no técnicos

**Casos de uso:**
```
# Caso 1: Análisis ad-hoc para ejecutivos
EJECUTIVO: "¿Cuáles son los 10 productos con mayor 
revenue en Q1 2024?"

GENIE SPACE: Genera query + tabla + gráfico barras

EJECUTIVO: "Muestra el growth % vs Q1 2023"

GENIE SPACE: Añade columna de YoY growth + color coding

EJECUTIVO: "Agrupa por categoría"

GENIE SPACE: Refina análisis con nueva dimensión

# Caso 2: Data quality assessment
ANALISTA: "Analiza calidad de tabla clientes_master:
- % de valores faltantes por columna
- Duplicados por email
- Outliers en edad, ingreso
- Distribución de segmentos"

GENIE SPACE: Report completo con viz + recomendaciones

# Caso 3: Conversión de preguntas a dashboards
PRODUCT MANAGER: "Necesito dashboard de KPIs:
- DAU, WAU, MAU
- Retention D1, D7, D30
- Funnel signup → activation → retention
- Breakdown por plataforma y país"

GENIE SPACE: Genera visualizaciones interactivas
→ Exporta a Lakeview Dashboard
```

**Resultado:** Democratización del análisis de datos

---

### 15_05_Generacion_Dashboards_Prompts_Naturales
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* Crear dashboards con descripción en lenguaje natural
* Genie → Lakeview Dashboard workflow
* Visualizaciones complejas (cohort tables, funnels)
* Interactividad (filters, drill-downs)
* Actualización automática

**Pipeline completo:**
```
USER: "Crea dashboard ejecutivo de ventas:

KPI Cards (top):
- Revenue Total (MoM growth %)
- Tickets Promedio (MoM growth %)
- # Transacciones (MoM growth %)
- # Clientes Únicos (MoM growth %)

Visualizaciones:
1. Line chart: Revenue y Margen % mensual (últimos 12m)
2. Bar chart horizontal: Top 10 productos por revenue
3. Treemap: Revenue por Región → Categoría
4. Cohort table: Retention por mes de primera compra
5. Funnel: Homepage → Cart → Checkout → Purchase

Filtros interactivos:
- Date range picker
- Multi-select: Región, Categoría
- Toggle: Include/Exclude returns

Datos: catalog.retail.ventas (última versión Delta)"

GENIE: Genera:
1. Queries SQL para cada viz
2. Configuración de parámetros
3. Dashboard YAML completo
4. Instrucciones de deployment
```

**Resultado:** Dashboards en minutos en vez de días

---

### 15_06_Caso_Practico_Pipeline_End_to_End_con_IA
**Duración:** 80 min | **Dificultad:** Avanzado

**Temas:**
* Proyecto integrador completo
* Arquitectura guiada por IA
* Implementación asistida paso a paso
* Testing y debugging con Genie
* Deployment y monitoreo

**Proyecto: Sistema de Alertas de Anomalías**
```
OBJETIVO: Detectar caídas anómalas en revenue y alertar

REQUERIMIENTOS:
- Procesar ventas diarias (tabla Delta)
- Calcular baseline: MA 28 días, σ
- Detectar anomalías: valor < (MA - 2σ)
- Generar alertas con contexto:
  * Revenue esperado vs actual
  * % drop
  * Breakdown por región/categoría
- Enviar notificación (simulado con log)
- Dashboard de monitoreo

WORKFLOW CON GENIE:

Paso 1: Arquitectura
USER: "Diseña arquitectura para sistema de alertas..."
GENIE: Diagrama + componentes + stack tech

Paso 2: Pipeline Bronze
USER: "Genera código para capa Bronze..."
GENIE: Código ingestión + validación

Paso 3: Pipeline Silver
USER: "Calcula métricas diarias y baseline..."
GENIE: Código agregaciones + window functions

Paso 4: Detección de anomalías
USER: "Implementa lógica de detección con z-score..."
GENIE: Código detección + scoring

Paso 5: Alertas
USER: "Genera mensajes de alerta con contexto..."
GENIE: Template de alertas + logger

Paso 6: Dashboard
USER: "Crea dashboard de monitoreo..."
GENIE: Queries + visualizaciones

Paso 7: Testing
USER: "Genera test cases con datos sintéticos..."
GENIE: Test data + pytest code

Paso 8: Deployment
USER: "Configura job de Databricks para ejecutar diario..."
GENIE: Job config YAML + schedule
```

**Resultado:** Sistema completo en 2 horas vs 2 semanas

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar patrones de prompting efectivos
* Nombrar casos de uso de Genie Code
* Identificar cuándo usar Genie vs codear manual

### Nivel 2: Comprensión
* Explicar cómo funciona chain-of-thought prompting
* Describir workflow de debugging agéntico
* Interpretar outputs de Genie Space

### Nivel 3: Aplicación
* Escribir prompts efectivos para análisis complejos
* Usar Genie para generación de código PySpark
* Implementar EDA automatizado
* Crear dashboards con lenguaje natural

### Nivel 4: Análisis
* Evaluar cuándo IA acelera vs complica workflow
* Diseñar pipelines híbridos humano-IA
* Medir ROI de analítica agéntica en tu organización

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Análisis Completo Asistido
```
"Soy analista nuevo en empresa retail.
Tengo tabla `ventas_retail` pero no conozco:
- Qué columnas tiene
- Qué datos contiene
- Qué análisis son relevantes

Guíame paso a paso:
1. EDA completo automático
2. Identifica 5 preguntas de negocio interesantes
3. Responde cada pregunta con análisis + viz
4. Resume insights en formato ejecutivo
5. Recomienda próximos análisis

Actúa como mi mentor de datos."
```

### Prompt 2: Migración de Stack Completo
```
"Tengo proyecto en Pandas + MySQL que procesa 50GB:
[descripción de pipeline actual]

Necesito migrar a Databricks (PySpark + Delta):
1. Audita código actual (bottlenecks, limitaciones)
2. Diseña arquitectura Databricks óptima
3. Genera código migrado componente por componente
4. Identifica mejoras de performance
5. Estima speedup esperado
6. Plan de testing y rollout

Genera documentación técnica completa."
```

### Prompt 3: Asistente Personal de Analítica
```
"Configúrate como mi asistente personal de datos.

CONTEXTO:
- Soy analista de producto en e-commerce
- Tablas principales: users, orders, products, events
- Analíticas típicas: funnels, cohorts, A/B tests
- Reporto a VP Product semanalmente

TAREAS RECURRENTES:
- Weekly KPI dashboard refresh
- Ad-hoc analyses para product managers
- A/B test analysis (significancia estadística)
- Investigación de bugs/anomalías

PREFERENCIAS:
- Código claro y comentado
- Visualizaciones con Plotly
- Reports en Markdown con executive summary

Ahora, ayúdame con: [describe tarea actual]"
```

---

## 💡 Mejores Prácticas de Analítica Agéntica

### 1. Humano en el Loop
* ✅ USA IA para: generación rápida, exploración, debugging
* ❌ NO uses IA para: decisiones críticas sin revisión humana
* 📝 Siempre revisa código generado antes de producción

### 2. Context is King
* Alimenta a Genie con: schemas, ejemplos, constraints
* Cuanto más contexto, mejor output
* Usa notebooks documentados como contexto acumulativo

### 3. Iteración Incremental
* No esperes código perfecto en primer intento
* Refina iterativamente con feedback específico
* "Make it work, make it right, make it fast" - asistido por IA

### 4. Domain Expertise Matters
* IA acelera ejecución, NO reemplaza tu expertise
* Valida lógica de negocio siempre
* IA puede alucinar SQL/código incorrecto - verifica

### 5. Documenta el Proceso
* Guarda prompts exitosos en biblioteca
* Documenta decisiones tomadas con asistencia de IA
* Facilita onboarding de nuevos analistas

---

## 🔧 Solución de Problemas

### Problema 1: Genie genera código incorrecto
**Causa:** Prompt ambiguo o falta de contexto  
**Solución:** Refina prompt con ejemplos y constraints
```
❌ MALO: "Crea query de ventas"

✅ BUENO: "Crea query SQL sobre tabla ventas con columnas:
- id (int)
- fecha (date)
- monto (decimal)

Calcula revenue total por mes de últimos 12 meses.
Output: mes (YYYY-MM), revenue (decimal 2 decimales)
Orden: mes descendente"
```

### Problema 2: Código generado no escala
**Causa:** Genie no conoce tamaño de datos  
**Solución:** Especifica escala en prompt
```
"Genera código PySpark para procesar 500M filas.
Requiere:
- Particionamiento óptimo
- Broadcast joins donde aplique
- Evitar collect()
- Cache solo si necesario"
```

### Problema 3: Genie repite soluciones previas
**Causa:** Falta de feedback específico  
**Solución:** Sé específico sobre qué cambiar
```
"El código anterior funciona pero es lento.
Problema específico: join causa shuffle de 200GB.
Optimiza usando broadcast join ya que df_small tiene solo 1000 filas."
```

---

## 📖 Recursos Adicionales

### Documentación
* [Databricks Assistant](https://docs.databricks.com/assistant/index.html)
* [Genie Spaces](https://docs.databricks.com/genie/index.html)

### Artículos
* [Prompt Engineering for Data](https://databricks.com/blog/prompt-engineering-data)
* [AI-Assisted Analytics](https://databricks.com/blog/ai-assisted-analytics)

---

## ✅ Checklist de Completitud

**Prompting:**
- [ ] Patrones de prompts efectivos
- [ ] Chain-of-thought para problemas complejos
- [ ] Biblioteca de prompts reutilizables

**Generación de Código:**
- [ ] Migración Pandas → PySpark
- [ ] SQL complejo generado
- [ ] Code review con IA

**Debugging:**
- [ ] Describir errores efectivamente
- [ ] Root cause analysis asistido
- [ ] Performance optimization con IA

**Dashboards:**
- [ ] EDA automatizado con Genie Spaces
- [ ] Generación de dashboards con prompts
- [ ] Exportar análisis a notebooks

**Proyecto Integrador:**
- [ ] Pipeline end-to-end con asistencia IA
- [ ] Testing asistido
- [ ] Deployment automatizado

---

## 🎉 Fin del Módulo 15

**¡Felicitaciones!** Has completado el último módulo técnico de "Saliendo de lo Pandito".

Ahora dominas:
* 📊 Análisis de datos con Pandas y PySpark
* 🗄️ Ingeniería de datos con Delta Lake
* 📈 Visualización con Plotly
* 🗺️ Análisis geoespacial
* 🧞 Analítica agéntica con IA

**Tu velocidad de análisis se multiplicó por 10.**

---

## 🚀 Próximo Paso

**➡️ [Módulo 16: Proyectos Integradores](../16_Proyectos_Integradores/)**

Aplica todo lo aprendido en proyectos end-to-end reales.

---

[📖 Volver al Índice](../README.md)
