from src import repositorio
from src.modelos import Videojuego
from src.servicio_imagenes import servicio_imagenes

servicio_img=servicio_imagenes()

def agregar_videojuego(nombre, precio, cantidad, compania, portada, fecha_publicacion):
    """Agrega un nuevo videojuego al inventario
    antes de que se agregue se verifica"""
    try:
        #se agrega la imagen primero
        if not portada:
            return {
                "ok": False,
                "error": "La portada es obligatoria"
            }
        ruta_portada = servicio_img.guardar_imagen(portada, portada.name)        
        #luego se crea el juego
        juego = Videojuego(
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
            compania=compania,
            portada=ruta_portada,
            fecha_publicacion=fecha_publicacion
        ) 
    except ValueError as e:
        return {
            "ok": False,
            "error": str(e)  # mensaje de error del modelo (ej: fecha inválida
        }
    repositorio.agregar_juego(juego.to_dict())
    return {
        "ok": True,
        "id": juego.id,
        "mensaje ": f"Videojuego '{juego.nombre}' agregado con éxito"
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
    
    juego=repositorio.buscar_por_id(id)
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
        return {"ok": False, "error": f"No existe un videojuego con nombre '{nombre}'"}
    
def listar_juegos(ordenar_por_nombre=False):
    try:
       juegos=repositorio.listar_juegos()
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    if not juegos:
        return {"ok": True, "resultado": []}
    if ordenar_por_nombre:
        juegos = sorted(juegos, key=lambda j: j["nombre"].lower())
    return {"ok": True, "resultado": juegos}



