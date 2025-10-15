# [file name]: test_videojuegos.py
import sys
import os

# Añadir el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos import Videojuego
import servicio
from repositorio import obtener_inventario, guardar_inventario
import json
from datetime import datetime

def test_videojuegos():
    """Función principal de pruebas para validaciones de Videojuego"""
    
    print("=" * 60)
    print("INICIANDO PRUEBAS DE VALIDACIÓN DE VIDEOJUEGOS")
    print("=" * 60)
    
    # Guardar el inventario original para restaurarlo después
    inventario_original = obtener_inventario()
    
    # Lista para almacenar resultados de pruebas
    resultados = []
    
    # Caso 1: Falta nombre
    print("\n1. Probando falta de NOMBRE...")
    try:
        juego = Videojuego(
            nombre="",  # Campo vacío
            precio=59.99,
            cantidad=10,
            compania="Nintendo",
            portada="imagenes/portadas/mario.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Falta nombre", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta nombre", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta nombre", f"✗ {e}", "ERROR"))
    
    # Caso 2: Falta precio
    print("\n2. Probando falta de PRECIO...")
    try:
        juego = Videojuego(
            nombre="The Legend of Zelda",
            precio=0,  # Precio vacío
            cantidad=10,
            compania="Nintendo",
            portada="imagenes/portadas/zelda.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Falta precio", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta precio", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta precio", f"✗ {e}", "ERROR"))
    
    # Caso 3: Precio negativo
    print("\n3. Probando precio NEGATIVO...")
    try:
        juego = Videojuego(
            nombre="Super Mario",
            precio=-10.0,  # Precio negativo
            cantidad=10,
            compania="Nintendo",
            portada="imagenes/portadas/mario.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Precio negativo", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Precio negativo", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Precio negativo", f"✗ {e}", "ERROR"))
    
    # Caso 4: Falta cantidad
    print("\n4. Probando falta de CANTIDAD...")
    try:
        juego = Videojuego(
            nombre="Metroid Prime",
            precio=49.99,
            cantidad=0,  # Cantidad vacía
            compania="Nintendo",
            portada="imagenes/portadas/metroid.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Falta cantidad", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta cantidad", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta cantidad", f"✗ {e}", "ERROR"))
    
    # Caso 5: Cantidad negativa
    print("\n5. Probando cantidad NEGATIVA...")
    try:
        juego = Videojuego(
            nombre="Donkey Kong",
            precio=39.99,
            cantidad=-5,  # Cantidad negativa
            compania="Nintendo",
            portada="imagenes/portadas/dk.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Cantidad negativa", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Cantidad negativa", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Cantidad negativa", f"✗ {e}", "ERROR"))
    
    # Caso 6: Cantidad decimal (no permitido)
    print("\n6. Probando cantidad DECIMAL...")
    try:
        juego = Videojuego(
            nombre="Kirby",
            precio=29.99,
            cantidad=10.5,  # Cantidad decimal
            compania="Nintendo",
            portada="imagenes/portadas/kirby.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Cantidad decimal", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Cantidad decimal", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Cantidad decimal", f"✗ {e}", "ERROR"))
    
    # Caso 7: Falta compañía
    print("\n7. Probando falta de COMPAÑÍA...")
    try:
        juego = Videojuego(
            nombre="Pokémon",
            precio=59.99,
            cantidad=15,
            compania="",  # Compañía vacía
            portada="imagenes/portadas/pokemon.jpg",
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Falta compañía", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta compañía", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta compañía", f"✗ {e}", "ERROR"))
    
    # Caso 8: Falta portada
    print("\n8. Probando falta de PORTADA...")
    try:
        juego = Videojuego(
            nombre="Animal Crossing",
            precio=54.99,
            cantidad=20,
            compania="Nintendo",
            portada="",  # Portada vacía
            fecha_publicacion="2023-05-15"
        )
        resultados.append(("Falta portada", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta portada", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta portada", f"✗ {e}", "ERROR"))
    
    # Caso 9: Falta fecha
    print("\n9. Probando falta de FECHA...")
    try:
        juego = Videojuego(
            nombre="Splatoon",
            precio=49.99,
            cantidad=8,
            compania="Nintendo",
            portada="imagenes/portadas/splatoon.jpg",
            fecha_publicacion=""  # Fecha vacía
        )
        resultados.append(("Falta fecha", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Falta fecha", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Falta fecha", f"✗ {e}", "ERROR"))
    
    # Caso 10: Formato de fecha incorrecto
    print("\n10. Probando formato de FECHA incorrecto...")
    try:
        juego = Videojuego(
            nombre="Mario Kart",
            precio=59.99,
            cantidad=12,
            compania="Nintendo",
            portada="imagenes/portadas/mariokart.jpg",
            fecha_publicacion="15-05-2023"  # Formato incorrecto
        )
        resultados.append(("Formato fecha incorrecto", "FALLÓ - No detectó error", "ERROR"))
    except ValueError as e:
        print(f"   ✓ Correctamente detectado: {e}")
        resultados.append(("Formato fecha incorrecto", f"✓ {e}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Formato fecha incorrecto", f"✗ {e}", "ERROR"))
    
    # Caso 11: TODOS los parámetros correctos
    print("\n11. Probando TODOS los parámetros CORRECTOS...")
    try:
        juego = Videojuego(
            nombre="The Legend of Zelda: Breath of the Wild",
            precio=69.99,
            cantidad=25,
            compania="Nintendo",
            portada="imagenes/portadas/zelda_botw.jpg",
            fecha_publicacion="2023-03-03"  # Formato correcto YYYY-MM-DD
        )
        print(f"   ✓ Juego creado exitosamente: {juego.nombre}")
        print(f"     ID generado: {juego.id}")
        resultados.append(("Todos parámetros correctos", f"✓ Juego creado: {juego.nombre}", "ÉXITO"))
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        resultados.append(("Todos parámetros correctos", f"✗ {e}", "ERROR"))
    
    # Mostrar resumen de resultados
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitos = 0
    fallos = 0
    
    for prueba, resultado, estado in resultados:
        if estado == "ÉXITO":
            exitos += 1
            print(f"✓ {prueba}: {resultado}")
        else:
            fallos += 1
            print(f"✗ {prueba}: {resultado}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {exitos} pruebas exitosas, {fallos} pruebas fallidas")
    
    if fallos == 0:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f"⚠️  {fallos} pruebas fallaron - revisar las validaciones")
    
    print("=" * 60)
    
    # Restaurar el inventario original
    guardar_inventario(inventario_original)
    print("\nInventario restaurado al estado original")

if __name__ == "__main__":
    test_videojuegos()