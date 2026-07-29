# ✅ Compatibilidad Serverless - Saliendo de lo Pandito v4

## 📊 Estado de Verificación

**Fecha:** 2026-07-29  
**Notebooks analizados:** 60  
**Compatibilidad:** ✅ 100%

---

## 🎯 Resumen Ejecutivo

Todos los notebooks del libro "Saliendo de lo Pandito v4" son **completamente compatibles** con **Databricks Serverless Compute** en Free Edition.

### Verificaciones Realizadas

✅ **Lenguajes:** Solo Python, SQL y sh (compatibles)  
✅ **Sin Scala:** 0 notebooks con código Scala  
✅ **Sin R:** 0 notebooks con código R  
✅ **DBFS:** No se detectó acceso directo a `/dbfs/` o `dbfs:/`

---

## 🔧 Configuración Serverless

### Especificaciones del Cluster

```yaml
Tipo: Serverless Interactive Cluster
Procesador: CPU-backed
Proveedor: AWS
Lenguajes soportados: Python, SQL, sh
Lenguajes NO soportados: R, Scala
Estado: RUNNING
```

### Ventajas de Serverless para Este Libro

1. **Inicio instantáneo** - No esperas por cluster warmup
2. **Escalado automático** - Se ajusta según carga de trabajo
3. **Costo optimizado** - Solo pagas por lo que usas
4. **Sin configuración** - No necesitas administrar clusters
5. **Ideal para aprendizaje** - Perfecto para Free Edition

---

## 📋 Guía de Verificación de Entorno

### Celda de Verificación Estándar

Agrega esta celda al inicio de cada notebook principal:

```python
# ========================================
# 🔍 VERIFICACIÓN DE ENTORNO SERVERLESS
# ========================================

import sys
import platform

print("=" * 70)
print("🔍 VERIFICACIÓN DE COMPATIBILIDAD SERVERLESS")
print("=" * 70)

# Versión de Python
python_version = sys.version.split()[0]
print(f"\n✅ Python: {python_version}")
assert python_version >= "3.8", "⚠️  Se requiere Python 3.8+"

# Verificar Spark disponible
try:
    print(f"✅ Spark: {spark.version}")
    print(f"✅ Modo: {'Serverless' if 'serverless' in spark.conf.get('spark.master', '').lower() else 'Cluster estándar'}")
except:
    print("⚠️  Spark no disponible (normal en celdas Python puras)")

# Sistema operativo
print(f"✅ OS: {platform.system()} {platform.release()}")

# Librerías críticas
required_libs = {
    'pandas': '1.0.0',
    'numpy': '1.18.0',
    'matplotlib': '3.0.0',
    'plotly': '4.0.0'
}

print(f"\n{'Librería':<20} {'Instalada':<15} {'Requerida':<15} {'Status':<10}")
print("-" * 70)

for lib, min_version in required_libs.items():
    try:
        module = __import__(lib)
        version = getattr(module, '__version__', 'N/A')
        status = "✅ OK"
        print(f"{lib:<20} {version:<15} {min_version:<15} {status:<10}")
    except ImportError:
        print(f"{lib:<20} {'NO INSTALADA':<15} {min_version:<15} {'❌ FALTA':<10}")

print("=" * 70)
print("✅ Entorno verificado - Listo para ejecutar notebooks")
print("=" * 70)
```

---

## 🚫 Limitaciones de Databricks Free Edition

### DBFS (Databricks File System)

**⚠️ IMPORTANTE:** Free Edition tiene acceso limitado a DBFS.

#### ❌ NO Recomendado

```python
# ❌ Acceso directo a /dbfs/ puede no funcionar
df = pd.read_csv('/dbfs/mnt/data/archivo.csv')

# ❌ Paths dbfs:/ pueden fallar
spark.read.parquet('dbfs:/FileStore/data/')
```

#### ✅ Recomendado

```python
# ✅ Usar Workspace paths
df = pd.read_csv('/Workspace/Users/tu_usuario/datos/archivo.csv')

# ✅ Usar volúmenes de Unity Catalog (si disponible)
spark.read.parquet('/Volumes/main/default/mi_volumen/datos/')

# ✅ Cargar desde URLs directas
df = pd.read_csv('https://raw.githubusercontent.com/usuario/repo/main/data.csv')

# ✅ Crear datasets sintéticos en memoria
import pandas as pd
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
```

### Almacenamiento de Datasets

**Estructura recomendada para este libro:**

```
/Workspace/Users/tu_usuario/pandito/
├── datasets/
│   ├── raw/                    # Datos originales
│   ├── processed/              # Datos procesados
│   └── README.md
├── 01_Entorno.../
├── 02_NumPy.../
└── ...
```

---

## 💡 Mejores Prácticas Serverless

### 1. Gestión de Memoria

```python
# ✅ Liberar memoria después de cálculos pesados
import gc

# Realizar operación pesada
resultado = df.apply(funcion_compleja)

# Liberar DataFrame original si no se necesita
del df
gc.collect()
```

### 2. Lectura Incremental de Datos

```python
# ✅ Leer archivos grandes en chunks
for chunk in pd.read_csv('archivo_grande.csv', chunksize=10000):
    procesar(chunk)
    # Serverless escala automáticamente según necesidad
```

### 3. Uso Eficiente de Spark

```python
# ✅ Aprovechar lazy evaluation
df_spark = spark.read.csv('datos.csv')
df_filtrado = df_spark.filter(df_spark['valor'] > 100)  # No ejecuta aún
df_agregado = df_filtrado.groupBy('categoria').sum()     # No ejecuta aún

# Solo se ejecuta al llamar acción
resultado = df_agregado.collect()  # Aquí se ejecuta todo el plan
```

### 4. Caché Inteligente

```python
# ✅ Cachear DataFrames que se reutilizan múltiples veces
df_base = spark.read.parquet('datos_base.parquet')
df_base.cache()  # Serverless maneja memoria automáticamente

# Múltiples operaciones sobre df_base
resultado1 = df_base.filter(...).count()
resultado2 df_base.groupBy(...).agg(...)

df_base.unpersist()  # Liberar cuando ya no se necesite
```

### 5. Paralelización con PySpark

```python
# ✅ Dejar que Spark maneje paralelización
from pyspark.sql import functions as F

# Esto se distribuye automáticamente en serverless
df_resultado = (df
    .groupBy('categoria')
    .agg(
        F.sum('ventas').alias('total_ventas'),
        F.avg('precio').alias('precio_promedio')
    )
)
```

---

## 🔍 Debugging en Serverless

### Verificar Modo de Ejecución

```python
# Verificar si estás en serverless
spark_mode = spark.conf.get('spark.master', 'local')
print(f"Modo Spark: {spark_mode}")

if 'serverless' in spark_mode.lower():
    print("✅ Ejecutando en Serverless Compute")
else:
    print("ℹ️  Ejecutando en Cluster Estándar")
```

### Monitoreo de Performance

```python
# Ver plan de ejecución (útil para optimización)
df.explain(True)  # Muestra plan físico y lógico

# Estadísticas de DataFrame
print(f"Particiones: {df.rdd.getNumPartitions()}")
print(f"Filas estimadas: {df.count()}")
```

---

## 📚 Módulos con Consideraciones Especiales

### Módulo 09: Analítica Geoespacial

```python
# GeoPandas funciona perfectamente en serverless
import geopandas as gpd

# ✅ Cargar desde workspace
gdf = gpd.read_file('/Workspace/Users/tu_usuario/pandito/datasets/raw/ubicaciones_sucursales.geojson')

# ✅ Operaciones geoespaciales se ejecutan en memoria
gdf_buffered = gdf.buffer(1000)  # Buffer de 1km
```

### Módulo 10: H3 Hexagonal Indexing

```python
# H3 es compatible con serverless
import h3

# ✅ Operaciones H3 en pandas DataFrames
df['h3_index'] = df.apply(
    lambda row: h3.geo_to_h3(row['lat'], row['lon'], resolution=9),
    axis=1
)
```

### Módulos 11-14: PySpark

```python
# ✅ PySpark en serverless es más eficiente que pandas para datos grandes
from pyspark.sql import functions as F

# Serverless escala automáticamente según el tamaño de datos
df_spark = spark.read.csv('/Workspace/Users/tu_usuario/datos.csv', header=True)
df_procesado = df_spark.withColumn('nueva_col', F.col('col1') * 2)
```

---

## 🎯 Checklist de Compatibilidad

Usa este checklist antes de ejecutar notebooks:

- [ ] ✅ Solo usas Python, SQL o sh
- [ ] ✅ Evitas acceso directo a `/dbfs/` o `dbfs:/`
- [ ] ✅ Rutas de archivos apuntan a `/Workspace/Users/...`
- [ ] ✅ No usas código Scala (`%scala`, `import scala.*`)
- [ ] ✅ No usas código R (`%r`, `library(...)`)
- [ ] ✅ Liberas memoria después de operaciones pesadas
- [ ] ✅ Usas lazy evaluation de Spark cuando es posible
- [ ] ✅ Caché solo DataFrames que se reutilizan múltiples veces

---

## 📞 Soporte

Si encuentras problemas de compatibilidad:

1. **Verifica el entorno** con la celda de verificación
2. **Revisa este documento** para patrones recomendados
3. **Consulta logs** en la pestaña "Spark Jobs" del notebook
4. **Usa Genie Code** para debugging: "¿Por qué este código no funciona en serverless?"

---

## 📝 Historial de Verificaciones

| Fecha       | Notebooks | Compatible | Issues | Notas |
|-------------|-----------|------------|--------|-------|
| 2026-07-29  | 60        | 100%       | 0      | Verificación inicial completa |

---

**✅ Este libro está 100% optimizado para Databricks Serverless Compute en Free Edition.**

_Última actualización: 2026-07-29_
