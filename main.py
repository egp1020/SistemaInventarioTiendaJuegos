import sys
import os
from pathlib import Path

# Configurar path para importar desde src
sys.path.append(str(Path(__file__).parent / "src"))

from modelos import Videojuego
from servicio import agregar_videojuego, buscar_por_Id, listar_juegos
from repositorio import obtener_inventario, guardar_inventario, inicializar_inventario

# Clase para simular archivos subidos en Streamlit
class MockArchivo:
    def __init__(self, nombre_archivo="test.png"):
        self.name = nombre_archivo
        self._content = b"fake_image_data_" + nombre_archivo.encode()
    
    def getvalue(self):
        return self._content
    
    def read(self):
        return self._content

def limpiar_inventario():
    """Limpia el inventario para pruebas"""
    guardar_inventario([])
    print("🧹 Inventario limpiado")

def prueba_validaciones_modelo():
    """Prueba las validaciones del modelo Videojuego"""
    print("=" * 60)
    print("🧪 PRUEBAS DE VALIDACIÓN DEL MODELO")
    print("=" * 60)
    
    # Test 1: Portada vacía (DEBE FALLAR según tu código)
    print("\n1. Probando portada vacía (debe fallar)...")
    try:
        juego = Videojuego(
            nombre="Zelda Test",
            precio=59.99,
            cantidad=10,
            compania="Nintendo",
            portada="",  # PORTADA VACÍA - DEBE FALLAR
            fecha_publicacion="2023-05-12"
        )
        print("   ❌ ERROR: Debió fallar por portada vacía")
        return False
    except ValueError as e:
        if "portada" in str(e).lower() or "obligatoria" in str(e).lower():
            print(f"   ✅ CORRECTO: {e}")
            return True
        else:
            print(f"   ❌ ERROR inesperado: {e}")
            return False
    
    # Test 2: Datos válidos (DEBE FUNCIONAR)
    print("\n2. Probando datos válidos...")
    try:
        juego = Videojuego(
            nombre="The Legend of Zelda",
            precio=59.99,
            cantidad=15,
            compania="Nintendo",
            portada="imagenes/portadas/zelda.png",  # Ruta válida
            fecha_publicacion="2017-03-03"
        )
        print(f"   ✅ CORRECTO: Juego creado - ID: {juego.id}")
        print(f"   📝 Nombre: {juego.nombre}")
        return True
    except ValueError as e:
        print(f"   ❌ ERROR inesperado: {e}")
        return False

def prueba_servicio_agregar():
    """Prueba el servicio de agregar videojuegos"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS DEL SERVICIO - AGREGAR JUEGOS")
    print("=" * 60)
    
    limpiar_inventario()
    
    # Test 1: Agregar sin portada (DEBE FALLAR)
    print("\n1. Agregar juego sin portada...")
    resultado = agregar_videojuego(
        nombre="Mario Sin Imagen",
        precio=49.99,
        cantidad=8,
        compania="Nintendo",
        portada=None,  # ✅ CORREGIDO: parámetro 'portada'
        fecha_publicacion="2023-05-15"
    )
    
    if not resultado["ok"]:
        print(f"   ✅ CORRECTO: {resultado['error']}")
    else:
        print("   ❌ ERROR: Debió fallar por falta de portada")
        return False, None
    
    # Test 2: Agregar con portada (DEBE FUNCIONAR)
    print("\n2. Agregar juego con portada...")
    archivo_prueba = MockArchivo("super_mario_odyssey.png")
    
    resultado = agregar_videojuego(
        nombre="Super Mario Odyssey",
        precio=59.99,
        cantidad=12,
        compania="Nintendo",
        portada=archivo_prueba,  # ✅ CORREGIDO: parámetro 'portada'
        fecha_publicacion="2017-10-27"
    )
    
    if resultado["ok"]:
        print(f"   ✅ CORRECTO: {resultado.get('mensaje ', 'Juego agregado')}")
        mario_id = resultado["id"]
        print(f"   🆔 ID generado: {mario_id}")
        
        # Verificar que se guardó en el inventario
        inventario = obtener_inventario()
        if len(inventario) == 1:
            print("   📦 Juego guardado en inventario correctamente")
            
            # Verificar que se guardó la ruta, no el objeto
            juego_guardado = inventario[0]
            if juego_guardado["portada"].startswith("imagenes/portadas/"):
                print("   🖼️  Ruta de portada guardada correctamente")
                return True, mario_id
            else:
                print(f"   ❌ ERROR: Ruta de portada inválida: {juego_guardado['portada']}")
                return False, None
        else:
            print("   ❌ ERROR: Juego no apareció en inventario")
            return False, None
    else:
        print(f"   ❌ ERROR: {resultado['error']}")
        return False, None

def prueba_busqueda_y_listado(mario_id):
    """Prueba las funciones de búsqueda y listado"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS DE BÚSQUEDA Y LISTADO")
    print("=" * 60)
    
    if not mario_id:
        print("   ⚠️  Saltando pruebas de búsqueda (ID no disponible)")
        return False
    
    # Test 1: Buscar por ID existente
    print("\n1. Buscar juego por ID...")
    resultado = buscar_por_Id(mario_id)
    
    if resultado["ok"]:
        juego = resultado["resultado"]
        print(f"   ✅ ENCONTRADO: {juego['nombre']}")
        print(f"   💰 Precio: ${juego['precio']}")
        print(f"   🖼️ Portada: {juego['portada']}")
        
        # Verificar que la portada es una ruta string, no objeto
        if isinstance(juego['portada'], str) and juego['portada'].startswith("imagenes/portadas/"):
            print("   ✅ Portada es ruta string válida")
        else:
            print(f"   ❌ ERROR: Portada no es ruta válida: {type(juego['portada'])} - {juego['portada']}")
            return False
    else:
        print(f"   ❌ ERROR: {resultado['error']}")
        return False
    
    # Test 2: Buscar por ID inexistente
    print("\n2. Buscar por ID inexistente...")
    resultado = buscar_por_Id("id-inexistente-123")
    
    if not resultado["ok"]:
        print(f"   ✅ CORRECTO: {resultado['error']}")
    else:
        print("   ❌ ERROR: Debió fallar con ID inexistente")
        return False
    
    # Test 3: Listar todos los juegos
    print("\n3. Listar todos los juegos...")
    resultado = listar_juegos()
    
    if resultado["ok"]:
        juegos = resultado["resultado"]
        print(f"   📊 Total de juegos: {len(juegos)}")
        for juego in juegos:
            print(f"   🎮 {juego['nombre']} (ID: {juego['id']})")
        return True
    else:
        print(f"   ❌ ERROR: {resultado['error']}")
        return False

def prueba_repositorio_directo():
    """Prueba directa del repositorio"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS DIRECTAS DEL REPOSITORIO")
    print("=" * 60)
    
    limpiar_inventario()
    
    # Test directo del repositorio
    from repositorio import agregar_juego, buscar_por_id
    
    juego_directo = {
        "id": "test-directo-123",
        "nombre": "Juego de Prueba Directa",
        "precio": 39.99,
        "cantidad": 7,
        "compania": "Test Company",
        "portada": "imagenes/portadas/direct_test.png",  # Ruta de portada
        "fecha_publicacion": "2023-01-01"
    }
    
    agregar_juego(juego_directo)
    
    # Verificar que se guardó
    inventario = obtener_inventario()
    print(f"   📦 Juegos en inventario: {len(inventario)}")
    
    # Buscar el juego agregado
    juego_encontrado = buscar_por_id("test-directo-123")
    if juego_encontrado:
        print(f"   ✅ Juego encontrado: {juego_encontrado['nombre']}")
        return True
    else:
        print("   ❌ Juego no encontrado")
        return False

def mostrar_estado_final():
    """Muestra el estado final del sistema"""
    print("\n" + "=" * 60)
    print("📊 ESTADO FINAL DEL INVENTARIO")
    print("=" * 60)
    
    inventario = obtener_inventario()
    print(f"Total de juegos en inventario: {len(inventario)}")
    
    if inventario:
        print("\n📋 Lista completa de juegos:")
        for i, juego in enumerate(inventario, 1):
            print(f"{i}. {juego['nombre']}")
            print(f"   ID: {juego['id']}")
            print(f"   Precio: ${juego['precio']}")
            print(f"   Cantidad: {juego['cantidad']} unidades")
            print(f"   Portada: {juego['portada']}")
            print(f"   Fecha: {juego['fecha_publicacion']}")
            print()

def main():
    """Función principal de pruebas"""
    print("🎮 SISTEMA DE INVENTARIO DE VIDEOJUEGOS")
    print("🔧 EJECUTANDO PRUEBAS CON TU CÓDIGO ACTUAL")
    print("📝 Portada es OBLIGATORIA según tu configuración")
    print()
    
    try:
        # Asegurar que el inventario existe
        inicializar_inventario()
        
        # Ejecutar pruebas
        prueba1 = prueba_validaciones_modelo()
        prueba2, mario_id = prueba_servicio_agregar()
        prueba3 = prueba_busqueda_y_listado(mario_id) if prueba2 else False
        prueba4 = prueba_repositorio_directo()
        
        mostrar_estado_final()
        
        # Resumen de resultados
        print("=" * 60)
        print("📈 RESUMEN DE PRUEBAS")
        print("=" * 60)
        print(f"✅ Validaciones modelo: {'Éxito' if prueba1 else 'Fallo'}")
        print(f"✅ Servicio agregar: {'Éxito' if prueba2 else 'Fallo'}")
        print(f"✅ Búsqueda/listado: {'Éxito' if prueba3 else 'Fallo'}")
        print(f"✅ Repositorio directo: {'Éxito' if prueba4 else 'Fallo'}")
        
        if all([prueba1, prueba2, prueba3, prueba4]):
            print("\n🎉 ¡Todas las pruebas pasaron! El sistema funciona correctamente.")
        else:
            print("\n⚠️  Algunas pruebas fallaron. Revisa los mensajes de error.")
            
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()