# 🧞 Módulo 00: Guía Rápida de Genie Code & Databricks Assistant

## 🎯 Objetivo del Módulo

Este módulo es tu **puerta de entrada** al mundo de la analítica asistida por IA. Antes de sumergirte en Python, Pandas o PySpark, aprenderás a usar **Genie Code** como tu copiloto de análisis de datos.

### ¿Por Qué Empezar Aquí?

Genie Code te permite:
* ⚡ **Acelerar tu aprendizaje 10x** - genera código mientras aprendes sintaxis
* 👥 **Tener un mentor 24/7** - resuelve dudas y errores al instante
* 🧠 **Enfocarte en el negocio** - piensa en "qué" quieres, no en "cómo" codificarlo
* 🔥 **Experimentar sin miedo** - prueba ideas sin preocuparte por romper cosas

---

## 📚 Contenido del Módulo

### [00_01_Que_es_Genie_Code](./00_01_Que_es_Genie_Code)
**Duración:** 20 minutos

* ¿Qué es Genie Code y cómo funciona?
* Diferencias con ChatGPT, Claude y GitHub Copilot
* Cómo acceder a Genie en Databricks (4 métodos)
* Tu primer prompt: ejercicio práctico
* Anatomía de un prompt efectivo

**Habilidades clave:** Entender la analítica agéntica, escribir prompts básicos

---

### [00_02_Prompts_Efectivos_Analisis_Datos](./00_02_Prompts_Efectivos_Analisis_Datos)
**Duración:** 30 minutos

* 6 patrones de prompts por tipo de análisis:
  - Exploración de datos (EDA)
  - Cálculo de KPIs y métricas
  - Joins y combinaciones de tablas
  - Filtrado y segmentación
  - Series de tiempo
  - Visualizaciones
* Biblioteca de prompts por industria (Finanzas, Retail, SaaS, Logística)
* Templates reutilizables para casos comunes

**Habilidades clave:** Dominar patrones de prompts, adaptar templates a tu contexto

---

### [00_03_Debugging_Asistido_IA](./00_03_Debugging_Asistido_IA)
**Duración:** 25 minutos

* Cómo describir errores efectivamente a Genie
* Interpretación de stacktraces y errores comunes
* Debugging de performance (consultas lentas)
* Depuración de lógica de negocio
* Casos de estudio: errores reales y sus soluciones

**Habilidades clave:** Resolver errores 5x más rápido, entender stacktraces

---

### [00_04_Generacion_Codigo_PySpark_SQL](./00_04_Generacion_Codigo_PySpark_SQL)
**Duración:** 30 minutos

* Generación de código PySpark desde cero
* Migración de Pandas a PySpark con Genie
* Optimización de consultas SQL
* Patrones de ETL comunes con IA
* Buenas prácticas: revisar y entender el código generado

**Habilidades clave:** Generar código Big Data, migrar de Pandas a Spark

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Ninguno! Este módulo es para principiantes absolutos
* Único requisito: saber usar una computadora y navegador web

**Herramientas:**
* Cuenta en Databricks Community Edition (gratuita)
* Navegador web moderno (Chrome, Firefox, Edge)

---

## 🛤️ Roadmap de Aprendizaje

### Opción A: Recorrido Completo (2 horas)
```
00_01 → 00_02 → 00_03 → 00_04
```
**Recomendado para:** Quienes quieren dominio total de Genie Code

### Opción B: Rápido (45 minutos)
```
00_01 → 00_02
```
**Recomendado para:** Quienes quieren empezar a usar Genie YA, volverán a 00_03 y 00_04 cuando necesiten debugging/optimización

### Opción C: Solo Referencia
```
Guardar este módulo como bookmark
Consultar 00_02 (biblioteca de prompts) cuando necesites
```
**Recomendado para:** Quienes ya usan IA generativa y solo necesitan templates

---

## 💡 Cómo Usar Este Módulo Durante el Libro

### Durante el Aprendizaje (Módulos 01-14)
* **Cada vez que veas un ejercicio**: pide a Genie que lo resuelva primero, luego compara con tu solución
* **Cada vez que tengas un error**: abre 00_03 y sigue el patrón de debugging
* **Al final de cada módulo**: usa Genie para crear 3 ejercicios adicionales de práctica

### Como Referencia Rápida
* **00_02 (Prompts)**: tu cheatsheet para análisis comunes
* **00_03 (Debugging)**: cuando tengas errores que no entiendes
* **00_04 (PySpark/SQL)**: cuando necesites optimizar código o migrar a Spark

---

## 🎮 Ejercicio Integrador del Módulo

Después de completar los 4 notebooks, realiza este desafío:

### Desafío: Reporte Ejecutivo Automatizado

**Escenario:** Eres analista de una empresa de e-commerce. Tu jefe te pide un reporte semanal de ventas.

**Usando SOLO Genie Code, genera:**

1. **DataFrame de ventas sintético** (100 transacciones de la semana pasada)
   - Columnas: fecha, producto, categoría, cantidad, precio_unitario, región, vendedor

2. **KPIs principales:**
   - Revenue total
   - Número de transacciones
   - Ticket promedio
   - Top 5 productos por ventas
   - Top 3 vendedores por revenue

3. **Análisis de tendencias:**
   - Ventas por día de la semana
   - Comparación vs semana anterior (simular datos)
   - Identificar día con mayor/menor actividad

4. **Visualización:**
   - Dashboard con 3 gráficos:
     * Líneas: revenue diario
     * Barras: revenue por categoría
     * Pie chart: distribución por región

**Objetivo:** Completar todo usando prompts a Genie. Tiempo estimado: 15 minutos.

**Criterio de éxito:** Si lograste esto sin escribir código manualmente, ¡dominas Genie Code!

---

## 📌 Recursos Adicionales

* **Documentación oficial:** [Databricks Genie Code](https://docs.databricks.com/en/genie/index.html)
* **Video tutoriales:** [YouTube - Databricks Channel](https://www.youtube.com/@Databricks)
* **Comunidad:** [Databricks Community Forums](https://community.databricks.com/)

---

## ❓ Preguntas Frecuentes

**P: ¿Genie Code está disponible en Free Edition?**  
R: Sí, el Databricks Assistant (versión de Genie en notebooks) está disponible en Community Edition.

**P: ¿Mis datos se comparten con el modelo de IA?**  
R: No, Genie procesa todo dentro de tu workspace de Databricks con estándares de seguridad empresarial.

**P: ¿Puedo usar Genie para código de producción?**  
R: Sí, pero SIEMPRE revisa y entiende el código generado. Genie es un asistente, no un reemplazo de tu criterio.

**P: ¿Qué hago si Genie genera código incorrecto?**  
R: Refina tu prompt con más contexto. Si persiste, reporta el caso (ayuda a mejorar el modelo).

---

## 🎓 Certificación de Dominio

Completaste este módulo si puedes:

* ☑️ Explicar qué es analítica agéntica
* ☑️ Escribir prompts efectivos para análisis comunes
* ☑️ Usar Genie para depurar errores en < 2 minutos
* ☑️ Generar código PySpark/SQL sin escribir una línea manualmente
* ☑️ Completar el "Desafío: Reporte Ejecutivo" en < 20 minutos

---

## 🚀 Próximo Módulo

Ahora que dominas tu copiloto de IA, es momento de aprender los fundamentos:

---

## 📂 Notebook 05: Setup Maestro de Datos del Proyecto

### 🎯 Notebook Especial - Ejecutar PRIMERO

**📁 Ubicación:** `00_05_Preparacion_Datos_Empresariales.ipynb`

**🚨 IMPORTANTE:** Este notebook es diferente a los demás. En lugar de ser un tutorial educativo, es un **notebook de infraestructura** que genera los datos base de todo el proyecto.

### 🏭 Qué Hace Este Notebook

**1. Genera Datos Sintéticos Realistas:**
* 5 sucursales de "Los Andes Market" en Mendoza, Argentina
* 60 meses de datos de ventas (2019-2024)
* Georeferenciación con coordenadas GPS + índices H3
* Total: 300 registros

**2. Aplica Feature Engineering:**
* Features temporales: lags, rolling statistics, cíclicos
* Features geoespaciales: distancia al centro, densidad H3
* Normalización con MinMaxScaler

**3. Crea Secuencias para Deep Learning:**
* Secuencias de 12 meses para LSTM/RNN
* Splits: Train (70%), Validation (15%), Test (15%)
* Total: 204 secuencias listas para usar

**4. Guarda en Unity Catalog:**
* `pandito_ds.default.ventas_mensuales_mendoza_h3`
* `pandito_ds.default.dl_sequences_lstm`
* `pandito_ds.default.dl_metadata_lstm`

### 🔄 Flujo de Trabajo Recomendado

```
1. EJECUTAR 🎯 00_05_Preparacion_Datos_Empresariales.ipynb
   ↓
   Genera 3 tablas en Unity Catalog
   ↓
2. Navegar a cualquier módulo (01-16)
   ↓
3. Los notebooks pueden opcionalmente cargar datos reales:
   df = spark.table('pandito_ds.default.ventas_mensuales_mendoza_h3').toPandas()
```

### 📄 Tablas Disponibles

**Tabla 1: `ventas_mensuales_mendoza_h3`**
* 🏪 Datos base georeferenciados
* 📅 300 registros (60 meses × 5 sucursales)
* 📊 Columnas: fecha, sucursal, ventas, lat, lon, zona, h3_index
* **Usar en:** Módulos 06 (Agregaciones), 07 (Series), 09 (Geo), 10 (H3)

**Tabla 2: `dl_sequences_lstm`**
* 🧠 Secuencias temporales para LSTM
* 🔢 204 secuencias (train/val/test)
* 📊 Formato: 12 meses × N features
* **Usar en:** Módulos de Deep Learning, forecasting avanzado

**Tabla 3: `dl_metadata_lstm`**
* ⚙️ Metadatos + scaler serializado
* 📊 Parámetros del modelo
* **Usar en:** Reconstruir pipeline, desnormalizar predicciones

### 💻 Patrón de Uso en Otros Notebooks

Al inicio de cualquier notebook:

```python
# Definir referencias
CATALOG = "pandito_ds"
SCHEMA = "default"

# Cargar datos
df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()

print(f"✅ Datos cargados: {len(df):,} registros")
```

### ✨ Beneficios de Este Approach

✅ **Consistencia:** Todos usan los mismos datos  
✅ **Reproducibilidad:** Ejecuta una vez, usa everywhere  
✅ **Colaboración:** Equipo comparte datasets  
✅ **Realismo:** Datos más complejos que ejemplos simples  
✅ **Persistencia:** Unity Catalog guarda permanentemente

---


**➡️ [Módulo 01: Entorno Databricks Free Edition & GitHub](../01_Entorno_Databricks_Free_Edition_GitHub/)**

Aprende a configurar tu workspace, conectar GitHub y dominar el entorno de desarrollo.

---

<div align="center">

### 🧪 Tu Superpoder Está Activado

**"Con Genie Code, tu única limitación es tu imaginación, no tu memoria de sintaxis."**

[📖 Volver al Índice Principal](../README.md)

</div>