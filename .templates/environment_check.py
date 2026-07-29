# ========================================
# 🔍 VERIFICACIÓN DE ENTORNO SERVERLESS
# ========================================
# Copia este código en la primera celda de cada notebook principal

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
    spark_master = spark.conf.get('spark.master', 'unknown')
    if 'serverless' in spark_master.lower() or 'local' in spark_master.lower():
        print(f"✅ Modo: Serverless Compute")
    else:
        print(f"ℹ️  Modo: {spark_master}")
except NameError:
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

all_ok = True
for lib, min_version in required_libs.items():
    try:
        module = __import__(lib)
        version = getattr(module, '__version__', 'N/A')
        status = "✅ OK"
        print(f"{lib:<20} {version:<15} {min_version:<15} {status:<10}")
    except ImportError:
        print(f"{lib:<20} {'NO INSTALADA':<15} {min_version:<15} {'❌ FALTA':<10}")
        all_ok = False

print("=" * 70)
if all_ok:
    print("✅ Entorno verificado - Listo para ejecutar notebooks")
else:
    print("⚠️  Faltan librerías - Instalar con: %pip install <librería>")
print("=" * 70)
