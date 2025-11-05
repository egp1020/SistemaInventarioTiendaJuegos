import hashlib
import os

from .config import CARPETA_PORTADAS, RUTA_RELATIVA_PORTADAS


class servicio_imagenes:
    """
    Servicio para guardar imágenes en disco y evitar duplicados usando hash.
    """

    def __init__(self):
        CARPETA_PORTADAS.mkdir(parents=True, exist_ok=True)
        self.carpeta_portadas = CARPETA_PORTADAS

    def guardar_imagen(self, archivo_imagen, nombre_original):
        """
        Guarda una imagen en disco usando SHA256 como nombre único.
        Si la imagen ya existe (mismo contenido), no la duplica.
        Retorna la ruta relativa que se debe guardar en el JSON.
        """
        # Leer contenido en bytes
        if hasattr(archivo_imagen, "getvalue"):
            contenido = archivo_imagen.getvalue()
        else:
            contenido = archivo_imagen.read()

        # Calcular hash SHA256
        hash_archivo = hashlib.sha256(contenido).hexdigest()
        # Mantener extensión original
        extension = os.path.splitext(nombre_original)[1].lower()
        nombre_unico = f"{hash_archivo}{extension}"

        ruta_guardado = self.carpeta_portadas / nombre_unico

        # Guardar solo si no existe ya
        if not ruta_guardado.exists():
            with open(ruta_guardado, "wb") as f:
                f.write(contenido)

        # Retornar ruta relativa homogénea (la definida en config)
        return f"{RUTA_RELATIVA_PORTADAS}/{nombre_unico}"
