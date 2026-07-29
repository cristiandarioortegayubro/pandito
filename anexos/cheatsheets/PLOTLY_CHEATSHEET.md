# 📊 Plotly Cheatsheet - Saliendo de lo Pandito v4

**Referencia rápida de Plotly para visualizaciones interactivas**

---

## 📦 Importación y Setup

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
```

---

## 🎨 Plotly Express (Alto Nivel - Recomendado)

### Scatter Plot
```python
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', 
                 color='species', size='petal_length',
                 title='Iris Dataset')
fig.show()
```

### Line Chart
```python
df = pd.DataFrame({
    'mes': ['Ene', 'Feb', 'Mar', 'Abr'],
    'ventas': [100, 150, 120, 180]
})
fig = px.line(df, x='mes', y='ventas', 
              title='Ventas Mensuales',
              markers=True)
fig.show()
```

### Bar Chart
```python
fig = px.bar(df, x='categoria', y='ventas',
             color='region',
             title='Ventas por Categoría',
             barmode='group')  # 'stack', 'group', 'overlay'
fig.show()
```

### Horizontal Bar
```python
fig = px.bar(df, x='ventas', y='producto',
             orientation='h',
             title='Top 10 Productos')
fig.show()
```

### Histogram
```python
fig = px.histogram(df, x='edad', nbins=20,
                   title='Distribución de Edades',
                   color='genero')
fig.show()
```

### Box Plot
```python
fig = px.box(df, x='categoria', y='precio',
             title='Distribución de Precios',
             points='all')  # 'all', 'outliers', False
fig.show()
```

### Pie Chart
```python
fig = px.pie(df, values='cantidad', names='categoria',
             title='Proporción por Categoría',
             hole=0.3)  # 0.0 = pie, >0 = donut
fig.show()
```

### Sunburst (Jerárquico)
```python
fig = px.sunburst(df, path=['region', 'ciudad', 'sucursal'],
                  values='ventas',
                  title='Ventas Jerárquicas')
fig.show()
```

### Treemap
```python
fig = px.treemap(df, path=['region', 'producto'],
                 values='ventas',
                 color='margen',
                 title='Ventas y Margen')
fig.show()
```

### Heatmap
```python
# Matriz de correlación
corr = df.corr()
fig = px.imshow(corr,
                text_auto=True,
                title='Matriz de Correlación',
                color_continuous_scale='RdBu_r')
fig.show()
```

### Scatter Matrix
```python
fig = px.scatter_matrix(df,
                        dimensions=['col1', 'col2', 'col3'],
                        color='categoria',
                        title='Scatter Matrix')
fig.show()
```

### Facet / Subplots Automáticos
```python
fig = px.scatter(df, x='x', y='y',
                 facet_col='categoria',  # Columnas
                 facet_row='region',     # Filas
                 title='Faceted Plot')
fig.show()
```

---

## 🏗️ Graph Objects (Bajo Nivel - Mayor Control)

### Scatter Plot Básico
```python
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17],
    mode='lines+markers',
    name='Serie 1'
))
fig.update_layout(title='Mi Gráfico')
fig.show()
```

### Múltiples Trazas
```python
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['fecha'], y=df['ventas'], name='Ventas'))
fig.add_trace(go.Scatter(x=df['fecha'], y=df['objetivo'], name='Objetivo'))
fig.update_layout(title='Ventas vs Objetivo')
fig.show()
```

### Bar Chart
```python
fig = go.Figure()
fig.add_trace(go.Bar(
    x=['Ene', 'Feb', 'Mar'],
    y=[100, 150, 120],
    name='2024'
))
fig.add_trace(go.Bar(
    x=['Ene', 'Feb', 'Mar'],
    y=[90, 140, 110],
    name='2023'
))
fig.update_layout(barmode='group')
fig.show()
```

### Waterfall Chart
```python
fig = go.Figure(go.Waterfall(
    name='P&L', orientation='v',
    x=['Ingresos', 'COGS', 'Gastos Op', 'EBITDA'],
    y=[1000, -400, -300, 300],
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
))
fig.update_layout(title='Estado de Resultados')
fig.show()
```

### Candlestick (Financiero)
```python
fig = go.Figure(data=[go.Candlestick(
    x=df['fecha'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
fig.update_layout(title='Gráfico de Velas')
fig.show()
```

---

## 🎨 Personalización de Layout

```python
fig.update_layout(
    title='Título del Gráfico',
    title_font_size=20,
    xaxis_title='Eje X',
    yaxis_title='Eje Y',
    font=dict(family='Arial', size=12, color='black'),
    showlegend=True,
    legend=dict(x=0.01, y=0.99),
    hovermode='x unified',  # 'closest', 'x', 'y', 'x unified'
    template='plotly_white',  # 'plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn'
    height=600,
    width=1000,
    margin=dict(l=50, r=50, t=100, b=50)
)
```

---

## 🎯 Personalización de Ejes

```python
fig.update_xaxes(
    title='Fecha',
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    tickformat='%Y-%m-%d',  # Formato de fecha
    tickangle=-45
)

fig.update_yaxes(
    title='Ventas ($)',
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    tickprefix='$',  # Prefijo de moneda
    tickformat=',.0f',  # Formato de número
    range=[0, 1000]  # Rango manual
)
```

---

## 🌈 Escalas de Color

```python
# Color continuo
fig = px.scatter(df, x='x', y='y', color='valor',
                 color_continuous_scale='Viridis')
# Opciones: 'Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis',
#           'Blues', 'Reds', 'Greens', 'RdBu', 'RdYlBu'

# Color discreto
fig = px.bar(df, x='categoria', y='ventas', color='categoria',
             color_discrete_sequence=px.colors.qualitative.Set2)

# Paleta personalizada
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
fig = px.bar(df, x='x', y='y', color='categoria',
             color_discrete_sequence=custom_colors)
```

---

## 📊 Subplots (Múltiples Gráficos)

```python
from plotly.subplots import make_subplots

# 2 filas, 2 columnas
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Plot 1', 'Plot 2', 'Plot 3', 'Plot 4'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'pie'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30]), row=1, col=2)
fig.add_trace(go.Histogram(x=df['edad']), row=2, col=1)
fig.add_trace(go.Pie(values=[30, 40, 30], labels=['A', 'B', 'C']), row=2, col=2)

fig.update_layout(height=800, showlegend=False, title_text='Dashboard')
fig.show()
```

---

## 🗺️ Mapas Geográficos

### Choropleth (Mapa de Coropletas)
```python
fig = px.choropleth(df,
                    locations='codigo_pais',  # ISO country codes
                    color='valor',
                    hover_name='pais',
                    title='Mapa Mundial')
fig.show()
```

### Scatter Geo
```python
fig = px.scatter_geo(df,
                     lat='latitud',
                     lon='longitud',
                     size='ventas',
                     color='region',
                     title='Ubicaciones')
fig.show()
```

### Mapbox (Mejor para zooms locales)
```python
fig = px.scatter_mapbox(df,
                        lat='latitud',
                        lon='longitud',
                        size='ventas',
                        color='categoria',
                        zoom=10,
                        mapbox_style='open-street-map')
fig.show()
```

---

## 📈 Anotaciones y Formas

```python
# Añadir línea vertical
fig.add_vline(x='2024-03-01', line_dash='dash', line_color='red',
              annotation_text='Evento Importante')

# Añadir línea horizontal
fig.add_hline(y=1000, line_dash='dot', line_color='green',
              annotation_text='Objetivo')

# Añadir rectángulo
fig.add_shape(type='rect',
              x0='2024-01-01', x1='2024-03-31',
              y0=0, y1=1,
              fillcolor='lightblue', opacity=0.3,
              layer='below', line_width=0)

# Añadir texto
fig.add_annotation(x='2024-06-15', y=1500,
                   text='Pico de Ventas',
                   showarrow=True,
                   arrowhead=2)
```

---

## 🎭 Interactividad Avanzada

### Botones
```python
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name='Lineal'))
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 9], name='Cuadrático', visible=False))

fig.update_layout(
    updatemenus=[
        dict(buttons=[
            dict(label='Lineal', method='update',
                 args=[{'visible': [True, False]}]),
            dict(label='Cuadrático', method='update',
                 args=[{'visible': [False, True]}]),
        ])
    ]
)
fig.show()
```

### Slider
```python
fig = px.scatter(df, x='x', y='y', animation_frame='año',
                 title='Evolución Temporal')
fig.show()
```

### Hover Personalizado
```python
fig = px.scatter(df, x='x', y='y',
                 hover_data={'x': ':.2f',  # 2 decimales
                             'y': ':.2f',
                             'categoria': True,
                             'id': False})  # No mostrar

# Hover template personalizado
fig.update_traces(
    hovertemplate='<b>%{text}</b><br>Valor: %{y:,.0f}<extra></extra>'
)
```

---

## 💾 Guardar y Exportar

```python
# Guardar como HTML interactivo
fig.write_html('grafico.html')

# Guardar como imagen estática (requiere kaleido)
fig.write_image('grafico.png')
fig.write_image('grafico.pdf')
fig.write_image('grafico.svg')

# Mostrar en Databricks
import plotly.io as pio
pio.renderers.default = 'databricks'
fig.show()
```

---

## 🎯 Casos de Uso Comunes

### Dashboard Financiero
```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Ingresos', 'Margen', 'Top Productos', 'Tendencia'),
    specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
           [{'type': 'bar'}, {'type': 'scatter'}]]
)

# KPIs
fig.add_trace(go.Indicator(
    mode='number+delta',
    value=1250000,
    title='Ingresos',
    delta={'reference': 1000000, 'relative': True}
), row=1, col=1)

fig.add_trace(go.Indicator(
    mode='gauge+number',
    value=35,
    title='Margen %',
    gauge={'axis': {'range': [0, 50]}}
), row=1, col=2)

# Top productos
fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[100, 200, 150]), row=2, col=1)

# Tendencia
fig.add_trace(go.Scatter(x=df['fecha'], y=df['ventas'], mode='lines'), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
fig.show()
```

### Comparación Año sobre Año
```python
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_2023['mes'], y=df_2023['ventas'], name='2023', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=df_2024['mes'], y=df_2024['ventas'], name='2024'))
fig.update_layout(title='Ventas YoY', hovermode='x unified')
fig.show()
```

### Análisis de Cohortes
```python
fig = px.imshow(cohort_data,
                labels=dict(x='Mes', y='Cohorte', color='Retención %'),
                x=cohort_data.columns,
                y=cohort_data.index,
                text_auto='.0f',
                color_continuous_scale='Blues',
                title='Análisis de Retención por Cohorte')
fig.show()
```

---

## ⚡ Tips de Performance

```python
# 1. Reducir datos antes de plotear
df_sample = df.sample(n=1000)  # Para datasets grandes
fig = px.scatter(df_sample, x='x', y='y')

# 2. Usar WebGL para muchos puntos
fig = px.scatter(df, x='x', y='y', render_mode='webgl')

# 3. Deshabilitar animaciones
fig.update_layout(transition_duration=0)

# 4. Simplificar hover
fig.update_traces(hoverinfo='skip')
```

---

## 🎨 Temas y Estilos

```python
# Temas predefinidos
templates = ['plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 
             'seaborn', 'simple_white', 'presentation']

fig.update_layout(template='plotly_dark')

# Tema personalizado
pio.templates['mi_tema'] = go.layout.Template(
    layout=go.Layout(
        font=dict(family='Arial', size=14),
        plot_bgcolor='#F5F5F5',
        paper_bgcolor='white',
        colorway=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
)
fig.update_layout(template='mi_tema')
```

---

## 📚 Recursos Adicionales

* **Plotly Express:** https://plotly.com/python/plotly-express/
* **Graph Objects:** https://plotly.com/python/graph-objects/
* **Galería de ejemplos:** https://plotly.com/python/
* **Databricks Plotly:** https://docs.databricks.com/visualizations/plotly.html

---

**💡 Tip:** En Databricks, usa `displayHTML()` para mostrar gráficos Plotly en notebooks.

_Última actualización: 2026-07-29_
