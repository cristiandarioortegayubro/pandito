# 📊 Módulo 08: Visualización con Plotly y Dashboards

## 🎯 Objetivo del Módulo

**Transforma datos en insights visuales** con Plotly Express, Plotly Graph Objects, y dashboards interactivos de Databricks.

Una visualización efectiva comunica hallazgos complejos en segundos. Este módulo te enseña a crear gráficos profesionales, interactivos y listos para presentar a stakeholders.

**Al finalizar este módulo podrás:**
* ✅ Crear gráficos interactivos con Plotly Express
* ✅ Personalizar visualizaciones con Graph Objects
* ✅ Construir dashboards ejecutivos en Databricks
* ✅ Aplicar mejores prácticas de visualización de datos
* ✅ Diseñar visualizaciones para storytelling de negocio

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 03-07 completados
* Familiaridad con agregaciones y métricas

**Datasets:**
* Todos los datasets previos (ventas, transacciones, ubicaciones)

**Tiempo estimado:** 4 horas

---

## 📚 Contenido del Módulo

### 08_01_Introduccion_Plotly_Express
**Duración:** 50 min | **Dificultad:** Principiante

**Temas:**
* `px.scatter()`, `px.line()`, `px.bar()`, `px.histogram()`
* Parámetros: color, size, hover_data, facet_col
* Templates: plotly, plotly_white, plotly_dark
* Exportar a HTML estático

**Casos de uso:**
* Scatter plots de correlación precio-demanda
* Line charts de revenue temporal
* Histogramas de distribución de compras

---

### 08_02_Graficos_Avanzados_Plotly
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* `px.box()`, `px.violin()` para distribuciones
* `px.sunburst()`, `px.treemap()` para jerarquías
* `px.funnel()` para conversion funnels
* `px.scatter_mapbox()` para datos geoespaciales
* Animaciones con `animation_frame`

**Aplicaciones:**
* Funnel de conversión e-commerce
* Treemap de revenue por categoría/región
* Boxplot de comparación de KPIs entre segmentos

---

### 08_03_Graph_Objects_y_Personalizacion
**Duración:** 55 min | **Dificultad:** Intermedio-Avanzado

**Temas:**
* `go.Figure()`, `go.Scatter()`, `go.Bar()`
* Múltiples traces en un gráfico
* Ejes secundarios (secondary y-axis)
* Anotaciones, shapes, botones interactivos
* Layout personalizado (títulos, leyendas, grids)

**Casos de uso:**
* Combinar barras (revenue) + línea (margen%) en un gráfico
* Anotar eventos importantes en series temporales
* Crear dashboards de 1 página con subplots

---

### 08_04_Databricks_Dashboards_Interactivos
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* Integración de Plotly con notebooks Databricks
* Widgets para interactividad (dropdowns, sliders)
* `display()` vs `display(fig)` vs `fig.show()`
* Databricks SQL Dashboards
* Conexión de dashboards a queries y notebooks

**Workflow:**
1. Crear análisis en notebook
2. Generar visualizaciones Plotly
3. Publicar dashboard con filtros interactivos
4. Compartir con stakeholders

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar tipos de gráficos disponibles en Plotly
* Identificar componentes de un gráfico (traces, layout, axes)
* Nombrar templates de estilo disponibles

### Nivel 2: Comprensión
* Explicar cuándo usar scatter vs line vs bar
* Describir diferencia entre Plotly Express y Graph Objects
* Interpretar un funnel chart de conversión

### Nivel 3: Aplicación
* Crear gráficos interactivos con px
* Personalizar colores, títulos, leyendas
* Combinar múltiples traces en un gráfico
* Exportar visualización a HTML

### Nivel 4: Análisis
* Decidir tipo de gráfico óptimo según datos y mensaje
* Evaluar efectividad de visualización (claridad, engagement)
* Diseñar dashboard que cuente una historia de negocio

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Dashboard Ejecutivo Interactivo
```
"Crea un dashboard de 1 página con 4 visualizaciones:
1. KPI cards: revenue total, MoM growth %, clientes activos
2. Line chart: evolución mensual de revenue y margen %
3. Bar chart horizontal: top 10 productos por revenue
4. Treemap: distribución de revenue por región > categoría

Usa Plotly con template 'plotly_white'.
Añade título, subtítulo con fecha de actualización.
Todos los gráficos deben compartir paleta de colores corporativa."
```

### Prompt 2: Funnel de Conversión Animado
```
"Visualiza funnel de conversión e-commerce con animación mensual:
Etapas: Visitantes → Carrito → Checkout → Compra

Muestra:
- % de conversión entre etapas
- Etiquetas con cantidad absoluta
- Animación por mes con slider
- Identificación de mes con peor conversión

Usa px.funnel() con animación."
```

### Prompt 3: Análisis Multivariado Scatter
```
"Crea scatter plot interactivo de productos:
- X: precio_unitario
- Y: unidades_vendidas
- Color: categoría
- Tamaño: margen_bruto_total
- Hover: nombre_producto, revenue, margen%

Agrega líneas de tendencia por categoría.
Identifica productos en cada cuadrante:
- Alto precio + Alta demanda (premium)
- Bajo precio + Alta demanda (volumen)
- Alto precio + Baja demanda (nicho)
- Bajo precio + Baja demanda (eliminar)"
```

---

## 🎨 Mejores Prácticas de Visualización

### 1. Elegir el Gráfico Correcto
| Objetivo | Gráfico Recomendado |
|----------|---------------------|
| Comparar categorías | Bar chart |
| Mostrar tendencia temporal | Line chart |
| Distribución de variable | Histogram, box plot |
| Relación entre 2 variables | Scatter plot |
| Parte del total | Pie chart, treemap |
| Flujo o proceso | Funnel, sankey |
| Jerarquía | Sunburst, treemap |

### 2. Principios de Diseño
* **Simplicidad:** Menos es más - elimina elementos innecesarios
* **Contraste:** Destaca lo importante con color/tamaño
* **Consistencia:** Usa misma paleta y estilos en todo el dashboard
* **Accesibilidad:** Colores distinguibles para daltónicos
* **Contexto:** Siempre incluye títulos, etiquetas de ejes, unidades

### 3. Storytelling con Datos
* **Comienza con el mensaje clave** (KPI principal)
* **Agrega contexto** (comparación temporal, benchmark)
* **Drill-down progresivo** (del agregado al detalle)
* **Termina con acción** (recomendación, próximos pasos)

---

## 🔧 Solución de Problemas

### Problema 1: Gráfico no se muestra en Databricks
**Causa:** Usando `fig.show()` en vez de `display()`  
**Solución:** Usa `display(fig)` en notebooks Databricks
```python
import plotly.express as px
fig = px.bar(df, x='mes', y='revenue')
display(fig)  # ✅ Correcto en Databricks
```

### Problema 2: Leyenda ocupa mucho espacio
**Solución:** Ajusta posición y orientación
```python
fig.update_layout(
    legend=dict(
        orientation="h",  # horizontal
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
```

### Problema 3: Colores no distinguibles
**Solución:** Usa paletas accesibles
```python
# Paleta colorblind-friendly
px.bar(df, x='region', y='revenue', 
       color_discrete_sequence=px.colors.qualitative.Safe)
```

---

## 📖 Recursos Adicionales

### Documentación
* [Plotly Express](https://plotly.com/python/plotly-express/)
* [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
* [Databricks Dashboards](https://docs.databricks.com/dashboards/index.html)

### Paletas de Colores
* [ColorBrewer](https://colorbrewer2.org/)
* [Plotly Color Scales](https://plotly.com/python/builtin-colorscales/)

### Inspiración
* [Financial Times Graphics](https://www.ft.com/graphics)
* [Tableau Public Gallery](https://public.tableau.com/app/discover)

---

## ✅ Checklist

**Plotly Express:**
- [ ] Gráficos básicos (scatter, line, bar, histogram)
- [ ] Parámetros de estilo (color, size, hover)
- [ ] Templates y temas
- [ ] Exportar a HTML

**Gráficos Avanzados:**
- [ ] Box plots y violin plots
- [ ] Treemap y sunburst
- [ ] Funnel charts
- [ ] Animaciones

**Graph Objects:**
- [ ] Múltiples traces
- [ ] Ejes secundarios
- [ ] Anotaciones
- [ ] Layout personalizado

**Databricks:**
- [ ] Integración con display()
- [ ] Widgets interactivos
- [ ] Publicar dashboards

---

## 🚀 Próximo Módulo

**➡️ [Módulo 09: Analítica Geoespacial](../09_Analitica_Geoespacial_GeoPandas/)**

---

[📖 Volver al Índice](../README.md)
