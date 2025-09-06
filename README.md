# Sistema de Inventario de una Tienda de Juegos/Videojuegos

## 🔀 Flujo de ramas

- **`main`**
  - Rama protegida.
  - Contiene el código estable listo para entregar.
  - Solo se actualiza mediante *pull requests* desde `develop` con al menos 1 aprobación.

- **`develop`**
  - Rama de integración.
  - Recibe *pull requests* desde ramas `feature/*`.
  - Se usa para probar funcionalidades antes de llevarlas a `main`.

- **`feature/*`**
  - Ramas para nuevas funcionalidades o correcciones.
  - Se crean a partir de `develop`.
  - Ejemplo: `feature/login-usuario`.
  - Una vez lista, se hace PR → `develop`.

## 📝 Reglas de commits

- Mensajes de commit claros y en tiempo presente.
- Prefijo recomendado según el tipo de cambio:
  - `feat: ...` → nueva funcionalidad
  - `fix: ...` → corrección de error
  - `docs: ...` → documentación
  - `chore: ...` → tareas menores

**Ejemplo:**
feat: agregar validación de correo en formulario de registro

## 🔒 Reglas de Pull Requests

- Todo cambio debe entrar mediante **PR**, no está permitido el push directo a `main` ni `develop`.
- El PR debe:
  - Describir brevemente los cambios.
  - Relacionarse con un issue o tarea, si aplica.
  - Ser revisado y aprobado por al menos un integrante del equipo.
  - Resolver todas las conversaciones antes de poder mergear.
