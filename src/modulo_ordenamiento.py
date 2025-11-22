"""
Módulo de Ordenamiento para Videojuegos
Permite clasificar listas de videojuegos por diferentes criterios.
"""

from typing import Any, Dict, List


def ordenar_juegos(
    juegos: List[Dict[str, Any]], criterio: str = "nombre", orden: str = "ascendente"
) -> Dict[str, Any]:
    """
    Ordena una lista de videojuegos según el criterio especificado.

    Args:
        juegos: Lista de diccionarios con información de videojuegos
        criterio: Campo por el cual ordenar. Opciones:
            - 'nombre': Orden alfabético por nombre
            - 'precio': Orden numérico por precio
            - 'fecha': Orden cronológico por fecha de publicación
            - 'compania': Orden alfabético por compañía
            - 'cantidad': Orden numérico por cantidad/stock
        orden: Dirección del ordenamiento:
            - 'ascendente': De menor a mayor (A-Z, 0-9, fechas antiguas primero)
            - 'descendente': De mayor a menor (Z-A, 9-0, fechas recientes primero)

    Returns:
        Diccionario con:
            - ok (bool): True si se ordenó correctamente, False si hubo error
            - resultado (List): Lista de juegos ordenados
            - error (str): Mensaje de error si aplica
            - criterio_aplicado (str): Criterio usado para ordenar
            - orden_aplicado (str): Orden usado
    """
    try:
        # Validar entrada
        if not juegos:
            return {
                "ok": True,
                "resultado": [],
                "criterio_aplicado": criterio,
                "orden_aplicado": orden,
                "mensaje": "No hay juegos para ordenar",
            }

        # Validar criterio
        criterios_validos = ["nombre", "precio", "fecha", "compania", "cantidad"]
        if criterio not in criterios_validos:
            return {
                "ok": False,
                "error": f"Criterio no válido. Opciones: {', '.join(criterios_validos)}",
                "resultado": juegos,
            }

        # Validar orden
        ordenes_validos = ["ascendente", "descendente"]
        if orden not in ordenes_validos:
            return {
                "ok": False,
                "error": f"Orden no válido. Opciones: {', '.join(ordenes_validos)}",
                "resultado": juegos,
            }

        # Determinar si es orden inverso
        reverso = orden == "descendente"

        # Realizar ordenamiento según el criterio
        try:
            if criterio == "nombre":
                juegos_ordenados = sorted(
                    juegos, key=lambda j: j.get("nombre", "").lower(), reverse=reverso
                )

            elif criterio == "precio":
                juegos_ordenados = sorted(
                    juegos, key=lambda j: float(j.get("precio", 0)), reverse=reverso
                )

            elif criterio == "fecha":
                # Las fechas están en formato YYYY-MM-DD, se ordenan alfabéticamente
                juegos_ordenados = sorted(
                    juegos,
                    key=lambda j: j.get("fecha_publicacion", ""),
                    reverse=reverso,
                )

            elif criterio == "compania":
                juegos_ordenados = sorted(
                    juegos, key=lambda j: j.get("compania", "").lower(), reverse=reverso
                )

            elif criterio == "cantidad":
                juegos_ordenados = sorted(
                    juegos, key=lambda j: int(j.get("cantidad", 0)), reverse=reverso
                )

            else:
                # No debería llegar aquí por la validación previa
                return {
                    "ok": False,
                    "error": f"Criterio '{criterio}' no implementado",
                    "resultado": juegos,
                }

            return {
                "ok": True,
                "resultado": juegos_ordenados,
                "criterio_aplicado": criterio,
                "orden_aplicado": orden,
                "mensaje": f"Ordenado por {criterio} ({orden})",
                "total": len(juegos_ordenados),
            }

        except (ValueError, KeyError, TypeError) as e:
            return {
                "ok": False,
                "error": f"Error al ordenar por {criterio}: {str(e)}",
                "resultado": juegos,
            }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Error inesperado al ordenar: {str(e)}",
            "resultado": juegos if juegos else [],
        }


def obtener_criterios_disponibles() -> List[Dict[str, str]]:
    """
    Obtiene la lista de criterios de ordenamiento disponibles.

    Returns:
        Lista de diccionarios con 'valor' y 'etiqueta' para cada criterio
    """
    return [
        {"valor": "nombre", "etiqueta": "Nombre (A-Z)"},
        {"valor": "precio", "etiqueta": "Precio ($)"},
        {"valor": "fecha", "etiqueta": "Fecha de Publicación"},
        {"valor": "compania", "etiqueta": "Compañía"},
        {"valor": "cantidad", "etiqueta": "Stock/Cantidad"},
    ]


def obtener_ordenes_disponibles() -> List[Dict[str, str]]:
    """
    Obtiene las opciones de orden disponibles.

    Returns:
        Lista de diccionarios con 'valor' y 'etiqueta' para cada orden
    """
    return [
        {"valor": "ascendente", "etiqueta": "Ascendente ↑"},
        {"valor": "descendente", "etiqueta": "Descendente ↓"},
    ]
