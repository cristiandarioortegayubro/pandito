# 📈 Módulo 07: Series de Tiempo Financieras

## 🎯 Objetivo del Módulo

**Domina el análisis temporal financiero:** desde parseo de fechas hasta detección de tendencias y estacionalidad en datos de mercado.

Las decisiones financieras se basan en **patrones temporales, volatilidad y forecasting**. Este módulo te enseña técnicas específicas para series de tiempo en contexto de finanzas y negocios.

**Al finalizar este módulo podrás:**
* ✅ Parsear y manipular fechas/timestamps en cualquier formato
* ✅ Calcular retornos, volatilidad y métricas de riesgo
* ✅ Aplicar rolling windows para suavizado y alertas
* ✅ Resamplear series temporales (diario → mensual)
* ✅ Detectar tendencias, estacionalidad y anomalías
* ✅ Construir forecasts básicos con modelos ARIMA

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulos 03 (Pandas) y 06 (Agregaciones) completados
* Familiaridad con conceptos financieros básicos (retorno, volatilidad)

**Datasets:**
* `transacciones_financieras.parquet`
* `logs_ecommerce.json` (timestamps)

**Tiempo estimado:** 3.5 horas

---

## 📚 Contenido del Módulo

### 07_01_Fechas_Datetime_y_Componentes_Temporales
**Duración:** 45 min | **Dificultad:** Principiante

**Temas:**
* `pd.to_datetime()` con formatos personalizados
* Extracción de componentes: `.dt.year`, `.dt.month`, `.dt.day`, `.dt.dayofweek`
* Nombres de días/meses: `.dt.day_name()`, `.dt.month_name()`
* Creación de rangos: `pd.date_range()`
* Manejo de zonas horarias

**Casos de uso:**
* Agrupar transacciones por mes/trimestre
* Identificar patrones por día de semana
* Filtrar datos por rango de fechas

---

### 07_02_Operaciones_Timedelta_y_Frecuencias
**Duración:** 40 min | **Dificultad:** Principiante

**Temas:**
* Diferencias entre fechas (`pd.Timedelta`)
* Operaciones aritméticas con fechas
* Cálculo de tiempo transcurrido
* Frecuencias: D (día), W (semana), M (mes), Q (trimestre), Y (año)

**Aplicaciones:**
* Días desde última transacción
* Tiempo promedio entre compras
* Antigüedad de cuentas

---

### 07_03_Resampling_y_Agregaciones_Temporales
**Duración:** 55 min | **Dificultad:** Intermedio

**Temas:**
* `.resample()`: cambiar frecuencia temporal
* Downsampling (día → mes): sum, mean, last
* Upsampling (mes → día): forward fill, interpolación
* Agregaciones personalizadas en resample

**Ejemplos:**
```python
# Datos diarios → mensuales (suma)
df.resample('M', on='fecha').sum()

# Datos horarios → diarios (promedio)
df.resample('D').mean()

# Rellenar gaps con forward fill
df.resample('H').ffill()
```

---

### 07_04_Rolling_Windows_Metricas_Moviles
**Duración:** 50 min | **Dificultad:** Intermedio

**Temas:**
* `.rolling()` para ventanas móviles
* Media móvil (SMA) 7, 30, 90 días
* Rolling sum, std, min, max
* Expanding windows (`.expanding()`)
* Aplicaciones en finanzas: volatilidad móvil, bandas de Bollinger

**Casos de uso:**
* Suavizado de series ruidosas (revenue, tráfico)
* Detección de tendencias
* Alertas cuando valor excede rolling mean ± 2σ

---

### 07_05_Retornos_Volatilidad_y_Metricas_Riesgo
**Duración:** 60 min | **Dificultad:** Avanzado

**Temas:**
* Retornos simples y logarítmicos
* Volatilidad histórica (desviación estándar de retornos)
* Sharpe Ratio, Sortino Ratio
* Value at Risk (VaR) histórico
* Maximum Drawdown

**Fórmulas:**
```python
# Retorno simple
returns = (price_t / price_t-1) - 1

# Retorno logarítmico
log_returns = np.log(price_t / price_t-1)

# Volatilidad anualizada
volatility = returns.std() * np.sqrt(252)

# Sharpe Ratio
sharpe = (mean_return - risk_free_rate) / volatility
```

---

## 🎓 Objetivos de Aprendizaje

### Nivel 1: Conocimiento
* Listar componentes de un datetime
* Nombrar métodos de resample disponibles
* Identificar diferencia entre rolling y expanding

### Nivel 2: Comprensión
* Explicar cuándo usar resample vs groupby
* Interpretar una media móvil de 7 días
* Describir qué es la volatilidad anualizada

### Nivel 3: Aplicación
* Parsear fechas en formatos no estándar
* Calcular MoM growth con resample
* Aplicar rolling mean para suavizar ventas
* Calcular volatilidad de retornos

### Nivel 4: Análisis
* Identificar estacionalidad en series de tiempo
* Comparar tendencia vs fluctuación aleatoria
* Evaluar riesgo-retorno con Sharpe Ratio

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Análisis de Estacionalidad
```
"Analiza la serie 'ventas_diarias' (columnas: fecha, revenue).
Genera:
1. Gráfico de serie completa
2. Revenue promedio por día de semana
3. Revenue promedio por mes del año
4. Identificación de picos y valles anómalos
5. Descomposición: tendencia, estacionalidad, residuos
6. Recomendaciones de estrategia de inventario"
```

### Prompt 2: Dashboard de Métricas Móviles
```
"Crea dashboard con:
- Revenue diario (línea gris)
- MA 7 días (línea azul)
- MA 30 días (línea naranja)
- Bandas de ±1σ alrededor de MA30
- Marcadores en días que exceden MA + 2σ

Identifica periodos de crecimiento sostenido."
```

### Prompt 3: Análisis de Riesgo-Retorno
```
"Tengo precios diarios de 3 activos.
Calcula para cada uno:
1. Retorno acumulado (%)
2. Volatilidad anualizada
3. Sharpe Ratio (risk-free = 2%)
4. Maximum Drawdown
5. VaR al 95% (pérdida máxima esperada)

Compara en tabla y gráfico de riesgo-retorno."
```

---

## 🔧 Solución de Problemas

### Problema 1: ValueError al parsear fechas no estándar
**Solución:** Especifica formato con `format`
```python
pd.to_datetime('15-Ene-2024', format='%d-%b-%Y')
```

### Problema 2: Resample genera NaN
**Solución:** Usa `fill_value` o `ffill`
```python
df.resample('D').sum(fill_value=0)
# o
df.resample('D').ffill()
```

### Problema 3: Rolling con ventana mayor a dataset
**Solución:** Usa `min_periods`
```python
df['ma'] = df['value'].rolling(window=30, min_periods=1).mean()
```

---

## 📖 Recursos Adicionales

### Documentación
* [Pandas Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
* [Pandas Resampling](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html)

### Librerías
* **prophet**: Forecasting robusto (Facebook)
* **statsmodels**: ARIMA, descomposición
* **pmdarima**: Auto-ARIMA

---

## ✅ Checklist

- [ ] Parseo con pd.to_datetime()
- [ ] Extracción de componentes con .dt
- [ ] Cálculo de diferencias temporales
- [ ] Resample (downsampling y upsampling)
- [ ] Media móvil simple (SMA)
- [ ] Rolling std para volatilidad
- [ ] Retornos simples y log
- [ ] Volatilidad anualizada
- [ ] Sharpe Ratio

---

## 🚀 Próximo Módulo

**➡️ [Módulo 08: Visualización con Plotly](../08_Visualizacion_Plotly_Databricks_Dashboards/)**

---

[📖 Volver al Índice](../README.md)
