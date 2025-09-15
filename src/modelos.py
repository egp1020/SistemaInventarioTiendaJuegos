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
        # Validar formatos
        try:
            datetime.strptime(self.fecha_publicacion, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
        if isinstance(self.cantidad, float):
            raise ValueError("La cantidad no puede ser decimal")
        if not isinstance(self.cantidad, int):
            raise ValueError("La cantidad debe ser un numero")
        if not isinstance(self.precio, (int, float)):
            raise ValueError("El precio debe ser un número") 
        #validar que los campos esten llenos
        if not self.nombre:
            raise ValueError("El nombre es obligatorio")
        if self.precio is 0:
            raise ValueError("El precio no puede estar vacio")
        if self.cantidad is 0:
            raise ValueError("La cantidad no puede estar vacia")
        if not self.compania:
            raise ValueError("La compañía es obligatoria")
        if not self.portada:
            raise ValueError("La portada es obligatoria")    
        if self.fecha_publicacion is None:
            raise ValueError("La fecha es obligatoria")
        #verificar errores logicos
        if self.precio <= 0:
            raise ValueError("El precio no puede ser menor o igual a 0")
        if self.cantidad <= 0:
            raise ValueError("La cantidad no puede ser menor o igual a 0")

    def to_dict(self):
        return asdict(self)
    
