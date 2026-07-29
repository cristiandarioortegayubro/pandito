# 🚀 Módulo 01: Entorno de Trabajo Unificado con Databricks Free Edition & GitHub

## 🎯 Objetivo del Módulo

Este módulo establece los cimientos de tu infraestructura de análisis de datos en la nube. Aprenderás a configurar **Databricks Community Edition (Free Edition)**, conectar tu repositorio de GitHub y dominar el entorno interactivo de notebooks.

**Al finalizar este módulo podrás:**
* ✅ Crear y configurar tu workspace de Databricks Free Edition
* ✅ Conectar GitHub Repos para versionamiento de código
* ✅ Navegar el entorno de notebooks y ejecutar código Python/SQL
* ✅ Comprender la arquitectura de DBFS (Databricks File System)
* ✅ Establecer buenas prácticas de desarrollo para análisis

---

## 📚 Contenido del Módulo

### [01_01_Configuracion_Databricks_y_Git](./01_01_Configuracion_Databricks_y_Git)
**Duración:** 30 minutos | **Dificultad:** Principiante

**Temas cubiertos:**
* Registro en Databricks Community Edition (paso a paso)
* Arquitectura básica de Databricks (workspace, clusters, notebooks)
* Configuración de Git integration con GitHub
* Clonación del repositorio del libro
* Primera ejecución de código en Databricks

**Conceptos clave:**
* Databricks Workspace vs Home directory
* Serverless compute (qué es y qué limitaciones tiene)
* Git repos en Databricks

**Resultado esperado:** Workspace configurado y repositorio clonado

---

### [01_02_Introduccion_a_Python_en_Databricks](./01_02_Introduccion_a_Python_en_Databricks)
**Duración:** 40 minutos | **Dificultad:** Principiante

**Temas cubiertos:**
* Variables y tipos de datos básicos
* Operadores aritméticos y lógicos
* Estructuras de datos: listas, diccionarios, tuplas, sets
* Contexto empresarial: modelar datos de negocio con estructuras nativas

**Ejercicios prácticos:**
* Crear diccionarios para productos con precios
* Listas de transacciones diarias
* Operaciones básicas con datos financieros

**Resultado esperado:** Dominio de sintaxis Python básica aplicada a datos de negocio

---

### [01_03_Estructuras_Control_y_Funciones](./01_03_Estructuras_Control_y_Funciones)
**Duración:** 45 minutos | **Dificultad:** Principiante

**Temas cubiertos:**
* Condicionales (if/elif/else) para lógica de negocio
* Bucles (for/while) para procesamiento iterativo
* List comprehensions (estilo pythonic)
* Funciones: definición, parámetros, retorno
* Lambda functions

**Casos de uso empresariales:**
* Calcular comisiones por vendedor según reglas de negocio
* Aplicar descuentos escalonados
* Filtrar transacciones por múltiples criterios
* Crear funciones reutilizables para cálculos financieros

**Resultado esperado:** Capacidad de escribir lógica de negocio en Python

---

### [01_04_Entorno_Interactivo_Jupyter](./01_04_Entorno_Interactivo_Jupyter)
**Duración:** 30 minutos | **Dificultad:** Principiante

**Temas cubiertos:**
* Anatomía de un notebook: celdas de código, markdown, comandos mágicos
* Comandos `%md`, `%sql`, `%sh`, `%fs`
* Atajos de teclado para productividad
* Visualizaciones inline
* Debugging básico en notebooks
* Exportar notebooks

**Productividad:**
* Shortcuts esenciales (Shift+Enter, Ctrl+Enter, etc.)
* Organización de notebooks por proyecto
* Documentación con markdown

**Resultado esperado:** Dominio del entorno de notebooks de Databricks

---

## 🏁 Pre-requisitos

**Conocimientos:**
* Ninguno! Este es el punto de partida del libro
* No se requiere experiencia en programación
* Útil: familiaridad básica con conceptos de negocio (ventas, costos, margen)

**Herramientas:**
* Navegador web moderno (Chrome, Firefox, Edge)
* Cuenta de email para registro
* Cuenta de GitHub (gratuita) - [Crear aquí](https://github.com/signup)

**Tiempo estimado total:** 2.5 horas

---

## 🎓 Objetivos de Aprendizaje Detallados

Al completar este módulo, serás capaz de:

### Nivel 1: Conocimiento (Recordar)
* [ ] Listar los componentes de Databricks (workspace, cluster, notebook)
* [ ] Identificar los lenguajes soportados en serverless (Python, SQL, sh)
* [ ] Nombrar los tipos de datos básicos en Python

### Nivel 2: Comprensión (Entender)
* [ ] Explicar la diferencia entre DBFS y Unity Catalog
* [ ] Describir cómo funciona Git integration en Databricks
* [ ] Interpretar mensajes de error comunes en Python

### Nivel 3: Aplicación (Hacer)
* [ ] Configurar tu propio workspace de Databricks
* [ ] Conectar un repositorio de GitHub
* [ ] Escribir funciones Python para cálculos financieros
* [ ] Crear notebooks documentados con markdown

### Nivel 4: Análisis (Analizar)
* [ ] Comparar ejecución local vs serverless compute
* [ ] Evaluar cuándo usar listas vs diccionarios
* [ ] Decidir entre Databricks Free vs Standard Edition

---

## 💻 Ejercicios Prácticos

### Ejercicio 1: Configuración Completa
**Objetivo:** Verificar que tu entorno está 100% funcional

1. Crear workspace en Databricks Community
2. Conectar tu repositorio de GitHub
3. Clonar el repositorio "pandito"
4. Ejecutar el notebook `01_01_Configuracion_Databricks_y_Git`
5. Verificar que puedes ejecutar código Python, SQL y comandos shell

**Criterio de éxito:** Todos los notebooks del módulo 01 ejecutan sin errores

---

### Ejercicio 2: Función de Descuentos Escalonados
**Objetivo:** Aplicar estructuras de control en contexto de negocio

```python
# Implementa esta función:
def calcular_descuento(monto_compra):
    """
    Calcula descuento según reglas:
    - 0-100: 0%
    - 100-500: 5%
    - 500-1000: 10%
    - 1000+: 15%
    """
    # TU CÓDIGO AQUÍ
    pass

# Casos de prueba
assert calcular_descuento(50) == 0
assert calcular_descuento(200) == 10  # 5% de 200
assert calcular_descuento(750) == 75  # 10% de 750
assert calcular_descuento(1500) == 225  # 15% de 1500
```

**Pista:** Usa `if/elif/else` y retorna `monto_compra * porcentaje`

---

### Ejercicio 3: Procesar Lista de Transacciones
**Objetivo:** Dominar bucles y list comprehensions

```python
transacciones = [
    {'producto': 'Laptop', 'precio': 899, 'cantidad': 2},
    {'producto': 'Mouse', 'precio': 25, 'cantidad': 5},
    {'producto': 'Teclado', 'precio': 79, 'cantidad': 3},
]

# Tarea 1: Calcular revenue total usando bucle
total_revenue = 0
for txn in transacciones:
    total_revenue += txn['precio'] * txn['cantidad']

# Tarea 2: Mismo cálculo con list comprehension + sum()
total_revenue_v2 = sum([txn['precio'] * txn['cantidad'] for txn in transacciones])

# Tarea 3: Filtrar productos con precio > 50
productos_premium = [txn for txn in transacciones if txn['precio'] > 50]
```

---

## 🧪 Experimenta con Genie Code

Usa Genie para acelerar tu aprendizaje:

### Prompt 1: Exploración del Entorno
```
"Muéstrame los comandos esenciales de Databricks notebooks:
- Listar archivos en DBFS
- Ver mi directorio actual
- Cambiar permisos de archivos
- Instalar una librería Python adicional"
```

### Prompt 2: Debugging
```
"Tengo este error: NameError: name 'pd' is not defined
¿Qué significa y cómo lo soluciono?"
```

### Prompt 3: Generación de Función
```
"Crea una función que calcule el CAGR (Compound Annual Growth Rate)
entre un valor inicial y final, dado un número de años.
Incluye docstring y casos de prueba."
```

---

## 🔧 Solución de Problemas Comunes

### Problema 1: "Cluster not found"
**Causa:** Estás intentando seleccionar un cluster inexistente en Free Edition  
**Solución:** Usa serverless compute (se selecciona automáticamente al ejecutar celda)

### Problema 2: "Git authentication failed"
**Causa:** Token de GitHub expirado o mal configurado  
**Solución:**
1. Ve a GitHub Settings → Developer Settings → Personal Access Tokens
2. Genera nuevo token con permisos `repo`
3. Vuelve a configurar en Databricks User Settings → Git Integration

### Problema 3: "NameError: name 'X' is not defined"
**Causa:** Variable no definida o celda no ejecutada en orden  
**Solución:** Ejecuta todas las celdas desde el inicio (Run All)

### Problema 4: "SyntaxError: invalid syntax"
**Causa:** Error de tipeo en código Python  
**Solución:** Revisa:
- Dos puntos `:` al final de if/for/def
- Indentación correcta (4 espacios)
- Comillas pareadas `"texto"`
- Paréntesis balanceados `()`

---

## 📖 Recursos Adicionales

### Documentación Oficial
* [Databricks Community Edition](https://community.cloud.databricks.com/)
* [Databricks Notebooks Guide](https://docs.databricks.com/notebooks/index.html)
* [Python Tutorial (official)](https://docs.python.org/3/tutorial/)
* [GitHub Getting Started](https://docs.github.com/en/get-started)

### Videos Recomendados
* [Databricks for Beginners (YouTube)](https://www.youtube.com/watch?v=example)
* [Python Crash Course](https://www.youtube.com/watch?v=rfscVS0vtbw)

### Cheatsheets
* [Python Basics Cheatsheet](https://www.pythoncheatsheet.org/)
* [Databricks Keyboard Shortcuts](https://docs.databricks.com/notebooks/notebooks-use.html#keyboard-shortcuts)

---

## ✅ Checklist de Completitud

Marca cada item al terminarlo:

**Configuración:**
- [ ] Cuenta de Databricks Community creada
- [ ] Repositorio GitHub conectado
- [ ] Todos los notebooks del módulo ejecutados sin errores

**Conceptos:**
- [ ] Entiendo la diferencia entre workspace y home directory
- [ ] Puedo explicar qué es serverless compute
- [ ] Sé usar comandos mágicos (%md, %sql, %sh)

**Habilidades:**
- [ ] Puedo escribir funciones Python con parámetros y retorno
- [ ] Domino if/elif/else para lógica de negocio
- [ ] Uso list comprehensions correctamente
- [ ] Sé documentar notebooks con markdown

**Ejercicios:**
- [ ] Completé Ejercicio 1 (Configuración)
- [ ] Completé Ejercicio 2 (Descuentos)
- [ ] Completé Ejercicio 3 (Transacciones)

---

## 🎯 Evaluación de Conocimientos

**Pregunta 1:** ¿Qué lenguajes NO están soportados en serverless compute?  
A) Python  
B) SQL  
C) R  
D) sh

<details>
<summary>Ver respuesta</summary>
C) R (también Scala no está soportado)
</details>

**Pregunta 2:** ¿Cuál es la mejor estructura para almacenar datos de producto con precio?  
A) Lista: `['Laptop', 899]`  
B) Diccionario: `{'producto': 'Laptop', 'precio': 899}`  
C) Tupla: `('Laptop', 899)`  
D) Set: `{'Laptop', 899}`

<details>
<summary>Ver respuesta</summary>
B) Diccionario - permite acceso por clave semántica (ej: producto['precio'])
</details>

**Pregunta 3:** ¿Qué hace este código?  
```python
[x * 2 for x in range(5) if x % 2 == 0]
```

<details>
<summary>Ver respuesta</summary>
[0, 4, 8] - Duplica los números pares de 0 a 4
</details>

---

## 🚀 Próximo Módulo

Ahora que dominas el entorno y Python básico, es momento de aprender **computación numérica eficiente**:

**➡️ [Módulo 02: NumPy y Vectorización Financiera](../02_NumPy_Vectorizacion_Financiera/)**

Aprende a procesar arrays de datos 100x más rápido con NumPy.

---

<div align="center">

### 🎓 ¡Felicitaciones por Completar el Módulo 01!

**"El viaje de mil líneas de código comienza con un notebook."**

[📖 Volver al Índice Principal](../README.md)

</div>