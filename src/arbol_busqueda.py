"""
Módulo de Árbol Binario de Búsqueda (BST)
Permite indexar y buscar videojuegos por campos con
valores repetidos.
"""

from typing import Any, List, Optional, Tuple


class NodoArbol:
    """
    Nodo de un árbol binario de búsqueda.
    Cada nodo almacena una clave y una lista de valores (IDs de juegos).
    """

    def __init__(self, clave: Any):
        self.clave = clave
        self.valores: List[str] = []  # Lista de IDs de videojuegos
        self.izquierdo: Optional["NodoArbol"] = None
        self.derecho: Optional["NodoArbol"] = None

    def agregar_valor(self, valor: str):
        """Agrega un ID de videojuego a la lista de valores de este nodo"""
        if valor not in self.valores:
            self.valores.append(valor)


class ArbolBusqueda:
    """
    Árbol Binario de Búsqueda para indexar videojuegos.
    Soporta múltiples valores por clave (para manejar valores repetidos).
    """

    def __init__(self):
        self.raiz: Optional[NodoArbol] = None

    def insertar(self, clave: Any, valor: str):
        """
        Inserta un valor (ID de juego) bajo una clave específica.
        Si la clave ya existe, agrega el valor a la lista del nodo.
        Si la clave no existe, crea un nuevo nodo.

        Args:
            clave: Clave para búsqueda (fecha, compañía, etc.)
            valor: ID del videojuego
        """
        if self.raiz is None:
            self.raiz = NodoArbol(clave)
            self.raiz.agregar_valor(valor)
        else:
            self._insertar_recursivo(self.raiz, clave, valor)

    def _insertar_recursivo(self, nodo: NodoArbol, clave: Any, valor: str):
        """Método auxiliar recursivo para insertar en el árbol"""
        if clave == nodo.clave:
            # La clave ya existe, agregar el valor a la lista
            nodo.agregar_valor(valor)
        elif clave < nodo.clave:
            # Ir al subárbol izquierdo
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(clave)
                nodo.izquierdo.agregar_valor(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, clave, valor)
        else:
            # Ir al subárbol derecho
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(clave)
                nodo.derecho.agregar_valor(valor)
            else:
                self._insertar_recursivo(nodo.derecho, clave, valor)

    def buscar(self, clave: Any) -> List[str]:
        """
        Busca todos los IDs de videojuegos asociados con una clave específica.

        Args:
            clave: Clave a buscar

        Returns:
            Lista de IDs de videojuegos, o lista vacía si no se encuentra
        """
        if self.raiz is None:
            return []
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo: Optional[NodoArbol], clave: Any) -> List[str]:
        """Método auxiliar recursivo para buscar en el árbol"""
        if nodo is None:
            return []

        if clave == nodo.clave:
            return nodo.valores.copy()
        elif clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierdo, clave)
        else:
            return self._buscar_recursivo(nodo.derecho, clave)

    def buscar_rango(self, clave_inicio: Any, clave_fin: Any) -> List[str]:
        """
        Busca todos los IDs de videojuegos en un rango de claves [inicio, fin].

        Args:
            clave_inicio: Clave inicial del rango (inclusive)
            clave_fin: Clave final del rango (inclusive)

        Returns:
            Lista de IDs de videojuegos en el rango
        """
        if self.raiz is None:
            return []

        resultado = []
        self._buscar_rango_recursivo(self.raiz, clave_inicio, clave_fin, resultado)
        return resultado

    def _buscar_rango_recursivo(
        self,
        nodo: Optional[NodoArbol],
        clave_inicio: Any,
        clave_fin: Any,
        resultado: List[str],
    ):
        """Método auxiliar recursivo para buscar en un rango"""
        if nodo is None:
            return

        # Si la clave del nodo está en el rango, agregar sus valores
        if clave_inicio <= nodo.clave <= clave_fin:
            resultado.extend(nodo.valores)

        # Explorar subárbol izquierdo si puede contener valores en el rango
        if nodo.clave > clave_inicio:
            self._buscar_rango_recursivo(
                nodo.izquierdo, clave_inicio, clave_fin, resultado
            )

        # Explorar subárbol derecho si puede contener valores en el rango
        if nodo.clave < clave_fin:
            self._buscar_rango_recursivo(
                nodo.derecho, clave_inicio, clave_fin, resultado
            )

    def recorrido_inorden(self) -> List[Tuple[Any, List[str]]]:
        """
        Realiza un recorrido inorden del árbol (devuelve elementos ordenados).

        Returns:
            Lista de tuplas (clave, lista_de_valores) ordenadas por clave
        """
        resultado = []
        self._recorrido_inorden_recursivo(self.raiz, resultado)
        return resultado

    def _recorrido_inorden_recursivo(
        self, nodo: Optional[NodoArbol], resultado: List[Tuple[Any, List[str]]]
    ):
        """Método auxiliar recursivo para recorrido inorden"""
        if nodo is not None:
            self._recorrido_inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.clave, nodo.valores.copy()))
            self._recorrido_inorden_recursivo(nodo.derecho, resultado)

    def esta_vacio(self) -> bool:
        """Verifica si el árbol está vacío"""
        return self.raiz is None

    def obtener_todas_claves(self) -> List[Any]:
        """
        Obtiene todas las claves únicas del árbol en orden.

        Returns:
            Lista de claves ordenadas
        """
        return [clave for clave, _ in self.recorrido_inorden()]

    def contar_nodos(self) -> int:
        """Cuenta el número total de nodos en el árbol"""
        return self._contar_nodos_recursivo(self.raiz)

    def _contar_nodos_recursivo(self, nodo: Optional[NodoArbol]) -> int:
        """Método auxiliar recursivo para contar nodos"""
        if nodo is None:
            return 0
        return (
            1
            + self._contar_nodos_recursivo(nodo.izquierdo)
            + self._contar_nodos_recursivo(nodo.derecho)
        )

    def contar_valores_totales(self) -> int:
        """Cuenta el número total de valores (IDs) almacenados en el árbol"""
        total = 0
        for _, valores in self.recorrido_inorden():
            total += len(valores)
        return total
