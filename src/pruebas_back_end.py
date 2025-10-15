# archivo: src/test_agregar_eliminar.py
import os
import sys
from pathlib import Path
from io import BytesIO

# Como está en la misma carpeta src, podemos importar directamente
from servicio import agregar_videojuego, eliminar_juego, buscar_por_Id
from repositorio import obtener_inventario
import repositorio

def crear_imagen_falsa(nombre_archivo="portada_test.jpg"):
    """Crea una imagen falsa en memoria para pruebas"""
    imagen_falsa = BytesIO()
    imagen_falsa.write(b"fake image data for testing purposes")
    imagen_falsa.name = nombre_archivo
    imagen_falsa.seek(0)
    return imagen_falsa

def limpiar_inventario_manual():
    """Función manual para limpiar el inventario (alternativa)"""
    try:
        ruta_archivo = Path(__file__).parent.parent / "inventario.json"
        if ruta_archivo.exists():
            os.remove(ruta_archivo)
        ruta_indice = Path(__file__).parent.parent / "tabla_hash.json"
        if ruta_indice.exists():
            os.remove(ruta_indice)
        print("✅ Inventario limpiado manualmente")
    except Exception as e:
        print(f"⚠️  Advertencia al limpiar: {e}")

def test_agregar_y_eliminar():
    """Prueba completa: Agregar un juego y luego eliminarlo"""
    print("🧪 INICIANDO PRUEBA: AGREGAR Y ELIMINAR ELEMENTO")
    print("=" * 60)
    
    # Limpiar inventario antes de empezar (usando función manual)
    limpiar_inventario_manual()
    
    # Paso 1: Agregar un juego
    print("\n1. AGREGANDO JUEGO...")
    portada = crear_imagen_falsa("test_game_cover.jpg")
    
    resultado_agregar = agregar_videojuego(
        nombre="The Legend of Zelda: Tears of the Kingdom",
        precio=69.99,
        cantidad=20,
        compania="Nintendo",
        portada=portada,
        fecha_publicacion="2023-05-12"
    )
    
    print(f"Resultado agregar: {resultado_agregar}")
    
    if not resultado_agregar["ok"]:
        print("❌ ERROR: No se pudo agregar el juego")
        return False
    
    juego_id = resultado_agregar["id"]
    print(f"✅ Juego agregado exitosamente con ID: {juego_id}")
    
    # Paso 2: Verificar que el juego fue agregado
    print("\n2. VERIFICANDO QUE EL JUEGO FUE AGREGADO...")
    resultado_busqueda = buscar_por_Id(juego_id)
    print(f"Resultado búsqueda: {resultado_busqueda}")
    
    if not resultado_busqueda["ok"]:
        print("❌ ERROR: No se encontró el juego después de agregarlo")
        return False
    
    juego_encontrado = resultado_busqueda["resultado"]
    print(f"✅ Juego encontrado: {juego_encontrado['nombre']}")
    
    # Verificar datos del juego
    assert juego_encontrado["nombre"] == "The Legend of Zelda: Tears of the Kingdom"
    assert juego_encontrado["precio"] == 69.99
    assert juego_encontrado["cantidad"] == 20
    assert juego_encontrado["compania"] == "Nintendo"
    print("✅ Datos del juego verificados correctamente")
    
    # Paso 3: Eliminar el juego
    print("\n3. ELIMINANDO JUEGO...")
    resultado_eliminar = eliminar_juego(juego_id)
    print(f"Resultado eliminar: {resultado_eliminar}")
    
    if not resultado_eliminar["ok"]:
        print("❌ ERROR: No se pudo eliminar el juego")
        return False
    
    print("✅ Juego eliminado exitosamente")
    
    # Paso 4: Verificar que el juego fue eliminado
    print("\n4. VERIFICANDO QUE EL JUEGO FUE ELIMINADO...")
    resultado_busqueda_despues = buscar_por_Id(juego_id)
    print(f"Resultado búsqueda después de eliminar: {resultado_busqueda_despues}")
    
    if resultado_busqueda_despues["ok"]:
        print("❌ ERROR: El juego todavía existe después de eliminarlo")
        return False
    
    print("✅ Juego correctamente eliminado (no se encuentra en búsquedas)")
    
    # Paso 5: Verificar inventario vacío
    print("\n5. VERIFICANDO INVENTARIO FINAL...")
    inventario_final = obtener_inventario()
    juegos_con_ese_id = [j for j in inventario_final if j["id"] == juego_id]
    
    if len(juegos_con_ese_id) > 0:
        print("❌ ERROR: El juego todavía existe en el inventario")
        return False
    
    print(f"✅ Inventario final: {len(inventario_final)} juegos")
    print("✅ El juego fue completamente removido del sistema")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("✓ Juego agregado correctamente")
    print("✓ Juego encontrado en búsquedas") 
    print("✓ Juego eliminado correctamente")
    print("✓ Juego removido de búsquedas")
    print("✓ Juego removido del inventario")
    print(f"✓ ID del juego testeado: {juego_id}")
    
    return True

def test_eliminar_juego_inexistente():
    """Prueba eliminar un juego que no existe"""
    print("\n\n🧪 PRUEBA: ELIMINAR JUEGO INEXISTENTE")
    print("=" * 60)
    
    resultado = eliminar_juego("id-inexistente-99999")
    print(f"Resultado eliminar juego inexistente: {resultado}")
    
    # Debería fallar (ok: False)
    if not resultado["ok"]:
        print("✅ Comportamiento correcto: No se puede eliminar juego inexistente")
        return True
    else:
        print("❌ Comportamiento incorrecto: Se eliminó un juego que no existe")
        return False

if __name__ == "__main__":
    try:
        # Ejecutar prueba principal
        resultado_principal = test_agregar_y_eliminar()
        
        # Ejecutar prueba de eliminación de juego inexistente
        resultado_inexistente = test_eliminar_juego_inexistente()
        
        # Resumen general
        print("\n" + "=" * 60)
        print("📊 RESUMEN GENERAL DE PRUEBAS")
        print("=" * 60)
        print(f"Prueba agregar/eliminar: {'✅ PASÓ' if resultado_principal else '❌ FALLÓ'}")
        print(f"Prueba eliminar inexistente: {'✅ PASÓ' if resultado_inexistente else '❌ FALLÓ'}")
        
        if resultado_principal and resultado_inexistente:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        else:
            print("\n⚠️ Algunas pruebas fallaron")
            
    except Exception as e:
        print(f"\n💥 ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
eliminar_juego("a80a5bc8-e8ff-4b76-a369-02a9a7dd8537")