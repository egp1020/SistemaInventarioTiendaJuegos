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
    id_norm=id.strip().lower()
    for juego in inventario:
        if juego["id"].lower() == id_norm:
            return juego
    return None

def listar_juegos():
    if not os.path.exists(ruta_archivo):
        return []
    try:
        data = obtener_inventario()
        if not isinstance(data,list):
            raise ValueError("El archivo JSON no tiene el formato correcto (se esperaba una lista).")
        return data
    except json.JSONDecodeError:
        raise ValueError("El archivo JSON está dañado o mal formado.")

#el nombre debera ser unico
def buscar_por_nombre(nombre):
    inventario = obtener_inventario()
    nombre_norm=nombre.strip().lower()
    for j in inventario: 
        if nombre_norm in j["nombre"].strip().lower():
            return j
    return None


def juegos_existen():
    if not os.path.exists(ruta_archivo):
        return False
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        try:
            inventario=json.load(f)
            return len(inventario)>0
        except json.JSONDecodeError:
            raise ValueError("el archivo JSON esta dañado o mal formado")
    
def id_existe(id):
    inventario = obtener_inventario()
    return any(juego["id"] == id for juego in inventario)

