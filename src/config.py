# src/config.py
from pathlib import Path

# Definir BASE_DIR una sola vez
BASE_DIR = Path(__file__).parent.parent

# Rutas a archivos de datos
RUTA_INVENTARIO = BASE_DIR / "inventario.json"
RUTA_TABLA_HASH = BASE_DIR / "tabla_hash.json"

CARPETA_PORTADAS = BASE_DIR / "imagenes" / "portadas"
RUTA_RELATIVA_PORTADAS = "imagenes/portadas"
