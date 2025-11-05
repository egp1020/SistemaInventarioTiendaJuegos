import json
import os
import shutil
from datetime import datetime
from typing import Any, Dict

from .config import RUTA_INVENTARIO, BASE_DIR
from .tabla_hash import TablaHash

ruta_archivo = RUTA_INVENTARIO
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


# se modifico el codigo de agregar
def agregar_juego(juego):
    inventario = obtener_inventario()

    # Agregar al final de la lista
    posicion = len(inventario)  # Posición donde se insertará
    inventario.append(juego)
    guardar_inventario(inventario)

    # Agregar a la tabla hash con la posición
    tabla_hash.agregar(juego["id"], posicion)


# se modifico
def buscar_por_id(id):
    # Buscar posición en la tabla hash O(1)
    posicion = tabla_hash.buscar_posicion(id)

    if posicion is None:
        return None

    # Acceso directo al inventario O(1)
    inventario = obtener_inventario()

    if posicion < len(inventario) and inventario[posicion]["id"] == id:
        return inventario[posicion]

    # Si hay inconsistencia, buscar linealmente y reconstruir índice
    return buscar_lineal_y_reconstruir(id)


# se modifico
def eliminar_juego_por_id(id):
    """Elimina un juego usando la tabla hash como índice"""
    # Buscar posición usando tabla hash O(1)
    posicion = tabla_hash.buscar_posicion(id)

    if posicion is None:
        return False

    inventario = obtener_inventario()

    # Verificar consistencia
    if posicion >= len(inventario) or inventario[posicion]["id"] != id:
        return buscar_lineal_y_eliminar(id)

    # ELIMINACIÓN OPTIMIZADA con actualización de índices
    ultima_posicion = len(inventario) - 1

    if posicion != ultima_posicion:
        # Intercambiar con el último elemento
        inventario[posicion], inventario[ultima_posicion] = (
            inventario[ultima_posicion],
            inventario[posicion],
        )

        # Actualizar la posición del elemento movido en la tabla hash
        id_movido = inventario[posicion]["id"]
        tabla_hash.actualizar_posicion(id_movido, posicion)

    # Eliminar el último elemento
    inventario.pop()
    guardar_inventario(inventario)

    # Eliminar el ID de la tabla hash
    tabla_hash.eliminar(id)

    return True


# se crearon nuevas funciones para buscar linealmente en caso de que haya
# fallos
def buscar_lineal_y_reconstruir(id):
    """Búsqueda lineal y reconstrucción del índice en caso de inconsistencia"""
    inventario = obtener_inventario()

    for i, juego in enumerate(inventario):
        if juego["id"] == id:
            # Reconstruir la posición en la tabla hash
            tabla_hash.agregar(id, i)
            return juego

    return None


def buscar_lineal_y_eliminar(id):
    """Eliminación lineal y reconstrucción del índice"""
    inventario = obtener_inventario()

    for i in range(len(inventario)):
        if inventario[i]["id"] == id:
            # Eliminar y actualizar índices para elementos posteriores
            inventario.pop(i)
            guardar_inventario(inventario)

            # Reconstruir tabla hash completa
            reconstruir_tabla_hash_completa()
            return True

    return False


# en caso de que se dañe la tabla hash esta se reconstruye


def reconstruir_tabla_hash_completa():
    """Reconstruye toda la tabla hash desde el inventario"""
    global tabla_hash
    tabla_hash = TablaHash(tamano=100)

    inventario = obtener_inventario()
    for i, juego in enumerate(inventario):
        tabla_hash.agregar(juego["id"], i)


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


def descargar_tabla_indices(ruta_destino: str = None) -> Dict[str, Any]:
    """
    Crea una copia del archivo tabla_hash.json (índices)
    en la ruta especificada o devuelve los datos para descargar
    """
    try:
        archivo_indice = BASE_DIR / "tabla_hash.json"

        if not os.path.exists(archivo_indice):
            return {"ok": False, "error": "No existe el archivo de índices"}

        if ruta_destino:
            # Copiar el archivo a la ruta destino
            shutil.copy2(archivo_indice, ruta_destino)
            return {
                "ok": True,
                "mensaje": f"Tabla de índices descargada en {ruta_destino}",
                "ruta": ruta_destino,
            }
        else:
            # Devolver los datos para descargar
            with open(archivo_indice, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"tabla_indices_backup_{timestamp}.json"

            return {
                "ok": True,
                "datos": datos,
                "nombre_archivo": nombre_archivo,
                "timestamp": timestamp,
                "tipo": "indices",
            }

    except Exception as e:
        return {"ok": False, "error": f"Error al descargar tabla de índices: {str(e)}"}


# funcion para ver la tabla hash en consola
def obtener_tabla_hash_visual():
    """Obtiene la tabla hash en formato visual (solo posiciones e IDs)"""
    return tabla_hash.obtener_tabla_visual()
