# 🧹 Módulo 04: Limpieza y Preparación de Datos

## 🎯 Objetivo del Módulo

**"Los datos reales son sucios."** Este módulo te enseña técnicas profesionales para transformar datos empresariales caóticos en datasets limpios listos para análisis.

En el mundo real, **el 80% del tiempo de un analista se gasta en limpieza de datos**. Este módulo te convierte en un experto en detectar y resolver problemas de calidad de datos que encontrarás en cualquier organización.

**Al finalizar este módulo podrás:**
* ✅ Detectar y tratar valores faltantes con estrategias apropiadas
* ✅ Aplicar imputación estadística (media, mediana, forward-fill, KNN)
* ✅ Identificar y eliminar duplicados exactos y fuzzy
* ✅ Limpiar y estandarizar cadenas de texto (nombres, direcciones, emails)
* ✅ Detectar y tratar outliers con métodos estadísticos (IQR, Z-score)
* ✅ Validar y formatear datos (fechas, monedas, teléfonos, códigos postales)

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Módulo 03 (Pandas Fundamentos) completado
* Familiaridad con DataFrames, Series, indexación y filtrado
* Conceptos básicos de estadística descriptiva (media, mediana, desviación estándar, percentiles)

**Datasets:**
* `ventas_retail.csv` (del repositorio datasets/raw)
* Datasets con datos sucios (provistos en notebooks)

**Tiempo estimado total:** 5 horas 10 minutos (310 minutos)

**Total de celdas educativas:** 43 (portadas + teoría + práctica + casos integradores + conclusiones)

---

## 📚 Contenido del Módulo

### 04_01_Valores_Faltantes_y_Duplicados
**Duración:** 70 minutos | **Dificultad:** 🟡 Intermedio | **Celdas:** 11

**Temas cubiertos:**
* 🔍 **Teoría de valores nulos:** MCAR, MAR, MNAR, causas empresariales
* 📊 **Detección exhaustiva:** `.isnull()`, `.notnull()`, análisis por columna y fila
* ⚙️ **Estrategias de manejo:** Eliminar vs Rellenar, reglas de oro (% de nulos)
* 🛠️ **Eliminación selectiva:** `.dropna()` con parámetros (how, subset, thresh, axis)
* 📊 **7 métodos de imputación:** constante, promedio, mediana, moda, ffill, bfill, interpolación lineal
* 🔄 **Teoría de duplicados:** tipos (exactos, parciales, fuzzy), causas, impacto
* 🔄 **Detección y eliminación:** `.duplicated()`, `.drop_duplicates()` con keep (first, last, False)
* 💼 **Caso integrador:** Pipeline completo de limpieza de cuentas por cobrar

**Resultado esperado:** Dominio completo de detección, estrategias y métodos de tratamiento de nulos y duplicados

---

### 04_02_Imputacion_Estatistica_y_Metodos
**Duración:** 60 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* Imputación de numéricos: media, mediana, moda
* Forward fill / Backward fill para series de tiempo
* Imputación por grupos (media por categoría)
* KNN Imputation con scikit-learn
* Evaluación de impacto de la imputación

**Resultado esperado:** Capacidad de elegir método de imputación óptimo según contexto

---

### 04_03_Transformacion_Cadenas_Texto
**Duración:** 55 minutos | **Dificultad:** Intermedio

**Temas cubiertos:**
* Métodos `.str`: `.strip()`, `.upper()`, `.lower()`, `.title()`
* Extracción con regex: `.str.extract()`, `.str.extractall()`
* Validación con regex
* Normalización Unicode y acentos

**Resultado esperado:** Dominio de limpieza y validación de texto con regex

---

### 04_04_Depuracion_Maestros_Clientes
**Duración:** 50 minutos | **Dificultad:** Avanzado

**Temas cubiertos:**
* Estandarización de nombres de empresa
* Normalización de direcciones
* Detección de duplicados fuzzy
* Consolidación de registros duplicados

**Resultado esperado:** Pipeline de limpieza de maestro de clientes listo para producción

---

### 04_05_Tratamiento_Outliers_y_Formato
**Duración:** 50 minutos | **Dificultad:** Intermedio-Avanzado

**Temas cubiertos:**
* Método IQR (Interquartile Range) para detección
* Z-score y desviación estándar modificada
* Tratamiento: eliminación, winsorizing, transformación log
* Formateo de monedas y fechas
* Validación de formatos numéricos

**Resultado esperado:** Capacidad de identificar y tratar outliers según contexto de negocio

---

## 🎓 Objetivos de Aprendizaje Detallados

### Nivel 1: Conocimiento
* Listar los tipos de valores faltantes
* Identificar métodos de detección de outliers
* Nombrar técnicas de imputación

### Nivel 2: Comprensión
* Explicar cuándo usar dropna() vs fillna()
* Describir el impacto de eliminar outliers
* Interpretar resultados de df.info()

### Nivel 3: Aplicación
* Aplicar imputación apropiada según tipo de dato
* Limpiar strings con métodos .str y regex
* Detectar y eliminar duplicados exactos y fuzzy
* Estandarizar formatos de fecha y moneda

### Nivel 4: Análisis
* Evaluar qué estrategia de imputación usar
* Comparar impacto de diferentes métodos de tratamiento
* Decidir cuándo eliminar vs imputar vs flag datos faltantes

---

## 🧪 Experimenta con Genie Code

### Prompt 1: Análisis de Calidad de Datos
```
"Tengo un DataFrame 'df_clientes' con datos sucios.
Genera un reporte completo de calidad que incluya:
1. % de valores faltantes por columna
2. Duplicados exactos y % de duplicación
3. Distribución de tipos de datos
4. Top 10 valores más frecuentes por columna categórica
5. Detección de outliers en columnas numéricas (método IQR)
6. Identificación de columnas con baja cardinalidad
7. Visualización: heatmap de correlación de faltantes

Presenta el reporte en formato profesional."
```

### Prompt 2: Limpieza Automática de Direcciones
```
"Tengo una columna 'direccion' con formatos inconsistentes.
Genera código que:
1. Estandariza a Title Case
2. Elimina espacios extra
3. Separa en columnas: calle, colonia, ciudad, codigo_postal
4. Valida códigos postales (5 dígitos)
5. Marca registros con direcciones incompletas

Usa regex y métodos .str de pandas."
```

### Prompt 3: Comparación de Métodos de Imputación
```
"Compara 4 métodos de imputación para la columna 'salario' con 25% nulls:
1. Media
2. Mediana
3. Media por 'departamento'
4. KNN (k=5)

Para cada método muestra:
- Estadísticas descriptivas antes y después
- Distribución con histograma
- Recomendación de cuál usar y por qué"
```

---

## 🔧 Solución de Problemas Comunes

### Problema 1: ValueError con NaN y conversión a int
**Causa:** Intentando convertir columna con NaN a tipo int  
**Solución:** Imputa/elimina NaN primero, o usa Int64
```python
df['edad'] = df['edad'].fillna(0).astype(int)
# o
df['edad'] = df['edad'].astype('Int64')  # nullable integer
```

### Problema 2: KeyError al usar .mode()[0]
**Causa:** Columna vacía o sin valores  
**Solución:** Verificar longitud antes
```python
if len(df[col].mode()) > 0:
    df[col].fillna(df[col].mode()[0], inplace=True)
else:
    df[col].fillna('DESCONOCIDO', inplace=True)
```

### Problema 3: Regex no funciona con NaN
**Causa:** Métodos .str fallan con NaN  
**Solución:** Convierte a string o usa fillna
```python
df['email_domain'] = df['email'].astype(str).str.extract(r'@(.+)$')
```

---

## 📖 Recursos Adicionales

### Documentación Oficial
* [Pandas Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
* [Pandas String Methods](https://pandas.pydata.org/docs/user_guide/text.html)
* [Scikit-learn Imputation](https://scikit-learn.org/stable/modules/impute.html)

### Librerías Recomendadas
* **fuzzywuzzy / rapidfuzz**: Fuzzy string matching
* **pyjanitor**: API fluida para limpieza de datos
* **great_expectations**: Framework de validación de calidad
* **missingno**: Visualización de patrones de valores faltantes

---

## ✅ Checklist de Completitud

**Técnicas de Valores Faltantes:**
- [ ] Detección con .isna(), .isnull()
- [ ] Eliminación con dropna()
- [ ] Imputación simple (media, mediana, moda)
- [ ] Forward fill / Backward fill
- [ ] Imputación por grupos
- [ ] KNN Imputation

**Duplicados:**
- [ ] Detección con .duplicated()
- [ ] Eliminación con .drop_duplicates()
- [ ] Duplicados fuzzy con fuzzywuzzy

**Limpieza de Texto:**
- [ ] Métodos .str básicos
- [ ] Regex con .str.extract()
- [ ] Validación de formatos

**Outliers:**
- [ ] Detección con IQR
- [ ] Detección con Z-score
- [ ] Tratamiento apropiado

---

## 🚀 Próximo Módulo

**➡️ [Módulo 05: Reshaping y Conciliaciones](../05_Reshaping_y_Conciliaciones/)**

Aprende a transformar estructuras de datos y realizar conciliaciones bancarias automatizadas.

---

[📖 Volver al Índice](../README.md)
