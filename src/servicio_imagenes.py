import os
import uuid
from pathlib import Path
class servicio_imagenes:
    def __init__(self):
        self.ruta_base = Path(__file__).parent.parent
        self.carpeta_portadas = self.ruta_base / "imagenes" / "portadas"
        
        # Crear carpetas si no existen
        self.carpeta_portadas.mkdir(parents=True, exist_ok=True)
    def guardar_imagen(self, archivo_imagen, nombre_original):
        try:
            # Generar nombre único
            extension = os.path.splitext(nombre_original)[1].lower()
            nombre_unico = f"{uuid.uuid4().hex}{extension}"
            
            # Ruta completa donde se guardará
            ruta_guardado = self.carpeta_portadas / nombre_unico
            
            # Guardar la imagen
            with open(ruta_guardado, "wb") as f:
                if hasattr(archivo_imagen, 'getvalue'):
                    f.write(archivo_imagen.getvalue())
                else:
                    f.write(archivo_imagen.read())
            
            # Devolver ruta relativa
            return f"imagenes/portadas/{nombre_unico}"
            
        except Exception as e:
            raise Exception(f"Error al guardar imagen: {str(e)}")
    
 