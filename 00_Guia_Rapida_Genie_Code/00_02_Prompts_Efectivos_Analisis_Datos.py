# Databricks notebook source
# DBTITLE 1,Portada
# MAGIC %md
# MAGIC # Saliendo de lo Pandito v4
# MAGIC ## Módulo 00.2: Biblioteca de Prompts Efectivos para Análisis de Datos
# MAGIC
# MAGIC ### 🎯 Objetivos:
# MAGIC 1. Dominar patrones de prompts por tipo de análisis
# MAGIC 2. Crear tu biblioteca personal de prompts reutilizables
# MAGIC 3. Aprender a adaptar prompts según el contexto de negocio
# MAGIC 4. Maximizar la efectividad de Genie Code en tareas comunes
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Filosofía de Este Notebook
# MAGIC
# MAGIC **No necesitas memorizar sintaxis de código.**  
# MAGIC **Necesitas dominar cómo comunicarte con tu asistente de IA.**
# MAGIC
# MAGIC Este notebook es tu "cheatsheet" de prompts para situaciones reales de negocio.

# COMMAND ----------

# DBTITLE 1,Patrón 1: Exploración de Datos
# MAGIC %md
# MAGIC ## 🔍 Patrón 1: Exploración de Datos (EDA)
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Explora la tabla/DataFrame [NOMBRE].
# MAGIC Muestra:
# MAGIC - Dimensiones (filas x columnas)
# MAGIC - Tipos de datos
# MAGIC - Valores nulos por columna
# MAGIC - Estadísticas descriptivas
# MAGIC - Primeras 5 filas de muestra
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Real: Tabla de Clientes
# MAGIC ```
# MAGIC Explora la tabla 'clientes_corporativos'.
# MAGIC Muestra:
# MAGIC - Total de clientes
# MAGIC - Distribución por industria
# MAGIC - Rango de ingresos anuales
# MAGIC - Clientes con datos faltantes en 'email'
# MAGIC - Top 5 clientes por revenue
# MAGIC ```
# MAGIC
# MAGIC ### Variantes Comunes
# MAGIC
# MAGIC **Para Data Quality:**
# MAGIC ```
# MAGIC Analiza la calidad de datos en 'ventas_2024':
# MAGIC - % de valores nulos por columna
# MAGIC - Duplicados (basado en 'id_transaccion')
# MAGIC - Outliers en 'monto_venta' (método IQR)
# MAGIC - Valores fuera de rango en 'descuento' (debe ser 0-100)
# MAGIC ```
# MAGIC
# MAGIC **Para Entendimiento de Negocio:**
# MAGIC ```
# MAGIC Crea un reporte ejecutivo de la tabla 'inventario':
# MAGIC - Total de productos
# MAGIC - Categorías con más SKUs
# MAGIC - Productos con stock < 10 unidades
# MAGIC - Valor total del inventario
# MAGIC - Producto más caro y más barato
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Patrón 2: Agregaciones y KPIs
# MAGIC %md
# MAGIC ## 📊 Patrón 2: Cálculo de Métricas y KPIs
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Usando [TABLA/DF], calcula:
# MAGIC - [METRICA_1]: [definición]
# MAGIC - [METRICA_2]: [definición]
# MAGIC Agrupa por [DIMENSION].
# MAGIC Ordena por [CRITERIO].
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Real: Métricas de Marketing
# MAGIC ```
# MAGIC Usando la tabla 'campanas_marketing', calcula:
# MAGIC - CAC (Customer Acquisition Cost): costo_campana / nuevos_clientes
# MAGIC - ROAS (Return on Ad Spend): ingresos_generados / costo_campana
# MAGIC - CTR (Click-Through Rate): clicks / impresiones * 100
# MAGIC Agrupa por canal (email, social, paid_search).
# MAGIC Ordena por ROAS descendente.
# MAGIC Muestra solo canales con ROAS > 2.0
# MAGIC ```
# MAGIC
# MAGIC ### Métricas Financieras
# MAGIC ```
# MAGIC Calcula el EBITDA mensual de 'estados_financieros':
# MAGIC - Ingresos: suma de 'revenue'
# MAGIC - COGS: suma de 'cost_of_goods'
# MAGIC - Gastos operativos: suma de 'opex'
# MAGIC - EBITDA = Ingresos - COGS - Gastos operativos
# MAGIC Agrupa por mes del año 2024.
# MAGIC Crea un gráfico waterfall mostrando la evolución mes a mes.
# MAGIC ```
# MAGIC
# MAGIC ### Métricas SaaS
# MAGIC ```
# MAGIC Calcula métricas SaaS de 'subscripciones':
# MAGIC - MRR (Monthly Recurring Revenue): suma de 'plan_price' donde status='activo'
# MAGIC - Churn Rate: (cancelaciones del mes / usuarios iniciales del mes) * 100
# MAGIC - ARPU: MRR / total de usuarios activos
# MAGIC - LTV: ARPU / Churn Rate
# MAGIC Compara mes actual vs mes anterior.
# MAGIC Highlight cambios > 10%.
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Patrón 3: Joins y Combinaciones
# MAGIC %md
# MAGIC ## 🔗 Patrón 3: Joins y Combinación de Tablas
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Combina [TABLA_1] con [TABLA_2] usando [TIPO_JOIN].
# MAGIC Clave: [COLUMNA_COMUN].
# MAGIC Selecciona: [COLUMNAS_FINALES].
# MAGIC Filtra: [CONDICIONES].
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo Real: Análisis de Pedidos
# MAGIC ```
# MAGIC Combina 'pedidos' con 'clientes' usando LEFT JOIN.
# MAGIC Clave: pedidos.customer_id = clientes.id
# MAGIC Además, combina con 'productos' usando LEFT JOIN.
# MAGIC Clave: pedidos.product_id = productos.sku
# MAGIC
# MAGIC Selecciona:
# MAGIC - pedidos.order_id
# MAGIC - clientes.nombre
# MAGIC - clientes.segmento
# MAGIC - productos.categoria
# MAGIC - pedidos.cantidad
# MAGIC - pedidos.precio_total
# MAGIC
# MAGIC Filtra solo pedidos de Q4 2024.
# MAGIC Agrupa por segmento de cliente y categoría de producto.
# MAGIC Muestra el total de ventas por combinación.
# MAGIC ```
# MAGIC
# MAGIC ### Join con Verificación de Calidad
# MAGIC ```
# MAGIC Combina 'transacciones' con 'usuarios' (INNER JOIN en user_id).
# MAGIC Antes de combinar:
# MAGIC - Verifica duplicados en ambas tablas por las claves
# MAGIC - Identifica registros en 'transacciones' sin match en 'usuarios'
# MAGIC - Muestra ¿cuántos registros se perderían con INNER vs LEFT JOIN?
# MAGIC Después, procede con el join que preserve todas las transacciones.
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Patrón 4: Filtrado y Segmentación
# MAGIC %md
# MAGIC ## 🎯 Patrón 4: Filtrado Complejo y Segmentación
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Filtra [TABLA/DF] donde:
# MAGIC - [CONDICION_1]
# MAGIC - [CONDICION_2]
# MAGIC - [CONDICION_3]
# MAGIC Retorna: [CAMPOS]
# MAGIC ```
# MAGIC
# MAGIC ### Segmentación RFM (Recency, Frequency, Monetary)
# MAGIC ```
# MAGIC Segmenta la tabla 'clientes' usando análisis RFM:
# MAGIC
# MAGIC 1. Recency: días desde última compra
# MAGIC    - Alta: < 30 días
# MAGIC    - Media: 30-90 días  
# MAGIC    - Baja: > 90 días
# MAGIC
# MAGIC 2. Frequency: número de compras en últimos 12 meses
# MAGIC    - Alta: >= 10 compras
# MAGIC    - Media: 5-9 compras
# MAGIC    - Baja: < 5 compras
# MAGIC
# MAGIC 3. Monetary: total gastado en últimos 12 meses
# MAGIC    - Alto: >= $5,000
# MAGIC    - Medio: $1,000-$4,999
# MAGIC    - Bajo: < $1,000
# MAGIC
# MAGIC Crea una columna 'segmento' combinando los tres:
# MAGIC Ejemplo: 'Alta_Recency_Alta_Frequency_Alto_Monetary' = 'Champions'
# MAGIC
# MAGIC Muestra la distribución de clientes por segmento con gráfico de barras.
# MAGIC ```
# MAGIC
# MAGIC ### Filtrado de Series de Tiempo
# MAGIC ```
# MAGIC De la tabla 'ventas_diarias', filtra:
# MAGIC - Solo días laborables (lunes a viernes)
# MAGIC - Excluye festivos de [lista_festivos]
# MAGIC - Solo transacciones con monto > percentil 25 (eliminar ruido)
# MAGIC - Periodo: Q4 2023 y Q4 2024 (para comparación YoY)
# MAGIC
# MAGIC Calcula las ventas promedio diarias para cada Q4.
# MAGIC Muestra el % de cambio.
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Patrón 5: Series de Tiempo
# MAGIC %md
# MAGIC ## 📈 Patrón 5: Análisis de Series de Tiempo
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Analiza la serie de tiempo en [TABLA] con columna fecha [COLUMNA_FECHA].
# MAGIC Métrica: [METRICA].
# MAGIC Calcula:
# MAGIC - Tendencia: [método]
# MAGIC - Estacionalidad: [periodo]
# MAGIC - Comparaciones: [YoY/MoM/WoW]
# MAGIC ```
# MAGIC
# MAGIC ### Ejemplo: Análisis de Revenue
# MAGIC ```
# MAGIC Analiza el revenue mensual de 'ventas' (2022-2024).
# MAGIC
# MAGIC Calcula:
# MAGIC 1. Revenue total por mes
# MAGIC 2. Promedio móvil de 3 meses (suavizar volatilidad)
# MAGIC 3. Crecimiento MoM (Month-over-Month): (mes_actual - mes_anterior) / mes_anterior
# MAGIC 4. Crecimiento YoY (Year-over-Year): comparar mismo mes año anterior
# MAGIC 5. Detecta meses atípicos (outliers) usando desviación estándar
# MAGIC
# MAGIC Visualiza todo en un gráfico de líneas múltiple:
# MAGIC - Línea azul: revenue real
# MAGIC - Línea roja: promedio móvil
# MAGIC - Banda gris: rango de confianza ± 1 std
# MAGIC ```
# MAGIC
# MAGIC ### Detección de Patrones
# MAGIC ```
# MAGIC Identifica patrones estacionales en 'trafico_web':
# MAGIC - Agrupa por día de la semana (lun-dom)
# MAGIC - Agrupa por hora del día (0-23)
# MAGIC - Crea un heatmap 2D: día x hora
# MAGIC - Valores: promedio de visitas
# MAGIC - Destaca las celdas con tráfico > promedio global + 1 std
# MAGIC
# MAGIC Respuesta esperada: ¿Cuándo deberíamos programar mantenimiento? (horarios de bajo tráfico)
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Patrón 6: Visualizaciones
# MAGIC %md
# MAGIC ## 🎨 Patrón 6: Generación de Visualizaciones
# MAGIC
# MAGIC ### Template Base
# MAGIC ```
# MAGIC Crea un [TIPO_GRAFICO] de [DATOS].
# MAGIC Eje X: [VARIABLE_X]
# MAGIC Eje Y: [VARIABLE_Y]
# MAGIC Color/Agrupación: [DIMENSION]
# MAGIC Estilo: [PREFERENCIAS]
# MAGIC ```
# MAGIC
# MAGIC ### Dashboard Ejecutivo Completo
# MAGIC ```
# MAGIC Crea un dashboard de ventas con 4 visualizaciones:
# MAGIC
# MAGIC 1. **KPI Cards** (arriba):
# MAGIC    - Revenue Total (número grande + % cambio vs mes anterior)
# MAGIC    - Número de Pedidos (número + % cambio)
# MAGIC    - Ticket Promedio (número + % cambio)
# MAGIC    - Tasa de Conversión (número + % cambio)
# MAGIC
# MAGIC 2. **Gráfico de Líneas** (izquierda):
# MAGIC    - Título: "Revenue Mensual vs Objetivo"
# MAGIC    - Línea azul sólida: revenue real
# MAGIC    - Línea verde punteada: objetivo
# MAGIC    - Periodo: últimos 12 meses
# MAGIC
# MAGIC 3. **Gráfico de Barras Horizontal** (derecha arriba):
# MAGIC    - Título: "Top 10 Productos por Ventas"
# MAGIC    - Color degradado según valor
# MAGIC    - Etiquetas con valores formateados ($XX,XXX)
# MAGIC
# MAGIC 4. **Heatmap** (derecha abajo):
# MAGIC    - Título: "Ventas por Región y Categoría"
# MAGIC    - Filas: regiones
# MAGIC    - Columnas: categorías de producto
# MAGIC    - Escala: verde (bajo) a rojo (alto)
# MAGIC
# MAGIC Usa Plotly. Estilo corporativo: colores #2C3E50, #E74C3C, #3498DB.
# MAGIC ```
# MAGIC
# MAGIC ### Waterfall Chart (P&L)
# MAGIC ```
# MAGIC Crea un gráfico waterfall del P&L trimestral:
# MAGIC
# MAGIC Datos de entrada:
# MAGIC - Ingresos: $500,000 (barra verde, hacia arriba)
# MAGIC - COGS: -$200,000 (barra roja, hacia abajo)
# MAGIC - Margen Bruto: $300,000 (barra azul, total parcial)
# MAGIC - Gastos de Ventas: -$80,000 (roja)
# MAGIC - Gastos Administrativos: -$60,000 (roja)
# MAGIC - EBITDA: $160,000 (barra azul, total parcial)
# MAGIC - Depreciación: -$20,000 (roja)
# MAGIC - Utilidad Neta: $140,000 (barra verde oscura, total final)
# MAGIC
# MAGIC Conectores entre barras. Etiquetas con valores. Título: "P&L Q4 2024".
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Biblioteca de Prompts por Industria
# MAGIC %md
# MAGIC ## 🏭 Biblioteca de Prompts por Industria
# MAGIC
# MAGIC ### 💰 Finanzas / Banca
# MAGIC ```
# MAGIC # Análisis de Cartera de Créditos
# MAGIC "Analiza la cartera de préstamos:
# MAGIC - Segmenta por score crediticio (300-579: malo, 580-669: regular, 670-739: bueno, 740+: excelente)
# MAGIC - Calcula tasa de morosidad (% con atraso > 30 días) por segmento
# MAGIC - Identifica correlación entre monto del préstamo y morosidad
# MAGIC - Proyecta pérdida esperada (morosidad * exposición)
# MAGIC - Visual: scatter plot con tamaño de punto = monto, color = morosidad"
# MAGIC
# MAGIC # Detección de Fraude
# MAGIC "Identifica transacciones sospechosas:
# MAGIC - Monto > 3 desviaciones estándar del promedio del usuario
# MAGIC - Transacciones en horario inusual (2am-6am)
# MAGIC - Cambios bruscos de geografía (transacción en 2 países en < 1 hora)
# MAGIC - Patrones de compras inconsistentes con historial
# MAGIC - Marca como 'alto_riesgo', 'medio_riesgo', 'bajo_riesgo'"
# MAGIC ```
# MAGIC
# MAGIC ### 🛍️ Retail / E-commerce
# MAGIC ```
# MAGIC # Market Basket Analysis
# MAGIC "Analiza combinaciones frecuentes de productos:
# MAGIC - Encuentra pares de productos comprados juntos (mínimo 50 transacciones)
# MAGIC - Calcula soporte: % de transacciones con ambos productos
# MAGIC - Calcula confianza: P(producto_B | producto_A)
# MAGIC - Calcula lift: confianza / P(producto_B)
# MAGIC - Recomienda 5 bundles con mayor lift > 1.5
# MAGIC - Estima incremento de revenue si se implementan"
# MAGIC
# MAGIC # Optimización de Inventario
# MAGIC "Analiza rotación de inventario:
# MAGIC - Calcula días de inventario: (stock_actual / ventas_promedio_dia)
# MAGIC - Identifica productos con > 90 días (overstocked)
# MAGIC - Identifica productos con < 7 días (riesgo de stockout)
# MAGIC - Sugiere cantidad óptima de reorden por producto
# MAGIC - Visualiza en matriz: rotación vs margen (priorizar acciones)"
# MAGIC ```
# MAGIC
# MAGIC ### 📦 Logística / Supply Chain
# MAGIC ```
# MAGIC # Análisis de Eficiencia de Rutas
# MAGIC "Analiza las rutas de entrega:
# MAGIC - Calcula distancia promedio por entrega
# MAGIC - Calcula tiempo promedio por entrega
# MAGIC - Identifica rutas con tiempo/distancia > percentil 75 (ineficientes)
# MAGIC - Agrupa entregas por zona geográfica (usar clustering k-means)
# MAGIC - Sugiere consolidación de rutas para reducir 15% los kms recorridos
# MAGIC - Estima ahorro en combustible ($3.50/galón, rendimiento 8 km/L)"
# MAGIC ```
# MAGIC
# MAGIC ### 🏭 SaaS / Tech
# MAGIC ```
# MAGIC # Cohort Retention Analysis
# MAGIC "Analiza retención de usuarios por cohorte de signup:
# MAGIC - Agrupa usuarios por mes de registro (cohortes)
# MAGIC - Para cada cohorte, calcula % de usuarios activos en mes 1, 2, 3, ..., 12
# MAGIC - Crea heatmap de retención: filas = cohortes, columnas = meses desde signup
# MAGIC - Identifica el mes con mayor churn (mayor caída %)
# MAGIC - Calcula LTV promedio por cohorte (asumiendo ARPU = $50/mes)
# MAGIC - Compara cohortes pre y post lanzamiento de feature X"
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Prompts para Debugging y Optimización
# MAGIC %md
# MAGIC ## 🔧 Prompts para Debugging y Optimización
# MAGIC
# MAGIC ### Debugging de Errores
# MAGIC ```
# MAGIC # Error Genérico
# MAGIC "Tengo este error: [COPIAR ERROR COMPLETO]
# MAGIC
# MAGIC Código que lo genera:
# MAGIC [COPIAR CÓDIGO]
# MAGIC
# MAGIC Explica:
# MAGIC 1. ¿Qué causa este error?
# MAGIC 2. ¿Cómo lo soluciono?
# MAGIC 3. ¿Cómo prevenirlo en el futuro?
# MAGIC 4. Dame el código corregido completo"
# MAGIC
# MAGIC # Performance Lento
# MAGIC "Esta consulta tarda 5 minutos en ejecutarse:
# MAGIC [SQL O PYSPARK]
# MAGIC
# MAGIC Tabla: 10M de filas, 50 columnas.
# MAGIC Optímizala:
# MAGIC - Sugerencias de índices
# MAGIC - Reescritura de la query
# MAGIC - Uso de particionamiento
# MAGIC - Filtrado temprano
# MAGIC - Evitar operaciones costosas
# MAGIC Dame el código optimizado y explica por qué es más rápido."
# MAGIC ```
# MAGIC
# MAGIC ### Refactorización de Código
# MAGIC ```
# MAGIC # De Pandas a PySpark
# MAGIC "Convierte este código Pandas a PySpark optimizado:
# MAGIC [CÓDIGO PANDAS]
# MAGIC
# MAGIC Consideraciones:
# MAGIC - La tabla tiene 500 GB (no cabe en memoria)
# MAGIC - Usa particionamiento por fecha
# MAGIC - Evita collect() y toPandas()
# MAGIC - Optimiza los joins (broadcast si aplica)
# MAGIC - Usa Delta Lake para escritura"
# MAGIC
# MAGIC # Limpieza de Código
# MAGIC "Refactoriza este código siguiendo mejores prácticas:
# MAGIC [CÓDIGO SUCIO]
# MAGIC
# MAGIC Mejora:
# MAGIC - Nombres de variables descriptivos
# MAGIC - Elimina código duplicado (DRY)
# MAGIC - Agrega docstrings
# MAGIC - Manejo de errores (try/except)
# MAGIC - Type hints (Python 3.10+)
# MAGIC - Comentarios claros
# MAGIC Dame el código refactorizado completo."
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Conclusiones
# MAGIC %md
# MAGIC ## 🎓 Conclusiones del Notebook 00_02
# MAGIC
# MAGIC ### ✅ Lo Que Aprendiste
# MAGIC
# MAGIC 1. **6 patrones de prompts** para casos de uso comunes:
# MAGIC    - Exploración de datos (EDA)
# MAGIC    - Cálculo de KPIs
# MAGIC    - Joins y combinaciones
# MAGIC    - Filtrado y segmentación
# MAGIC    - Series de tiempo
# MAGIC    - Visualizaciones
# MAGIC
# MAGIC 2. **Biblioteca de prompts por industria** (Finanzas, Retail, SaaS, Logística)
# MAGIC
# MAGIC 3. **Prompts de debugging y optimización**
# MAGIC
# MAGIC ### 📚 Cómo Usar Esta Biblioteca
# MAGIC
# MAGIC **Paso 1:** Identifica tu tipo de análisis (EDA, KPI, Join, etc.)  
# MAGIC **Paso 2:** Copia el template correspondiente  
# MAGIC **Paso 3:** Reemplaza los placeholders con tus datos específicos  
# MAGIC **Paso 4:** Pégalo en Genie Code  
# MAGIC **Paso 5:** Refina iterativamente si es necesario
# MAGIC
# MAGIC ### 💡 Próximo Paso
# MAGIC
# MAGIC Ahora que dominas los prompts, aprende cómo **depurar errores** efectivamente con IA:
# MAGIC
# MAGIC **Siguiente notebook:** [00_03_Debugging_Asistido_IA](#notebook-00_03)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <div style="background: #27ae60; padding: 15px; border-radius: 10px; color: white;">
# MAGIC   <h3>📖 Bookmark Este Notebook</h3>
# MAGIC   <p><i>Volverás aquí constantemente durante tu aprendizaje.</i></p>
# MAGIC </div>