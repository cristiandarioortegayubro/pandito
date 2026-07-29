# 🐼 Pandas Cheatsheet - Saliendo de lo Pandito v4

**Referencia rápida de comandos esenciales de Pandas para análisis de datos**

---

## 📦 Importación y Creación

```python
import pandas as pd
import numpy as np

# Crear DataFrame desde diccionario
df = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c']
})

# Crear desde lista de diccionarios
df = pd.DataFrame([
    {'nombre': 'Ana', 'edad': 28},
    {'nombre': 'Juan', 'edad': 34}
])

# Crear desde arrays
df = pd.DataFrame(
    data=np.array([[1, 2], [3, 4]]),
    columns=['A', 'B']
)

# Series
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
```

---

## 📂 Lectura y Escritura de Archivos

```python
# CSV
df = pd.read_csv('archivo.csv')
df = pd.read_csv('archivo.csv', sep=';', encoding='utf-8')
df.to_csv('salida.csv', index=False)

# Excel
df = pd.read_excel('archivo.xlsx', sheet_name='Hoja1')
df.to_excel('salida.xlsx', sheet_name='Datos', index=False)

# JSON
df = pd.read_json('archivo.json')
df.to_json('salida.json', orient='records')

# Parquet (recomendado para Big Data)
df = pd.read_parquet('archivo.parquet')
df.to_parquet('salida.parquet')

# SQL
import sqlite3
conn = sqlite3.connect('base_datos.db')
df = pd.read_sql('SELECT * FROM tabla', conn)
df.to_sql('tabla', conn, if_exists='replace', index=False)
```

---

## 🔍 Inspección de Datos

```python
# Primeras/últimas filas
df.head(10)        # Primeras 10 filas
df.tail(5)         # Últimas 5 filas
df.sample(10)      # 10 filas aleatorias

# Información del DataFrame
df.info()          # Tipos de datos, memoria, nulls
df.describe()      # Estadísticas descriptivas
df.shape           # (filas, columnas)
df.columns         # Lista de columnas
df.dtypes          # Tipos de datos por columna
df.index           # Índice del DataFrame

# Valores únicos
df['columna'].unique()           # Array de valores únicos
df['columna'].nunique()          # Cantidad de valores únicos
df['columna'].value_counts()     # Frecuencia de valores
```

---

## 🎯 Selección e Indexación

```python
# Selección de columnas
df['columna']                    # Una columna (Series)
df[['col1', 'col2']]            # Múltiples columnas (DataFrame)

# loc - por etiqueta/nombre
df.loc[0]                        # Fila con índice 0
df.loc[0:5, 'columna']          # Filas 0-5, columna específica
df.loc[df['edad'] > 30]         # Filtrado booleano

# iloc - por posición numérica
df.iloc[0]                       # Primera fila
df.iloc[0:5, 0:3]               # Primeras 5 filas, primeras 3 columnas
df.iloc[:, -1]                   # Última columna

# at/iat - acceso a valor individual (más rápido)
df.at[0, 'columna']             # Por etiqueta
df.iat[0, 1]                     # Por posición
```

---

## 🔎 Filtrado

```python
# Filtrado simple
df[df['edad'] > 30]
df[df['ciudad'] == 'Madrid']

# Múltiples condiciones
df[(df['edad'] > 30) & (df['ciudad'] == 'Madrid')]
df[(df['edad'] < 25) | (df['edad'] > 65)]
df[~df['estado'].isin(['INACTIVO', 'SUSPENDIDO'])]  # NOT IN

# Filtrado con query (más legible)
df.query('edad > 30 and ciudad == "Madrid"')
df.query('salario >= 50000 and salario <= 100000')

# Filtrado por texto
df[df['nombre'].str.contains('Ana', case=False)]
df[df['email'].str.endswith('@gmail.com')]
df[df['codigo'].str.startswith('VEN')]

# Filtrado por nulls
df[df['columna'].isna()]        # Solo valores nulos
df[df['columna'].notna()]       # Sin valores nulos
```

---

## 🔧 Transformaciones de Columnas

```python
# Crear nueva columna
df['nueva'] = df['col1'] + df['col2']
df['doble'] = df['valor'] * 2

# Modificar columna existente
df['precio'] = df['precio'] * 1.21  # Agregar IVA

# Aplicar función
df['mayuscula'] = df['nombre'].str.upper()
df['absoluto'] = df['valor'].abs()

# apply - función personalizada
df['categoria'] = df['edad'].apply(lambda x: 'Joven' if x < 30 else 'Adulto')

# map - mapeo de valores
mapa = {'A': 'Alto', 'B': 'Bajo', 'M': 'Medio'}
df['nivel_desc'] = df['nivel'].map(mapa)

# replace - reemplazo de valores
df['estado'] = df['estado'].replace({'ACT': 'ACTIVO', 'INA': 'INACTIVO'})

# Renombrar columnas
df.rename(columns={'old_name': 'new_name'}, inplace=True)
df.columns = ['col1', 'col2', 'col3']  # Renombrar todas
```

---

## 📊 Agregaciones y GroupBy

```python
# Agregaciones simples
df['ventas'].sum()
df['precio'].mean()
df['cantidad'].median()
df['valor'].std()
df['fecha'].min()
df['fecha'].max()

# GroupBy básico
df.groupby('categoria')['ventas'].sum()
df.groupby('ciudad')['precio'].mean()

# GroupBy múltiples columnas
df.groupby(['categoria', 'subcategoria'])['ventas'].sum()

# Múltiples agregaciones
df.groupby('categoria').agg({
    'ventas': 'sum',
    'precio': 'mean',
    'cantidad': ['min', 'max', 'count']
})

# Agregaciones nombradas
df.groupby('categoria').agg(
    ventas_totales=('ventas', 'sum'),
    precio_promedio=('precio', 'mean'),
    num_transacciones=('id', 'count')
).reset_index()

# Agregaciones personalizadas
df.groupby('categoria')['ventas'].agg(['sum', 'mean', lambda x: x.max() - x.min()])
```

---

## 🔄 Merge, Join y Concatenación

```python
# Merge (similar a SQL JOIN)
pd.merge(df1, df2, on='id')                        # INNER JOIN
pd.merge(df1, df2, on='id', how='left')           # LEFT JOIN
pd.merge(df1, df2, on='id', how='right')          # RIGHT JOIN
pd.merge(df1, df2, on='id', how='outer')          # FULL OUTER JOIN

# Join en columnas con nombres diferentes
pd.merge(df1, df2, left_on='id_cliente', right_on='cliente_id')

# Join en múltiples columnas
pd.merge(df1, df2, on=['id', 'fecha'])

# Concatenación vertical (apilar)
pd.concat([df1, df2], ignore_index=True)

# Concatenación horizontal (lado a lado)
pd.concat([df1, df2], axis=1)
```

---

## 🔀 Pivot y Reshape

```python
# Pivot Table
df.pivot_table(
    values='ventas',
    index='categoria',
    columns='mes',
    aggfunc='sum',
    fill_value=0
)

# Pivot simple (sin agregación)
df.pivot(index='id', columns='variable', values='valor')

# Melt (de wide a long)
df.melt(
    id_vars=['id', 'nombre'],
    value_vars=['ene', 'feb', 'mar'],
    var_name='mes',
    value_name='ventas'
)

# Stack/Unstack
df.set_index(['fecha', 'producto']).unstack()
df.stack()
```

---

## 🧹 Limpieza de Datos

```python
# Valores faltantes
df.isna().sum()                  # Contar nulls por columna
df.dropna()                      # Eliminar filas con nulls
df.dropna(subset=['col1'])       # Eliminar nulls en columna específica
df.fillna(0)                     # Rellenar nulls con 0
df.fillna(method='ffill')        # Forward fill
df.fillna(method='bfill')        # Backward fill
df['col'].fillna(df['col'].mean())  # Rellenar con media

# Duplicados
df.duplicated().sum()            # Contar duplicados
df.drop_duplicates()             # Eliminar duplicados
df.drop_duplicates(subset=['col1'], keep='last')

# Ordenamiento
df.sort_values('columna')                    # Ascendente
df.sort_values('columna', ascending=False)   # Descendente
df.sort_values(['col1', 'col2'])            # Múltiples columnas
df.sort_index()                              # Por índice

# Resetear índice
df.reset_index(drop=True)

# Cambiar tipo de datos
df['columna'] = df['columna'].astype('int')
df['fecha'] = pd.to_datetime(df['fecha'])
df['precio'] = df['precio'].astype('float')
```

---

## 📅 Manejo de Fechas

```python
# Conversión a datetime
df['fecha'] = pd.to_datetime(df['fecha'])
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

# Extraer componentes
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['dia'] = df['fecha'].dt.day
df['dia_semana'] = df['fecha'].dt.day_name()
df['trimestre'] = df['fecha'].dt.quarter

# Operaciones con fechas
df['dias_desde'] = (pd.Timestamp.now() - df['fecha']).dt.days
df['fecha_futura'] = df['fecha'] + pd.Timedelta(days=30)

# Resampling (series de tiempo)
df.set_index('fecha').resample('M').sum()    # Mensual
df.set_index('fecha').resample('Q').mean()   # Trimestral
df.set_index('fecha').resample('Y').max()    # Anual
```

---

## 🎨 Strings (Texto)

```python
# Operaciones de texto
df['nombre'].str.upper()                 # Mayúsculas
df['nombre'].str.lower()                 # Minúsculas
df['nombre'].str.title()                 # Title Case
df['nombre'].str.strip()                 # Quitar espacios laterales
df['nombre'].str.replace('viejo', 'nuevo')

# Búsqueda y filtrado
df['email'].str.contains('@gmail.com')
df['codigo'].str.startswith('VEN')
df['archivo'].str.endswith('.pdf')

# Extracción
df['email'].str.split('@').str[0]        # Parte antes de @
df['codigo'].str[:3]                      # Primeros 3 caracteres
df['texto'].str.extract(r'(\d+)')        # Extraer números con regex

# Longitud
df['nombre'].str.len()
```

---

## 🔢 Operaciones Numéricas

```python
# Estadísticas
df['ventas'].sum()
df['ventas'].mean()
df['ventas'].median()
df['ventas'].std()
df['ventas'].var()
df['ventas'].quantile([0.25, 0.5, 0.75])

# Operaciones entre columnas
df['total'] = df['cantidad'] * df['precio']
df['margen'] = (df['precio_venta'] - df['costo']) / df['precio_venta']

# Normalización
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['normalizado'] = scaler.fit_transform(df[['valor']])

# Percentiles
df['percentil'] = df['valor'].rank(pct=True)

# Ventanas móviles
df['promedio_movil_7d'] = df['valor'].rolling(window=7).mean()
df['suma_acumulada'] = df['valor'].cumsum()
```

---

## 💾 Optimización de Memoria

```python
# Ver uso de memoria
df.memory_usage(deep=True)

# Reducir tamaño de columnas numéricas
df['entero'] = df['entero'].astype('int32')    # En lugar de int64
df['decimal'] = df['decimal'].astype('float32')  # En lugar de float64

# Categorical para strings repetitivos
df['categoria'] = df['categoria'].astype('category')

# Informe de memoria
print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

---

## 🔍 Visualización Rápida

```python
# Con pandas (matplotlib)
df['columna'].plot()                     # Gráfico de líneas
df['columna'].plot(kind='bar')          # Barras
df['columna'].plot(kind='hist')         # Histograma
df.plot.scatter(x='col1', y='col2')     # Scatter

# Guardar figura
import matplotlib.pyplot as plt
df.plot()
plt.savefig('grafico.png')
plt.close()
```

---

## ⚡ Tips de Performance

```python
# 1. Usar vectorización en lugar de loops
# ❌ Lento
for i in range(len(df)):
    df.loc[i, 'nueva'] = df.loc[i, 'col1'] * 2

# ✅ Rápido
df['nueva'] = df['col1'] * 2

# 2. Usar query() para filtros complejos
# ✅ Más rápido que múltiples []
df.query('edad > 30 and ciudad == "Madrid"')

# 3. Especificar dtypes al leer CSV
df = pd.read_csv('archivo.csv', dtype={'id': 'int32', 'categoria': 'category'})

# 4. Usar chunksize para archivos grandes
for chunk in pd.read_csv('grande.csv', chunksize=10000):
    procesar(chunk)

# 5. Evitar .append() en loops (usar lista + concat)
# ❌ Lento
resultado = pd.DataFrame()
for chunk in chunks:
    resultado = resultado.append(chunk)

# ✅ Rápido
resultados = []
for chunk in chunks:
    resultados.append(chunk)
resultado = pd.concat(resultados, ignore_index=True)
```

---

## 🎯 Casos de Uso Comunes

### 📊 Análisis de Ventas
```python
# Top 10 productos por ventas
top_productos = (df.groupby('producto')['ventas']
                   .sum()
                   .sort_values(ascending=False)
                   .head(10))

# Ventas por mes
ventas_mensuales = (df.groupby(df['fecha'].dt.to_period('M'))['ventas']
                      .sum())

# Tasa de crecimiento mes a mes
ventas_mensuales.pct_change() * 100
```

### 💰 Análisis Financiero
```python
# ARPU (Average Revenue Per User)
arpu = df.groupby('usuario_id')['ingreso'].sum().mean()

# Churn Rate
total_clientes = df['cliente_id'].nunique()
clientes_activos = df[df['estado'] == 'ACTIVO']['cliente_id'].nunique()
churn_rate = (1 - clientes_activos / total_clientes) * 100

# Margen Bruto
df['margen_bruto'] = df['ingresos'] - df['costo_ventas']
df['porcentaje_margen'] = (df['margen_bruto'] / df['ingresos']) * 100
```

### 🏦 Conciliación Bancaria
```python
# Encontrar transacciones no conciliadas
libro = pd.read_csv('libro_banco.csv')
extracto = pd.read_csv('extracto_bancario.csv')

no_conciliadas = pd.merge(
    libro, 
    extracto, 
    on=['fecha', 'monto'], 
    how='outer', 
    indicator=True
)
no_conciliadas = no_conciliadas[no_conciliadas['_merge'] != 'both']
```

---

## 📚 Recursos Adicionales

* **Documentación oficial:** https://pandas.pydata.org/docs/
* **10 minutes to pandas:** https://pandas.pydata.org/docs/user_guide/10min.html
* **Pandas Cookbook:** https://github.com/jvns/pandas-cookbook

---

**💡 Tip:** Guarda este cheatsheet en tu carpeta de referencias y úsalo como consulta rápida durante el libro.

_Última actualización: 2026-07-29_
