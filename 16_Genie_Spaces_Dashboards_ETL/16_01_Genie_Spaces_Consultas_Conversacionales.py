# Databricks notebook source
# DBTITLE 1,⚡ Portada
# MAGIC %md
# MAGIC # 🤖 Módulo 16 - Notebook 01: Genie Spaces y consultas conversacionales
# MAGIC
# MAGIC ## 💬 Analítica con lenguaje natural sobre datos
# MAGIC
# MAGIC **Libro:** Saliendo de lo Pandito  
# MAGIC **Módulo:** 16 - Genie Spaces, Dashboards AI/BI y ETL  
# MAGIC **Duración estimada:** 60 minutos  
# MAGIC **Dificultad:** 🟡 Intermedio  
# MAGIC **Plataforma:** Databricks Free Edition
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objetivos de aprendizaje
# MAGIC
# MAGIC ✅ **Entender** qué es Genie Spaces y cómo funciona  
# MAGIC ✅ **Crear** un Genie Space sobre tablas de Unity Catalog  
# MAGIC ✅ **Hacer** consultas en lenguaje natural  
# MAGIC ✅ **Diferenciar** Genie Spaces de Genie Code  
# MAGIC ✅ **Integrar** Genie Spaces en el flujo de trabajo  
# MAGIC ✅ **Aplicar** analítica conversacional a casos reales
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Pre-requisitos
# MAGIC
# MAGIC * ✅ Módulos 05-15 completados
# MAGIC * ✅ Tablas en Unity Catalog (pandito_ds.default)
# MAGIC * ✅ Familiaridad con SQL y PySpark
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📚 Contenido
# MAGIC
# MAGIC 1. **¿Qué es Genie Spaces?** - Data rooms con IA
# MAGIC 2. **Crear un Genie Space** - Configuración
# MAGIC 3. **Consultas conversacionales** - Lenguaje natural a SQL
# MAGIC 4. **Genie Spaces vs Genie Code** - Diferencias
# MAGIC 5. **Casos de uso empresariales** - Análisis sin código

# COMMAND ----------

# DBTITLE 1,💾 Cargar Datos Reales
import pandas as pd

print("💾 VERIFICACIÓN DE DATOS PARA GENIE SPACES")
print("="*70)

CATALOG = "pandito_ds"
SCHEMA = "default"

try:
    df = spark.table(f"{CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3").toPandas()
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"✅ Tabla disponible: {CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
    print(f"   Registros: {len(df)}")
    print(f"   Columnas: {list(df.columns)}")
    print(f"   Sucursales: {df['sucursal_id'].nunique()}")
    print(f"   Período: {df['fecha'].min().strftime('%Y-%m')} a {df['fecha'].max().strftime('%Y-%m')}")
    USAR_DATOS_REALES = True
except Exception as e:
    print(f"⚠️  No se pudo cargar: {e}")
    USAR_DATOS_REALES = False

print("\n📌 Para crear un Genie Space:")
print(f"   1. Ve a Databricks > Genie > Create Space")
print(f"   2. Selecciona la tabla: {CATALOG}.{SCHEMA}.ventas_mensuales_mendoza_h3")
print(f"   3. Describe las columnas y su significado de negocio")
print(f"   4. Haz preguntas en lenguaje natural")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,📚 Teoría: Genie Spaces
# MAGIC %md
# MAGIC ## 📚 Teoría: Genie Spaces y Analítica Conversacional
# MAGIC
# MAGIC ### 🤖 ¿Qué es Genie Spaces?
# MAGIC
# MAGIC **Genie Spaces** (antes "Genie Rooms") son espacios de datos conversacionales donde usuarios no técnicos pueden hacer preguntas en lenguaje natural y recibir respuestas con datos, gráficos y tablas.
# MAGIC
# MAGIC ```
# MAGIC Usuario: "¿Cuál fue la sucursal con más ventas en 2023?"
# MAGIC     ↓
# MAGIC Genie Space (IA)
# MAGIC     ↓
# MAGIC Genera SQL automáticamente
# MAGIC     ↓
# MAGIC Respuesta: Tabla + Gráfico + Explicación
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔄 Genie Code vs Genie Spaces
# MAGIC
# MAGIC | Aspecto | Genie Code (Módulo 02) | Genie Spaces (Módulo 16) |
# MAGIC |---------|----------------------|--------------------------|
# MAGIC | **Qué hace** | Genera código Python/SQL | Responde preguntas en lenguaje natural |
# MAGIC | **Para quién** | Analistas que programan | Cualquier persona de negocio |
# MAGIC | **Salida** | Código en notebooks | Tablas, gráficos, respuestas |
# MAGIC | **Dónde** | En el notebook editor | Interfaz dedicada de Genie |
# MAGIC | **Requisito** | Conocer programación | Solo saber preguntar |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏗️ Cómo Crear un Genie Space
# MAGIC
# MAGIC 1. **Ir a Databricks > Genie > Create Space**
# MAGIC 2. **Seleccionar tablas** de Unity Catalog
# MAGIC 3. **Describir columnas**: Agregar descripciones de negocio
# MAGIC    * `ventas`: Monto total de ventas mensuales en ARS
# MAGIC    * `sucursal_id`: Código único de cada sucursal (S001-S005)
# MAGIC 4. **Agregar ejemplos**: Preguntas frecuentes con respuestas SQL
# MAGIC 5. **Probar**: Hacer preguntas y validar respuestas
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💬 Ejemplos de Consultas Conversacionales
# MAGIC
# MAGIC | Pregunta | SQL Generado |
# MAGIC |----------|-------------|
# MAGIC | "Top 5 sucursales por ventas" | `SELECT sucursal_id, SUM(ventas) ... ORDER BY ... LIMIT 5` |
# MAGIC | "Ventas por trimestre en 2023" | `SELECT QUARTER(fecha), SUM(ventas) ... WHERE YEAR(fecha) = 2023` |
# MAGIC | "Mes con menor ventas" | `SELECT fecha, ventas ... ORDER BY ventas ASC LIMIT 1` |
# MAGIC | "Comparar 2022 vs 2023" | `SELECT YEAR(fecha), SUM(ventas) ... GROUP BY YEAR(fecha)` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Por qué importa
# MAGIC
# MAGIC **Genie Spaces democratiza la analítica:**
# MAGIC * 📊 Cualquier persona puede consultar datos sin SQL
# MAGIC * 💬 Lenguaje natural = cero barrera técnica
# MAGIC * 🎯 Resultados inmediatos con gráficos automáticos
# MAGIC * 🔄 Actualizado: siempre usa datos frescos de Unity Catalog
# MAGIC * 🏢 Ideal para ejecutivos, gerentes, y equipos de negocio

# COMMAND ----------

# DBTITLE 1,💻 Setup Inicial
import pandas as pd

print("💻 SETUP: SIMULACIÓN DE CONSULTAS GENIE SPACES")
print("="*70)

if USAR_DATOS_REALES:
    # Simular lo que Genie Spaces haría con consultas en lenguaje natural
    print("\n📝 EJEMPLOS DE CONSULTAS CONVERSACIONALES:")
    print("\nPregunta: '¿Cuál fue la sucursal con más ventas totales?'")
    top_sucursal = df.groupby('sucursal_id')['ventas'].sum().idxmax()
    top_valor = df.groupby('sucursal_id')['ventas'].sum().max()
    print(f"Respuesta: {top_sucursal} con ${top_valor:,.2f} en ventas totales")

    print("\nPregunta: '¿Cómo evolucionaron las ventas por año?'")
    df['anio'] = df['fecha'].dt.year
    ventas_anuales = df.groupby('anio')['ventas'].agg(['sum', 'mean', 'count']).round(2)
    print(ventas_anuales)

    print("\nPregunta: '¿Cuál fue el mes con menores ventas en toda la historia?'")
    peor_mes = df.loc[df['ventas'].idxmin()]
    print(f"Respuesta: {peor_mes['fecha'].strftime('%Y-%m')} con ${peor_mes['ventas']:,.2f}")

    print("\nPregunta: 'Compara las ventas promedio de 2022 vs 2023'")
    v22 = df[df['anio']==2022]['ventas'].mean()
    v23 = df[df['anio']==2023]['ventas'].mean()
    print(f"2022: ${v22:,.2f} | 2023: ${v23:,.2f} | Diferencia: {(v23-v22)/v22*100:+.1f}%")

    print("\n📌 Estas consultas pueden hacerse en Genie Spaces sin escribir código")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)
print("✅ Genie Spaces revisado - Crear el space desde la interfaz de Databricks")

# COMMAND ----------

# DBTITLE 1,🤖 Teoría: Genie Spaces con datos reales
# MAGIC %md
# MAGIC ## 🤖 Genie Spaces aplicado a Los Andes Market
# MAGIC
# MAGIC ### 💬 Preguntas de negocio en lenguaje natural
# MAGIC
# MAGIC Un Genie Space sobre `ventas_mensuales_mendoza_h3` permitiría a ejecutivos de **Los Andes Market** hacer preguntas como:
# MAGIC
# MAGIC | Pregunta natural | SQL que Genie generaría |
# MAGIC |------------------|----------------------|
# MAGIC | "¿Qué zona vende más?" | `SELECT zona, SUM(ventas) ... GROUP BY zona` |
# MAGIC | "Top 3 sucursales de 2023" | `SELECT sucursal_nombre, SUM(ventas) ... WHERE YEAR(fecha)=2023 ORDER BY ... LIMIT 3` |
# MAGIC | "Ventas por trimestre" | `SELECT QUARTER(fecha), SUM(ventas) ... GROUP BY QUARTER(fecha)` |
# MAGIC | "¿Hay estacionalidad?" | `SELECT MONTH(fecha), AVG(ventas) ... GROUP BY MONTH(fecha)` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏗️ Configuración recomendada para Los Andes Market
# MAGIC
# MAGIC ```sql
# MAGIC -- Descripciones de columnas para Genie:
# MAGIC -- ventas: Monto total de ventas mensuales en ARS
# MAGIC -- sucursal_id: Código único de cada sucursal (SUC001-SUC005)
# MAGIC -- sucursal_nombre: Nombre legible de la sucursal
# MAGIC -- zona: Tipo de zona comercial (Centro Comercial, Zona Residencial, Corredor Comercial)
# MAGIC -- lat/lon: Coordenadas GPS de la sucursal en Mendoza
# MAGIC -- h3_index: Índice hexagonal H3 resolución 9 (~174m)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Para crear el Genie Space real
# MAGIC 1. Databricks > Genie > Create Space
# MAGIC 2. Seleccionar `pandito_ds.default.ventas_mensuales_mendoza_h3`
# MAGIC 3. Agregar las descripciones de columnas arriba
# MAGIC 4. Agregar 5-10 preguntas de ejemplo con sus respuestas SQL

# COMMAND ----------

# DBTITLE 1,🤖 Práctica: Simulación de Genie Spaces
import pandas as pd
import plotly.express as px

print("🤖 SIMULACIÓN DE CONSULTAS GENIE SPACES CON LOS ANDES MARKET")
print("="*70)

if USAR_DATOS_REALES and df is not None:
    df['anio'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    print("\n💬 CONSULTA 1: '¿Qué zona vende más en total?'")
    print("-"*70)
    zona_ventas = df.groupby('zona')['ventas'].sum().sort_values(ascending=False)
    print(f"\n   Respuesta:")
    for zona, ventas in zona_ventas.items():
        print(f"      {zona}: ${ventas:,.0f}")
    print(f"\n   💡 Genie generaría: SELECT zona, SUM(ventas) FROM ... GROUP BY zona ORDER BY SUM(ventas) DESC")

    print("\n" + "="*70)
    print("\n💬 CONSULTA 2: 'Top 5 sucursales por ventas promedio'")
    print("-"*70)
    top5 = df.groupby('sucursal_nombre')['ventas'].mean().sort_values(ascending=False).head(5)
    print(f"\n   Respuesta:")
    for suc, prom in top5.items():
        print(f"      {suc}: ${prom:,.0f}")

    print("\n" + "="*70)
    print("\n💬 CONSULTA 3: 'Compara ventas 2022 vs 2023 por zona'")
    print("-"*70)
    comp = df[df['anio'].isin([2022, 2023])].groupby(['zona', 'anio'])['ventas'].sum().unstack()
    comp['variacion_pct'] = ((comp[2023] - comp[2022]) / comp[2022] * 100).round(1)
    print(f"\n   Respuesta:")
    print(comp.round(0))

    print("\n" + "="*70)
    print("\n💬 CONSULTA 4: '¿Cuál es el mes con más ventas históricamente?'")
    print("-"*70)
    mes_avg = df.groupby('mes')['ventas'].mean().sort_values(ascending=False)
    print(f"\n   Mes con mayor promedio: Mes {mes_avg.index[0]} (${mes_avg.iloc[0]:,.0f})")
    print(f"   Mes con menor promedio: Mes {mes_avg.index[-1]} (${mes_avg.iloc[-1]:,.0f})")
    print("\n   Estacionalidad mensual:")
    print(mes_avg.round(0))

    print("\n" + "="*70)
    print("\n💬 CONSULTA 5: 'Muestra la evolución de ventas en un gráfico'")
    print("-"*70)
    evolucion = df.groupby('fecha')['ventas'].sum().reset_index()
    fig = px.line(evolucion, x='fecha', y='ventas',
                  title='Evolución de Ventas Totales - Los Andes Market',
                  template='plotly_white')
    fig.show()
    print("   💡 Genie generaría el SQL + el gráfico automáticamente")

    print("\n" + "="*70)
    print("\n📌 Para crear el Genie Space real:")
    print("   1. Databricks > Genie > Create Space")
    print("   2. Tabla: pandito_ds.default.ventas_mensuales_mendoza_h3")
    print("   3. Describir columnas con contexto de negocio")
    print("   4. Agregar estas 5 preguntas como ejemplos")
else:
    print("⚠️  No hay datos reales disponibles")

print("\n" + "="*70)

# COMMAND ----------

# DBTITLE 1,🎓 Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del notebook 16_01
# MAGIC
# MAGIC ### ✅ Lo que aprendiste
# MAGIC
# MAGIC 1. **Genie Spaces — analítica conversacional:**
# MAGIC    - Espacios de datos donde usuarios no técnicos hacen preguntas en lenguaje natural
# MAGIC    - La IA genera SQL automáticamente y devuelve tablas, gráficos y explicaciones
# MAGIC    - Cero barrera técnica: solo saber preguntar
# MAGIC
# MAGIC 2. **Crear un Genie Space:**
# MAGIC    - Databricks > Genie > Create Space
# MAGIC    - Seleccionar tablas de Unity Catalog
# MAGIC    - Describir columnas con contexto de negocio (ej: `ventas` = Monto mensual en ARS)
# MAGIC    - Agregar ejemplos de preguntas frecuentes con respuestas SQL
# MAGIC
# MAGIC 3. **Consultas conversacionales:**
# MAGIC    - Top 5 sucursales por ventas → `SELECT ... ORDER BY ... LIMIT 5`
# MAGIC    - Ventas por trimestre en 2023 → `SELECT QUARTER(fecha), SUM(ventas) ...`
# MAGIC    - Mes con menor ventas → `SELECT ... ORDER BY ventas ASC LIMIT 1`
# MAGIC    - La IA traduce lenguaje natural a SQL sin que el usuario escriba código
# MAGIC
# MAGIC 4. **Genie Spaces vs Genie Code:**
# MAGIC    - Genie Code: genera código Python/SQL para analistas que programan
# MAGIC    - Genie Spaces: responde preguntas en lenguaje natural para cualquier persona
# MAGIC    - Genie Code → notebooks; Genie Spaces → interfaz dedicada
# MAGIC
# MAGIC 5. **Casos de uso empresariales:**
# MAGIC    - Ejecutivos consultan KPIs sin esperar al equipo de datos
# MAGIC    - Gerentes analizan tendencias sin escribir SQL
# MAGIC    - Equipos de negocio exploran datos de forma autónoma
# MAGIC    - Siempre usa datos frescos de Unity Catalog
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎯 Reglas de Oro
# MAGIC
# MAGIC 👉 **Regla #1: Describir columnas con contexto de negocio**
# MAGIC ```python
# MAGIC # MALO: sin descripciones, Genie no entiende el significado
# MAGIC # ventas: DOUBLE
# MAGIC # sucursal_id: STRING
# MAGIC
# MAGIC # BUENO: descripciones con contexto
# MAGIC # ventas: Monto total de ventas mensuales en ARS
# MAGIC # sucursal_id: Codigo unico de cada sucursal (SUC001-SUC005)
# MAGIC # zona: Tipo de zona comercial (Centro, Residencial, Corredor)
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #2: Agregar ejemplos de preguntas frecuentes**
# MAGIC ```python
# MAGIC # MALO: Genie Space sin ejemplos, respuestas impredecibles
# MAGIC # (Genie adivina la intencion de cada pregunta desde cero)
# MAGIC
# MAGIC # BUENO: ejemplos guian a la IA
# MAGIC # Ejemplo 1: "Top 5 sucursales por ventas"
# MAGIC #   SELECT sucursal_id, SUM(ventas) GROUP BY sucursal_id ORDER BY SUM(ventas) DESC LIMIT 5
# MAGIC # Ejemplo 2: "Ventas por trimestre"
# MAGIC #   SELECT QUARTER(fecha) AS trimestre, SUM(ventas) GROUP BY trimestre
# MAGIC ```
# MAGIC
# MAGIC 👉 **Regla #3: Validar respuestas antes de compartir con stakeholders**
# MAGIC ```python
# MAGIC # MALO: compartir el Genie Space sin probar
# MAGIC # (respuestas incorrectas generan desconfianza permanente)
# MAGIC
# MAGIC # BUENO: probar 10-20 preguntas tipicas antes de publicar
# MAGIC # 1. Hacer la pregunta en Genie Space
# MAGIC # 2. Verificar el SQL generado
# MAGIC # 3. Comparar con el resultado esperado
# MAGIC # 4. Solo compartir cuando todo es correcto
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Guía de Decisión
# MAGIC
# MAGIC | Situación | Herramienta |
# MAGIC |-----------|-------------|
# MAGIC | Analista que programa necesita código | Genie Code (notebook editor) |
# MAGIC | Ejecutivo quiere KPIs sin código | Genie Spaces (interfaz dedicada) |
# MAGIC | Explorar datos interactivamente | Genie Spaces |
# MAGIC | Construir pipeline ETL | Genie Code (PySpark) |
# MAGIC | Crear dashboard para stakeholders | Genie Spaces + AI/BI Dashboards |
# MAGIC | Consulta ad-hoc de negocio | Genie Spaces |
# MAGIC | Reporte repetitivo programado | Genie Code + Databricks Jobs |
# MAGIC | Pregunta compleja con joins | Genie Code (más control) |
# MAGIC | Pregunta simple de negocio | Genie Spaces (más rápido) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
# MAGIC   <h3>🤖 ¡Genie Spaces y consultas conversacionales dominados!</h3>
# MAGIC   <p><i>"Genie Spaces democratiza la analítica: cualquier persona puede consultar datos sin escribir una línea de SQL."</i></p>
# MAGIC </div>