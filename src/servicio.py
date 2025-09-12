from src import repositorio
from src.modelos import Videojuego

def agregar_Videojuego(nombre, precio, cantidad, compania, portada, fecha_publicacion):
    """Agrega un nuevo videojuego al inventario
    antes de que se agregue se verifica"""
    try:
        juego = Videojuego(
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
            compania=compania,
            portada=portada,
            fecha_publicacion=fecha_publicacion
        ) 
    except ValueError as e:
        return {
            "ok": False,
            "error": str(e)  # mensaje de error del modelo (ej: fecha inválida
        }
    repositorio.agregar_al_inventario(juego.to_dict())
    return {
        "ok": True,
        "id": juego.id,
        "mensaje ": f"Videojuego '{juego.nombre}' agregado con éxito"
    }
