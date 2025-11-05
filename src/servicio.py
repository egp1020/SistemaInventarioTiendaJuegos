from typing import Any, Dict

from . import repositorio

from .modelos import Videojuego
from .servicio_imagenes import servicio_imagenes

servicio_img = servicio_imagenes()


def agregar_videojuego(nombre, precio, cantidad, compania, portada, fecha_publicacion):
    """Agrega un nuevo videojuego al inventario
    antes de que se agregue se verifica"""
    try:
        # se agrega la imagen primero
        if not portada:
            return {"ok": False, "error": "La portada es obligatoria"}
        ruta_portada = servicio_img.guardar_imagen(portada, portada.name)
        # luego se crea el juego
        juego = Videojuego(
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
            compania=compania,
            portada=ruta_portada,
            fecha_publicacion=fecha_publicacion,
        )
    except ValueError as e:
        return {
            "ok": False,
            "error": str(e),  # mensaje de error del modelo (ej: fecha inválida
        }
    repositorio.agregar_juego(juego.to_dict())
    return {
        "ok": True,
        "id": juego.id,
        "mensaje ": f"Videojuego '{juego.nombre}' agregado con éxito",
    }


def buscar_por_Id(id):
    """Busca un videojuego por su id"""
    try:
        if not repositorio.juegos_existen():
            return {"ok": False, "error": "No hay videojuegos registrados"}
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    if not id:
        return {"ok": False, "error": "El ID es obligatorio"}

    juego = repositorio.buscar_por_id(id)
    if juego:
        return {"ok": True, "resultado": juego}
    else:
        return {"ok": False, "error": f"No existe un videojuego con ID {id}"}


def buscar_por_nombre(nombre):
    """Busca un videojuego por su nombre exacto"""
    try:
        if not repositorio.juegos_existen():
            return {"ok": False, "error": "No hay videojuegos registrados"}
    except ValueError as e:
        return {"ok": False, "error": str(e)}

    if not nombre:
        return {"ok": False, "error": "El nombre es obligatorio"}

    juego = repositorio.buscar_por_nombre(nombre)
    if juego:
        return {"ok": True, "resultado": juego}
    else:
        return {
            "ok": False,
            "error": (f"No existe un videojuego con nombre '{nombre}'"),
        }


def listar_juegos(ordenar_por_nombre=False):
    try:
        juegos = repositorio.listar_juegos()
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    if not juegos:
        return {"ok": True, "resultado": []}
    if ordenar_por_nombre:
        juegos = sorted(juegos, key=lambda j: j["nombre"].lower())
    return {"ok": True, "resultado": juegos}


def eliminar_juego(id):
    """Elimina un videojuego por ID"""
    try:
        if not repositorio.juegos_existen():
            return {"ok": False, "error": "No hay videojuegos registrados"}
    except ValueError as e:
        return {"ok": False, "error": str(e)}

    if not id:
        return {"ok": False, "error": "El ID es obligatorio"}

    if repositorio.eliminar_juego_por_id(id):
        return {
            "ok": True,
            "mensaje": f"Videojuego con ID {id} eliminado correctamente",
        }
    else:
        return {"ok": False, "error": f"No existe un videojuego con ID {id}"}


def descargar_inventario_como_json() -> Dict[str, Any]:
    """
    Prepara los datos del inventario para descargar como archivo JSON
    """
    try:
        resultado = repositorio.descargar_inventario()
        return resultado
    except Exception as e:
        return {"ok": False, "error": f"Error al preparar descarga: {str(e)}"}


def descargar_inventario_como_archivo(ruta_destino: str) -> Dict[str, Any]:
    """
    Guarda una copia del inventario en la ruta especificada
    """
    try:
        resultado = repositorio.descargar_inventario(ruta_destino)
        return resultado
    except Exception as e:
        return {"ok": False, "error": f"Error al guardar archivo: {str(e)}"}


def cargar_inventario_desde_ruta(ruta_archivo: str) -> Dict[str, Any]:
    """
    Carga un inventario desde un archivo JSON en la ruta especificada
    """
    try:
        if not ruta_archivo:
            return {"ok": False, "error": "No se especificó archivo"}

        resultado = repositorio.cargar_inventario_desde_archivo(ruta_archivo)
        return resultado
    except Exception as e:
        return {"ok": False, "error": f"Error al cargar archivo: {str(e)}"}


def cargar_inventario_desde_json(datos_json: str) -> Dict[str, Any]:
    """
    Carga un inventario desde un string JSON
    Útil cuando el frontend envía el archivo como texto
    """
    try:
        if not datos_json:
            return {"ok": False, "error": "No se proporcionaron datos JSON"}

        resultado = repositorio.cargar_inventario_desde_datos(datos_json)
        return resultado
    except Exception as e:
        return {"ok": False, "error": f"Error al procesar JSON: {str(e)}"}


def obtener_estado_inventario() -> Dict[str, Any]:
    """
    Obtiene información del estado actual del inventario
    """
    try:
        juegos = repositorio.listar_juegos()
        stats = repositorio.obtener_estadisticas_tabla_hash()

        return {
            "ok": True,
            "total_juegos": len(juegos),
            "estadisticas_hash": stats,
            "ruta_archivo": str(repositorio.ruta_archivo),
            "ultima_actualizacion": (
                repositorio.obtener_ultima_modificacion()
                if hasattr(repositorio, "obtener_ultima_modificacion")
                else "N/A"
            ),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def descargar_tabla_indices_como_json() -> Dict[str, Any]:
    """
    Prepara los datos de la tabla de índices para descargar como archivo JSON
    """
    try:
        resultado = repositorio.descargar_tabla_indices()
        return resultado
    except Exception as e:
        return {
            "ok": False,
            "error": f"Error al preparar descarga de índices: {str(e)}",
        }


def obtener_estadisticas_indice() -> Dict[str, Any]:
    """Obtiene estadísticas del índice hash"""
    try:
        stats = repositorio.obtener_estadisticas_tabla_hash()
        return {"ok": True, "estadisticas": stats}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def obtener_tabla_hash_visual() -> Dict[str, Any]:
    """Obtiene la tabla hash en formato visual (posiciones e IDs)"""
    try:
        tabla_visual = repositorio.obtener_tabla_hash_visual()
        return {
            "ok": True,
            "tabla_hash": tabla_visual,
            "mensaje": "Tabla hash obtenida (posiciones y IDs)",
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
