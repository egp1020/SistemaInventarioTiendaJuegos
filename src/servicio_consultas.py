"""
Servicio de Consultas usando Árboles Binarios de Búsqueda
Permite realizar búsquedas eficientes por fecha y compañía.
"""

from typing import Any, Dict, List

from . import repositorio
from .arbol_busqueda import ArbolBusqueda


class ServicioConsultas:
    """
    Servicio para realizar consultas avanzadas sobre el inventario
    utilizando estructuras de árbol binario de búsqueda.
    """

    def __init__(self):
        self.arbol_fechas: ArbolBusqueda = ArbolBusqueda()
        self.arbol_companias: ArbolBusqueda = ArbolBusqueda()
        self._indices_construidos = False

    def construir_indices_arboles(self):
        """
        Construye los árboles BST a partir del inventario actual.
        Debe llamarse antes de realizar cualquier consulta.
        """
        try:
            # Limpiar árboles existentes
            self.arbol_fechas = ArbolBusqueda()
            self.arbol_companias = ArbolBusqueda()

            # Obtener todos los juegos del inventario
            juegos = repositorio.listar_juegos()

            if not juegos:
                self._indices_construidos = False
                return {
                    "ok": False,
                    "error": "No hay videojuegos en el inventario para indexar",
                }

            # Construir índices
            for juego in juegos:
                juego_id = juego.get("id")
                fecha = juego.get("fecha_publicacion")
                compania = juego.get("compania", "").strip()

                # Insertar en árbol de fechas
                if fecha:
                    self.arbol_fechas.insertar(fecha, juego_id)

                # Insertar en árbol de compañías (normalizado a minúsculas)
                if compania:
                    compania_normalizada = compania.lower()
                    self.arbol_companias.insertar(compania_normalizada, juego_id)

            self._indices_construidos = True
            return {
                "ok": True,
                "mensaje": f"Índices construidos: {len(juegos)} juegos indexados",
                "total_juegos": len(juegos),
            }

        except Exception as e:
            self._indices_construidos = False
            return {"ok": False, "error": f"Error al construir índices: {str(e)}"}

    def _verificar_indices(self) -> Dict[str, Any]:
        """Verifica que los índices estén construidos"""
        if not self._indices_construidos:
            # Intentar construir automáticamente
            resultado = self.construir_indices_arboles()
            if not resultado["ok"]:
                return resultado
        return {"ok": True}

    def invalidar_indices(self):
        """
        Invalida los índices BST para forzar su reconstrucción
        en la próxima consulta. Se debe llamar cuando el inventario cambia.
        """
        self._indices_construidos = False

    def buscar_por_fecha(self, fecha: str) -> Dict[str, Any]:
        """
        Busca videojuegos por fecha exacta de publicación.

        Args:
            fecha: Fecha en formato YYYY-MM-DD

        Returns:
            Diccionario con ok, resultado (lista de juegos), y error si aplica
        """
        try:
            # Verificar índices
            verificacion = self._verificar_indices()
            if not verificacion["ok"]:
                return verificacion

            # Validar entrada
            if not fecha:
                return {"ok": False, "error": "La fecha es obligatoria"}

            # Buscar IDs en el árbol
            ids_encontrados = self.arbol_fechas.buscar(fecha)

            # Convertir IDs a juegos completos
            juegos = self._obtener_juegos_de_ids(ids_encontrados)

            if not juegos:
                return {
                    "ok": True,
                    "resultado": [],
                    "mensaje": f"No se encontraron videojuegos con fecha {fecha}",
                }

            return {
                "ok": True,
                "resultado": juegos,
                "mensaje": f"Se encontraron {len(juegos)} videojuego(s) con fecha {fecha}",
            }

        except Exception as e:
            return {"ok": False, "error": f"Error al buscar por fecha: {str(e)}"}

    def buscar_por_rango_fechas(
        self, fecha_inicio: str, fecha_fin: str
    ) -> Dict[str, Any]:
        """
        Busca videojuegos en un rango de fechas de publicación.

        Args:
            fecha_inicio: Fecha inicial en formato YYYY-MM-DD (inclusive)
            fecha_fin: Fecha final en formato YYYY-MM-DD (inclusive)

        Returns:
            Diccionario con ok, resultado (lista de juegos), y error si aplica
        """
        try:
            # Verificar índices
            verificacion = self._verificar_indices()
            if not verificacion["ok"]:
                return verificacion

            # Validar entrada
            if not fecha_inicio or not fecha_fin:
                return {
                    "ok": False,
                    "error": "Ambas fechas son obligatorias para búsqueda por rango",
                }

            # Validar que fecha_inicio <= fecha_fin
            if fecha_inicio > fecha_fin:
                return {
                    "ok": False,
                    "error": "La fecha inicial debe ser menor o igual a la fecha final",
                }

            # Buscar IDs en el rango
            ids_encontrados = self.arbol_fechas.buscar_rango(fecha_inicio, fecha_fin)

            # Convertir IDs a juegos completos
            juegos = self._obtener_juegos_de_ids(ids_encontrados)

            if not juegos:
                return {
                    "ok": True,
                    "resultado": [],
                    "mensaje": f"No se encontraron videojuegos entre {fecha_inicio} y {fecha_fin}",
                }

            return {
                "ok": True,
                "resultado": juegos,
                "mensaje": f"Se encontraron {len(juegos)} videojuego(s) entre {fecha_inicio} y {fecha_fin}",
            }

        except Exception as e:
            return {
                "ok": False,
                "error": f"Error al buscar por rango de fechas: {str(e)}",
            }

    def buscar_por_compania_arbol(self, compania: str) -> Dict[str, Any]:
        """
        Busca videojuegos por compañía usando el árbol BST.

        Args:
            compania: Nombre de la compañía (no distingue mayúsculas/minúsculas)

        Returns:
            Diccionario con ok, resultado (lista de juegos), y error si aplica
        """
        try:
            # Verificar índices
            verificacion = self._verificar_indices()
            if not verificacion["ok"]:
                return verificacion

            # Validar entrada
            if not compania or not compania.strip():
                return {"ok": False, "error": "El nombre de la compañía es obligatorio"}

            # Normalizar búsqueda
            compania_normalizada = compania.strip().lower()

            # Buscar IDs en el árbol
            ids_encontrados = self.arbol_companias.buscar(compania_normalizada)

            # Convertir IDs a juegos completos
            juegos = self._obtener_juegos_de_ids(ids_encontrados)

            if not juegos:
                return {
                    "ok": True,
                    "resultado": [],
                    "mensaje": f"No se encontraron videojuegos de la compañía '{compania}'",
                }

            return {
                "ok": True,
                "resultado": juegos,
                "mensaje": f"Se encontraron {len(juegos)} videojuego(s) de '{compania}'",
            }

        except Exception as e:
            return {"ok": False, "error": f"Error al buscar por compañía: {str(e)}"}

    def obtener_companias_disponibles(self) -> Dict[str, Any]:
        """
        Obtiene lista de todas las compañías disponibles en el inventario.

        Returns:
            Diccionario con ok y lista de compañías ordenadas alfabéticamente
        """
        try:
            # Verificar índices
            verificacion = self._verificar_indices()
            if not verificacion["ok"]:
                return verificacion

            # Obtener claves del árbol (ya están ordenadas por el recorrido inorden)
            companias_normalizadas = self.arbol_companias.obtener_todas_claves()

            # Obtener nombres originales desde el inventario
            juegos = repositorio.listar_juegos()
            companias_originales = {}

            for juego in juegos:
                compania_original = juego.get("compania", "").strip()
                compania_normalizada = compania_original.lower()
                if compania_normalizada not in companias_originales:
                    companias_originales[compania_normalizada] = compania_original

            # Mapear nombres normalizados a originales
            companias = [companias_originales.get(c, c) for c in companias_normalizadas]

            return {"ok": True, "companias": companias, "total": len(companias)}

        except Exception as e:
            return {"ok": False, "error": f"Error al obtener compañías: {str(e)}"}

    def obtener_fechas_disponibles(self) -> Dict[str, Any]:
        """
        Obtiene lista de todas las fechas de publicación disponibles.

        Returns:
            Diccionario con ok y lista de fechas ordenadas cronológicamente
        """
        try:
            # Verificar índices
            verificacion = self._verificar_indices()
            if not verificacion["ok"]:
                return verificacion

            # Obtener claves del árbol (ya están ordenadas)
            fechas = self.arbol_fechas.obtener_todas_claves()

            return {"ok": True, "fechas": fechas, "total": len(fechas)}

        except Exception as e:
            return {"ok": False, "error": f"Error al obtener fechas: {str(e)}"}

    def _obtener_juegos_de_ids(self, lista_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Convierte una lista de IDs en objetos de juego completos.

        Args:
            lista_ids: Lista de IDs de videojuegos

        Returns:
            Lista de diccionarios con información completa de los juegos
        """
        if not lista_ids:
            return []

        juegos = []
        for juego_id in lista_ids:
            juego = repositorio.buscar_por_id(juego_id)
            if juego:
                juegos.append(juego)

        return juegos

    def obtener_estadisticas_arboles(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas sobre los árboles BST construidos.

        Returns:
            Diccionario con estadísticas de los árboles
        """
        try:
            if not self._indices_construidos:
                return {"ok": False, "error": "Los índices no han sido construidos"}

            return {
                "ok": True,
                "estadisticas": {
                    "arbol_fechas": {
                        "nodos": self.arbol_fechas.contar_nodos(),
                        "valores_totales": self.arbol_fechas.contar_valores_totales(),
                        "fechas_unicas": len(self.arbol_fechas.obtener_todas_claves()),
                    },
                    "arbol_companias": {
                        "nodos": self.arbol_companias.contar_nodos(),
                        "valores_totales": self.arbol_companias.contar_valores_totales(),
                        "companias_unicas": len(
                            self.arbol_companias.obtener_todas_claves()
                        ),
                    },
                },
            }

        except Exception as e:
            return {"ok": False, "error": f"Error al obtener estadísticas: {str(e)}"}


# Instancia global del servicio
servicio_consultas = ServicioConsultas()
