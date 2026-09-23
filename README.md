# 📊 Saliendo de lo Pandito - 1º Ed.
### Analítica de Datos para Negocios con Databricks Free Edition & Genie Code

[![Databricks](https://img.shields.io/badge/Databricks-Free_Edition-FF3621?style=flat&logo=databricks)](https://community.cloud.databricks.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-E25A1C?style=flat&logo=apache-spark)](https://spark.apache.org/)
[![Genie](https://img.shields.io/badge/AI-Genie_Code-9B59B6?style=flat)](https://www.databricks.com/)

---

## 🎯 Sobre el Libro

**"Saliendo de lo Pandito"** es un libro práctico diseñado para profesionales de negocios, analistas y emprendedores que desean dominar el análisis de datos moderno.

### ¿Por qué "Saliendo de lo Pandito"?
El título hace referencia a **Pandas**, la biblioteca más popular de Python para análisis de datos. El libro comienza con Pandas y te lleva paso a paso hacia herramientas empresariales más profundas como **PySpark**, analítica geoespacial, visualización interactiva y **analítica agéntica con IA**.

---

## 👥 ¿Para quién es este Libro?

✅ **Analistas de Negocios** que trabajan con Excel y quieren escalar a Big Data  
✅ **Profesionales de Ciencias Económicas** que necesitan automatizar KPIs y reportes  
✅ **Emprendedores y Product Managers** que quieren tomar decisiones basadas en datos  
✅ **Estudiantes y Autodidactas** sin experiencia previa en programación  
✅ **Equipos de Data Analitycs** que buscan democratizar analítica con herramientas de IA

---

## 🛠️ Tecnologías y herramientas

### Plataforma principal: **Databricks Free Edition**
- ✨ **100% Gratuita** - Sin tarjeta de crédito requerida
- ☁️ **Compute Serverless** - Sin configuración de infraestructura
- 🔄 **Integración Git** - Sincronización directa con GitHub
- 📊 **Notebooks Interactivos** - Jupyter-style en la nube
- 🧠 **Genie Code & Assistant** - Analítica asistida por IA

### Stack tecnológico completo:
| Capa | Tecnologías |
|------|-------------|
| **Lenguaje Base** | Python 3.10+ |
| **Análisis Tabulado** | Pandas |
| **Big Data** | PySpark, Delta Lake |
| **SQL** | Databricks SQL Editor, Unity Catalog |
| **Visualización** | Plotly, AI/BI Dashboards (Lakeview) |
| **Geoespacial** | GeoPandas, Uber H3 |
| **Machine Learning** | MLflow, scikit-learn, TensorFlow/Keras |
| **IA Generativa** | Genie Code, Genie Spaces, Databricks Assistant |
| **Versionamiento** | Git, GitHub |

---

## 📚 Estructura del repositorio

El repositorio contiene **18 módulos progresivos** con más de **60 notebooks prácticos**:

### 🔰 Fundamentos (Módulos 1-4)
- **01** - Entorno Databricks Free Edition & GitHub
- **02** - Python: Fundamentos y Estructuras de Control
- **03** - Pandas: Series y DataFrames
- **04** - Genie Code: Tu Copiloto de IA

### 📊 Manipulación de Datos (Módulos 5-7)
- **05** - Limpieza y Preparación de Datos
- **06** - Reshaping y Conciliaciones
- **07** - Agregaciones y Métricas KPI

### 📈 Análisis Especializado (Módulos 8-11)
- **08** - Series de Tiempo Financieras
- **09** - Visualización con Plotly
- **10** - Analítica Geoespacial con GeoPandas
- **11** - Indexación Hexagonal (Uber H3)

### ⚡ Big Data & SQL (Módulos 12-15)
- **12** - PySpark Core y SparkSession
- **13** - PySpark Transformación Avanzada
- **14** - SQL Editor y Databricks SQL
- **15** - Delta Lake, Window Functions y Optimización

### 🤖 IA, ML & Proyectos (Módulos 16-18)
- **16** - Genie Spaces, Dashboards AI/BI y ETL
- **17** - Machine Learning con MLflow
- **18** - Proyectos Integradores & GitHub Portfolio

---

## 🚀 Guía de inicio rápido

### Paso 1: Crear cuenta en Databricks Free Edition
```bash
1. Visita: https://databricks.com/
2. Regístrate con tu email (sin tarjeta de crédito)
3. Verifica tu cuenta por email
```

### Paso 2: Clonar este repositorio
```bash
# Opción A: Desde la interfaz de Databricks
1. En Databricks, ve a "Repos" en el menú lateral
2. Click en "Add Repo"
3. Pega la URL de este repositorio
4. Click "Create Repo"

# Opción B: Git Clone (si tienes configurado Git)
git clone https://github.com/cristiandarioortegayubro/pandito.git
```

### Paso 3: Configurar Compute
```python
# El compute serverless se selecciona automáticamente
# Lenguajes soportados: Python, SQL, sh
# NO soportados en Free Edition: R, Scala
```

### Paso 4: Abrir el primer notebook
```
pandito/
└── 01_Entorno_Databricks_Free_Edition_GitHub/
    └── 01_01_Configuracion_Databricks_y_Git.ipynb  ⬅️ EMPIEZA AQUÍ
```

---

## 🧠 Cómo usar Genie Code durante el libro

**Genie Code** es tu asistente de IA integrado en Databricks. Úsalo para:

1. **Generar código automáticamente**
   ```
   Prompt: "Crea un DataFrame de ventas y calcula el total por categoría"
   → Genie genera el código PySpark/Pandas completo
   ```

2. **Depurar errores**
   ```
   Prompt: "Este código da KeyError, ¿cómo lo arreglo?"
   → Genie analiza el error y sugiere soluciones
   ```

3. **Optimizar consultas**
   ```
   Prompt: "Optimiza esta consulta SQL para mejor performance"
   → Genie refactoriza con mejores prácticas
   ```

4. **Explicar conceptos**
   ```
   Prompt: "Explica qué es un window function con ejemplo"
   → Genie genera explicación + código ejecutable
   ```

> 💡 **Recomendación**: Después de cada módulo, pídele a Genie que genere ejercicios adicionales para reforzar lo aprendido.

---

## 📖 Orden de estudio recomendado

### 🔹 Track Básico (8-10 semanas)
Ideal para principiantes absolutos:
```
Módulos: 01 → 02 → 03 → 04 → 07 → 09 → 16 → 18
```

### 🔸 Track Intermedio (12-14 semanas)
Para quienes conocen Python básico:
```
Módulos: 01 → 02 → 03 → 04 → 05 → 07 → 09 → 12 → 14 → 16 → 17 → 18
```

### 🔺 Track Avanzado (18-22 semanas)
Ruta completa para dominio total:
```
Módulos: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18
```

---

## 💼 Casos de uso empresariales cubiertos

✔️ **Finanzas**: Cálculo de EBITDA, márgenes, análisis de P&L, ratios financieros  
✔️ **Marketing**: ARPU, CAC, LTV, Churn Rate, cohort analysis  
✔️ **Operaciones**: Análisis de inventario, optimización de rutas (H3), forecasting  
✔️ **Ventas**: Dashboards ejecutivos, waterfalls de revenue, análisis territorial  
✔️ **Riesgo**: Heatmaps de correlación, análisis de volatilidad, stress testing  
✔️ **Machine Learning**: Regresión, clasificación, clustering, experimentos con MLflow  
✔️ **SQL Analytics**: Consultas SQL, vistas, Unity Catalog, Databricks SQL Editor  
✔️ **IA Agéntica**: Genie Spaces, consultas conversacionales, generación de código  

---

## 🤝 Contribuciones

Este es un proyecto educativo en evolución. Si encuentras errores, tienes sugerencias o quieres contribuir:

1. **Reporta Issues**: Usa GitHub Issues para errores o sugerencias
2. **Pull Requests**: Se aceptan mejoras a notebooks y documentación
3. **Feedback**: Comparte tu experiencia usando Discussions

---

## 📧 Contacto

- **Autor**: Cristian Dario Ortega Yubro 
- **Email**: cristiandarioortega@gmail.com - cortega@uda.edu.ar
- **LinkedIn**: [linkedin.com/in/cristiandarioortegayubro](https://linkedin.com/in/cristiandarioortegayubro)  

---

## 📜 Licencia

Este material educativo está disponible bajo licencia MIT. Puedes usar, modificar y distribuir el contenido libremente con atribución al autor original.

---

## ⭐ Agradecimientos

Gracias a la comunidad de Databricks, los contribuidores de librerías open-source (Pandas, PySpark, Plotly, GeoPandas, MLflow, scikit-learn), y a todos los estudiantes y profesionales que han brindado feedback durante el desarrollo de este material.

---
