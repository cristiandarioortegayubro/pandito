# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🗄️ Módulo 15 - Notebook 03: Delta Lake ACID y Time Travel
# MAGIC
# MAGIC ## ⏪ Almacenamiento transaccional y versionado de datos
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 15 - Delta Lake, Window Functions y Optimización  
# MAGIC **Duración estimada:** 70 minutos  
# MAGIC **Dificultad:** 🔴 Avanzado  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué es Delta Lake y sus ventajas  
# MAGIC ✅ **Aplicar** operaciones ACID en tablas Delta  
# MAGIC ✅ **Usar** Time Travel para auditoría y rollback  
# MAGIC ✅ **Gestionar** versiones de datos con DESCRIBE HISTORY  
# MAGIC ✅ **Implementar** MERGE, UPDATE y DELETE en Delta  
# MAGIC ✅ **Optimizar** tablas Delta (OPTIMIZE, VACUUM)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC * ✅ Notebooks 15_01 y 15_02 completados
# MAGIC * ✅ Conocimiento de PySpark SQL
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC 1. **Delta Lake** - Formato ACID para data lakes
# MAGIC 2. **CREATE TABLE Delta** - Crear tablas transaccionales
# MAGIC 3. **Time Travel** - Versionado y rollback
# MAGIC 4. **MERGE/UPDATE/DELETE** - Operaciones ACID
# MAGIC 5. **OPTIMIZE y VACUUM** - Mantenimiento de tablas

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
from pyspark.sql.functions import col

print("💾 SETUP DELTA LAKE")
print("="*70)

# Crear tabla Delta de prueba
spark.sql("USE CATALOG pandito_ds")
spark.sql("USE SCHEMA default")

# Verificar si la tabla principal es Delta
print("\n📋 Verificando formato de tablas:")
try:
    spark.sql("DESCRIBE TABLE EXTENDED pandito_ds.default.ventas_mensuales_mendoza_h3").show(truncate=False)
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Delta Lake
# MAGIC %md
# MAGIC ## 📚 Teoría: Delta Lake y Time Travel
# MAGIC
# MAGIC ### 🗄️ ¿Qué es Delta Lake?
# MAGIC
# MAGIC **Delta Lake** es una capa de almacenamiento transaccional (ACID) sobre data lakes (Parquet).
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────┐
# MAGIC │        Aplicaciones / SQL       │
# MAGIC ├─────────────────────────────────┤
# MAGIC │      DELTA LAKE (ACID)          │  ← Transacciones, Time Travel
# MAGIC ├─────────────────────────────────┤
# MAGIC │      Parquet + Log              │  ← Archivos inmutables
# MAGIC ├─────────────────────────────────┤
# MAGIC │     Almacenamiento (S3/ADLS)    │
# MAGIC └─────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚡ Ventajas de Delta Lake
# MAGIC
# MAGIC | Característica | Parquet | Delta Lake |
# MAGIC |----------------|---------|-------------|
# MAGIC | **ACID** | ❌ No | ✅ Sí |
# MAGIC | **Time Travel** | ❌ No | ✅ Versionado |
# MAGIC | **MERGE/UPSERT** | ❌ No | ✅ Sí |
# MAGIC | **Schema Evolution** | Limitado | ✅ Automático |
# MAGIC | **Concurrencia** | Conflictos | ✅ Aislamiento |
# MAGIC | **Streaming** | Requiere extra | ✅ Nativo |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⏪ Time Travel: Viajar en el Tiempo
# MAGIC
# MAGIC ```sql
# MAGIC -- Ver historial de versiones
# MAGIC DESCRIBE TABLE EXTENDED pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Consultar versión anterior (por timestamp)
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3 VERSION AS OF 1;
# MAGIC
# MAGIC -- Consultar por timestamp
# MAGIC SELECT * FROM ventas_mensuales_mendoza_h3 TIMESTAMP AS OF '2024-01-01';
# MAGIC
# MAGIC -- Comparar dos versiones
# MAGIC SELECT COUNT(*) FROM ventas_mensuales_mendoza_h3 VERSION AS OF 1;
# MAGIC SELECT COUNT(*) FROM ventas_mensuales_mendoza_h3 VERSION AS OF 2;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 MERGE: Upsert en Delta Lake
# MAGIC
# MAGIC ```sql
# MAGIC MERGE INTO pandito_ds.default.ventas_mensuales_mendoza_h3 AS target
# MAGIC USING nuevos_datos AS source
# MAGIC ON target.sucursal_id = source.sucursal_id AND target.fecha = source.fecha
# MAGIC WHEN MATCHED THEN UPDATE SET ventas = source.ventas
# MAGIC WHEN NOT MATCHED THEN INSERT *;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Mantenimiento: OPTIMIZE y VACUUM
# MAGIC
# MAGIC ```sql
# MAGIC -- Compactar archivos pequeños
# MAGIC OPTIMIZE pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Con ZORDER (clustering)
# MAGIC OPTIMIZE pandito_ds.default.ventas_mensuales_mendoza_h3 ZORDER BY (sucursal_id);
# MAGIC
# MAGIC -- Limpiar versiones antiguas
# MAGIC VACUUM pandito_ds.default.ventas_mensuales_mendoza_h3 RETAIN 168 HOURS;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Delta Lake = confianza en datos:**
# MAGIC * 🔒 **ACID:** Transacciones confiables en Big Data
# MAGIC * ⏪ **Auditoría:** Quién cambió qué y cuándo
# MAGIC * 🔄 **Rollback:** Revertir cambios erróneos
# MAGIC * 📊 **Streaming + Batch:** Un formato para ambos mundos
# MAGIC * 🏢 **Producción:** Estándar en Databricks

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
from pyspark.sql.functions import col, lit
import warnings
warnings.filterwarnings('ignore')

print("💻 EJERCICIOS: DELTA LAKE Y TIME TRAVEL")
print("="*70)

# Ejercicio 1: Crear tabla Delta de prueba
print("\n1️⃣ Creando tabla Delta de prueba:")
spark.sql("""
    CREATE TABLE IF NOT EXISTS pandito_ds.default.delta_prueba
    USING DELTA
    AS SELECT sucursal_id, fecha, ventas 
    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
    WHERE ventas > 50000
""")
count1 = spark.sql("SELECT COUNT(*) as total FROM pandito_ds.default.delta_prueba").collect()[0][0]
print(f"   Registros iniciales: {count1}")

# Ejercicio 2: Insertar más datos (crear versión 2)
print("\n2️⃣ Insertando nuevos datos (versión 2):")
spark.sql("""
    INSERT INTO pandito_ds.default.delta_prueba
    SELECT sucursal_id, fecha, ventas
    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
    WHERE ventas <= 50000 AND ventas > 30000
""")
count2 = spark.sql("SELECT COUNT(*) as total FROM pandito_ds.default.delta_prueba").collect()[0][0]
print(f"   Registros después de insert: {count2}")

# Ejercicio 3: Time Travel - comparar versiones
print("\n3️⃣ Time Travel - Versiones:")
try:
    old_count = spark.sql("SELECT COUNT(*) as total FROM pandito_ds.default.delta_prueba VERSION AS OF 1").collect()[0][0]
    print(f"   Versión 1: {old_count} registros")
    print(f"   Versión actual: {count2} registros")
    print(f"   Diferencia: {count2 - old_count} registros agregados")
except Exception as e:
    print(f"   Time Travel requiere versiones múltiples: {e}")

# Ejercicio 4: DESCRIBE HISTORY
print("\n4️⃣ Historial de la tabla:")
try:
    spark.sql("DESCRIBE HISTORY pandito_ds.default.delta_prueba").select("version", "operation", "operationParameters").show(5)
except Exception as e:
    print(f"   {e}")

# Limpiar tabla de prueba
spark.sql("DROP TABLE IF EXISTS pandito_ds.default.delta_prueba")

print("\n" + "="*70)
print("✅ Delta Lake y Time Travel completado")

# COMMAND ----------

# DBTITLE 1,🗄️ Teoría: Delta Lake con datos reales
# MAGIC %md
# MAGIC ## 🗄️ Delta Lake aplicado a Los Andes Market
# MAGIC
# MAGIC ### ⏪ Time Travel para auditoría de ventas
# MAGIC
# MAGIC La tabla `ventas_mensuales_mendoza_h3` es una tabla Delta en Unity Catalog. Esto significa:
# MAGIC * **ACID:** Cada operación es transaccional (rollback automático ante fallo)
# MAGIC * **Time Travel:** Podemos consultar versiones anteriores de los datos
# MAGIC * **MERGE:** Upsert atómico para actualizar/insertar en una sola operación
# MAGIC
# MAGIC ```sql
# MAGIC -- Ver historial de cambios en la tabla
# MAGIC DESCRIBE HISTORY pandito_ds.default.ventas_mensuales_mendoza_h3;
# MAGIC
# MAGIC -- Consultar versión anterior
# MAGIC SELECT COUNT(*) FROM pandito_ds.default.ventas_mensuales_mendoza_h3 VERSION AS OF 1;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Casos de negocio con Delta Lake
# MAGIC * **Auditoría:** ¿Qué cambió entre versiones de la tabla?
# MAGIC * **Rollback:** Restaurar datos a una versión anterior tras un error
# MAGIC * **MERGE:** Actualizar ventas de un mes específico sin afectar el resto
# MAGIC * **OPTIMIZE:** Compactar archivos para consultas más rápidas

# COMMAND ----------

# DBTITLE 1,🗄️ Práctica: Delta Lake con datos reales
from pyspark.sql.functions import col, lit

print("🗄️ DELTA LAKE APLICADO A LOS ANDES MARKET")
print("="*70)

print("\n1️⃣  DESCRIBE HISTORY: Historial de la tabla real")
print("-"*70)
try:
    spark.sql("DESCRIBE HISTORY pandito_ds.default.ventas_mensuales_mendoza_h3")
        .select("version", "operation", "operationParameters")
        .show(5, truncate=50)
except Exception as e:
    print(f"   {e}")

print("\n" + "="*70)
print("\n2️⃣  TIME TRAVEL: Contar registros por versión")
print("-"*70)
try:
    current = spark.sql("SELECT COUNT(*) AS total FROM pandito_ds.default.ventas_mensuales_mendoza_h3").collect()[0][0]
    print(f"   Versión actual: {current:,} registros")

    for v in range(3):
        try:
            c = spark.sql(f"SELECT COUNT(*) AS total FROM pandito_ds.default.ventas_mensuales_mendoza_h3 VERSION AS OF {v}").collect()[0][0]
            print(f"   Versión {v}: {c:,} registros")
        except:
            pass
except Exception as e:
    print(f"   {e}")

print("\n" + "="*70)
print("\n3️⃣  MERGE: Simular UPSERT en tabla Delta")
print("-"*70)

# Crear tabla Delta de prueba con ventas de Los Andes Market
spark.sql("""
    CREATE TABLE IF NOT EXISTS pandito_ds.default.delta_ventas_prueba
    USING DELTA
    AS SELECT sucursal_id, sucursal_nombre, zona, fecha, ventas
    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
    WHERE ventas > 100000
""")
count_before = spark.sql("SELECT COUNT(*) AS total FROM pandito_ds.default.delta_ventas_prueba").collect()[0][0]
print(f"   Tabla creada: {count_before:,} registros (ventas > 100k)")

# Crear datos de actualización (ventas ajustadas)
spark.sql("""
    CREATE OR REPLACE TEMP VIEW actualizaciones AS
    SELECT sucursal_id, sucursal_nombre, zona, fecha, 
           ROUND(ventas * 1.1, 2) AS ventas
    FROM pandito_ds.default.ventas_mensuales_mendoza_h3
    WHERE ventas > 150000
    LIMIT 20
""")

# Ejecutar MERGE
spark.sql("""
    MERGE INTO pandito_ds.default.delta_ventas_prueba AS target
    USING actualizaciones AS source
    ON target.sucursal_id = source.sucursal_id AND target.fecha = source.fecha
    WHEN MATCHED THEN UPDATE SET ventas = source.ventas
    WHEN NOT MATCHED THEN INSERT *
""")
count_after = spark.sql("SELECT COUNT(*) AS total FROM pandito_ds.default.delta_ventas_prueba").collect()[0][0]
print(f"   Después de MERGE: {count_after:,} registros")
print(f"   Registros afectados: {count_after - count_before}")
print("   💡 MERGE actualiza existentes + inserta nuevos en una operación atómica")

print("\n" + "="*70)
print("\n4️⃣  TIME TRAVEL en tabla de prueba: Antes vs después del MERGE")
print("-"*70)
try:
    before_merge = spark.sql("SELECT COUNT(*) AS total FROM pandito_ds.default.delta_ventas_prueba VERSION AS OF 0").collect()[0][0]
    after_merge = spark.sql("SELECT COUNT(*) AS total FROM pandito_ds.default.delta_ventas_prueba").collect()[0][0]
    print(f"   Antes del MERGE (v0): {before_merge:,}")
    print(f"   Después del MERGE:    {after_merge:,}")
    print("   ⏪ Time Travel permite comparar antes/después de cualquier operación")
except Exception as e:
    print(f"   {e}")

print("\n" + "="*70)
print("\n5️⃣  OPTIMIZE: Compactar archivos de la tabla de prueba")
print("-"*70)
try:
    spark.sql("OPTIMIZE pandito_ds.default.delta_ventas_prueba ZORDER BY (sucursal_id)")
    print("   ✅ OPTIMIZE + ZORDER BY (sucursal_id) ejecutado")
    print("   💡 ZORDER agrupa registros con mismo sucursal_id en archivos cercanos")
except Exception as e:
    print(f"   OPTIMIZE no disponible en Free Edition: {e}")

# Limpieza
spark.sql("DROP TABLE IF EXISTS pandito_ds.default.delta_ventas_prueba")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 15_03
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Delta Lake — capa transaccional ACID sobre Parquet:**
# MAGIC    - `USING DELTA` al crear tablas habilita ACID, Time Travel y MERGE
# MAGIC    - Archivos Parquet inmutables + transaction log (`_delta_log/`)
# MAGIC    - Estándar en Databricks: reemplaza a Parquet plano en producción
# MAGIC
# MAGIC 2. **CREATE TABLE Delta y CTAS:**
# MAGIC    - `CREATE TABLE ... USING DELTA AS SELECT ...` — crear desde consulta
# MAGIC    - `INSERT INTO ... SELECT ...` — agregar datos (crea nueva versión)
# MAGIC    - Cada operación crea una versión incremental en el log
# MAGIC
# MAGIC 3. **Time Travel — versionado y rollback:**
# MAGIC    - `SELECT ... VERSION AS OF N` — consultar versión específica
# MAGIC    - `SELECT ... TIMESTAMP AS OF '2024-01-01'` — consultar por timestamp
# MAGIC    - `DESCRIBE HISTORY tabla` — ver todas las versiones y operaciones
# MAGIC    - Permite auditoría: qué cambió, cuándo y quién
# MAGIC
# MAGIC 4. **MERGE / UPDATE / DELETE — operaciones ACID:**
# MAGIC    - `MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT`
# MAGIC    - UPSERT atómico: insertar nuevos + actualizar existentes en una operación
# MAGIC    - `UPDATE ... WHERE ...` y `DELETE ... WHERE ...` — modificaciones transaccionales
# MAGIC
# MAGIC 5. **OPTIMIZE y VACUUM — mantenimiento:**
# MAGIC    - `OPTIMIZE tabla` — compacta archivos pequeños en archivos más grandes
# MAGIC    - `OPTIMIZE tabla ZORDER BY (col)` — clustering para queries más rápidas
# MAGIC    - `VACUUM tabla RETAIN 168 HOURS` — elimina versiones antiguas (default: 7 días)
# MAGIC    - VACUUM libera espacio pero elimina capacidad de Time Travel
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Siempre usar USING DELTA en producción**
# MAGIC ```sql
# MAGIC -- MALO: Parquet plano, sin ACID ni Time Travel
# MAGIC CREATE TABLE ventas AS SELECT * FROM fuente;
# MAGIC
# MAGIC -- BUENO: Delta Lake con ACID y versionado
# MAGIC CREATE TABLE ventas USING DELTA AS SELECT * FROM fuente;
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: VACUUM elimina Time Travel, usar con cuidado**
# MAGIC ```sql
# MAGIC -- MALO: VACUUM sin retención, borra TODAS las versiones antiguas
# MAGIC VACUUM tabla RETAIN 0 HOURS;  -- ⚠️ No se puede hacer Time Travel
# MAGIC
# MAGIC -- BUENO: retener al menos 7 días para auditoría
# MAGIC VACUUM tabla RETAIN 168 HOURS;  -- 7 días de historial preservado
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: MERGE para UPSERT, no INSERT + UPDATE separados**
# MAGIC ```sql
# MAGIC -- MALO: dos operaciones separadas, no atómicas
# MAGIC INSERT INTO tabla SELECT * FROM nuevos WHERE id NOT IN (SELECT id FROM tabla);
# MAGIC UPDATE tabla SET ventas = (SELECT ventas FROM nuevos WHERE id = tabla.id);
# MAGIC
# MAGIC -- BUENO: MERGE atómico en una sola operación
# MAGIC MERGE INTO tabla AS t USING nuevos AS s
# MAGIC ON t.id = s.id
# MAGIC WHEN MATCHED THEN UPDATE SET ventas = s.ventas
# MAGIC WHEN NOT MATCHED THEN INSERT *;
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Método |
# MAGIC |-----------|--------|
# MAGIC | Crear tabla transaccional | `CREATE TABLE ... USING DELTA` |
# MAGIC | Crear desde consulta | `CREATE TABLE ... USING DELTA AS SELECT ...` |
# MAGIC | Consultar versión anterior | `SELECT ... VERSION AS OF N` |
# MAGIC | Consultar por fecha | `SELECT ... TIMESTAMP AS OF 'fecha'` |
# MAGIC | Ver historial de cambios | `DESCRIBE HISTORY tabla` |
# MAGIC | Insertar o actualizar (UPSERT) | `MERGE INTO ... WHEN MATCHED / NOT MATCHED` |
# MAGIC | Actualizar filas existentes | `UPDATE tabla SET col = val WHERE cond` |
# MAGIC | Eliminar filas | `DELETE FROM tabla WHERE cond` |
# MAGIC | Compactar archivos pequeños | `OPTIMIZE tabla` |
# MAGIC | Optimizar queries por columna | `OPTIMIZE tabla ZORDER BY (col)` |
# MAGIC | Liberar espacio antiguo | `VACUUM tabla RETAIN 168 HOURS` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>⏪ ¡Delta Lake ACID y Time Travel dominados!</h3>
# MAGIC   <p><i>"Delta Lake = confianza: ACID para transacciones, Time Travel para auditoría, MERGE para UPSERT atómico."</i></p>
# MAGIC </div>