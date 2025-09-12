#librerias usadas: dataclasses
#la portada se guarda como una ruta hacia carpeta que contiene las imagenes
#la fecha aunque se ingresa en el formato date se guarda como un string
from dataclasses import dataclass, asdict, field
import uuid
from datetime import datetime
@dataclass
class Videojuego:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str = ""
    precio: float = 0.0
    cantidad: int = 0
    compania: str = ""
    portada: str = ""
    fecha_publicacion: str = ""
    def __post_init__(self):
        # Validar formato de fecha
        try:
            datetime.strptime(self.fecha_publicacion, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
        if not self.nombre:
            raise ValueError("El nombre es obligatorio")
        if self.precio is None:
            raise ValueError("El precio no puede estar vacio")
        if self.precio <= 0:
            raise ValueError("El precio no puede ser negativo")
        if self.cantidad is None:
            raise ValueError("La cantidad no puede estar vacia")
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if self.cantidad is float:
            raise ValueError("La cantidad no puede ser decimal")
        if not self.compania:
            raise ValueError("La compañía es obligatoria")
        if not self.portada:
            raise ValueError("La portada es obligatoria")    
        if self.fecha_publicacion is None:
            raise ValueError("La fecha es obligatoria")
    

    def to_dict(self):
        return asdict(self)
    
