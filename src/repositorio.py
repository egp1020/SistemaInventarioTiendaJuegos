import json
import os


ruta_archivo= "inventario.json"
 
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
    
def buscar_por_id(id):
    inventario = obtener_inventario()
    for juego in inventario:
        if juego["id"] == id:
            return juego
    return None

def id_existe(id):
    inventario = obtener_inventario()
    return any(juego["id"] == id for juego in inventario)
    
