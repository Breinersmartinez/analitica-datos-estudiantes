"""
Clase 10 - Reto: la plantilla del tablero de su equipo.

Se levanta desde una terminal parada en esta carpeta:

    streamlit run streamlit_app_starter.py

Tal como esta, levanta con el dataset de calidad del aire del demo. El trabajo de
su equipo es cambiarlo por el suyo, de arriba hacia abajo: primero el bloque 1, que
ya pone algo en pantalla, y solo despues los demas.

El orden de trabajo, los casos especiales y los errores frecuentes estan en reto.md.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# 1. LO MINIMO PARA VER ALGO EN PANTALLA
#    Cambie estas tres lineas, guarde, y ya deberia tener una pagina con titulo.
# ---------------------------------------------------------------------------

# TODO: apunte a su propio CSV.
# Si su archivo esta en la carpeta de datos del curso, deje el patron de abajo y
# cambie solo el nombre. Si esta en otra parte, reemplace la linea entera por la
# ruta a su archivo: relativa a la carpeta donde esta ESTE archivo, o absoluta.
RUTA_DATOS = Path(__file__).resolve().parents[1] / "datos" / "calidad_aire_risaralda.csv"

# TODO: el titulo de la pagina y una linea que diga que datos son y de donde salieron.
TITULO_APP = "Calidad del aire en Risaralda"
DESCRIPCION = "Descripcion pendiente: que datos son, de que periodo y de que fuente."

st.set_page_config(page_title=TITULO_APP, layout="wide")


@st.cache_data
def leer_crudo() -> pd.DataFrame:
    """Lee el CSV tal como viene. @st.cache_data hace que se lea una sola vez.

    Sin ese decorador el archivo se releeria en cada movimiento de un control,
    porque Streamlit vuelve a ejecutar este archivo completo cada vez.
    """
    return pd.read_csv(RUTA_DATOS)


crudo = leer_crudo()

st.title(TITULO_APP)
st.write(DESCRIPCION)
st.caption(f"{len(crudo):,} filas y {crudo.shape[1]} columnas leidas de {RUTA_DATOS.name}")

# Hasta aqui la app ya levanta y ya se ve algo. Lo que sigue es el tablero.


# ---------------------------------------------------------------------------
# 2. SUS COLUMNAS
#    Nombres cortos, en minuscula, sin tildes ni espacios. La clave del
#    diccionario es el nombre exacto que trae el archivo; el valor es como lo va
#    a usar usted en todo el resto del archivo.
# ---------------------------------------------------------------------------

RENOMBRES = {
    "Municipio": "categoria",
    "Fecha": "fecha",
    "Diametro aerodinamico": "grupo",
    "Medicion": "valor",
}

# TODO: los nombres (ya renombrados) de las cuatro columnas que mueven el tablero.
COLUMNA_CATEGORIA = "categoria"   # el filtro categorico principal
COLUMNA_GRUPO = "grupo"           # el segundo filtro categorico, distinto del primero
COLUMNA_VALOR = "valor"           # la medida numerica que se resume y se grafica

# El tercer filtro es de rango. Hay dos caminos y solo hay que elegir uno:
#
#   USA_FECHA = True   -> el rango es de fechas. Necesita COLUMNA_FECHA y FORMATO_FECHA.
#   USA_FECHA = False  -> el rango es numerico. Necesita COLUMNA_RANGO.
#
# Es lo unico que hay que cambiar para el caso "mi dataset no tiene fecha": el
# resto del archivo ya tiene resueltos los dos caminos.
USA_FECHA = True

COLUMNA_FECHA = "fecha"                        # solo se usa si USA_FECHA es True
FORMATO_FECHA = "%m/%d/%Y %I:%M:%S %p"         # TODO: el formato con el que viene su fecha

COLUMNA_RANGO = "anio"    # solo se usa si USA_FECHA es False. Una columna numerica
                          # ORDENADA: anio, mes, edad, estrato. Es la que va a mover
                          # el deslizador y la que va en el eje x del primer grafico.

# TODO: lo que va a leer el usuario en los filtros y en los ejes.
ETIQUETA_CATEGORIA = "Municipio"
ETIQUETA_GRUPO = "Tipo de particula"
ETIQUETA_RANGO = "Rango de anios"
UNIDAD_VALOR = "ug/m3"

# TODO: si su columna numerica tiene valores imposibles, ponga el tope. Si no aplica, None.
LIMITE_VALOR = 500


# Guarda: si alguna de las columnas declaradas arriba no existe, la app lo dice en
# la pagina en vez de reventar con un error que no se entiende.
COLUMNAS_NECESARIAS = [COLUMNA_CATEGORIA, COLUMNA_GRUPO, COLUMNA_VALOR]
COLUMNAS_NECESARIAS.append(COLUMNA_FECHA if USA_FECHA else COLUMNA_RANGO)

nombres_renombrados = [RENOMBRES.get(columna, columna) for columna in crudo.columns]
faltantes = [columna for columna in COLUMNAS_NECESARIAS if columna not in nombres_renombrados]

if faltantes:
    st.error(
        f"El bloque 2 de este archivo declara columnas que el CSV no tiene: {faltantes}.\n\n"
        f"Columnas disponibles despues del rename: {sorted(set(nombres_renombrados))}.\n\n"
        "Revise dos cosas, en este orden: que RENOMBRES tenga a la izquierda el nombre EXACTO "
        "que trae el archivo (con sus tildes, espacios y mayusculas), y que COLUMNA_CATEGORIA, "
        "COLUMNA_GRUPO, COLUMNA_VALOR y la columna del rango usen los nombres nuevos."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 3. CARGA Y LIMPIEZA
# ---------------------------------------------------------------------------


@st.cache_data
def preparar_datos() -> pd.DataFrame:
    """Renombra, convierte tipos y descarta lo que no se puede graficar."""
    df = leer_crudo().rename(columns=RENOMBRES)

    df[COLUMNA_VALOR] = pd.to_numeric(df[COLUMNA_VALOR], errors="coerce")

    for columna in [COLUMNA_CATEGORIA, COLUMNA_GRUPO]:
        df[columna] = df[columna].astype(str).str.strip()

    if USA_FECHA:
        df[COLUMNA_FECHA] = pd.to_datetime(
            df[COLUMNA_FECHA], format=FORMATO_FECHA, errors="coerce"
        )
        columna_orden = COLUMNA_FECHA
    else:
        df[COLUMNA_RANGO] = pd.to_numeric(df[COLUMNA_RANGO], errors="coerce")
        columna_orden = COLUMNA_RANGO

    df = df.dropna(subset=[columna_orden, COLUMNA_VALOR])

    if LIMITE_VALOR is not None:
        df = df[(df[COLUMNA_VALOR] > 0) & (df[COLUMNA_VALOR] <= LIMITE_VALOR)]

    return df.sort_values(columna_orden).reset_index(drop=True)


df = preparar_datos()

if df.empty:
    st.error(
        "Despues de convertir tipos y limpiar no quedo ninguna fila. Lo mas probable es "
        "que FORMATO_FECHA no describa el formato real de su columna de fecha, o que "
        "LIMITE_VALOR este dejando todo por fuera."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 4. FILTROS (minimo 3: al menos uno categorico y uno de rango)
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Filtros")

    opciones_categoria = sorted(df[COLUMNA_CATEGORIA].unique())
    opciones_grupo = sorted(df[COLUMNA_GRUPO].unique())

    categorias_elegidas = st.multiselect(
        ETIQUETA_CATEGORIA,
        options=opciones_categoria,
        default=opciones_categoria,
    )

    grupos_elegidos = st.multiselect(
        ETIQUETA_GRUPO,
        options=opciones_grupo,
        default=opciones_grupo,
    )

    if USA_FECHA:
        minimo = df[COLUMNA_FECHA].min().date()
        maximo = df[COLUMNA_FECHA].max().date()
    else:
        minimo = int(df[COLUMNA_RANGO].min())
        maximo = int(df[COLUMNA_RANGO].max())

    rango_elegido = st.slider(
        ETIQUETA_RANGO,
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
    )

    mostrar_tabla = st.checkbox("Mostrar los datos filtrados", value=False)


# Guardas: sin esto la app revienta cuando el usuario deselecciona todo.
if not categorias_elegidas:
    st.warning(f"Seleccione al menos un valor en {ETIQUETA_CATEGORIA}.")
    st.stop()

if not grupos_elegidos:
    st.warning(f"Seleccione al menos un valor en {ETIQUETA_GRUPO}.")
    st.stop()


# ---------------------------------------------------------------------------
# 5. FILTRADO DEL DATAFRAME
# ---------------------------------------------------------------------------

if USA_FECHA:
    en_el_rango = df[COLUMNA_FECHA].dt.date.between(rango_elegido[0], rango_elegido[1])
else:
    en_el_rango = df[COLUMNA_RANGO].between(rango_elegido[0], rango_elegido[1])

df_filtrado = df[
    df[COLUMNA_CATEGORIA].isin(categorias_elegidas)
    & df[COLUMNA_GRUPO].isin(grupos_elegidos)
    & en_el_rango
].copy()

if df_filtrado.empty:
    st.error("Ninguna fila cumple los filtros seleccionados.")
    st.stop()


# ---------------------------------------------------------------------------
# 6. KPIs (minimo 3, y los tres tienen que cambiar al mover los filtros)
# ---------------------------------------------------------------------------

col_1, col_2, col_3 = st.columns(3)

promedio = df_filtrado[COLUMNA_VALOR].mean()
maximo_valor = df_filtrado[COLUMNA_VALOR].max()

with col_1:
    st.metric(f"Promedio ({UNIDAD_VALOR})", f"{promedio:,.1f}")

with col_2:
    st.metric(f"Maximo ({UNIDAD_VALOR})", f"{maximo_valor:,.1f}")

with col_3:
    # TU CODIGO AQUI
    # Defina el tercer KPI. Que numero cambiaria una decision?
    # Ideas: un conteo de filas, un porcentaje sobre un umbral, cuantas
    # categorias distintas hay en la vista, la diferencia entre dos grupos.
    # Reemplace las dos lineas de abajo.
    tercer_kpi = 0
    st.metric("Tercer KPI (cambiar)", f"{tercer_kpi:,}")


# ---------------------------------------------------------------------------
# 7. GRAFICOS (minimo 3, y cada uno responde una pregunta distinta)
# ---------------------------------------------------------------------------

col_izq, col_der = st.columns(2)

with col_izq:
    # Grafico 1: como evoluciona la medida a lo largo del eje ordenado.
    # Recuerde: px NO agrega por usted. El groupby va antes, siempre.
    if USA_FECHA:
        eje_x = COLUMNA_FECHA
        serie = df_filtrado.groupby(
            [pd.Grouper(key=COLUMNA_FECHA, freq="ME"), COLUMNA_GRUPO], as_index=False
        )[COLUMNA_VALOR].mean()
    else:
        eje_x = COLUMNA_RANGO
        serie = df_filtrado.groupby(
            [COLUMNA_RANGO, COLUMNA_GRUPO], as_index=False
        )[COLUMNA_VALOR].mean()

    serie = serie.sort_values(eje_x)

    fig_linea = px.line(
        serie,
        x=eje_x,
        y=COLUMNA_VALOR,
        color=COLUMNA_GRUPO,
        # TODO: cambie este titulo por el mensaje que quiere que el usuario concluya.
        title="Titulo descriptivo (cambielo por un mensaje)",
    )
    fig_linea.update_layout(
        xaxis_title="", yaxis_title=f"Promedio ({UNIDAD_VALOR})", legend_title=""
    )
    st.plotly_chart(fig_linea, width="stretch")

with col_der:
    # Grafico 2: comparacion entre categorias.
    resumen = (
        df_filtrado.groupby(COLUMNA_CATEGORIA, as_index=False)[COLUMNA_VALOR]
        .mean()
        .sort_values(COLUMNA_VALOR, ascending=False)
    )

    fig_barras = px.bar(
        resumen,
        x=COLUMNA_CATEGORIA,
        y=COLUMNA_VALOR,
        # TODO: cambie este titulo por un mensaje.
        title="Titulo descriptivo (cambielo por un mensaje)",
    )
    fig_barras.update_layout(
        xaxis_title="", yaxis_title=f"Promedio ({UNIDAD_VALOR})", showlegend=False
    )
    st.plotly_chart(fig_barras, width="stretch")


# TU CODIGO AQUI
# Grafico 3. Sugerencia: px.box para mostrar la variabilidad que el promedio esconde.
# Necesita: crear la figura, ajustar el layout y renderizarla con
# st.plotly_chart(fig, width="stretch").


# ---------------------------------------------------------------------------
# 8. EL INSIGHT ESCRITO
# ---------------------------------------------------------------------------

# TU CODIGO AQUI
# Una frase, con cifra, calculada a partir de df_filtrado, que siga siendo cierta
# sin importar como el usuario mueva los filtros. Use st.info(...).
# Este es el puente con la clase 9: el dashboard no termina en el grafico,
# termina en una conclusion.


if mostrar_tabla:
    st.subheader("Datos filtrados")
    st.dataframe(df_filtrado, width="stretch")
