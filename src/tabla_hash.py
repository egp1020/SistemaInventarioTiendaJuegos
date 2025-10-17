import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class NodoHash:
    """Nodo para la lista simplemente enlazada"""

    def __init__(self, id_juego: str, juego: Dict[str, Any]):
        self.id_juego = id_juego
        self.juego = juego
        self.siguiente: Optional["NodoHash"] = None


class TablaHash:
    """Tabla hash con encadenamiento (listas simplemente enlazadas)"""

    def __init__(self, tamano: int = 100, archivo_indice: str = "tabla_hash.json"):
        # Subir dos carpetas para guardar el índice
        BASE_DIR = Path(__file__).parent.parent.parent
        self.archivo_indice = BASE_DIR / archivo_indice
        self.tamano = tamano
        self.tabla: list[Optional[NodoHash]] = [None] * tamano
        self.cargar_tabla()

    def funcion_hash(self, id_juego: str) -> int:
        """
        Función hash personalizada que usa los números del ID
        """
        # Extraer todos los números del UUID
        numeros = "".join(filter(str.isdigit, id_juego))
        if not numeros:
            numeros = "0"

        # Convertir a número y calcular hash
        numero_hash = sum(int(digit) * (i + 1)
                          for i, digit in enumerate(numeros))

        # Aplicar módulo para obtener índice en el vector
        return numero_hash % self.tamano

    def agregar(self, id_juego: str, juego: Dict[str, Any]):
        """Agrega un juego a la tabla hash"""
        indice = self.funcion_hash(id_juego)
        nuevo_nodo = NodoHash(id_juego, juego)

        # Si la posición está vacía, insertar directamente
        if self.tabla[indice] is None:
            self.tabla[indice] = nuevo_nodo
        else:
            # Si hay colisión, agregar al final de la lista
            actual = self.tabla[indice]
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

        self.guardar_tabla()

    def buscar(self, id_juego: str) -> Optional[Dict[str, Any]]:
        """Busca un juego por ID en la tabla hash"""
        indice = self.funcion_hash(id_juego)
        actual = self.tabla[indice]

        # Recorrer la lista enlazada en esa posición
        while actual is not None:
            if actual.id_juego == id_juego:
                return actual.juego
            actual = actual.siguiente

        return None

    def eliminar(self, id_juego: str) -> bool:
        """Elimina un juego de la tabla hash"""
        indice = self.funcion_hash(id_juego)
        actual = self.tabla[indice]
        anterior = None

        # Buscar el nodo a eliminar
        while actual is not None:
            if actual.id_juego == id_juego:
                # Eliminar el nodo
                if anterior is None:
                    # Es el primer nodo de la lista
                    self.tabla[indice] = actual.siguiente
                else:
                    # Es un nodo intermedio o final
                    anterior.siguiente = actual.siguiente

                self.guardar_tabla()
                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def guardar_tabla(self):
        """Convierte la tabla hash a formato serializable y guarda en disco"""
        datos_serializables = []

        for i, nodo in enumerate(self.tabla):
            lista_posicion = []
            actual = nodo

            while actual is not None:
                lista_posicion.append(
                    {"id_juego": actual.id_juego, "juego": actual.juego}
                )
                actual = actual.siguiente

            if lista_posicion:  # Solo guardar posiciones no vacías
                datos_serializables.append(
                    {"indice": i, "elementos": lista_posicion})

        with open(self.archivo_indice, "w", encoding="utf-8") as f:
            json.dump(
                {"tamano": self.tamano, "datos": datos_serializables},
                f,
                indent=4,
                ensure_ascii=False,
            )

    def cargar_tabla(self):
        """Carga la tabla hash desde disco"""
        if not os.path.exists(self.archivo_indice):
            return

        try:
            with open(self.archivo_indice, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Reconstruir la tabla desde los datos serializados
            for posicion in datos["datos"]:
                indice = posicion["indice"]
                elementos = posicion["elementos"]

                # Reconstruir la lista enlazada para esta posición
                if elementos:
                    # Crear el primer nodo
                    primer_elemento = elementos[0]
                    self.tabla[indice] = NodoHash(
                        primer_elemento["id_juego"], primer_elemento["juego"]
                    )

                    # Agregar los nodos siguientes
                    actual = self.tabla[indice]
                    for elemento in elementos[1:]:
                        actual.siguiente = NodoHash(
                            elemento["id_juego"], elemento["juego"]
                        )
                        actual = actual.siguiente

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error cargando tabla hash: {e}")
            # Si hay error, empezar con tabla vacía
            self.tabla = [None] * self.tamano

    def estadisticas(self) -> Dict[str, Any]:
        """Muestra estadísticas de la tabla hash"""
        total_elementos = 0
        colisiones = 0
        lista_longitudes = []

        for i in range(self.tamano):
            longitud = 0
            actual = self.tabla[i]

            while actual is not None:
                longitud += 1
                total_elementos += 1
                actual = actual.siguiente

            if longitud > 0:
                lista_longitudes.append(longitud)
                if longitud > 1:
                    colisiones += 1

        factor_carga = total_elementos / self.tamano if self.tamano > 0 else 0

        return {
            "total_elementos": total_elementos,
            "colisiones": colisiones,
            "factor_carga": factor_carga,
            "longitud_maxima": max(lista_longitudes) if lista_longitudes else 0,
            "longitud_promedio": (
                sum(lista_longitudes) /
                len(lista_longitudes) if lista_longitudes else 0
            ),
            "posiciones_ocupadas": len(lista_longitudes),
        }
