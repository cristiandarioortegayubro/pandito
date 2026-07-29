# 📊 Saliendo de lo Pandito v4
### Analítica de Datos para Negocios con Databricks Free Edition & Genie Code

[![Databricks](https://img.shields.io/badge/Databricks-Free_Edition-FF3621?style=flat&logo=databricks)](https://community.cloud.databricks.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-E25A1C?style=flat&logo=apache-spark)](https://spark.apache.org/)
[![Genie](https://img.shields.io/badge/AI-Genie_Code-9B59B6?style=flat)](https://www.databricks.com/)

---

## 🎯 Sobre el Libro

**"Saliendo de lo Pandito"** es un libro práctico diseñado para profesionales de negocios, analistas y emprendedores que desean dominar el análisis de datos moderno sin necesidad de un background técnico profundo.

### ¿Por qué "Saliendo de lo Pandito"?
El título hace referencia a **Pandas**, la biblioteca más popular de Python para análisis de datos. El libro comienza con Pandas y te lleva paso a paso hacia herramientas empresariales de Big Data como **PySpark**, analítica geoespacial, visualización interactiva y **analítica agéntica con IA**.

---

## 👥 ¿Para Quién es Este Libro?

✅ **Analistas de Negocios** que trabajan con Excel y quieren escalar a Big Data  
✅ **Profesionales de Finanzas/Contabilidad** que necesitan automatizar KPIs y reportes  
✅ **Emprendedores y Product Managers** que quieren tomar decisiones basadas en datos  
✅ **Estudiantes y Autodidactas** sin experiencia previa en programación  
✅ **Equipos de Data** que buscan democratizar analítica con herramientas de IA

---

## 🛠️ Tecnologías y Herramientas

### Plataforma Principal: **Databricks Free Edition (Community Cloud)**
- ✨ **100% Gratuita** - Sin tarjeta de crédito requerida
- ☁️ **Compute Serverless** - Sin configuración de infraestructura
- 🔄 **Integración Git** - Sincronización directa con GitHub
- 📊 **Notebooks Interactivos** - Jupyter-style en la nube
- 🧠 **Genie Code & Assistant** - Analítica asistida por IA

### Stack Tecnológico Completo:
| Capa | Tecnologías |
|------|-------------|
| **Lenguaje Base** | Python 3.10+ |
| **Análisis Tabulado** | Pandas, NumPy |
| **Big Data** | PySpark, Delta Lake |
| **Visualización** | Plotly, Databricks Dashboards |
| **Geoespacial** | GeoPandas, Uber H3 |
| **IA Generativa** | Genie Code, Databricks Assistant |
| **Versionamiento** | Git, GitHub |

---

## 📚 Estructura del Repositorio

El repositorio contiene **16 módulos progresivos** con más de **60 notebooks prácticos**:

### 🔰 Fundamentos (Módulos 1-3)
- **01** - Entorno Databricks Free Edition & GitHub
- **02** - NumPy y Vectorización Financiera
- **03** - Pandas: Series y DataFrames

### 📊 Manipulación de Datos (Módulos 4-6)
- **04** - Limpieza y Preparación de Datos
- **05** - Reshaping y Conciliaciones
- **06** - Agregaciones y Métricas KPI

### 📈 Análisis Especializado (Módulos 7-10)
- **07** - Series de Tiempo Financieras
- **08** - Visualización con Plotly & Dashboards
- **09** - Analítica Geoespacial con GeoPandas
- **10** - Indexación Hexagonal (Uber H3)

### ⚡ Big Data & PySpark (Módulos 11-14)
- **11** - PySpark Core y SparkSession
- **12** - Transformación Avanzada en PySpark
- **13** - PySpark SQL, Window Functions & Delta Lake
- **14** - Optimización de ETL Pipelines

### 🤖 IA & Proyectos (Módulos 15-16)
- **15** - Analítica Agéntica con Genie Code
- **16** - Proyectos Integradores & GitHub Portfolio

---

## 🚀 Guía de Inicio Rápido

### Paso 1: Crear Cuenta en Databricks Community
```bash
1. Visita: https://community.cloud.databricks.com/
2. Regístrate con tu email (sin tarjeta de crédito)
3. Verifica tu cuenta por email
```

### Paso 2: Clonar Este Repositorio
```bash
# Opción A: Desde la interfaz de Databricks
1. En Databricks, ve a "Repos" en el menú lateral
2. Click en "Add Repo"
3. Pega la URL de este repositorio
4. Click "Create Repo"

# Opción B: Git Clone (si tienes configurado Git)
git clone https://github.com/[tu-usuario]/pandito.git
```

### Paso 3: Configurar Compute
```python
# El compute serverless se selecciona automáticamente
# Lenguajes soportados: Python, SQL, sh
# NO soportados en Free Edition: R, Scala
```

### Paso 4: Abrir el Primer Notebook
```
pandito/
└── 01_Entorno_Databricks_Free_Edition_GitHub/
    └── 01_01_Configuracion_Databricks_y_Git.ipynb  ⬅️ EMPIEZA AQUÍ
```

---

## 🧠 Cómo Usar Genie Code Durante el Libro

**Genie Code** es tu asistente de IA integrado en Databricks. Úsalo para:

1. **Generar Código Automáticamente**
   ```
   Prompt: "Crea un DataFrame de ventas y calcula el total por categoría"
   → Genie genera el código PySpark/Pandas completo
   ```

2. **Depurar Errores**
   ```
   Prompt: "Este código da KeyError, ¿cómo lo arreglo?"
   → Genie analiza el error y sugiere soluciones
   ```

3. **Optimizar Consultas**
   ```
   Prompt: "Optimiza esta consulta SQL para mejor performance"
   → Genie refactoriza con mejores prácticas
   ```

4. **Explicar Conceptos**
   ```
   Prompt: "Explica qué es un window function con ejemplo"
   → Genie genera explicación + código ejecutable
   ```

> 💡 **Recomendación**: Después de cada módulo, pídele a Genie que genere ejercicios adicionales para reforzar lo aprendido.

---

## 📖 Orden de Estudio Recomendado

### 🔹 Track Básico (8-10 semanas)
Ideal para principiantes absolutos:
```
Módulos: 01 → 03 → 04 → 06 → 08 → 15
```

### 🔸 Track Intermedio (12-14 semanas)
Para quienes conocen Python básico:
```
Módulos: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 11 → 12 → 15 → 16
```

### 🔺 Track Avanzado (16-20 semanas)
Ruta completa para dominio total:
```
Módulos: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16
```

---

## 💼 Casos de Uso Empresariales Cubiertos

✔️ **Finanzas**: Cálculo de EBITDA, márgenes, análisis de P&L, ratios financieros  
✔️ **Marketing**: ARPU, CAC, LTV, Churn Rate, cohort analysis  
✔️ **Operaciones**: Análisis de inventario, optimización de rutas (H3), forecasting  
✔️ **Ventas**: Dashboards ejecutivos, waterfalls de revenue, análisis territorial  
✔️ **Riesgo**: Heatmaps de correlación, análisis de volatilidad, stress testing  

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

Gracias a la comunidad de Databricks, los contribuidores de librerías open-source (Pandas, PySpark, Plotly, GeoPandas), y a todos los estudiantes y profesionales que han brindado feedback durante el desarrollo de este material.

---

<div align="center">

### 🎓 ¡Comienza Tu Viaje en Analítica de Datos Hoy!

[📂 Ver Módulos](./01_Entorno_Databricks_Free_Edition_GitHub) | [🧠 Guía Genie Code](./00_Guia_Rapida_Genie_Code) | [📊 Datasets](./datasets)

**"De Excel a PySpark, de analista a científico de datos"**

</div>

---

## ✅ Compatibilidad Serverless Compute

Este libro está **100% verificado** para funcionar con **Databricks Serverless Compute** en Free Edition.

### Estado de Verificación

- **Notebooks analizados:** 60
- **Compatibilidad:** ✅ 100%
- **Lenguajes usados:** Python, SQL, sh (todos compatibles)
- **Sin código Scala/R:** ✅ Confirmado
- **Sin acceso DBFS directo:** ✅ Todas las rutas usan `/Workspace/`

### Ventajas de Serverless para Este Libro

1. ⚡ **Inicio instantáneo** - Sin tiempo de warmup de cluster
2. 📈 **Escalado automático** - Se ajusta según tu carga de trabajo
3. 💰 **Costo optimizado** - Solo pagas por lo que usas
4. 🔧 **Sin configuración** - No administras clusters manualmente
5. 🎓 **Ideal para aprender** - Perfecto para Databricks Free Edition

### Verificación de Entorno

Todos los notebooks principales incluyen una celda de verificación al inicio:

```python
# 🔍 Verificación rápida
import sys
print(f"✅ Python {sys.version.split()[0]}")
try:
    print(f"✅ Spark {spark.version}")
except:
    print("ℹ️  Spark no disponible")
print("✅ Serverless Compute compatible")
```

Para información detallada sobre compatibilidad, consulta: [SERVERLESS_COMPATIBILITY.md](./SERVERLESS_COMPATIBILITY.md)

---
