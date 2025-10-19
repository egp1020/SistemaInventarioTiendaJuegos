from datetime import date
from pathlib import Path

import streamlit as st

from src import repositorio, servicio
from src.servicio_imagenes import servicio_imagenes

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
    cols = st.columns([1, 1, 2, 1, 1, 2, 2])  # Ajusta proporciones a tu gusto
    headers = ["ID", "Portada", "Nombre", "Precio", "Stock", "Compañía", "Fecha"]

    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    # Filas de la tabla
    for j in juegos:
        cols = st.columns([1, 1, 2, 1, 1, 2, 2])

        # Portada
        with cols[1]:
            ruta_base = Path(__file__).parent.parent
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
else:
    st.info("No hay videojuegos registrados todavía.")
