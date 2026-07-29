# 📊 Datasets de Práctica - Saliendo de lo Pandito

Esta carpeta contiene datasets sintéticos diseñados específicamente para el libro "Saliendo de lo Pandito". Los datos son **ficticios pero realistas**, replicando estructuras y patrones de datos empresariales reales.

---

## 📁 Estructura de Carpetas

```
datasets/
├── raw/              # Datos en bruto (sin procesar)
│   ├── ventas_retail.csv
│   ├── transacciones_financieras.parquet
│   ├── ubicaciones_sucursales.geojson
│   └── logs_ecommerce.json
│
└── processed/       # Datos procesados (generados durante ejercicios)
    └── (vacío - lo poblarás durante el libro)
```

---

## 💾 Datasets Disponibles

### 1️⃣ ventas_retail.csv

**Descripción:** Transacciones de ventas de una cadena de retail tecnológico.

**Formato:** CSV (separado por comas)  
**Tamaño:** 1,000 filas × 15 columnas  
**Periodo:** Enero 2023 - Diciembre 2024  
**Encoding:** UTF-8

**Columnas:**
* `id_transaccion` (string): ID único de la transacción
* `fecha` (date): Fecha de la transacción (YYYY-MM-DD)
* `fecha_hora` (datetime): Fecha y hora completa
* `producto` (string): Nombre del producto vendido
* `categoria` (string): Categoría del producto (Computadoras, Accesorios, etc.)
* `cantidad` (int): Unidades vendidas
* `precio_unitario` (float): Precio por unidad
* `subtotal` (float): cantidad × precio_unitario
* `descuento_pct` (float): Porcentaje de descuento aplicado (0-30)
* `descuento_monto` (float): Monto en USD del descuento
* `total` (float): Monto final pagado
* `region` (string): Región geográfica (Norte, Sur, Este, Oeste, Centro)
* `vendedor` (string): Nombre del vendedor asignado
* `canal` (string): Canal de venta (Tienda, Online, App Móvil, Teléfono)
* `cliente_id` (string): ID del cliente

**Módulos donde se usa:** 03, 04, 05, 06, 07, 08, 12

**Casos de uso:**
* Análisis de ventas por categoría/región/vendedor
* Cálculo de KPIs (revenue, ticket promedio, productos top)
* Series de tiempo (tendencias mensuales)
* Visualizaciones (gráficos de barras, líneas, heatmaps)

---

### 2️⃣ transacciones_financieras.parquet

**Descripción:** Transacciones bancarias de 100 clientes ficticios.

**Formato:** Apache Parquet (columnar, comprimido)  
**Tamaño:** 1,500 filas × 15 columnas  
**Periodo:** Enero 2023 - Diciembre 2024  

**Columnas:**
* `transaccion_id` (string): ID único
* `fecha` (date): Fecha de la transacción
* `fecha_hora` (datetime): Timestamp completo
* `cliente_id` (string): ID del cliente
* `tipo_cuenta` (string): Corriente, Ahorro, Inversión
* `segmento` (string): Premium, Standard, Basic
* `tipo_transaccion` (string): Deposito, Retiro, Transferencia, etc.
* `categoria` (string): Supermercado, Restaurant, Electricidad, etc.
* `monto` (float): Monto de la transacción
* `tipo_movimiento` (string): Crédito o Débito
* `balance_anterior` (float): Balance antes de la transacción
* `balance_nuevo` (float): Balance después de la transacción
* `canal` (string): Cajero, Sucursal, App Móvil, Web, POS
* `status` (string): Aprobado, Rechazado, Pendiente
* `codigo_autorizacion` (string): Código de autorización (si aprobado)

**Módulos donde se usa:** 07, 11, 12, 13, 14

**Casos de uso:**
* Análisis de patrones de gasto por categoría
* Detección de anomalías (transacciones atípicas)
* Segmentación de clientes (RFM)
* Series de tiempo financieras
* Performance de PySpark con datos columnares

---

### 3️⃣ ubicaciones_sucursales.geojson

**Descripción:** Coordenadas y atributos de 50 sucursales en LATAM.

**Formato:** GeoJSON (estándar OGC)  
**Tamaño:** 50 features (puntos geográficos)  
**Sistema de coordenadas:** EPSG:4326 (WGS84)

**Propiedades:**
* `sucursal_id` (string): ID único
* `nombre` (string): Nombre de la sucursal
* `ciudad` (string): Ciudad donde se ubica
* `pais` (string): País
* `tipo` (string): Flagship, Regional, Local, Express
* `formato` (string): Mall, Street, Business District, Airport
* `fecha_apertura` (date): Fecha de inauguración
* `empleados` (int): Número de empleados
* `area_m2` (int): Área en metros cuadrados
* `ventas_anuales_usd` (int): Ventas anuales en USD
* `parking_disponible` (boolean): Tiene estacionamiento
* `horario_24h` (boolean): Abierto 24 horas
* `gerente` (string): Nombre del gerente
* `telefono` (string): Teléfono de contacto
* `rating_promedio` (float): Calificación promedio (3.5-5.0)

**Geometry:** Point (lat/lon)

**Módulos donde se usa:** 09, 10

**Casos de uso:**
* Visualización de sucursales en mapas
* Análisis de cobertura geográfica
* Clustering espacial (H3 hexagons)
* Optimización de logística y rutas
* Correlación entre ubicación y ventas

---

### 4️⃣ logs_ecommerce.json

**Descripción:** Eventos de comportamiento de usuarios en plataforma e-commerce.

**Formato:** JSON Lines (NDJSON - un objeto JSON por línea)  
**Tamaño:** 800 eventos  
**Periodo:** Diciembre 2024  

**Estructura:**
```json
{
  "timestamp": "2024-12-15T14:23:45",
  "event_id": "evt_000001",
  "user_id": "user_123",
  "session_id": "sess_456",
  "event_type": "product_view" | "add_to_cart" | "purchase" | ...,
  "event_data": { /* Datos específicos del evento */ },
  "device": {
    "type": "Desktop" | "Mobile" | "Tablet",
    "browser": "Chrome",
    "os": "Windows",
    "user_agent": "Mozilla/5.0...",
    "screen_resolution": "1920x1080"
  },
  "geo": {
    "country": "US",
    "city": "New York",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "is_bot": false,
  "response_time_ms": 234
}
```

**Tipos de eventos:**
* `page_view`: Visita a una página
* `product_view`: Ver detalle de producto
* `add_to_cart`: Agregar al carrito
* `remove_from_cart`: Eliminar del carrito
* `checkout_start`: Inicio de checkout
* `payment_info`: Ingreso de datos de pago
* `purchase`: Compra completada
* `search`: Búsqueda en el sitio
* `filter_apply`: Aplicación de filtro

**Módulos donde se usa:** 04, 11, 12, 13

**Casos de uso:**
* Funnel de conversión (visualización embudo)
* Análisis de comportamiento de usuarios
* Detección de bots (is_bot flag)
* Segmentación por dispositivo/navegador
* Performance analysis (response_time_ms)
* PySpark con datos semi-estructurados (JSON)

---

## 🛠️ Cómo Usar Estos Datasets

### Opción 1: Leer Directamente desde Notebooks

```python
import pandas as pd

# CSV
df_ventas = pd.read_csv('/Workspace/Users/<tu-email>/pandito/datasets/raw/ventas_retail.csv')

# Parquet
df_finanzas = pd.read_parquet('/Workspace/Users/<tu-email>/pandito/datasets/raw/transacciones_financieras.parquet')

# JSON Lines
df_logs = pd.read_json('/Workspace/Users/<tu-email>/pandito/datasets/raw/logs_ecommerce.json', lines=True)

# GeoJSON (requiere geopandas)
import geopandas as gpd
gdf_sucursales = gpd.read_file('/Workspace/Users/<tu-email>/pandito/datasets/raw/ubicaciones_sucursales.geojson')
```

### Opción 2: PySpark (Módulos 11-14)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("pandito").getOrCreate()

# CSV
df_ventas = spark.read.csv('/Workspace/Users/<tu-email>/pandito/datasets/raw/ventas_retail.csv', 
                           header=True, inferSchema=True)

# Parquet (más eficiente)
df_finanzas = spark.read.parquet('/Workspace/Users/<tu-email>/pandito/datasets/raw/transacciones_financieras.parquet')

# JSON
df_logs = spark.read.json('/Workspace/Users/<tu-email>/pandito/datasets/raw/logs_ecommerce.json')
```

### Opción 3: SQL Directo (Unity Catalog)

```sql
-- Primero, crear tablas externas
CREATE TABLE IF NOT EXISTS ventas_retail
USING CSV
OPTIONS (path '/Workspace/Users/<tu-email>/pandito/datasets/raw/ventas_retail.csv', header 'true');

-- Luego consultar
SELECT region, SUM(total) as revenue
FROM ventas_retail
GROUP BY region
ORDER BY revenue DESC;
```

---

## 💡 Buenas Prácticas

### 1️⃣ No Modifiques los Archivos en `/raw`
* Los datos en `raw/` son tu **fuente de verdad**
* Cualquier transformación guárdala en `processed/`
* Si necesitas regenerar datos, vuelve a ejecutar los scripts de generación

### 2️⃣ Nomenclatura de Archivos Procesados
```
processed/
├── ventas_retail_cleaned.csv           # Datos limpios
├── ventas_retail_agregado_mensual.csv  # Agregación
└── ventas_retail_con_kpis.parquet      # Con métricas calculadas
```

### 3️⃣ Formatos Recomendados
* **CSV**: Para datos pequeños (<10 MB) o cuando necesitas inspección manual
* **Parquet**: Para datos medianos/grandes (>10 MB), más rápido en PySpark
* **Delta Lake**: Para datos con versionamiento y ACID (módulos 13-14)

### 4️⃣ Versionamiento
Si modificas un dataset significativamente:
```
processed/
├── ventas_retail_v1.csv
├── ventas_retail_v2.csv  # Con columnas adicionales
└── ventas_retail_latest.csv  # Symlink o copia de la última versión
```

---

## 🤖 Generación de Datos Adicionales con Genie

**Prompt sugerido:**
```
Usando el esquema de ventas_retail.csv, genera 500 transacciones adicionales para Q1 2025.
Mantén consistencia en:
- Productos y precios similares
- Distribución de regiones
- Patrones de descuentos
Guarda como ventas_retail_q1_2025.csv en processed/
```

Genie Code puede generar datos adicionales que sigan los mismos patrones.

---

## 📊 Estadísticas de los Datasets

| Dataset | Formato | Tamaño en Disco | Filas | Columnas | Periodo |
|---------|---------|----------------|-------|----------|----------|
| ventas_retail | CSV | ~120 KB | 1,000 | 15 | 2023-2024 |
| transacciones_financieras | Parquet | ~80 KB | 1,500 | 15 | 2023-2024 |
| ubicaciones_sucursales | GeoJSON | ~25 KB | 50 | 15 + geometry | N/A |
| logs_ecommerce | JSON | ~600 KB | 800 | variable | Dic 2024 |

**Tamaño total:** ~825 KB

---

## ❓ Preguntas Frecuentes

**P: ¿Los datos son reales?**  
R: No, todos los datos son **completamente ficticios** generados con Python. Sin embargo, reflejan estructuras y patrones realistas de datos empresariales.

**P: ¿Puedo usar estos datos para proyectos personales?**  
R: Sí, los datos están bajo la misma licencia MIT del libro. Puedes usarlos libremente.

**P: ¿Cómo regenero los datasets si los daño?**  
R: Simplemente vuelve a ejecutar los notebooks de generación de datos (en esta carpeta o consulta al instructor).

**P: ¿Puedo crear mis propios datasets?**  
R: ¡Absolutamente! Usa los scripts de generación como templates y crea datasets para tu industria específica.

**P: ¿Por qué Parquet en vez de CSV para transacciones financieras?**  
R: Parquet es más eficiente para datos columnares y grandes volúmenes. Es el formato estándar en Big Data.

---

## 🔗 Recursos Adicionales

* **Pandas I/O:** [pandas.pydata.org/docs/user_guide/io.html](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)
* **PySpark Data Sources:** [spark.apache.org/docs/latest/sql-data-sources.html](https://spark.apache.org/docs/latest/sql-data-sources.html)
* **GeoPandas:** [geopandas.org](https://geopandas.org/)
* **GeoJSON Spec:** [geojson.org](https://geojson.org/)
* **Parquet Format:** [parquet.apache.org](https://parquet.apache.org/)

---

<div align="center">

### 🎓 ¡Feliz Análisis de Datos!

**"Datos de calidad = Análisis de calidad"**

[📖 Volver al Índice Principal](../README.md)

</div>