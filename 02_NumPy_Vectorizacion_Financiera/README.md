# ⚡ Módulo 02: NumPy y Vectorización Financiera

> ⚠️ **Estado Actual:** Los notebooks de este módulo tienen encabezados y celdas de conclusiones completas, pero el contenido educativo completo aún está en proceso de expansión. Los temas listados abajo representan el plan de contenido que se desarrollará en cada notebook.

## 🎯 Objetivo del Módulo

NumPy es la **base computacional** de todo el ecosistema de análisis de datos en Python. Este módulo te enseña a procesar grandes volúmenes de datos numéricos **hasta 100x más rápido** que con Python nativo, aplicado a casos reales de finanzas corporativas.

**Al finalizar este módulo podrás:**
* ✅ Crear y manipular arrays multidimensionales eficientemente
* ✅ Aplicar operaciones vectorizadas en millones de datos
* ✅ Dominar broadcasting para cálculos complejos sin bucles
* ✅ Implementar modelos financieros (VAN, TIR, Monte Carlo)
* ✅ Optimizar código para performance en producción

---

## 📚 Contenido del Módulo

### [02_01_NumPy_Arrays_y_Operaciones](./02_01_NumPy_Arrays_y_Operaciones)
**Duración:** 40 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* Creación de arrays: `np.array()`, `np.zeros()`, `np.ones()`, `np.arange()`, `np.linspace()`
* Arrays multidimensionales (1D, 2D, 3D)
* Atributos: `shape`, `dtype`, `ndim`, `size`
* Indexación y slicing avanzado
* Operaciones element-wise (+, -, *, /, **)
* Funciones universales (ufuncs): `np.sum()`, `np.mean()`, `np.std()`

**Casos de uso:**
* Arrays de precios históricos de acciones
* Matrices de transacciones diarias
* Cálculo de métricas financieras en batch

---

### [02_02_Vectorizacion_y_Broadcasting](./02_02_Vectorizacion_y_Broadcasting)
**Duración:** 50 minutos | **Dificultad:** Intermedio-Avanzado

**Temas cubiertos:**
* **Vectorización:** eliminar bucles for/while
* **Broadcasting:** operar arrays de diferentes shapes
* Comparación de performance: loops vs vectorizado (benchmarking)
* Operaciones lógicas con arrays booleanos
* Fancy indexing y boolean masking

**Ejemplo práctico:**
```python
# LENTO: Python nativo con bucle
precios = [100, 105, 98, 103, 110]
retornos = []
for i in range(1, len(precios)):
    retornos.append((precios[i] - precios[i-1]) / precios[i-1])

# RÁPIDO: NumPy vectorizado (100x más rápido)
precios = np.array([100, 105, 98, 103, 110])
retornos = (precios[1:] - precios[:-1]) / precios[:-1]
```

**Resultado esperado:** Entender cuándo y cómo vectorizar código

---

### [02_03_Modelos_Financieros_NumPy](./02_03_Modelos_Financieros_NumPy)
**Duración:** 60 minutos | **Dificultad:** Avanzado

**Temas cubiertos:**
* **Valor Presente Neto (VAN/NPV):**
  ```python
  flujos = np.array([-100000, 30000, 35000, 40000, 45000])
  tasa = 0.10
  van = np.sum(flujos / (1 + tasa) ** np.arange(len(flujos)))
  ```

* **Tasa Interna de Retorno (TIR):** `np.irr()` (deprecado) o implementación manual

* **Amortización de préstamos:**
  - Tabla de amortización completa
  - Saldo insoluto por periodo
  - Intereses vs capital

* **Portafolio de inversiones:**
  - Retorno esperado de portafolio
  - Volatilidad (desviación estándar)
  - Matriz de covarianza
  - Índice de Sharpe

**Casos de uso reales:**
* Evaluación de proyectos de inversión
* Pricing de bonos
* Optimización de portafolios

---

### [02_04_Simulacion_Montecarlo_VAN_TIR](./02_04_Simulacion_Montecarlo_VAN_TIR)
**Duración:** 70 minutos | **Dificultad:** Avanzado

**Temas cubiertos:**
* ¿Qué es una simulación Monte Carlo?
* Generación de números aleatorios: `np.random.normal()`, `np.random.uniform()`
* Simulación de 10,000 escenarios de flujos de caja
* Distribución de probabilidad de VAN
* Cálculo de percentiles (P10, P50, P90)
* Probabilidad de que VAN > 0 (probabilidad de viabilidad)
* Visualización de distribuciones

**Ejemplo:**
```python
# Simular 10,000 proyectos con incertidumbre en flujos
n_simulaciones = 10000
flujos_base = np.array([30000, 35000, 40000, 45000])
desv_std = 5000  # Incertidumbre ±$5K

flujos_simulados = np.random.normal(
    loc=flujos_base, 
    scale=desv_std, 
    size=(n_simulaciones, len(flujos_base))
)

# Calcular VAN para cada simulación
inversion_inicial = -100000
van_simulado = inversion_inicial + np.sum(
    flujos_simulados / (1.10 ** np.arange(1, 5)), 
    axis=1
)

# Análisis de riesgo
print(f"VAN Esperado: ${van_simulado.mean():,.0f}")
print(f"Percentil 10: ${np.percentile(van_simulado, 10):,.0f}")
print(f"Percentil 90: ${np.percentile(van_simulado, 90):,.0f}")
print(f"Prob(VAN>0): {(van_simulado > 0).mean():.1%}")
```

**Resultado esperado:** Capacidad de cuantificar riesgo en proyectos de inversión

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 01 completo (Python básico)
* Conceptos financieros básicos:
  - Valor del dinero en el tiempo
  - Tasa de descuento
  - Flujos de caja
* Opcional: Cálculo diferencial (para entender derivadas en optimización)

**Tiempo estimado total:** 3.5 horas

---

## 📊 Por Qué NumPy es Crucial

### Comparación de Performance

| Operación | Python Nativo | NumPy | Speedup |
|-----------|---------------|-------|----------|
| Suma de 1M números | 142 ms | 1.2 ms | **118x** |
| Producto elemento a elemento | 186 ms | 0.8 ms | **232x** |
| Cálculo de media | 95 ms | 0.5 ms | **190x** |
| Filtrado condicional | 203 ms | 3.1 ms | **65x** |

### ¿Por Qué Es Tan Rápido?

1. **Implementado en C:** Bajo nivel, cerca del hardware
2. **Memoria contigua:** Arrays almacenados en bloques continuos
3. **Operaciones vectorizadas:** SIMD (Single Instruction Multiple Data)
4. **Sin overhead de Python:** No hay interpretación línea por línea

---

## 💻 Ejercicios Prácticos

### Ejercicio 1: Retornos de Portafolio
```python
# Datos: precios de cierre diarios de 3 acciones (30 días)
import numpy as np

precios = np.array([
    [100, 150, 80],   # Día 1
    [102, 148, 82],   # Día 2
    # ... 28 días más
    [108, 155, 85]    # Día 30
])

# Tarea 1: Calcular retornos diarios (%) para cada acción
retornos = (precios[1:] - precios[:-1]) / precios[:-1]

# Tarea 2: Calcular retorno promedio diario por acción
retorno_promedio = retornos.mean(axis=0)

# Tarea 3: Calcular volatilidad (desv. estándar) por acción
volatilidad = retornos.std(axis=0)

# Tarea 4: Si tengo portafolio [40% acción1, 35% acción2, 25% acción3]
#          ¿Cuál es el retorno esperado del portafolio?
pesos = np.array([0.40, 0.35, 0.25])
retorno_portafolio = np.sum(retorno_promedio * pesos)
```

---

### Ejercicio 2: Tabla de Amortización
```python
# Préstamo: $100,000 a 5 años, tasa 8% anual, pagos mensuales
principal = 100000
tasa_anual = 0.08
meses = 5 * 12
tasa_mensual = tasa_anual / 12

# Calcular pago mensual fijo (fórmula de anualidad)
pago_mensual = principal * (tasa_mensual * (1 + tasa_mensual)**meses) / \
               ((1 + tasa_mensual)**meses - 1)

# Crear tabla de amortización
periodos = np.arange(1, meses + 1)
saldo = np.zeros(meses + 1)
saldo[0] = principal

for i in range(meses):
    interes = saldo[i] * tasa_mensual
    capital = pago_mensual - interes
    saldo[i + 1] = saldo[i] - capital

# Desafío: Reescribe esto SIN bucle usando NumPy puro (más difícil)
```

---

### Ejercicio 3: Backtest de Estrategia de Trading
```python
# Estrategia simple: Comprar cuando precio < media móvil 20 días
#                    Vender cuando precio > media móvil 20 días

precios = np.random.uniform(90, 110, size=250)  # 250 días de trading

# Calcular media móvil de 20 días
ventana = 20
media_movil = np.convolve(precios, np.ones(ventana)/ventana, mode='valid')

# Señales: 1 = comprar, -1 = vender, 0 = mantener
senales = np.where(precios[ventana-1:] < media_movil, 1, 
                   np.where(precios[ventana-1:] > media_movil, -1, 0))

# Calcular retornos de la estrategia
retornos_estrategia = senales[:-1] * (precios[ventana:] - precios[ventana-1:-1]) / precios[ventana-1:-1]

# Métricas
retorno_total = np.prod(1 + retornos_estrategia) - 1
sharpe_ratio = retornos_estrategia.mean() / retornos_estrategia.std() * np.sqrt(252)

print(f"Retorno Total: {retorno_total:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
```

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Optimización de Código
```
"Tengo este código con bucles que es muy lento:
[PEGA TU CÓDIGO]

Optímizalo usando NumPy vectorizado. Explica:
1. Por qué el código original es lento
2. Cómo funciona la versión vectorizada
3. Cuánto más rápido debería ser
"
```

### Prompt 2: Simulación Monte Carlo Personalizada
```
"Implementa una simulación Monte Carlo para evaluar un proyecto:
- Inversión inicial: $500,000
- Flujos esperados: [120K, 150K, 180K, 200K, 220K] (5 años)
- Incertidumbre: ±20% en cada flujo
- Tasa de descuento: 12%
- Simula 50,000 escenarios

Calcula:
- VAN esperado
- Rango de confianza 90% (P5 a P95)
- Probabilidad de pérdida (VAN < 0)
- Visualiza histograma de resultados
"
```

---

## 📖 Recursos Adicionales

### Documentación
* [NumPy Official Documentation](https://numpy.org/doc/stable/)
* [NumPy for Absolute Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
* [NumPy Tutorial (DataCamp)](https://www.datacamp.com/tutorial/python-numpy-tutorial)

### Artículos Técnicos
* [Why NumPy is Fast](https://realpython.com/numpy-array-programming/)
* [Broadcasting Explained](https://numpy.org/doc/stable/user/basics.broadcasting.html)
* [Monte Carlo in Finance (Investopedia)](https://www.investopedia.com/terms/m/montecarlosimulation.asp)

### Libros Recomendados
* "Python for Finance" - Yves Hilpisch
* "NumPy Beginner's Guide" - Ivan Idris

---

## ✅ Checklist de Completitud

**Conceptos:**
- [ ] Entiendo la diferencia entre lista Python y NumPy array
- [ ] Puedo explicar qué es broadcasting
- [ ] Sé cuándo vectorizar es apropiado

**Habilidades:**
- [ ] Creo arrays multidimensionales correctamente
- [ ] Aplico operaciones element-wise sin bucles
- [ ] Uso indexación avanzada (fancy indexing, boolean masking)
- [ ] Implemento fórmulas financieras con NumPy

**Ejercicios:**
- [ ] Completé Ejercicio 1 (Retornos de Portafolio)
- [ ] Completé Ejercicio 2 (Tabla de Amortización)
- [ ] Completé Ejercicio 3 (Backtest de Trading)

**Proyectos:**
- [ ] Implementé simulación Monte Carlo de VAN
- [ ] Comparé performance: loops vs vectorizado

---

## 🚀 Próximo Módulo

Ahora que dominas cómputo numérico eficiente, es momento de aprender la herramienta #1 para análisis de datos:

**➡️ [Módulo 03: Pandas - Series y DataFrames](../03_Pandas_Fundamentos/)**

Pandas es como Excel con superpoderes. Aprende a manipular datos tabulares con facilidad.

---

<div align="center">

### 🎓 ¡NumPy Dominado!

**"El código rápido no es opcional en producción, es un requisito."**

[📖 Volver al Índice Principal](../README.md)

</div>