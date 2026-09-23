# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🚀 Módulo 18 - Notebook 04: Setup Portafolio Oficial GitHub
# MAGIC
# MAGIC ## 📦 Publicación y Portfolio Profesional
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 18 - Proyectos Integradores y GitHub  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟢 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Crear** repositorio profesional en GitHub  
# MAGIC ✅ **Documentar** proyectos con README efectivos  
# MAGIC ✅ **Organizar** portafolio de Data Science  
# MAGIC ✅ **Publicar** notebooks en GitHub  
# MAGIC ✅ **Destacar** en procesos de selección
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Todos los módulos 01-17 completados
# MAGIC * ✅ Cuenta de GitHub creada
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. Estructura de Portfolio
# MAGIC 2. README Profesional
# MAGIC 3. Documentación de Proyectos
# MAGIC 4. GitHub Pages
# MAGIC 5. Próximos Pasos
# MAGIC 6. 🎓 ¡FELICITACIONES! Completaste el curso

# COMMAND ----------

# DBTITLE 1,💾 Verificar Entorno
import pandas as pd
import os
from datetime import datetime

print("💾 VERIFICACIÓN DE ENTORNO")
print("="*70)

print(f"\n✅ Versión de Pandas: {pd.__version__}")
try:
    import pyspark
    print(f"✅ PySpark disponible")
except:
    print("ℹ️  PySpark no disponible")

print(f"\n📊 RESUMEN DEL CURSO COMPLETADO:")
print(f"   • Módulos completados: 18 (01-18)")
print(f"   • Notebooks totales: ~65")
print(f"   • Proyectos integradores: 3 (Auditoría, Cash Flow, Geoespacial)")
print(f"   • Tecnologías: Python, Pandas, PySpark, SQL, Plotly, MLflow, Genie Code")
print(f"   • Fecha de finalización: {datetime.now().strftime('%Y-%m-%d')}")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Portfolio GitHub
# MAGIC %md
# MAGIC ## 📚 Teoría: Portfolio Profesional en GitHub
# MAGIC
# MAGIC ### 🚀 ¿Por qué un Portfolio?
# MAGIC
# MAGIC **Portfolio = tu carta de presentación profesional:**
# MAGIC
# MAGIC * 💼 **Empleo:** Reclutadores buscan en GitHub
# MAGIC * 🎯 **Credibilidad:** Demuestra skills reales
# MAGIC * 🚀 **Networking:** La comunidad te encuentra
# MAGIC * 💰 **Freelance:** Clientes ven tu trabajo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📦 Estructura Recomendada del Portfolio
# MAGIC
# MAGIC ```
# MAGIC tu-usuario.github.io/
# MAGIC ├── README.md              ← Presentación profesional
# MAGIC ├── projects/
# MAGIC │   ├── 01-auditoria/      ← Proyecto de Auditoría
# MAGIC │   │   ├── README.md       ← Descripción del proyecto
# MAGIC │   │   ├── notebook.ipynb  ← Código
# MAGIC │   │   └── images/        ← Screenshots
# MAGIC │   ├── 02-cashflow/       ← Análisis Financiero
# MAGIC │   └── 03-geoespacial/    ← Big Data Geoespacial
# MAGIC ├── skills/                ← Tecnologías dominadas
# MAGIC └── contact/               ← Información de contacto
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📝 README Profesional: Qué Incluir
# MAGIC
# MAGIC 1. **Título atractivo** - Tu nombre + especialidad
# MAGIC 2. **Bio corta** - Quién eres, qué haces
# MAGIC 3. **Skills destacadas** - Python, SQL, PySpark, ML, etc.
# MAGIC 4. **Proyectos** - 3 mejores con links y descripciones
# MAGIC 5. **Contacto** - Email, LinkedIn
# MAGIC 6. **GitHub Stats** - Contribuciones, repos
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎓 ¡FELICITACIONES!
# MAGIC
# MAGIC Has completado **Saliendo de lo Pandito v4**:
# MAGIC * ✅ 18 módulos de analítica moderna
# MAGIC * ✅ Python, Pandas, PySpark, SQL, ML
# MAGIC * ✅ Datos reales de Los Andes Market
# MAGIC * ✅ 3 proyectos portfolio-ready
# MAGIC * ✅ Genie Code, Dashboards, MLflow
# MAGIC
# MAGIC **"De Excel a PySpark, de analista a científico de datos"** 🚀

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import os
from datetime import datetime

print("💻 SETUP: PORTAFOLIO GITHUB")
print("="*70)

print("\n🎯 PROYECTOS PARA TU PORTFOLIO:")
projects = [
    {"nombre": "18_01 - Auditoría Automatizada", "skills": "Pandas, NumPy, SciPy, SQL"},
    {"nombre": "18_02 - Análisis Financiero y Cash Flow", "skills": "Pandas, Plotly, SQL"},
    {"nombre": "18_03 - Geoespacial Big Data con H3", "skills": "PySpark, GeoPandas, H3, SQL"}
]
for p in projects:
    print(f"   📁 {p['nombre']}")
    print(f"      Skills: {p['skills']}")

print("\n📋 CHECKLIST PARA PUBLICAR:")
checklist = [
    "1. Crear repo en GitHub: tu-usuario.github.io",
    "2. Clonar repo en Databricks via Git",
    "3. Copiar proyectos (18_01, 18_02, 18_03)",
    "4. Crear README.md profesional",
    "5. Agregar screenshots de dashboards",
    "6. Commit y Push desde Databricks",
    "7. Activar GitHub Pages (Settings > Pages)",
    "8. Compartir URL en LinkedIn"
]
for item in checklist:
    print(f"   {item}")

print(f"\n🎓 ¡FELICITACIONES! Has completado Saliendo de lo Pandito v4")
print(f"   Fecha de finalización: {datetime.now().strftime('%Y-%m-%d')}")
print(f"   📦 18 módulos | ~65 notebooks | 3 proyectos portfolio-ready")
print(f"\n   🚀 De Excel a PySpark, de analista a científico de datos")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 18_04
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Estructura de portfolio profesional:**
# MAGIC    ```markdown
# MAGIC    tu-usuario.github.io/
# MAGIC    ├── README.md              # Presentacion profesional
# MAGIC    ├── projects/
# MAGIC    │   ├── 01-auditoria/      # Proyecto de Auditoria
# MAGIC    │   ├── 02-cashflow/       # Analisis Financiero
# MAGIC    │   └── 03-geoespacial/    # Big Data Geoespacial
# MAGIC    ├── skills/               # Tecnologias dominadas
# MAGIC    └── contact/               # Informacion de contacto
# MAGIC    ```
# MAGIC
# MAGIC 2. **README profesional:**
# MAGIC    ```markdown
# MAGIC    # Tu Nombre - Data Scientist
# MAGIC    
# MAGIC    ## Sobre mi
# MAGIC    Analista de datos especializado en Python, SQL y PySpark...
# MAGIC    
# MAGIC    ## Skills
# MAGIC    Python | Pandas | PySpark | SQL | MLflow | Plotly | GeoPandas | H3
# MAGIC    
# MAGIC    ## Proyectos Destacados
# MAGIC    - [Auditoria Automatizada](link) - Deteccion de anomalias con Z-score e IQR
# MAGIC    - [Cash Flow Analysis](link) - Modelo financiero end-to-end con escenarios
# MAGIC    - [Geoespacial Big Data](link) - Optimizacion de sucursales con H3 y PySpark
# MAGIC    ```
# MAGIC
# MAGIC 3. **Publicacion desde Databricks a GitHub:**
# MAGIC    ```python
# MAGIC    # Flujo: Databricks Git Folder > Commit > Push > GitHub Pages
# MAGIC    # 1. Clonar repo en Databricks via Git
# MAGIC    # 2. Copiar notebooks de proyectos (18_01, 18_02, 18_03)
# MAGIC    # 3. Crear README.md profesional
# MAGIC    # 4. Commit y Push desde Databricks
# MAGIC    # 5. Activar GitHub Pages (Settings > Pages)
# MAGIC    # 6. Compartir URL en LinkedIn
# MAGIC    ```
# MAGIC
# MAGIC 4. **Proyectos portfolio-ready:**
# MAGIC    - **Auditoria:** Pandas, NumPy, SciPy, Z-score, IQR, Ley de Benford
# MAGIC    - **Cash Flow:** Pandas, Plotly, ratios financieros, escenarios
# MAGIC    - **Geoespacial:** PySpark, GeoPandas, H3, optimizacion de sucursales
# MAGIC
# MAGIC 5. **Checklist de publicacion:**
# MAGIC    - Repositorio creado en GitHub
# MAGIC    - README con bio, skills y proyectos
# MAGIC    - Screenshots de dashboards incluidos
# MAGIC    - GitHub Pages activado
# MAGIC    - URL compartida en LinkedIn
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Guía rápida de Portfolio GitHub
# MAGIC
# MAGIC **Caso 1: Estructurar el repositorio**
# MAGIC ```bash
# MAGIC # Crear repo: tu-usuario.github.io
# MAGIC # Clonar en Databricks via Git folder
# MAGIC mkdir -p projects/01-auditoria/images
# MAGIC mkdir -p projects/02-cashflow/images
# MAGIC mkdir -p projects/03-geoespacial/images
# MAGIC ```
# MAGIC
# MAGIC **Caso 2: README profesional del repositorio**
# MAGIC ```markdown
# MAGIC # Cristian Ortega - Data Scientist
# MAGIC
# MAGIC 📊 Analista de datos especializado en Python, SQL y PySpark.
# MAGIC
# MAGIC ## Skills
# MAGIC Python | Pandas | PySpark | SQL | MLflow | Plotly | GeoPandas | H3
# MAGIC
# MAGIC ## Proyectos
# MAGIC 1. [Auditoria Automatizada](projects/01-auditoria/) - Deteccion de anomalias
# MAGIC 2. [Cash Flow Analysis](projects/02-cashflow/) - Modelo financiero
# MAGIC 3. [Geoespacial Big Data](projects/03-geoespacial/) - H3 + PySpark
# MAGIC
# MAGIC ## Contacto
# MAGIC 📧 cristian@example.com | 💼 LinkedIn | 🐙 GitHub
# MAGIC ```
# MAGIC
# MAGIC **Caso 3: README por proyecto**
# MAGIC ```markdown
# MAGIC # Auditoria Automatizada de Ventas
# MAGIC
# MAGIC ## Descripcion
# MAGIC Pipeline de auditoria que analiza 100% de registros para detectar
# MAGIC anomalias usando Z-score, IQR y Ley de Benford.
# MAGIC
# MAGIC ## Tecnologias
# MAGIC Python, Pandas, NumPy, SciPy, Plotly
# MAGIC
# MAGIC ## Resultados
# MAGIC - 300 registros analizados en < 5 segundos
# MAGIC - 12 anomalias detectadas (4% del total)
# MAGIC - 3 criticas priorizadas para investigacion
# MAGIC
# MAGIC ## Como ejecutar
# MAGIC 1. Abrir notebook en Databricks
# MAGIC 2. Ejecutar celdas en orden
# MAGIC 3. Revisar dashboard de hallazgos
# MAGIC ```
# MAGIC
# MAGIC **Caso 4: Activar GitHub Pages**
# MAGIC ```bash
# MAGIC # Settings > Pages > Source: main branch > /root
# MAGIC # URL: https://tu-usuario.github.io
# MAGIC # Tu portfolio esta vivo y accesible
# MAGIC ```
# MAGIC
# MAGIC **Caso 5: Compartir en LinkedIn**
# MAGIC ```markdown
# MAGIC He completado "Saliendo de lo Pandito v4" - 18 modulos de
# MAGIC analitica moderna con Python, PySpark, SQL y ML.
# MAGIC
# MAGIC Mi portfolio: https://tu-usuario.github.io
# MAGIC
# MAGIC Proyectos:
# MAGIC 1. Auditoria automatizada con deteccion de anomalias
# MAGIC 2. Modelo financiero de Cash Flow con escenarios
# MAGIC 3. Big Data geoespacial con H3 y PySpark
# MAGIC
# MAGIC #DataScience #Python #PySpark #Databricks
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏆 ¡FELICITACIONES! Has completado el curso completo
# MAGIC
# MAGIC **Saliendo de lo Pandito v4 - Recorrido completo:**
# MAGIC
# MAGIC | Módulo | Tema | Notebooks |
# MAGIC |--------|------|-----------|
# MAGIC | 01 | Entorno Databricks y Git | 2 |
# MAGIC | 02 | Guía Rápida Genie Code | 5 |
# MAGIC | 03 | Fundamentos Python | 4 |
# MAGIC | 04 | Limpieza y Preparación | 5 |
# MAGIC | 05 | Reshaping y Conciliaciones | 4 |
# MAGIC | 06 | Agregaciones y KPIs | 4 |
# MAGIC | 07 | Series de Tiempo | 4 |
# MAGIC | 08 | Visualización Plotly | 5 |
# MAGIC | 09 | GeoPandas | 3 |
# MAGIC | 10 | Uber H3 | 3 |
# MAGIC | 11 | PySpark Core | 3 |
# MAGIC | 12 | PySpark Transformación | 3 |
# MAGIC | 13 | Performance Spark | 3 |
# MAGIC | 14 | SQL Editor | 4 |
# MAGIC | 15 | Delta Lake | 5 |
# MAGIC | 16 | Genie AI/BI | 4 |
# MAGIC | 17 | Machine Learning | 6 |
# MAGIC | 18 | Proyectos Integradores | 4 |
# MAGIC
# MAGIC **Total: 18 módulos | ~65 notebooks | 3 proyectos portfolio-ready**
# MAGIC
# MAGIC **Habilidades adquiridas:**
# MAGIC * ✅ Python, Pandas, NumPy, SciPy
# MAGIC * ✅ PySpark, Spark SQL, Delta Lake
# MAGIC * ✅ SQL Editor, Unity Catalog, gobernanza
# MAGIC * ✅ Plotly, AI/BI Dashboards, Genie Spaces
# MAGIC * ✅ GeoPandas, H3, analítica geoespacial
# MAGIC * ✅ MLflow, regresión, clasificación, clustering, LSTM
# MAGIC * ✅ ETL automatizado, Bronze/Silver/Gold
# MAGIC * ✅ Git, GitHub, portfolio profesional
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🎓 ¡Curso Completado! Saliendo de lo Pandito v4</h3>
# MAGIC   <p><i>"De Excel a PySpark, de analista a cientifico de datos. El unico limite ahora es tu imaginacion."</i></p>
# MAGIC   <p style="margin-top: 10px; font-size: 1.1em;">🚀 ¡Felicidades, Cristian! 🎉</p>
# MAGIC </div>