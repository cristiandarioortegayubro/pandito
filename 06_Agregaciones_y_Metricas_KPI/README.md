# 📊 Módulo 06: Agregaciones y Métricas KPI

## 🎯 Objetivo del Módulo

**Transforma datos granulares en insights de negocio** mediante agregaciones y cálculo de métricas clave (KPIs).

Este módulo te enseña a responder las preguntas que realmente importan a directivos y stakeholders: *¿Cuánto vendimos por región? ¿Cuál es nuestro ARPU? ¿Qué producto genera más margen?*

**Al finalizar este módulo podrás:**
* ✅ Dominar `.groupby()` con agregaciones múltiples
* ✅ Calcular métricas empresariales: ARPU, Churn, CAC, LTV
* ✅ Construir EBITDA y márgenes de contribución
* ✅ Crear tablas de frecuencia y distribuciones
* ✅ Aplicar window functions para cálculos móviles
* ✅ Generar reportes ejecutivos con métricas consolidadas

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 03 (Pandas) y 05 (Reshaping) completados
* Comprensión de agregaciones básicas (sum, mean, count)
* Conceptos de negocio: revenue, COGS, margen, KPIs

**Datasets:**
* `ventas_retail.csv`
* `transacciones_financieras.parquet`

**Tiempo estimado:** 3.5 horas

---

## 📚 Contenido del Módulo

### 06_01_GroupBy_Agregaciones_Multiples
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* `.groupby()` con una o múltiples columnas
* Agregaciones: sum, mean, count, std, min, max
* `.agg()` con diccionarios de funciones
* Named aggregations con `pd.NamedAgg`
* Transformaciones con `.transform()`

**Casos de uso:**
* Revenue total por región y mes
* Ticket promedio por tipo de cliente
* Cantidad de transacciones por vendedor

---

### 06_02_Metricas_Empresariales_ARPU_Churn
**Duración:** 60 min | **Dificultad:** Intermedio

**Temas:**
* **ARPU** (Average Revenue Per User)
* **Churn Rate** mensual y anual
* **CAC** (Customer Acquisition Cost)
* **LTV** (Lifetime Value)
* **Retention Rate** por cohorte

**Fórmulas cubiertas:**
```
ARPU = Revenue Total / # Usuarios Activos
Churn Rate = Usuarios Cancelados / Usuarios Inicio Periodo
CAC = Gasto en Marketing / Nuevos Clientes
LTV = ARPU × (1 / Churn Rate)
```

---

### 06_03_EBITDA_y_Margenes_Contribucion
**Duración:** 55 min | **Dificultad:** Intermedio-Avanzado

**Temas:**
* Estado de Resultados (P&L) agregado
* **EBITDA** = Ingresos - COGS - Gastos Operativos
* **Margen Bruto** = (Revenue - COGS) / Revenue
* **Margen Neto** = Utilidad Neta / Revenue
* **Margen de Contribución** por producto/región

**Aplicaciones:**
* Identificar productos más rentables
* Benchmarking de márgenes vs industria
* Decisiones de discontinuación de líneas

---

### 06_04_Frecuencias_y_Distribuciones
**Duración:** 45 min | **Dificultad:** Principiante

**Temas:**
* `.value_counts()` para conteo de frecuencias
* `.crosstab()` para tablas de contingencia
* Percentiles y deciles con `.quantile()`
* Binning con `pd.cut()` y `pd.qcut()`
* Distribuciones acumuladas

**Resultado:** Análisis de distribución de variables clave (ingresos, edades, compras)

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar las funciones de agregación disponibles en pandas
* Nombrar las métricas SaaS estándar (ARPU, Churn, CAC, LTV)
* Identificar componentes del EBITDA

### Nivel 2: Comprensión
* Explicar cuándo usar .groupby() vs .pivot_table()
* Interpretar un Churn Rate del 5% mensual
* Describir la diferencia entre margen bruto y neto

### Nivel 3: Aplicación
* Calcular ARPU por segmento de cliente
* Generar P&L agregado por línea de negocio
* Crear tabla de frecuencias con binning

### Nivel 4: Análisis
* Evaluar salud financiera de un producto vía EBITDA
* Comparar CAC vs LTV para determinar viabilidad
* Identificar palancas de mejora de margen

---

## 🧪 Experim enta con Genie Code

### Prompt 1: Dashboard Ejecutivo de KPIs
```
"Usando el DataFrame 'transacciones' con columnas: fecha, cliente_id, producto, revenue, cogs.
Genera un dashboard mensual con:
1. Revenue total y MoM growth %
2. ARPU (revenue / clientes únicos)
3. Margen bruto % = (revenue - cogs) / revenue
4. Top 5 productos por revenue
5. Distribución de clientes por decil de gasto
6. Gráfico de líneas: evolución mensual de revenue y margen

Presenta en formato ejecutivo con highlights."
```

### Prompt 2: Análisis de Cohortes con Retention
```
"Calcula Retention Rate por cohorte mensual.
Cohorte = mes de primera compra del cliente.
Para cada cohorte, muestra % de clientes que siguen activos en:
- Mes 1, 3, 6, 12 desde primera compra

Visualiza como heatmap de retention.
Identifica la cohorte con mejor retention y explica."
```

### Prompt 3: Comparación de Márgenes Multi-Dimensional
```
"Compara margen de contribución por:
- Producto
- Región
- Canal de venta

Identifica combinaciones con:
1. Mayor margen (top 10)
2. Menor margen (bottom 10)
3. Mayor volumen + margen negativo (problemas críticos)

Recomienda 3 acciones específicas para mejorar margen global."
```

---

## 🔧 Solución de Problemas

### Problema 1: GroupBy devuelve Series en vez de DataFrame
**Causa:** Agregación de una sola columna  
**Solución:** Usa dobles corchetes para mantener estructura
```python
# Devuelve Series
df.groupby('region')['revenue'].sum()

# Devuelve DataFrame
df.groupby('region')[['revenue']].sum()
```

### Problema 2: KeyError al aplicar .agg() con diccionario
**Causa:** Columna no existe o typo en nombre  
**Solución:** Verifica nombres de columnas
```python
# Ver columnas disponibles
print(df.columns.tolist())

# Usar .get() para evitar errores
agg_dict = {col: 'sum' for col in ['revenue', 'qty'] if col in df.columns}
```

### Problema 3: Churn Rate > 100%
**Causa:** Definición incorrecta del denominador  
**Solución:** Usa usuarios al inicio del periodo, no al final
```python
# ❌ INCORRECTO
churn = usuarios_cancelados / usuarios_actuales

# ✅ CORRECTO
churn = usuarios_cancelados / usuarios_inicio_periodo
```

---

## 📖 Recursos Adicionales

### Documentación
* [Pandas GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
* [Pandas Aggregation](https://pandas.pydata.org/docs/user_guide/basics.html#aggregation)

### Artículos
* [SaaS Metrics Guide](https://www.klipfolio.com/resources/kpi-examples/saas)
* [Financial Metrics Cheat Sheet](https://corporatefinanceinstitute.com/resources/knowledge/finance/financial-metrics/)

---

## ✅ Checklist de Completitud

**GroupBy:**
- [ ] Agregación simple (.sum(), .mean())
- [ ] Agregación múltiple con .agg()
- [ ] Named aggregations
- [ ] Transformaciones con .transform()

**Métricas SaaS:**
- [ ] ARPU calculado correctamente
- [ ] Churn Rate mensual y anual
- [ ] CAC, LTV y ratio LTV/CAC

**Métricas Financieras:**
- [ ] P&L agregado
- [ ] EBITDA por segmento
- [ ] Márgenes bruto, operativo y neto

**Distribuciones:**
- [ ] Frecuencias con value_counts()
- [ ] Binning con pd.cut()
- [ ] Crosstab para contingencia

---

## 🚀 Próximo Módulo

**➡️ [Módulo 07: Manipulación de Fechas y Series de Tiempo](../07_Fechas_y_Series_Tiempo/)**

---

[📖 Volver al Índice](../README.md)
