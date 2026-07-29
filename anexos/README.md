# 📚 Anexos - Saliendo de lo Pandito v4

**Recursos de referencia rápida para acompañarte durante todo el libro**

---

## 📖 Contenido

Este directorio contiene material de apoyo esencial para tu aprendizaje:

### 📄 Cheatsheets
Guías de consulta rápida con sintaxis y ejemplos:
* **[PANDAS_CHEATSHEET.md](cheatsheets/PANDAS_CHEATSHEET.md)** - 516 líneas de comandos esenciales de Pandas
* **[PYSPARK_CHEATSHEET.md](cheatsheets/PYSPARK_CHEATSHEET.md)** - 702 líneas de procesamiento distribuido con PySpark
* **[SQL_CHEATSHEET.md](cheatsheets/SQL_CHEATSHEET.md)** - 725 líneas de Databricks SQL
* **[PLOTLY_CHEATSHEET.md](cheatsheets/PLOTLY_CHEATSHEET.md)** - 530 líneas de visualizaciones interactivas

### 🔧 Troubleshooting
Soluciones a problemas comunes:
* **[COMMON_ERRORS.md](troubleshooting/COMMON_ERRORS.md)** - 658 líneas con errores frecuentes y sus soluciones

### 📖 Recursos
Material adicional y enlaces útiles

---

## 🎯 Cómo Usar Estos Anexos

### Durante el Estudio
1. **Mantén abierto el cheatsheet relevante** mientras trabajas en un módulo
2. **Usa Ctrl+F** para buscar comandos específicos rápidamente
3. **Copia y pega ejemplos** para probarlos en tus notebooks

### Durante el Debugging
1. **Consulta COMMON_ERRORS.md** cuando encuentres un error
2. **Busca el mensaje de error exacto** con Ctrl+F
3. **Aplica las soluciones sugeridas** paso a paso
4. Si no está en la guía, **pregúntale a Genie Code**

### Como Referencia Post-Libro
* Estos cheatsheets son **material de referencia permanente**
* Úsalos en tus proyectos reales después de terminar el libro
* Compártelos con tu equipo

---

## 📊 Estadísticas de Contenido

| Tipo | Archivos | Líneas Totales | Cobertura |
|------|----------|----------------|-----------|
| Cheatsheets | 4 | 2,473 líneas | Pandas, PySpark, SQL, Plotly |
| Troubleshooting | 1 | 658 líneas | 6 categorías de errores |
| **Total** | **5** | **3,131 líneas** | **Completo** |

---

## 🎓 Orden de Consulta Recomendado

### Módulos 01-03 (Python y NumPy)
* Consulta errores de Python en COMMON_ERRORS.md

### Módulos 03-10 (Pandas)
* Usa PANDAS_CHEATSHEET.md como referencia principal
* Consulta PLOTLY_CHEATSHEET.md para visualizaciones
* COMMON_ERRORS.md → Sección "Errores de Pandas"

### Módulos 11-14 (PySpark)
* Usa PYSPARK_CHEATSHEET.md como guía
* SQL_CHEATSHEET.md para consultas con spark.sql()
* COMMON_ERRORS.md → Sección "Errores de PySpark"

### Módulo 15 (Analítica Agéntica)
* Todos los cheatsheets son útiles
* Genie Code puede generar código basado en estos patrones

---

## 💡 Tips de Uso

### Búsqueda Eficiente
```
Ctrl+F (o Cmd+F en Mac) es tu mejor amigo:
- Busca "merge" en PANDAS_CHEATSHEET.md
- Busca "join" en PYSPARK_CHEATSHEET.md
- Busca "KeyError" en COMMON_ERRORS.md
```

### Copiar Código
Todos los ejemplos son:
* ✅ Probados y funcionales
* ✅ Listos para copiar y pegar
* ✅ Comentados con explicaciones
* ✅ Con variantes de uso

### Marcar Favoritos
Usa tu editor para marcar secciones frecuentes:
* En VS Code: Click derecho → "Add to Workspace Favorites"
* En navegador: Guarda como bookmark
* En Databricks: Agrega a "Favorites"

---

## 🔄 Actualizaciones

Este directorio se mantiene actualizado con:
* Nuevas soluciones a errores reportados por estudiantes
* Actualizaciones de sintaxis de Databricks
* Ejemplos adicionales solicitados
* Mejores prácticas emergentes

**Última actualización:** 2026-07-29

---

## 🤝 Contribuciones

Si encuentras:
* ❌ Un error no documentado
* 💡 Una solución más elegante
* 📝 Un ejemplo útil que falta

**¡Compártelo con la comunidad!**

---

## 📱 Acceso Rápido

### Enlaces Directos

* [Pandas Cheatsheet](cheatsheets/PANDAS_CHEATSHEET.md)
* [PySpark Cheatsheet](cheatsheets/PYSPARK_CHEATSHEET.md)
* [SQL Cheatsheet](cheatsheets/SQL_CHEATSHEET.md)
* [Plotly Cheatsheet](cheatsheets/PLOTLY_CHEATSHEET.md)
* [Guía de Errores](troubleshooting/COMMON_ERRORS.md)

### Por Categoría

**Lectura de Datos:**
* Pandas CSV: [PANDAS_CHEATSHEET.md](cheatsheets/PANDAS_CHEATSHEET.md#📂-lectura-y-escritura-de-archivos)
* PySpark Parquet: [PYSPARK_CHEATSHEET.md](cheatsheets/PYSPARK_CHEATSHEET.md#📂-lectura-de-datos)

**Transformaciones:**
* Pandas GroupBy: [PANDAS_CHEATSHEET.md](cheatsheets/PANDAS_CHEATSHEET.md#📊-agregaciones-y-groupby)
* PySpark Window: [PYSPARK_CHEATSHEET.md](cheatsheets/PYSPARK_CHEATSHEET.md#📐-window-functions)

**Visualizaciones:**
* Plotly Express: [PLOTLY_CHEATSHEET.md](cheatsheets/PLOTLY_CHEATSHEET.md#🎨-plotly-express-alto-nivel---recomendado)
* Dashboards: [PLOTLY_CHEATSHEET.md](cheatsheets/PLOTLY_CHEATSHEET.md#🎯-casos-de-uso-comunes)

---

## 🧞 Integración con Genie Code

**Tip Pro:** Combina estos cheatsheets con Genie Code:

```
Prompt: "Muéstrame cómo hacer un LEFT JOIN en PySpark según 
el cheatsheet, pero aplicado a mis tablas ventas y clientes"

→ Genie generará código personalizado basado en los patrones del cheatsheet
```

---

## 📚 Recursos Externos Complementarios

### Documentación Oficial
* **Databricks:** https://docs.databricks.com/
* **Pandas:** https://pandas.pydata.org/docs/
* **PySpark:** https://spark.apache.org/docs/latest/api/python/
* **Plotly:** https://plotly.com/python/

### Tutoriales Interactivos
* **Kaggle Learn:** https://www.kaggle.com/learn
* **DataCamp:** https://www.datacamp.com/
* **Real Python:** https://realpython.com/

### Comunidades
* **Stack Overflow - Databricks:** https://stackoverflow.com/questions/tagged/databricks
* **Stack Overflow - Pandas:** https://stackoverflow.com/questions/tagged/pandas
* **Reddit r/databricks:** https://reddit.com/r/databricks

---

## ✅ Checklist de Uso

Marca a medida que domines cada cheatsheet:

- [ ] He consultado PANDAS_CHEATSHEET.md al menos 5 veces
- [ ] He usado PYSPARK_CHEATSHEET.md para un proyecto real
- [ ] He visualizado datos con PLOTLY_CHEATSHEET.md
- [ ] He resuelto un error usando COMMON_ERRORS.md
- [ ] He guardado estos archivos en mis bookmarks
- [ ] He compartido estos recursos con un compañero

---

**💪 Objetivo:** Que estos cheatsheets se conviertan en tu segunda naturaleza. No se trata de memorizarlos, sino de saber *dónde* buscar cuando lo necesites.

_"El buen programador no es el que lo memoriza todo, sino el que sabe dónde buscar rápido."_

---

**🎓 Parte del libro "Saliendo de lo Pandito v4" - Databricks + Analítica Agéntica**
