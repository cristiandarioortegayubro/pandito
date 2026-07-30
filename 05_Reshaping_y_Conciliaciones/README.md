# 🔄 Módulo 05: Reshaping y Conciliaciones

## 🎯 Objetivo del Módulo

**Domina las transformaciones estructurales de datos** (pivot, melt, merge) **y conciliaciones financieras automatizadas.**

En el mundo real, los datos rara vez vienen en el formato que necesitas. Este módulo te enseña a **remodelar** estructuras de datos y **combinar** múltiples fuentes, con énfasis en casos de uso financieros como la conciliación bancaria.

**Al finalizar este módulo podrás:**
* ✅ Combinar tablas con merge/join (inner, left, right, outer)
* ✅ Automatizar conciliaciones bancarias (libro vs extracto)
* ✅ Crear pivot tables para análisis multidimensional
* ✅ Transformar entre formatos wide ↔ long con melt/pivot
* ✅ Trabajar con índices multinivel para P&L jerárquico
* ✅ Identificar y resolver discrepancias en datos financieros

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 03 (Pandas Fundamentos) y Módulo 04 (Limpieza) completados
* Familiaridad con DataFrames, filtrado y agregaciones básicas
* Conceptos financieros: conciliación bancaria, P&L, balances

**Datasets:**
* `transacciones_financieras.parquet` (del repositorio)
* Datasets de conciliación bancaria (provistos en notebooks)

**Tiempo estimado total:** 4 horas 10 minutos (250 minutos)

**Total de celdas educativas:** 16 (portadas + teoría + práctica + casos integradores + conclusiones)

---

## 📚 Contenido del Módulo

### 05_01_Merge_Join_Conciliacion_Bancaria
**Duración:** 75 minutos | **Dificultad:** 🟠 Intermedio-Avanzado | **Celdas:** 9

**Temas cubiertos:**
* 📚 **Teoría de Merge y Join:** Diferencias entre merge, concat y join; SQL análogos
* 🔗 **Los 4 Tipos de Join:**
  - `inner`: Solo coincidencias en AMBOS DataFrames
  - `left`: TODAS las filas de df1 + coincidencias de df2
  - `right`: TODAS las filas de df2 + coincidencias de df1
  - `outer`: TODAS las filas de AMBOS (para conciliación)
* 🔑 **Merge con Múltiples Claves:** `pd.merge(df1, df2, on=['Sucursal', 'Producto'])`
* ✅ **Validación de Merges:**
  - `indicator=True` para detectar origen de filas (_merge)
  - `validate='one_to_many'` para verificar cardinalidad
* 🏦 **Introducción a Conciliación Bancaria:** Algoritmo completo
* 💼 **Caso Integrador:** Conciliación automática libro vs extracto (15 movimientos)
  - Outer merge por comprobante
  - Cálculo de diferencias
  - Clasificación automática de estados
  - Reporte ejecutivo

**Resultado esperado:** Dominio completo de los 4 joins y capacidad de conciliar fuentes de datos financieros

---

### 05_02_Conciliacion_Automatica_Libro_Extracto
**Duración:** 65 minutos | **Dificultad:** 🟠 Intermedio-Avanzado | **Celdas:** 4

**Temas cubiertos:**
* 📊 **Conciliación con Tolerancia:** Permitir diferencias por redondeo (±$1.00)
  - Comparación estricta vs tolerante
  - Aumento de tasa de conciliación
* 🔍 **Matching por Múltiples Criterios:** Fecha + Monto + Referencia
* 💼 **Caso Integrador Completo:**
  - Libro: 15 movimientos
  - Banco: 13 movimientos (2 faltan, 1 con error)
  - Algoritmo de clasificación: Conciliado, Diferencia, Pendiente Banco, Pendiente Libro
  - Reporte ejecutivo con totales y análisis

**Técnicas avanzadas:**
* Manejo de tolerancia configurable
* Clasificación automática con lógica de negocio
* Reporte de partidas pendientes con montos

**Resultado esperado:** Pipeline automatizado de conciliación mensual con tolerancia

---

### 05_03_Pivot_Tables_y_Melt
**Duración:** 60 minutos | **Dificultad:** 🟡 Intermedio | **Celdas:** 2 (base, expandida con contenido teórico)

**Temas cubiertos:**
* 🔄 **Transformación de Estructuras:** Concepto de ancho ↔ largo
* 📊 **Pivot Tables:** `.pivot_table()` con agregaciones (sum, mean, count)
* 📉 **Melt:** Transformar formato ancho → largo
* 💼 **Casos empresariales:**
  - Reportes de ventas por región × mes
  - Tablas dinámicas de revenue por producto
  - Preparación para visualización

**Resultado esperado:** Dominio de transformaciones estructurales para reportes ejecutivos

---

### 05_04_Estructuras_Multinivel_P&L
**Duración:** 50 minutos | **Dificultad:** 🔴 Avanzado | **Celdas:** 1 (base)

**Temas cubiertos:**
* 🎯 **MultiIndex:** Índices jerárquicos con `.set_index()`
* 🏢 **Estado de Resultados (P&L) Jerárquico:**
  - Estructura: Ingresos → Ventas → Producto A/B
  - Subtotales por categoría
  - Cálculo de EBITDA
* 📊 **Navegación por Niveles:** `.loc[(nivel1, nivel2), :]`
* 💡 **Subtotales con `.groupby(level=...)`**

**Estructura ejemplo:**
```
Ingresos
  └─ Ventas
      └─ Producto A
      └─ Producto B
  └─ Servicios
Costos
  └─ COGS
  └─ Operativos
Gastos
  └─ Marketing
  └─ Administrativos
```

**Resultado esperado:** Generar P&L jerárquico profesional con drill-down

---

## 🎓 Objetivos de Aprendizaje Detallados

### Nivel 1: Conocimiento
* [ ] Listar los 4 tipos de joins (inner, left, right, outer)
* [ ] Identificar cuándo usar pivot vs melt
* [ ] Nombrar los parámetros clave de `pd.merge()`

### Nivel 2: Comprensión
* [ ] Explicar la diferencia entre left y right join
* [ ] Describir qué es un índice multinivel
* [ ] Interpretar resultado de un outer join con NaN

### Nivel 3: Aplicación
* [ ] Realizar conciliación bancaria con tolerancia
* [ ] Crear pivot table de ventas por región y mes
* [ ] Transformar DataFrame wide a long con melt
* [ ] Construir P&L con MultiIndex

### Nivel 4: Análisis
* [ ] Evaluar qué tipo de join usar según el caso
* [ ] Diagnosticar por qué una conciliación no coincide
* [ ] Decidir estructura óptima (wide vs long) para análisis

---

## 💻 Ejercicios Prácticos

### Ejercicio 1: Conciliación Bancaria Completa
**Objetivo:** Automatizar conciliación mensual

```python
import pandas as pd
import numpy as np

# Libro contable (registros internos)
libro = pd.DataFrame({
    'fecha': pd.to_datetime(['2024-01-05', '2024-01-07', '2024-01-10', '2024-01-15']),
    'concepto': ['Venta Cliente A', 'Compra Proveedor X', 'Pago Servicio', 'Venta Cliente B'],
    'monto': [1500.00, -800.50, -300.00, 2200.00],
    'referencia': ['FAC-001', 'COM-045', 'PAG-123', 'FAC-002']
})

# Extracto bancario (registros del banco)
extracto = pd.DataFrame({
    'fecha': pd.to_datetime(['2024-01-05', '2024-01-08', '2024-01-10', '2024-01-16']),
    'descripcion': ['DEP Cliente', 'RET Proveedor', 'PAG Servicio', 'DEP Cliente'],
    'importe': [1500.00, -800.49, -300.00, 2200.05],  # Nota: centavos de diferencia
    'referencia_bancaria': ['DEP-001', 'RET-045', 'PAG-123', 'DEP-002']
})

# PASO 1: Merge con outer join (preservar todo)
conciliacion = pd.merge(
    libro, 
    extracto, 
    left_on='fecha', 
    right_on='fecha', 
    how='outer', 
    suffixes=('_libro', '_extracto'),
    indicator=True
)

# PASO 2: Identificar status de conciliación
def clasificar_partida(row, tolerancia=0.05):
    # Ambos fuentes presentes
    if row['_merge'] == 'both':
        diferencia = abs(row['monto'] - row['importe'])
        if pd.isna(diferencia):
            return 'ERROR_DATOS'
        elif diferencia <= tolerancia:
            return 'CONCILIADO'
        else:
            return 'DISCREPANCIA'
    # Solo en libro
    elif row['_merge'] == 'left_only':
        return 'PENDIENTE_BANCO'
    # Solo en extracto
    else:
        return 'NO_CONTABILIZADO'

conciliacion['status'] = conciliacion.apply(clasificar_partida, axis=1)

# PASO 3: Calcular diferencias
conciliacion['diferencia'] = conciliacion['monto'] - conciliacion['importe']

# PASO 4: Reporte
print("="*60)
print("REPORTE DE CONCILIACIÓN BANCARIA - ENERO 2024")
print("="*60)
print(f"\n📊 Resumen:")
print(f"  ✅ Partidas conciliadas: {(conciliacion['status'] == 'CONCILIADO').sum()}")
print(f"  ⚠️  Discrepancias: {(conciliacion['status'] == 'DISCREPANCIA').sum()}")
print(f"  ⏳ Pendientes en banco: {(conciliacion['status'] == 'PENDIENTE_BANCO').sum()}")
print(f"  ❌ No contabilizadas: {(conciliacion['status'] == 'NO_CONTABILIZADO').sum()}")

# Mostrar discrepancias
print(f"\n🔍 Detalle de Discrepancias:")
discrepancias = conciliacion[conciliacion['status'] == 'DISCREPANCIA'][
    ['fecha', 'concepto', 'monto', 'importe', 'diferencia']
]
print(discrepancias)

# Partidas pendientes
print(f"\n⏳ Partidas Pendientes en Banco:")
pendientes = conciliacion[conciliacion['status'] == 'PENDIENTE_BANCO'][
    ['fecha', 'concepto', 'monto', 'referencia']
]
print(pendientes)
```

**Salida esperada:**
```
============================================================
REPORTE DE CONCILIACIÓN BANCARIA - ENERO 2024
============================================================

📊 Resumen:
  ✅ Partidas conciliadas: 2
  ⚠️  Discrepancias: 2
  ⏳ Pendientes en banco: 0
  ❌ No contabilizadas: 0

🔍 Detalle de Discrepancias:
       fecha           concepto   monto  importe  diferencia
1 2024-01-07  Compra Proveedor X -800.50  -800.49       -0.01
3 2024-01-15     Venta Cliente B 2200.00  2200.05       -0.05
```

---

### Ejercicio 2: Pivot Table de Ventas
**Objetivo:** Crear tabla dinámica multidimensional

```python
# Dataset de ventas
ventas = pd.DataFrame({
    'fecha': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-10', 
                             '2024-02-25', '2024-03-05', '2024-03-18']),
    'region': ['Norte', 'Sur', 'Norte', 'Centro', 'Sur', 'Norte'],
    'producto': ['Laptop', 'Mouse', 'Laptop', 'Teclado', 'Laptop', 'Mouse'],
    'cantidad': [2, 10, 3, 5, 1, 15],
    'precio_unitario': [899, 25, 899, 79, 899, 25]
})

# Calcular total
ventas['total'] = ventas['cantidad'] * ventas['precio_unitario']

# Extraer mes
ventas['mes'] = ventas['fecha'].dt.to_period('M')

# Pivot table: Revenue por Región x Mes
pivot_revenue = pd.pivot_table(
    ventas,
    values='total',
    index='region',
    columns='mes',
    aggfunc='sum',
    fill_value=0,
    margins=True,  # Totales
    margins_name='TOTAL'
)

print("💰 Revenue por Región y Mes:")
print(pivot_revenue)

# Pivot table: Unidades vendidas por Producto x Región
pivot_unidades = pd.pivot_table(
    ventas,
    values='cantidad',
    index='producto',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

print("\n📦 Unidades Vendidas por Producto y Región:")
print(pivot_unidades)
```

---

### Ejercicio 3: Transformación Wide ↔ Long
**Objetivo:** Remodelar estructura para análisis/visualización

```python
# Datos en formato WIDE (columnas = meses)
ventas_wide = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'Ene': [1500, 250, 390],
    'Feb': [1800, 300, 420],
    'Mar': [2100, 280, 450]
})

print("📊 Formato WIDE (original):")
print(ventas_wide)

# Transformar a formato LONG (mejor para análisis/gráficos)
ventas_long = pd.melt(
    ventas_wide,
    id_vars=['producto'],
    var_name='mes',
    value_name='revenue'
)

print("\n📊 Formato LONG (transformado):")
print(ventas_long)

# Volver a WIDE
ventas_wide_reconstruido = ventas_long.pivot(
    index='producto',
    columns='mes',
    values='revenue'
)

print("\n📊 De vuelta a WIDE:")
print(ventas_wide_reconstruido)
```

---

### Ejercicio 4: P&L con MultiIndex
**Objetivo:** Estado de resultados jerárquico

```python
# Crear P&L jerárquico
pl_data = {
    'categoria': ['Ingresos', 'Ingresos', 'Ingresos', 
                  'Costos', 'Costos', 'Costos',
                  'Gastos', 'Gastos'],
    'subcategoria': ['Ventas', 'Ventas', 'Servicios',
                     'COGS', 'Operativos', 'Operativos',
                     'Marketing', 'Administrativos'],
    'concepto': ['Producto A', 'Producto B', 'Consultoría',
                 'Mat. Prima', 'Sueldos', 'Renta',
                 'Publicidad', 'Legal'],
    'monto': [50000, 30000, 15000,
              -20000, -18000, -5000,
              -8000, -4000]
}

pl = pd.DataFrame(pl_data)

# Establecer índice multinivel
pl_multi = pl.set_index(['categoria', 'subcategoria', 'concepto'])

print("📄 P&L Jerárquico:")
print(pl_multi)

# Subtotales por categoría
print("\n💰 Subtotales por Categoría:")
subtotales = pl.groupby('categoria')['monto'].sum().sort_values(ascending=False)
print(subtotales)

# EBITDA (Ingresos - Costos - Gastos)
ingresos = subtotales.get('Ingresos', 0)
costos = subtotales.get('Costos', 0)
gastos = subtotales.get('Gastos', 0)
ebitda = ingresos + costos + gastos  # costos y gastos son negativos

print(f"\n🎯 EBITDA: ${ebitda:,.2f}")
```

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Conciliación con Tolerancia Variable
```
"Tengo dos DataFrames: libro_contable y extracto_bancario.
Ambos tienen columnas: fecha, monto, descripción.

Realiza una conciliación donde:
1. Match exacto por fecha + monto con tolerancia de $0.10
2. Si no hay match exacto, intenta match por fecha ± 2 días laborables
3. Clasifica cada partida como: 'CONCILIADO', 'DISCREPANCIA', 'PENDIENTE', 'NO_CONTABILIZADO'
4. Genera reporte con totales por status
5. Exporta partidas no conciliadas a CSV"
```

### Prompt 2: Pivot Multi-Agregación
```
"De la tabla ventas con columnas: fecha, region, producto, cantidad, precio_total,
crea un pivot table que muestre:
- Filas: región
- Columnas: mes
- Valores: 
  - Sum de precio_total (revenue)
  - Count de transacciones
  - Average de precio por transacción
Incluye totales y formatea montos con $"
```

### Prompt 3: Reshaping Complejo
```
"Tengo datos de ventas en formato wide:

| producto | ene_2024 | feb_2024 | mar_2024 |
|----------|----------|----------|----------|
| Laptop   | 1500     | 1800     | 2100     |

Transfórmalo a formato long con columnas:
- producto
- fecha (datetime en formato YYYY-MM-DD, usando el primer día de cada mes)
- revenue

Luego crea una columna de MoM% (variación mensual)"
```

---

## 🔧 Solución de Problemas Comunes

### Problema 1: "ValueError: You are trying to merge on object and int64 columns"
**Causa:** Tipos de datos incompatibles en claves de merge  
**Solución:** Convierte al mismo tipo antes del merge
```python
df1['id'] = df1['id'].astype(str)
df2['id'] = df2['id'].astype(str)
merged = pd.merge(df1, df2, on='id')
```

### Problema 2: "ValueError: Index contains duplicate entries"
**Causa:** Intentando pivot con valores duplicados en index/columns  
**Solución:** Usa `.pivot_table()` con aggfunc en vez de `.pivot()`
```python
# ❌ FALLA si hay duplicados
df.pivot(index='region', columns='mes', values='revenue')

# ✅ FUNCIONA con agregación
df.pivot_table(index='region', columns='mes', values='revenue', aggfunc='sum')
```

### Problema 3: Merge produce demasiadas filas
**Causa:** Relación muchos-a-muchos sin clave única  
**Solución:** Identifica y elimina duplicados antes del merge
```python
# Verificar duplicados en claves
print(df1[['key_col']].duplicated().sum())
print(df2[['key_col']].duplicated().sum())

# Opción A: Eliminar duplicados
df1_unique = df1.drop_duplicates(subset=['key_col'], keep='first')

# Opción B: Agregar antes del merge
df1_agg = df1.groupby('key_col').agg({'value': 'sum'}).reset_index()
```

### Problema 4: MultiIndex dificulta el acceso
**Causa:** Índices jerárquicos complejos de navegar  
**Solución:** Resetea índice cuando no lo necesites
```python
# Trabajar con MultiIndex
pl_multi.loc[('Ingresos', 'Ventas'), :]  # Acceso jerárquico

# Volver a columnas normales
pl_flat = pl_multi.reset_index()
```

---

## 📖 Recursos Adicionales

### Documentación Oficial
* [Pandas Merge](https://pandas.pydata.org/docs/user_guide/merging.html)
* [Reshaping and Pivot Tables](https://pandas.pydata.org/docs/user_guide/reshaping.html)
* [MultiIndex](https://pandas.pydata.org/docs/user_guide/advanced.html)

### Artículos Recomendados
* [Visual Guide to Joins](https://www.datacamp.com/tutorial/joining-dataframes-pandas)
* [Pivot Tables in Pandas](https://pbpython.com/pandas-pivot-table-explained.html)
* [Bank Reconciliation Automation](https://towardsdatascience.com/automating-bank-reconciliation-with-python-8a2b2d5c5e0a)

### Videos
* [Pandas Merge Tutorial](https://www.youtube.com/watch?v=example)
* [Pivot Tables Explained](https://www.youtube.com/watch?v=example)

---

## ✅ Checklist de Completitud

**Notebook 05_01 - Merge y Join:**
- [ ] Los 4 tipos de join (inner, left, right, outer)
- [ ] Merge con múltiples claves: `on=['col1', 'col2']`
- [ ] Uso de `indicator=True` para ver origen (_merge)
- [ ] Validación con `validate='one_to_many'`
- [ ] Algoritmo de conciliación bancaria
- [ ] Caso integrador: 15 movimientos conciliados

**Notebook 05_02 - Conciliación Avanzada:**
- [ ] Conciliación con tolerancia de diferencias
- [ ] Clasificación automática de estados
- [ ] Match por referencia + fecha + monto
- [ ] Reporte ejecutivo de discrepancias
- [ ] Pipeline automatizado completo

**Notebook 05_03 - Pivot y Melt:**
- [ ] `.pivot_table()` con agregaciones (sum, mean, count)
- [ ] `.melt()` para transformar wide → long
- [ ] `.pivot()` para transformar long → wide
- [ ] Preparación de datos para visualización
- [ ] Reportes ejecutivos por región × mes

**Notebook 05_04 - MultiIndex y P&L:**
- [ ] Crear MultiIndex con `.set_index()`
- [ ] Navegar por niveles: `.loc[(nivel1, nivel2), :]`
- [ ] Subtotales con `.groupby(level=...)`
- [ ] Estado de Resultados (P&L) jerárquico
- [ ] Cálculo de EBITDA

**Ejercicios Integradores:**
- [ ] Ejercicio 1: Conciliación bancaria completa ✅
- [ ] Ejercicio 2: Pivot tables multidimensionales ✅
- [ ] Ejercicio 3: Transformación Wide ↔ Long ✅
- [ ] Ejercicio 4: P&L jerárquico con drill-down ✅

---

## 🚀 Próximo Módulo

**➡️ [Módulo 06: Agregaciones y Métricas KPI](../06_Agregaciones_y_Metricas_KPI/)**

Calcula métricas empresariales (ARPU, Churn, EBITDA, CAC, LTV) con `.groupby()` y agregaciones avanzadas.

---

[📖 Volver al Índice](../README.md)
