import json
import os
from typing import Any, Dict, Optional

from .config import RUTA_TABLA_HASH


class NodoHash:
    """Nodo para la lista simplemente enlazada

    Guarda ID y posición en inventario
    """

    def __init__(self, id_juego: str, posicion_inventario: int):
        self.id_juego = id_juego
        # Posición en la lista de inventario
        self.posicion_inventario = posicion_inventario
        self.siguiente: Optional["NodoHash"] = None


class TablaHash:
    """Tabla hash que funciona como índice principal (id -> posición)"""

    def __init__(self, tamano: int = 100):
        self.archivo_indice = RUTA_TABLA_HASH
        self.tamano = tamano
        self.tabla: list[Optional[NodoHash]] = [None] * tamano
        self.cargar_tabla()

    def funcion_hash(self, id_juego: str) -> int:
        """Función hash personalizada que usa los números del ID"""
        numeros = "".join(filter(str.isdigit, id_juego))
        if not numeros:
            numeros = "0"

        numero_hash = sum(int(digit) * (i + 1) for i, digit in enumerate(numeros))
        return numero_hash % self.tamano

    def agregar(self, id_juego: str, posicion_inventario: int):
        """Agrega un ID con su posición en el inventario"""
        indice = self.funcion_hash(id_juego)
        nuevo_nodo = NodoHash(id_juego, posicion_inventario)

        if self.tabla[indice] is None:
            self.tabla[indice] = nuevo_nodo
        else:
            actual = self.tabla[indice]
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

        self.guardar_tabla()

    def buscar_posicion(self, id_juego: str) -> Optional[int]:
        """Busca la posición en el inventario para un ID"""
        indice = self.funcion_hash(id_juego)
        actual = self.tabla[indice]

        while actual is not None:
            if actual.id_juego == id_juego:
                return (
                    actual.posicion_inventario
                )  # ← Devuelve la posición en inventario
            actual = actual.siguiente

        return None

    def existe(self, id_juego: str) -> bool:
        """Verifica si un ID existe en la tabla hash"""
        return self.buscar_posicion(id_juego) is not None

    def eliminar(self, id_juego: str) -> bool:
        """Elimina un ID de la tabla hash"""
        indice = self.funcion_hash(id_juego)
        actual = self.tabla[indice]
        anterior = None

        while actual is not None:
            if actual.id_juego == id_juego:
                if anterior is None:
                    self.tabla[indice] = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                self.guardar_tabla()
                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def actualizar_posicion(self, id_juego: str, nueva_posicion: int):
        """Actualiza la posición de un ID en el inventario"""
        indice = self.funcion_hash(id_juego)
        actual = self.tabla[indice]

        while actual is not None:
            if actual.id_juego == id_juego:
                actual.posicion_inventario = nueva_posicion
                self.guardar_tabla()
                return True
            actual = actual.siguiente

        return False

    def guardar_tabla(self):
        """Guarda la tabla hash con IDs y posiciones"""
        datos_serializables = []

        for i, nodo in enumerate(self.tabla):
            lista_posicion = []
            actual = nodo

            while actual is not None:
                lista_posicion.append(
                    {
                        "id_juego": actual.id_juego,
                        # Guarda la posición en el inventario
                        "posicion_inventario": actual.posicion_inventario,
                    }
                )
                actual = actual.siguiente

            if lista_posicion:
                datos_serializables.append({"indice": i, "elementos": lista_posicion})

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

            for posicion in datos["datos"]:
                indice = posicion["indice"]
                elementos = posicion["elementos"]

                if elementos:
                    primer_elemento = elementos[0]
                    self.tabla[indice] = NodoHash(
                        primer_elemento["id_juego"],
                        primer_elemento["posicion_inventario"],
                    )

                    actual = self.tabla[indice]
                    for elemento in elementos[1:]:
                        actual.siguiente = NodoHash(
                            elemento["id_juego"],
                            elemento["posicion_inventario"],
                        )
                        actual = actual.siguiente

            print("✓ Tabla hash de índices cargada correctamente")

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error cargando tabla hash: {e}")
            self.tabla = [None] * self.tamano

    def obtener_tabla_visual(self) -> Dict[int, list]:
        """Obtiene la tabla hash en formato visual"""
        tabla_visual = {}

        for i in range(self.tamano):
            elementos = []
            actual = self.tabla[i]

            while actual is not None:
                elementos.append(f"{actual.id_juego}->pos{actual.posicion_inventario}")
                actual = actual.siguiente

            if elementos:
                tabla_visual[i] = elementos

        return tabla_visual

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
            "longitud_maxima": (max(lista_longitudes) if lista_longitudes else 0),
            "longitud_promedio": (
                sum(lista_longitudes) / len(lista_longitudes) if lista_longitudes else 0
            ),
            "posiciones_ocupadas": len(lista_longitudes),
            "tabla_visual": self.obtener_tabla_visual(),
        }
