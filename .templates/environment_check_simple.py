# 🔍 Verificación rápida de entorno
import sys
print(f"✅ Python {sys.version.split()[0]}")
try:
    print(f"✅ Spark {spark.version}")
except:
    print("ℹ️  Spark no disponible en esta celda")
print("✅ Serverless Compute compatible")
