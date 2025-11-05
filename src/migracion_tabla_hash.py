from .repositorio import obtener_inventario, tabla_hash


def migrar_a_tabla_hash():
    """Migra todos los juegos existentes a la tabla hash"""
    juegos = obtener_inventario()
    contador = 0

    print("Iniciando migración a tabla hash...")

    for juego in juegos:
        try:
            tabla_hash.agregar(juego["id"], juego)
            contador += 1
            print(f"✓ Migrado: {juego['nombre']} -> ID: {juego['id']}")
        except Exception as e:
            print(f"✗ Error migrando {juego['nombre']}: {e}")

    stats = tabla_hash.estadisticas()
    print("\n--- ESTADÍSTICAS DE LA TABLA HASH ---")
    print(f"Total elementos migrados: {contador}")
    print(f"Factor de carga: {stats['factor_carga']:.2f}")
    print(f"Colisiones: {stats['colisiones']}")
    print(f"Longitud máxima de lista: {stats['longitud_maxima']}")
    print(f"Posiciones ocupadas: {stats['posiciones_ocupadas']}/100")
    print("¡Migración completada!")


if __name__ == "__main__":
    migrar_a_tabla_hash()
