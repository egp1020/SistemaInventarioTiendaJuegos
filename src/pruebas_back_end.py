# archivo: src/pruebas_tabla_hash_index.py
import os
import sys
from io import BytesIO

from .config import RUTA_INVENTARIO, RUTA_TABLA_HASH
from .repositorio import obtener_inventario, tabla_hash
from .servicio import (
    agregar_videojuego,
    buscar_por_Id,
    eliminar_juego,
    obtener_estadisticas_indice,
    obtener_tabla_hash_visual,
)


def crear_imagen_falsa(nombre_archivo="portada_test.jpg"):
    """Crea una imagen falsa en memoria para pruebas"""
    imagen_falsa = BytesIO()
    imagen_falsa.write(b"fake image data for testing purposes")
    imagen_falsa.name = nombre_archivo
    imagen_falsa.seek(0)
    return imagen_falsa


def limpiar_inventario():
    """Limpia el inventario y la tabla hash para pruebas limpias"""
    try:
        for ruta in [RUTA_INVENTARIO, RUTA_TABLA_HASH]:
            if ruta.exists():
                os.remove(ruta)
        print("✅ Inventario y tabla hash limpiados")
    except Exception as e:
        print(f"⚠️  Advertencia al limpiar: {e}")


def test_agregar_y_buscar():
    """Prueba agregar juegos y buscarlos por ID usando la tabla hash"""
    print("\n🧪 PRUEBA 1: AGREGAR Y BUSCAR CON TABLA HASH")
    print("=" * 50)

    # Datos de prueba
    juego_prueba = {
        "nombre": "The Legend of Zelda: Breath of the Wild",
        "precio": 59.99,
        "cantidad": 15,
        "compania": "Nintendo",
        "portada_nombre": "zelda_botw.jpg",
        "fecha_publicacion": "2017-03-03",
    }

    # Agregar juego
    portada = crear_imagen_falsa(juego_prueba["portada_nombre"])
    resultado_agregar = agregar_videojuego(
        nombre=juego_prueba["nombre"],
        precio=juego_prueba["precio"],
        cantidad=juego_prueba["cantidad"],
        compania=juego_prueba["compania"],
        portada=portada,
        fecha_publicacion=juego_prueba["fecha_publicacion"],
    )

    if not resultado_agregar["ok"]:
        print(f"❌ Error al agregar: {resultado_agregar['error']}")
        return False

    id_agregado = resultado_agregar["id"]
    print(f"✅ Juego agregado con ID: {id_agregado}")

    # Buscar por ID usando tabla hash
    resultado_buscar = buscar_por_Id(id_agregado)

    if not resultado_buscar["ok"]:
        print(f"❌ Error al buscar: {resultado_buscar['error']}")
        return False

    juego_encontrado = resultado_buscar["resultado"]

    # Verificar datos
    assert juego_encontrado["nombre"] == juego_prueba["nombre"]
    assert juego_encontrado["precio"] == juego_prueba["precio"]
    assert juego_encontrado["cantidad"] == juego_prueba["cantidad"]
    assert juego_encontrado["compania"] == juego_prueba["compania"]
    assert juego_encontrado["fecha_publicacion"] == (juego_prueba["fecha_publicacion"])

    print("✅ Búsqueda por ID exitosa - Datos correctos")
    return True


def test_busqueda_rapida_multiple():
    """Prueba la velocidad de búsqueda con múltiples juegos"""
    print("\n🧪 PRUEBA 2: BÚSQUEDA RÁPIDA MÚLTIPLE")
    print("=" * 50)

    juegos_prueba = [
        {
            "nombre": "Super Mario Odyssey",
            "precio": 49.99,
            "cantidad": 20,
            "compania": "Nintendo",
            "portada_nombre": "mario_odyssey.jpg",
            "fecha_publicacion": "2017-10-27",
        },
        {
            "nombre": "Metroid Dread",
            "precio": 54.99,
            "cantidad": 12,
            "compania": "Nintendo",
            "portada_nombre": "metroid_dread.jpg",
            "fecha_publicacion": "2021-10-08",
        },
    ]

    ids_agregados = []

    # Agregar múltiples juegos
    for juego_data in juegos_prueba:
        portada = crear_imagen_falsa(juego_data["portada_nombre"])
        resultado = agregar_videojuego(
            nombre=juego_data["nombre"],
            precio=juego_data["precio"],
            cantidad=juego_data["cantidad"],
            compania=juego_data["compania"],
            portada=portada,
            fecha_publicacion=juego_data["fecha_publicacion"],
        )

        if resultado["ok"]:
            ids_agregados.append(resultado["id"])
            print(f"✅ Agregado: {juego_data['nombre']}")
        else:
            print(f"❌ Error: {resultado['error']}")
            return False

    # Buscar todos los IDs rápidamente
    for id_juego in ids_agregados:
        resultado = buscar_por_Id(id_juego)
        if resultado["ok"]:
            print(f"✅ Encontrado: {resultado['resultado']['nombre']}")
        else:
            print(f"❌ No encontrado: {id_juego}")
            return False

    print("✅ Todas las búsquedas fueron exitosas")
    return True


def test_eliminacion_eficiente():
    """Prueba la eliminación eficiente usando la tabla hash"""
    print("\n🧪 PRUEBA 3: ELIMINACIÓN EFICIENTE")
    print("=" * 50)

    # Agregar juego para eliminar
    juego_data = {
        "nombre": "Juego para Eliminar",
        "precio": 29.99,
        "cantidad": 5,
        "compania": "Test Company",
        "portada_nombre": "eliminar_test.jpg",
        "fecha_publicacion": "2023-01-01",
    }

    portada = crear_imagen_falsa(juego_data["portada_nombre"])
    resultado_agregar = agregar_videojuego(
        nombre=juego_data["nombre"],
        precio=juego_data["precio"],
        cantidad=juego_data["cantidad"],
        compania=juego_data["compania"],
        portada=portada,
        fecha_publicacion=juego_data["fecha_publicacion"],
    )

    if not resultado_agregar["ok"]:
        error_msg = resultado_agregar["error"]
        print(f"❌ Error al agregar juego para eliminar: {error_msg}")
        return False

    id_eliminar = resultado_agregar["id"]
    print(f"✅ Juego agregado para eliminar: {id_eliminar}")

    # Verificar que existe antes de eliminar
    resultado_buscar = buscar_por_Id(id_eliminar)
    if not resultado_buscar["ok"]:
        print("❌ Juego no encontrado antes de eliminar")
        return False

    # Eliminar usando tabla hash
    resultado_eliminar = eliminar_juego(id_eliminar)

    if not resultado_eliminar["ok"]:
        print(f"❌ Error al eliminar: {resultado_eliminar['error']}")
        return False

    print("✅ Juego eliminado exitosamente")

    # Verificar que ya no existe
    resultado_buscar_despues = buscar_por_Id(id_eliminar)
    if resultado_buscar_despues["ok"]:
        print("❌ Juego todavía existe después de eliminar")
        return False

    print("✅ Verificación post-eliminación exitosa")
    return True


def test_estadisticas_tabla_hash():
    """Prueba las estadísticas de la tabla hash"""
    print("\n🧪 PRUEBA 4: ESTADÍSTICAS DE TABLA HASH")
    print("=" * 50)

    resultado_estadisticas = obtener_estadisticas_indice()

    if not resultado_estadisticas["ok"]:
        print("❌ Error obteniendo estadísticas: " f"{resultado_estadisticas['error']}")
        return False

    stats = resultado_estadisticas["estadisticas"]

    print("📊 ESTADÍSTICAS DE TABLA HASH:")
    print(f"   • Total elementos: {stats['total_elementos']}")
    print(f"   • Colisiones: {stats['colisiones']}")
    print(f"   • Factor de carga: {stats['factor_carga']:.2f}")
    print(f"   • Longitud máxima: {stats['longitud_maxima']}")
    print(f"   • Posiciones ocupadas: {stats['posiciones_ocupadas']}/100")

    # Verificar que tenemos estadísticas válidas
    assert stats["total_elementos"] >= 0
    assert stats["colisiones"] >= 0
    assert 0 <= stats["factor_carga"] <= 1

    print("✅ Estadísticas válidas obtenidas")
    return True


def test_tabla_hash_visual():
    """Prueba la visualización de la tabla hash"""
    print("\n🧪 PRUEBA 5: VISUALIZACIÓN DE TABLA HASH")
    print("=" * 50)

    resultado_visual = obtener_tabla_hash_visual()

    if not resultado_visual["ok"]:
        print(f"❌ Error obteniendo tabla visual: {resultado_visual['error']}")
        return False

    tabla_visual = resultado_visual["tabla_hash"]

    print("🔍 TABLA HASH VISUAL:")
    if tabla_visual:
        for posicion, elementos in tabla_visual.items():
            print(f"   Posición {posicion}: {len(elementos)} elementos")
            # Mostrar solo 2 elementos por posición
            for elemento in elementos[:2]:
                print(f"     - {elemento}")
            if len(elementos) > 2:
                print(f"     ... y {len(elementos) - 2} más")
    else:
        print("   Tabla vacía")

    print("✅ Visualización de tabla hash obtenida")
    return True


def test_consistencia_indices():
    """Prueba la consistencia entre inventario y tabla hash"""
    print("\n🧪 PRUEBA 6: CONSISTENCIA DE ÍNDICES")
    print("=" * 50)

    inventario = obtener_inventario()
    stats = tabla_hash.estadisticas()

    # Verificar que el número de elementos coincide
    if len(inventario) != stats["total_elementos"]:
        print(
            f"❌ Inconsistencia: inventario tiene {len(inventario)}, "
            f"tabla hash tiene {stats['total_elementos']}"
        )
        return False

    print(f"✅ Consistencia verificada: {len(inventario)} elementos en ambos")

    # Verificar que todos los IDs del inventario están en la tabla hash
    for juego in inventario:
        if not tabla_hash.existe(juego["id"]):
            print(f"❌ ID {juego['id']} no encontrado en tabla hash")
            return False

    print("✅ Todos los IDs del inventario están indexados")
    return True


def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA DE ÍNDICES")
    print("=" * 60)

    # Limpiar antes de empezar
    limpiar_inventario()

    resultados = []

    # Ejecutar pruebas
    resultados.append(("Agregar y Buscar", test_agregar_y_buscar()))
    resultados.append(("Búsqueda Múltiple", test_busqueda_rapida_multiple()))
    resultados.append(("Eliminación Eficiente", test_eliminacion_eficiente()))
    resultados.append(("Estadísticas Tabla Hash", test_estadisticas_tabla_hash()))
    resultados.append(("Tabla Hash Visual", test_tabla_hash_visual()))
    resultados.append(("Consistencia Índices", test_consistencia_indices()))

    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("=" * 60)

    for nombre, resultado in resultados:
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"   {nombre}: {estado}")

    pruebas_pasadas = sum(1 for _, resultado in resultados if resultado)
    total_pruebas = len(resultados)

    print(f"\n🎯 RESULTADO: {pruebas_pasadas}/{total_pruebas} pruebas exitosas")

    if pruebas_pasadas == total_pruebas:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("El sistema de índices con tabla hash funciona correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron - revisar el sistema")

    return pruebas_pasadas == total_pruebas


if __name__ == "__main__":
    try:
        exito = ejecutar_todas_las_pruebas()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n💥 ERROR INESPERADO: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
