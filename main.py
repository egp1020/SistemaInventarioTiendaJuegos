from datetime import date
from pathlib import Path
import json

import streamlit as st

from src import repositorio, servicio
from src.servicio_imagenes import servicio_imagenes
import base64

ruta_base = Path(__file__).resolve().parent

servicio_img = servicio_imagenes()

st.set_page_config(layout="wide")
st.title("🎮 Registro de Videojuegos")
st.subheader("Formulario para agregar un nuevo videojuego")

# Inicializar valores por defecto en session_state (si no existen)
defaults = {"nombre": "", "precio": 0.0, "cantidad": 0, "compania": "", "fecha": None}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "portada_key" not in st.session_state:
    st.session_state["portada_key"] = 0

# Formulario
with st.form("formulario_juego", clear_on_submit=False):
    nombre = st.text_input("Nombre del videojuego", key="nombre")
    precio = st.number_input("Precio", step=0.01, key="precio")
    cantidad = st.number_input("Stock", step=1, min_value=0, key="cantidad")
    compania = st.text_input("Compañía", key="compania")
    if st.session_state["fecha"] is None:
        fecha_str = st.text_input("Fecha de publicación (YYYY-MM-DD)", value="")
        fecha_val = None
        if fecha_str:
            try:
                fecha_val = date.fromisoformat(fecha_str)
                st.session_state["fecha"] = fecha_val
            except ValueError:
                st.warning("⚠️ Ingrese una fecha válida con formato YYYY-MM-DD")
    else:
        fecha_val = st.date_input(
            "Fecha de publicación (YYYY-MM-DD)",
            value=st.session_state["fecha"],
            min_value=date(1900, 1, 1),
            max_value=date(2030, 12, 31),
            format="YYYY-MM-DD",
            key="fecha",
        )

    # ✅ File uploader SIN valor por defecto
    # ✅ File uploader con key dinámico
    portada = st.file_uploader(
        "Portada",
        type=["png", "jpg", "jpeg"],
        key=f"portada_{st.session_state['portada_key']}",
    )
    if portada is not None:
        st.image(portada, width=150, caption="Vista previa de portada")

    submit = st.form_submit_button("💾 Guardar")


if submit:
    nombre_val = nombre.strip()
    precio_val = precio
    cantidad_val = cantidad
    compania_val = compania.strip()
    portada_val = portada
    fecha_final = fecha_val

    try:
        if cantidad_val <= 0:
            raise ValueError("El stock es obligatorio y debe ser mayor que 0")
        if fecha_final is None:
            raise ValueError("La fecha es obligatoria")
        resultado = servicio.agregar_videojuego(
            nombre_val,
            precio_val,
            cantidad_val,
            compania_val,
            portada_val,
            fecha_val.strftime("%Y-%m-%d"),
        )

        if resultado["ok"]:
            st.success(
                f"✅ Videojuego agregado exitosamente.\n"
                f"ID generado: {resultado['id']}"
            )

            # 🔑 Limpiar solo si el registro fue exitoso
            for key in ["nombre", "precio", "cantidad", "compania", "fecha"]:
                if key in st.session_state:
                    del st.session_state[key]
            # 🔄 Forzar reset de la portada
            st.session_state["portada_key"] += 1

            st.rerun()

        else:
            st.error(f"❌ {resultado['error']}")

    except ValueError as ve:
        st.error(f"❌ Error de validación: {ve}")
    except Exception as e:
        st.error(f"⚠️ Error inesperado: {e}")


st.markdown("### ⚙️ Utilidades del Inventario")

col_u1, col_u2 = st.columns(2)

# Descargar inventario JSON
with col_u1:
    if st.button("⬇️ Descargar inventario JSON"):
        resultado = servicio.descargar_inventario_como_json()
        if resultado["ok"]:
            datos = resultado["datos"]
            nombre = resultado["nombre_archivo"]
            st.download_button(
                label="📥 Descargar archivo",
                data=json.dumps(datos, indent=4, ensure_ascii=False),
                file_name=nombre,
                mime="application/json",
            )
        else:
            st.error(resultado["error"])

# 🔹 Descargar tabla de índices
with col_u2:
    if st.button("📋 Descargar tabla de índices"):
        resultado = servicio.descargar_tabla_indices_como_json()
        if resultado["ok"]:
            st.download_button(
                label="📥 Descargar índices",
                data=json.dumps(resultado["datos"], indent=4, ensure_ascii=False),
                file_name="tabla_indices.json",
                mime="application/json",
            )
        else:
            st.error(resultado["error"])


# Mostrar juegos registrados
st.subheader("📋 Videojuegos Disponibles")

col1, col2, col3 = st.columns(3)
with col1:
    busqueda_id = st.text_input("🔎 Buscar por ID:")
with col2:
    busqueda_nombre = st.text_input("🔎 Buscar por Nombre:")
with col3:
    busqueda_compania = st.text_input("🔎 Buscar por Compañía:")

juegos = repositorio.listar_juegos()

# Filtrar por ID
if busqueda_id:
    resultado = servicio.buscar_por_Id(busqueda_id)
    if resultado["ok"]:
        juegos = [resultado["resultado"]]
    else:
        st.error(f"❌ {resultado['error']}")
        juegos = []
# Filtrar por Nombre
elif busqueda_nombre:
    resultado = servicio.buscar_por_nombre(busqueda_nombre)
    if resultado["ok"]:
        juegos = [resultado["resultado"]]
    else:
        st.error(f"❌ {resultado['error']}")
        juegos = []
# Filtrar por Compañía
elif busqueda_compania:
    juegos = [j for j in juegos if busqueda_compania.lower() in j["compania"].lower()]
    if not juegos:
        st.info("No se encontraron videojuegos para esa compañía.")

if juegos:
    # Encabezados de la tabla
    cols = st.columns([1, 1, 2, 1, 1, 2, 2, 1])  # Ajusta proporciones a tu gusto
    headers = ["ID", "Portada", "Nombre", "Precio", "Stock", "Compañía", "Fecha"]

    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    # Filas de la tabla
    # Filas de la tabla
    for j in juegos:
        cols = st.columns(
            [1, 1, 2, 1, 1, 2, 2, 1]
        )  # 🟩 agregamos una columna más (botón eliminar)

        # Portada
        with cols[1]:
            ruta_base = Path(__file__).resolve().parent
            ruta_imagen = ruta_base / j.get("portada", "")
            if ruta_imagen.exists():
                st.image(str(ruta_imagen), width=60)
            else:
                st.write("📷")

        # Otras columnas
        cols[0].write(j["id"])
        cols[2].write(j["nombre"])
        cols[3].write(f"${j['precio']}")
        cols[4].write(j["cantidad"])
        cols[5].write(j["compania"])
        cols[6].write(j["fecha_publicacion"])

        # 🟩 Nuevo: botón eliminar
        with cols[7]:
            # El botón de la papelera solo establece la ID a confirmar
            if st.button("🗑️", key=f"del_{j['id']}"):
                st.session_state["confirmar_eliminacion"] = j["id"]
                # No se necesita rerun aquí, ya que el estado se actualiza.
else:
    st.info("No hay videojuegos registrados todavía.")
# ----------------------------------------------------------------------
# 2. Lógica y UI del Cuadro de Confirmación (Fuera del bucle)
# ----------------------------------------------------------------------

if "confirmar_eliminacion" in st.session_state:
    juego_id = st.session_state["confirmar_eliminacion"]
    juego = next((x for x in juegos if x["id"] == juego_id), None)

    if juego:
        st.warning(
            f"⚠️ ¿Seguro que deseas eliminar '{juego['nombre']}' permanentemente?"
        )

        col_c1, col_c2 = st.columns(2)

        # Bandera para saber si se ha realizado una acción (eliminar o cancelar)
        accion_realizada = False
        mensaje_accion = None

        with col_c1:
            if st.button("✅ Sí, eliminar", key=f"confirmar_{juego_id}"):
                resultado = servicio.eliminar_juego(juego_id)
                if resultado["ok"]:
                    mensaje_accion = ("success", resultado["mensaje"])
                else:
                    mensaje_accion = ("error", resultado["error"])
                accion_realizada = True

        with col_c2:
            if st.button("❌ Cancelar", key=f"cancelar_{juego_id}"):
                mensaje_accion = ("info", "Eliminación cancelada.")
                accion_realizada = True

        # Manejar el resultado de la acción después de que los botones hayan sido procesados
        if accion_realizada:
            # Mostrar el mensaje
            tipo, mensaje = mensaje_accion
            if tipo == "success":
                st.success(mensaje)
            elif tipo == "error":
                st.error(mensaje)
            elif tipo == "info":
                st.info(mensaje)

            # Limpiar el estado y forzar el re-renderizado SÓLO después de la acción
            del st.session_state["confirmar_eliminacion"]
            st.rerun()


st.markdown("---")  # separador visual
st.subheader("📊 Estadísticas del sistema")

# --- Estadísticas de la tabla hash ---
estadisticas_hash = servicio.obtener_estadisticas_indice()
if estadisticas_hash["ok"]:
    stats = estadisticas_hash["estadisticas"]
    st.markdown("### 🧩 Estadísticas de la tabla hash")
    st.write(f"- **Tamaño de la tabla:** {stats.get('tamano', 'N/A')}")
    st.write(f"- **Elementos almacenados:** {stats.get('total_elementos', 'N/A')}")
    st.write(f"- **Colisiones:** {stats.get('colisiones', 'N/A')}")
    st.write(f"- **Factor de carga:** {stats.get('factor_carga', 'N/A')}")
    st.write(f"- **Longitud máxima de lista:** {stats.get('longitud_maxima', 'N/A')}")
    st.write(
        f"- **Longitud promedio de lista:** {stats.get('longitud_promedio', 'N/A')}"
    )
    st.write(f"- **Posiciones ocupadas:** {stats.get('posiciones_ocupadas', 'N/A')}")
else:
    st.error(estadisticas_hash["error"])

# --- Estado general del inventario ---
estado = servicio.obtener_estado_inventario()
if estado["ok"]:
    st.markdown("### 💾 Estado del inventario")
    st.write(f"- **Total de juegos:** {estado['total_juegos']}")
    st.write(f"- **Ruta del archivo:** `{estado['ruta_archivo']}`")
    st.write(f"- **Última actualización:** {estado['ultima_actualizacion']}")
else:
    st.error(estado["error"])
