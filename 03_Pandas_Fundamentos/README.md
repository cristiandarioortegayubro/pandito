# 🐼 Módulo 03: Pandas - Fundamentos de Series y DataFrames

## 🎯 Objetivo del Módulo

**Pandas es la herramienta #1 para análisis de datos en Python.** Este módulo te enseña los fundamentos de las dos estructuras clave: **Series** (columnas) y **DataFrames** (tablas completas), aplicándolas a datos empresariales reales.

**Al finalizar este módulo podrás:**
* ✅ Crear Series y DataFrames desde múltiples fuentes (CSV, Excel, diccionarios)
* ✅ Dominar indexación con `.loc[]` e `.iloc[]`
* ✅ Filtrar datos con lógica booleana compleja
* ✅ Aplicar operaciones básicas (ordenar, renombrar, agregar columnas)
* ✅ Leer y escribir archivos en múltiples formatos

---

## 📚 Contenido del Módulo

### [03_01_Estructuras_Series_DataFrames](./03_01_Estructuras_Series_DataFrames)
**Duración:** 45 minutos | **Dificultad:** Principiante

**Temas cubiertos:**
* **Series:** arrays 1D con índice
  ```python
  import pandas as pd
  ventas = pd.Series([1200, 1500, 980], index=['Ene', 'Feb', 'Mar'])
  ```
* **DataFrames:** tablas 2D (filas × columnas)
  ```python
  df = pd.DataFrame({
      'producto': ['Laptop', 'Mouse', 'Teclado'],
      'precio': [899, 29, 79],
      'stock': [15, 120, 45]
  })
  ```
* Atributos esenciales: `.shape`, `.columns`, `.index`, `.dtypes`
* Métodos de inspección: `.head()`, `.tail()`, `.info()`, `.describe()`

**Casos de uso:**
* Crear DataFrames desde datos de negocio
* Inspeccionar rápidamente estructura de datos

---

### [03_02_Ingesta_Lectura_Archivos](./03_02_Ingesta_Lectura_Archivos)
**Duración:** 50 minutos | **Dificultad:** Principiante-Intermedio

**Temas cubiertos:**
* **CSV:** `pd.read_csv()` con parámetros clave:
  ```python
  df = pd.read_csv('ventas.csv', 
                   sep=',',           # Separador
                   encoding='utf-8',  # Codificación
                   thousands=',',     # Separador de miles
                   decimal='.',       # Separador decimal
                   parse_dates=['fecha'])  # Convertir a datetime
  ```
* **Excel:** `pd.read_excel()` - múltiples hojas
* **JSON:** `pd.read_json()` - estructuras anidadas
* **Parquet:** `pd.read_parquet()` - formato columnar
* **Clipboard:** `pd.read_clipboard()` - copiar/pegar desde Excel

**Escritura:**
* `df.to_csv()`, `df.to_excel()`, `df.to_json()`, `df.to_parquet()`

**Dataset usado:** `ventas_retail.csv` del repositorio

---

### [03_03_Indexacion_loc_iloc](./03_03_Indexacion_loc_iloc)
**Duración:** 55 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* **`.loc[]`** - Selección por etiquetas (nombres)
  ```python
  df.loc[0, 'producto']           # Celda específica
  df.loc[0:5, ['producto', 'precio']]  # Rango de filas, columnas
  df.loc[df['precio'] > 50]       # Filtrado condicional
  ```

* **`.iloc[]`** - Selección por posiciones (enteros)
  ```python
  df.iloc[0, 1]           # Primera fila, segunda columna
  df.iloc[0:5, 0:3]       # Primeras 5 filas, primeras 3 columnas
  df.iloc[:, -1]          # Última columna
  ```

* **Diferencia clave:** `.loc` incluye el último, `.iloc` excluye

* **Asignación de valores:**
  ```python
  df.loc[df['stock'] < 10, 'alerta'] = 'BAJO STOCK'
  ```

**Anti-pattern común a evitar:**
```python
# ❌ MAL: Encadenamiento puede causar SettingWithCopyWarning
df[df['precio'] > 50]['descuento'] = 0.10

# ✅ BIEN: Usar .loc[] para asignación
df.loc[df['precio'] > 50, 'descuento'] = 0.10
```

---

### [03_04_Filtrado_Booleano_Contable](./03_04_Filtrado_Booleano_Contable)
**Duración:** 60 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* **Máscaras booleanas:**
  ```python
  mascara = df['precio'] > 100
  df_filtrado = df[mascara]
  ```

* **Operadores lógicos:**
  ```python
  # AND: &
  df[(df['precio'] > 50) & (df['stock'] < 20)]
  
  # OR: |
  df[(df['categoria'] == 'A') | (df['categoria'] == 'B')]
  
  # NOT: ~
  df[~(df['status'] == 'Cancelado')]
  ```

* **Métodos de filtrado:**
  ```python
  df['producto'].isin(['Laptop', 'Tablet'])  # Valores en lista
  df['nombre'].str.contains('Corp')          # Contiene texto
  df['fecha'].between('2024-01-01', '2024-12-31')  # Rango
  ```

* **Casos contables específicos:**
  - Transacciones de alto valor (> percentil 90)
  - Cuentas con saldo negativo
  - Facturas vencidas (fecha_vencimiento < hoy)
  - Clientes con más de 3 compras

---

### [03_05_Operaciones_Basales_DataFrames](./03_05_Operaciones_Basales_DataFrames)
**Duración:** 50 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* **Ordenar:**
  ```python
  df.sort_values('precio', ascending=False)  # Desc por precio
  df.sort_values(['categoria', 'precio'])    # Multi-nivel
  ```

* **Agregar/Eliminar columnas:**
  ```python
  df['total'] = df['precio'] * df['cantidad']  # Nueva columna
  df.drop('columna_innecesaria', axis=1, inplace=True)
  ```

* **Renombrar:**
  ```python
  df.rename(columns={'precio': 'price', 'cantidad': 'qty'}, inplace=True)
  ```

* **Valores únicos:**
  ```python
  df['categoria'].unique()        # Array de únicos
  df['categoria'].value_counts()  # Conteo de frecuencias
  ```

* **Aplicar funciones:**
  ```python
  df['precio'].apply(lambda x: x * 1.10)  # Aumentar 10%
  df['producto'].apply(len)               # Largo de cada string
  ```

**Resultado esperado:** Fluency en operaciones cotidianas de Pandas

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 01: Python básico
* Módulo 02: NumPy (recomendado pero no obligatorio)
* Conceptos de bases de datos relacionales (útil pero no requerido)

**Datasets:**
* `ventas_retail.csv` (del repositorio `/datasets`)

**Tiempo estimado total:** 4 horas

---

## 💻 Ejercicios Prácticos

### Ejercicio 1: Análisis Básico de Ventas
```python
import pandas as pd

# Cargar dataset
df = pd.read_csv('../datasets/raw/ventas_retail.csv')

# Tarea 1: ¿Cuántas transacciones totales?
print(f"Total transacciones: {len(df)}")

# Tarea 2: ¿Cuál es el ticket promedio?
ticket_promedio = df['total'].mean()

# Tarea 3: Top 5 productos por revenue
top_productos = df.groupby('producto')['total'].sum().sort_values(ascending=False).head(5)

# Tarea 4: ¿Qué % de ventas tienen descuento?
pct_con_descuento = (df['descuento_pct'] > 0).mean() * 100

# Tarea 5: Filtrar solo ventas de región Norte con total > $500
ventas_norte = df[(df['region'] == 'Norte') & (df['total'] > 500)]
```

---

### Ejercicio 2: Limpieza de Datos Básica
```python
# Crear DataFrame con datos "sucios"
data_sucia = {
    'Cliente': ['Acme Corp', 'ACME CORP', 'acme corp', 'TechStart', 'techstart'],
    'Monto': ['1,200', '2500', '1,800', '3,100', '950'],
    'Fecha': ['2024-01-15', '15/01/2024', '2024-01-17', '01-18-2024', '2024-01-19']
}
df_sucio = pd.DataFrame(data_sucia)

# Tarea 1: Estandarizar nombres de cliente (lowercase)
df_sucio['Cliente'] = df_sucio['Cliente'].str.lower()

# Tarea 2: Convertir Monto a numérico (eliminar comas)
df_sucio['Monto'] = df_sucio['Monto'].str.replace(',', '').astype(float)

# Tarea 3: Parsear fechas a formato datetime (DESAFÍO)
df_sucio['Fecha'] = pd.to_datetime(df_sucio['Fecha'], infer_datetime_format=True)

# Tarea 4: Consolidar clientes duplicados
df_limpio = df_sucio.groupby('Cliente', as_index=False).agg({
    'Monto': 'sum',
    'Fecha': 'max'
})
```

---

### Ejercicio 3: Creación de Dashboard Simple
```python
# Objetivo: Generar reporte ejecutivo de ventas

print("="*50)
print("       REPORTE EJECUTIVO DE VENTAS")
print("="*50)

# KPI 1: Revenue Total
revenue_total = df['total'].sum()
print(f"\n💰 Revenue Total: ${revenue_total:,.2f}")

# KPI 2: Ticket Promedio
ticket_avg = df['total'].mean()
print(f"🎫 Ticket Promedio: ${ticket_avg:.2f}")

# KPI 3: Número de Transacciones
print(f"📄 Total Transacciones: {len(df):,}")

# KPI 4: Top 3 Regiones
print("\n🌎 Top 3 Regiones por Revenue:")
top_regiones = df.groupby('region')['total'].sum().sort_values(ascending=False).head(3)
for region, revenue in top_regiones.items():
    print(f"  {region}: ${revenue:,.2f}")

# KPI 5: Mejor Vendedor
print("\n🏆 Mejor Vendedor:")
mejor_vendedor = df.groupby('vendedor')['total'].sum().idxmax()
ventas_vendedor = df.groupby('vendedor')['total'].sum().max()
print(f"  {mejor_vendedor}: ${ventas_vendedor:,.2f}")

print("\n" + "="*50)
```

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Exploración de Datos
```
"Tengo el dataset ventas_retail.csv cargado en df.
Genera un reporte de exploración que incluya:
1. Info básica (dimensiones, tipos de datos, nulos)
2. Estadísticas descriptivas de columnas numéricas
3. Valores únicos por cada columna categórica
4. Identificar posibles problemas de calidad de datos
"
```

### Prompt 2: Filtrado Complejo
```
"Filtra el DataFrame de ventas para obtener:
- Transacciones del Q4 2024 (Oct-Nov-Dic)
- Región Norte o Sur
- Productos de categoría 'Computadoras' o 'Monitores'
- Total > $500
- Con al menos 10% de descuento

Muestra el resultado ordenado por total descendente.
"
```

---

## 📖 Recursos Adicionales

### Documentación Oficial
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
* [Pandas Cheat Sheet (DataCamp)](https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet-for-data-science-in-python)

### Tutoriales
* [Real Python - Pandas Tutorial](https://realpython.com/pandas-python-explore-dataset/)
* [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas)

### Videos
* [Corey Schafer - Pandas Tutorial Series](https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS)

---

## ✅ Checklist de Completitud

**Conceptos:**
- [ ] Entiendo la diferencia entre Series y DataFrame
- [ ] Conozco cuándo usar `.loc[]` vs `.iloc[]`
- [ ] Puedo explicar qué es una máscara booleana

**Habilidades:**
- [ ] Leo archivos CSV/Excel sin problemas de encoding
- [ ] Filtro datos con múltiples condiciones lógicas
- [ ] Creo columnas calculadas correctamente
- [ ] Ordeno DataFrames por múltiples columnas
- [ ] Uso `.value_counts()` y `.unique()` efectivamente

**Ejercicios:**
- [ ] Completé Ejercicio 1 (Análisis de Ventas)
- [ ] Completé Ejercicio 2 (Limpieza de Datos)
- [ ] Completé Ejercicio 3 (Dashboard Simple)

---

## 🚀 Próximo Módulo

¡Felicitaciones! Dominas los fundamentos de Pandas. Ahora aprende a **limpiar datos reales** del mundo empresarial:

**➡️ [Módulo 04: Limpieza y Preparación de Datos](../04_Limpieza_y_Preparacion_Datos/)**

Los datos reales son sucios. Aprende técnicas profesionales de data cleaning.

---

<div align="center">

### 🎓 ¡Pandas Básico Dominado!

**"El 80% del tiempo de un analista se invierte en limpieza. El 20% en análisis. Domina ambos."**

[📖 Volver al Índice Principal](../README.md)

</div>