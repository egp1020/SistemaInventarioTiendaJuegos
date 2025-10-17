import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from tabla_hash import TablaHash

BASE_DIR = Path(__file__).parent.parent.parent
ruta_archivo = BASE_DIR / "inventario.json"
tabla_hash = TablaHash(tamano=100)


def inicializar_inventario():
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    else:
        print("ya existe")


def obtener_inventario():
    inicializar_inventario()
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_inventario(inventario):
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


def agregar_juego(juego):
    inventario = obtener_inventario()
    inventario.append(juego)
    guardar_inventario(inventario)
    # Agregar a la tabla hash para búsquedas rápidas
    tabla_hash.agregar(juego["id"], juego)


def buscar_por_id(id):
    # Usar la tabla hash para búsqueda O(1) en promedio
    return tabla_hash.buscar(id)


def eliminar_juego_por_id(id):
    """Elimina un juego por ID tanto del inventario como de la tabla hash"""
    inventario = obtener_inventario()

    # Eliminar del inventario principal
    nuevo_inventario = [juego for juego in inventario if juego["id"] != id]

    if len(nuevo_inventario) == len(inventario):
        return False  # No se encontró el juego

    guardar_inventario(nuevo_inventario)

    # Eliminar de la tabla hash
    return tabla_hash.eliminar(id)


def listar_juegos():
    if not os.path.exists(ruta_archivo):
        return []
    try:
        data = obtener_inventario()
        if not isinstance(data, list):
            raise ValueError(
                "El archivo JSON no tiene el formato correcto "
                "(se esperaba una lista)."
            )
        return data
    except json.JSONDecodeError:
        raise ValueError("El archivo JSON está dañado o mal formado.")


# el nombre debera ser unico
def buscar_por_nombre(nombre):
    inventario = obtener_inventario()
    nombre_norm = nombre.strip().lower()
    for j in inventario:
        if nombre_norm in j["nombre"].strip().lower():
            return j
    return None


def juegos_existen():
    if not os.path.exists(ruta_archivo):
        return False
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        try:
            inventario = json.load(f)
            return len(inventario) > 0
        except json.JSONDecodeError:
            raise ValueError("el archivo JSON esta dañado o mal formado")


def id_existe(id):
    return tabla_hash.buscar(id) is not None


def obtener_estadisticas_tabla_hash():
    """Obtiene estadísticas de la tabla hash"""
    return tabla_hash.estadisticas()


def descargar_inventario(ruta_destino: str = None) -> Dict[str, Any]:
    """
    Crea una copia del archivo inventario.json en la ruta especificada
    o devuelve los datos para descargar
    """
    try:
        if not os.path.exists(ruta_archivo):
            return {"ok": False, "error": "No existe el archivo de inventario"}

        if ruta_destino:
            # Copiar el archivo a la ruta destino
            shutil.copy2(ruta_archivo, ruta_destino)
            return {
                "ok": True,
                "mensaje": f"Inventario descargado en {ruta_destino}",
                "ruta": ruta_destino,
            }
        else:
            # Devolver los datos para descargar
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"inventario_backup_{timestamp}.json"

            return {
                "ok": True,
                "datos": datos,
                "nombre_archivo": nombre_archivo,
                "timestamp": timestamp,
            }

    except Exception as e:
        return {"ok": False, "error": f"Error al descargar inventario: {str(e)}"}


def cargar_inventario_desde_archivo(ruta_archivo_cargado: str) -> Dict[str, Any]:
    """
    Carga un archivo JSON y reemplaza el inventario actual
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ruta_archivo_cargado):
            return {"ok": False, "error": "El archivo no existe"}

        # Leer y validar el archivo cargado
        with open(ruta_archivo_cargado, "r", encoding="utf-8") as f:
            datos_cargados = json.load(f)

        # Validar formato básico
        if not isinstance(datos_cargados, list):
            return {
                "ok": False,
                "error": "Formato inválido: se esperaba una lista de juegos",
            }

        # Validar estructura de cada juego
        for i, juego in enumerate(datos_cargados):
            if not isinstance(juego, dict):
                return {"ok": False, "error": f"Elemento {i} no es un objeto válido"}

            campos_requeridos = [
                "id",
                "nombre",
                "precio",
                "cantidad",
                "compania",
                "portada",
                "fecha_publicacion",
            ]
            for campo in campos_requeridos:
                if campo not in juego:
                    return {"ok": False, "error": f"Juego {i} falta el campo: {campo}"}

        # Hacer backup del archivo actual antes de reemplazar
        if os.path.exists(ruta_archivo):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BASE_DIR / f"inventario_backup_{timestamp}.json"
            shutil.copy2(ruta_archivo, backup_path)

        # Reemplazar el inventario actual
        guardar_inventario(datos_cargados)

        # Reconstruir la tabla hash con los nuevos datos
        global tabla_hash
        tabla_hash = TablaHash(tamano=100)  # Reiniciar tabla

        for juego in datos_cargados:
            tabla_hash.agregar(juego["id"], juego)

        return {
            "ok": True,
            "mensaje": (
                "Inventario cargado exitosamente. "
                f"{len(datos_cargados)} juegos importados."
            ),
            "total_juegos": len(datos_cargados),
        }

    except json.JSONDecodeError:
        return {"ok": False, "error": "El archivo no es un JSON válido"}
    except Exception as e:
        return {"ok": False, "error": f"Error al cargar el inventario: {str(e)}"}


def cargar_inventario_desde_datos(datos_json: str) -> Dict[str, Any]:
    """
    Carga inventario desde datos JSON string (para cuando se sube el archivo)
    """
    try:
        # Parsear el JSON string
        datos_cargados = json.loads(datos_json)

        # Validaciones (igual que la función anterior)
        if not isinstance(datos_cargados, list):
            return {
                "ok": False,
                "error": "Formato inválido: se esperaba una lista de juegos",
            }

        for i, juego in enumerate(datos_cargados):
            if not isinstance(juego, dict):
                return {"ok": False, "error": f"Elemento {i} no es un objeto válido"}

            campos_requeridos = [
                "id",
                "nombre",
                "precio",
                "cantidad",
                "compania",
                "portada",
                "fecha_publicacion",
            ]
            for campo in campos_requeridos:
                if campo not in juego:
                    return {"ok": False, "error": f"Juego {i} falta el campo: {campo}"}

        # Backup del archivo actual
        if os.path.exists(ruta_archivo):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BASE_DIR / f"inventario_backup_{timestamp}.json"
            shutil.copy2(ruta_archivo, backup_path)

        # Reemplazar inventario
        guardar_inventario(datos_cargados)

        # Reconstruir tabla hash
        global tabla_hash
        tabla_hash = TablaHash(tamano=100)

        for juego in datos_cargados:
            tabla_hash.agregar(juego["id"], juego)

        return {
            "ok": True,
            "mensaje": (
                "Inventario cargado exitosamente. "
                f"{len(datos_cargados)} juegos importados."
            ),
            "total_juegos": len(datos_cargados),
        }

    except json.JSONDecodeError:
        return {"ok": False, "error": "El JSON no es válido"}
    except Exception as e:
        return {"ok": False, "error": f"Error al cargar el inventario: {str(e)}"}
