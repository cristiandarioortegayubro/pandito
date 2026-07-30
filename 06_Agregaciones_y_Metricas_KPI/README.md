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

**Tiempo estimado total:** 4 horas 10 minutos (250 minutos)

**Total de celdas educativas:** 30 (portadas + teoría + práctica + casos integradores + conclusiones)

---

## 📚 Contenido del Módulo

### 06_01_GroupBy_y_Operaciones_Grupales
**Duración:** 70 minutos | **Dificultad:** 🟡 Intermedio | **Celdas:** 10

**Temas cubiertos:**
* 🔢 **El Patrón Split-Apply-Combine:** División conceptual de agregaciones
* 📊 **GroupBy Básico:** `.groupby('col')['valor'].sum()`
* 📈 **Agregaciones Múltiples:** `.agg()` con diccionarios, funciones múltiples
* 🔢 **Múltiples Columnas:** `.groupby(['col1', 'col2']).agg(...)`
* 🔍 **Filtrado Post-Agregación:** Top N, filtrado por umbral
* 🔄 **Transformaciones por Grupo:** `.transform()`, ranking, % participación
* 💼 **Caso Integrador:** Análisis completo de ventas (5 preguntas de negocio)

**Resultado esperado:** Dominio completo de GroupBy y agregaciones en contextos empresariales

---

### 06_02_Calculo_Margen_Bruto_y_EBITDA
**Duración:** 65 minutos | **Dificultad:** 🟡 Intermedio | **Celdas:** 8

**Temas cubiertos:**
* 📚 **Teoría de Margen Bruto:** Definición, componentes, benchmarks por industria
* 💰 **Cálculo de Margen Bruto:** Fórmulas, margen %, análisis de rentabilidad
* 📈 **Teoría de EBITDA:** Definición, por qué importa, cálculo top-down y bottom-up
* 📈 **Cálculo de EBITDA:** Estado de resultados completo, EBIT, utilidad neta
* 💼 **Caso Integrador:** Análisis por línea de producto, ranking, análisis crítico

**Fórmulas clave:**
```python
Margen_Bruto = Ventas_Netas - Costo_Ventas
Margen_Bruto_% = (Margen_Bruto / Ventas_Netas) * 100

EBITDA = Margen_Bruto - Gastos_Operativos
EBIT = EBITDA - Depreciación - Amortización
Utilidad_Neta = EBIT - Intereses - Impuestos
```

**Resultado esperado:** Capacidad de construir estados financieros y analizar rentabilidad

---

### 06_03_Metricas_ARPU_y_Churn_Rate
**Duración:** 60 minutos | **Dificultad:** 🟠 Intermedio-Avanzado | **Celdas:** 6

**Temas cubiertos:**
* 📚 **Teoría de ARPU y Churn:** Definiciones, fórmulas, benchmarks por industria
* 💰 **Cálculo de ARPU y Churn:** Métricas mensuales, crecimiento neto, tasa de crecimiento
* 🔄 **LTV (Lifetime Value):** Fórmula simplificada, interpretación empresarial
* 💼 **Caso Integrador:** Análisis de cohortes, ARPU por cohorte y plan, Churn por segmento

**Fórmulas clave:**
```python
ARPU = Total_Revenue / Total_Active_Users
Churn_Rate_% = (Cancelaciones / Usuarios_Inicio) * 100
LTV = ARPU / (Churn_Rate / 100)
```

**Benchmarks:**
* B2C SaaS: ARPU $10-30, Churn 5-7%
* B2B SaaS: ARPU $50-500, Churn 2-3%
* Streaming: ARPU $10-20, Churn 3-5%

**Resultado esperado:** Dominio de métricas SaaS y capacidad de analizar cohortes

---

### 06_04_Agregaciones_Compuestas_agg
**Duración:** 55 minutos | **Dificultad:** 🟠 Intermedio-Avanzado | **Celdas:** 6

**Temas cubiertos:**
* 📦 **.agg() con Múltiples Funciones:** Una función, múltiples funciones, Named Aggregations
* 🔧 **Funciones Personalizadas:** Funciones custom, lambdas, métricas avanzadas (rango, coef. variación)
* 📊 **Dashboard de KPIs Integrador:** KPIs por región, producto, vendedor, métricas generales

**Métodos avanzados:**
```python
# Named Aggregations (RECOMENDADO)
df.groupby('col').agg(
    Total_Ventas=('ventas', 'sum'),
    Promedio=('ventas', 'mean'),
    Maximo=('ventas', 'max')
)

# Funciones personalizadas
def rango(x):
    return x.max() - x.min()

df.groupby('col').agg(Rango=('val', rango))
```

**Resultado esperado:** Dominio de .agg() avanzado y capacidad de construir dashboards de KPIs

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

**06_01 - GroupBy y Operaciones Grupales:**
- [ ] Comprender el patrón Split-Apply-Combine
- [ ] Realizar GroupBy básico con una columna
- [ ] Aplicar agregaciones múltiples con .agg()
- [ ] Agrupar por múltiples columnas
- [ ] Filtrar resultados post-agregación
- [ ] Usar .transform() para agregar valores a filas
- [ ] Calcular ranking dentro de grupos
- [ ] Resolver 5 preguntas de negocio con GroupBy

**06_02 - Margen Bruto y EBITDA:**
- [ ] Calcular Margen Bruto y Margen Bruto %
- [ ] Entender componentes del EBITDA
- [ ] Construir estado de resultados completo
- [ ] Calcular EBIT y Utilidad Neta
- [ ] Analizar rentabilidad por línea de producto
- [ ] Comparar márgenes con benchmarks de industria
- [ ] Identificar líneas rentables y no rentables

**06_03 - ARPU y Churn Rate:**
- [ ] Calcular ARPU mensual correctamente
- [ ] Medir Churn Rate por período
- [ ] Calcular LTV (Lifetime Value)
- [ ] Analizar métricas por cohorte
- [ ] Comparar ARPU y Churn por plan/segmento
- [ ] Interpretar benchmarks de industria

**06_04 - Agregaciones Compuestas:**
- [ ] Usar .agg() con múltiples funciones
- [ ] Crear funciones personalizadas de agregación
- [ ] Aplicar Named Aggregations
- [ ] Combinar múltiples niveles de agregación
- [ ] Construir dashboard completo de KPIs
- [ ] Generar KPIs por región, producto y vendedor

---

## 🚀 Próximo Módulo

**➡️ [Módulo 07: Manipulación de Fechas y Series de Tiempo](../07_Fechas_y_Series_Tiempo/)**

---

[📖 Volver al Índice](../README.md)
