"""Dashboard exploratorio del Momento 2 sobre dataset/train.csv.

Se ejecuta desde la raíz del repositorio con:

    streamlit run Momento1/dashboard.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

RUTA_DATOS = Path(__file__).resolve().parents[1] / "dataset" / "train.csv"

TITULO_APP = "Ventas por producto y tienda"
DESCRIPCION = (
    "8.523 registros de ventas de productos en 10 tiendas. El dataset no trae fecha "
    "de venta: el eje temporal disponible es el año de apertura de cada tienda."
)

RENOMBRES = {
    "Item_Identifier": "id_producto",
    "Item_Weight": "peso_producto",
    "Item_Fat_Content": "contenido_grasa",
    "Item_Visibility": "visibilidad_producto",
    "Item_Type": "tipo_producto",
    "Item_MRP": "precio_maximo",
    "Outlet_Identifier": "id_tienda",
    "Outlet_Establishment_Year": "anio_apertura",
    "Outlet_Size": "tamano_tienda",
    "Outlet_Location_Type": "tipo_ubicacion",
    "Outlet_Type": "tipo_tienda",
    "Item_Outlet_Sales": "ventas_totales",
}

MAPEO_GRASA = {
    "Low Fat": "Bajo en grasa",
    "low fat": "Bajo en grasa",
    "LF": "Bajo en grasa",
    "Regular": "Regular",
    "reg": "Regular",
}

MAPEO_PRODUCTO = {
    "Fruits and Vegetables": "Frutas y verduras",
    "Snack Foods": "Snacks",
    "Household": "Hogar",
    "Frozen Foods": "Congelados",
    "Dairy": "Lácteos",
    "Canned": "Enlatados",
    "Baking Goods": "Insumos de repostería",
    "Health and Hygiene": "Salud e higiene",
    "Soft Drinks": "Bebidas sin alcohol",
    "Meat": "Carnes",
    "Breads": "Panes",
    "Hard Drinks": "Licores",
    "Others": "Otros",
    "Starchy Foods": "Alimentos con almidón",
    "Breakfast": "Desayuno",
    "Seafood": "Mariscos",
}

MAPEO_TAMANO = {"Small": "Pequeña", "Medium": "Mediana", "High": "Grande"}
MAPEO_UBICACION = {"Tier 1": "Nivel 1", "Tier 2": "Nivel 2", "Tier 3": "Nivel 3"}
MAPEO_TIENDA = {
    "Grocery Store": "Tienda de abarrotes",
    "Supermarket Type1": "Supermercado tipo 1",
    "Supermarket Type2": "Supermercado tipo 2",
    "Supermarket Type3": "Supermercado tipo 3",
}

TAMANO_POR_TIENDA = {"OUT010": "Pequeña", "OUT017": "Pequeña", "OUT045": "Pequeña"}

COLORES_TIENDA = {
    "Supermercado tipo 1": "#1f77b4",
    "Supermercado tipo 2": "#ff7f0e",
    "Supermercado tipo 3": "#2ca02c",
    "Tienda de abarrotes": "#d62728",
}


st.set_page_config(page_title=TITULO_APP, layout="wide")


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    df = pd.read_csv(RUTA_DATOS).rename(columns=RENOMBRES)

    df["contenido_grasa"] = df["contenido_grasa"].replace(MAPEO_GRASA)
    df["tipo_producto"] = df["tipo_producto"].replace(MAPEO_PRODUCTO)
    df["tamano_tienda"] = df["tamano_tienda"].replace(MAPEO_TAMANO)
    df["tipo_ubicacion"] = df["tipo_ubicacion"].replace(MAPEO_UBICACION)
    df["tipo_tienda"] = df["tipo_tienda"].replace(MAPEO_TIENDA)

    for columna in ["id_producto", "id_tienda", "contenido_grasa", "tipo_producto",
                    "tamano_tienda", "tipo_ubicacion", "tipo_tienda"]:
        df[columna] = df[columna].astype("string").str.strip()

    df["tamano_tienda"] = df["tamano_tienda"].fillna(
        df["id_tienda"].map(TAMANO_POR_TIENDA)
    )
    df["tamano_tienda"] = df["tamano_tienda"].fillna("Desconocido")

    df["visibilidad_producto"] = pd.to_numeric(
        df["visibilidad_producto"], errors="coerce"
    ).replace(0, np.nan)
    df["visibilidad_producto"] = df["visibilidad_producto"].fillna(
        df.groupby("id_producto")["visibilidad_producto"].transform("median")
    )
    df["visibilidad_producto"] = df["visibilidad_producto"].fillna(
        df.groupby("tipo_producto")["visibilidad_producto"].transform("median")
    )
    df["visibilidad_producto"] = df["visibilidad_producto"].fillna(
        df["visibilidad_producto"].median()
    )

    for columna in ["precio_maximo", "ventas_totales", "anio_apertura"]:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

    columnas_clave = [
        "id_producto",
        "id_tienda",
        "tipo_tienda",
        "tipo_producto",
        "precio_maximo",
        "anio_apertura",
        "ventas_totales",
    ]
    df = df.dropna(subset=columnas_clave)
    df = df.drop(columns=["peso_producto"])
    df["anio_apertura"] = df["anio_apertura"].astype(int)

    return df.sort_values(["anio_apertura", "id_tienda"]).reset_index(drop=True)


try:
    df = cargar_datos()
except FileNotFoundError:
    st.error(f"No se encontró el archivo de datos en {RUTA_DATOS}.")
    st.stop()
except KeyError as error:
    st.error(
        f"El CSV no tiene la columna esperada {error}. Revise que sea el train.csv "
        "del proyecto."
    )
    st.stop()

if df.empty:
    st.error("El CSV quedó sin filas después de la limpieza. Revise la ruta y el archivo.")
    st.stop()


st.title(TITULO_APP)
st.write(DESCRIPCION)
st.caption(
    f"{len(df):,} filas y {df.shape[1]} columnas útiles. Fuente: "
    f"dataset/{RUTA_DATOS.name}."
)


with st.sidebar:
    st.header("Filtros")

    tipos_tienda = sorted(df["tipo_tienda"].unique())
    tipos_producto = sorted(df["tipo_producto"].unique())

    tipos_elegidos = st.multiselect(
        "Tipo de tienda",
        options=tipos_tienda,
        default=tipos_tienda,
    )

    productos_elegidos = st.multiselect(
        "Tipo de producto",
        options=tipos_producto,
        default=tipos_producto,
    )

    precio_min = float(np.floor(df["precio_maximo"].min()))
    precio_max = float(np.ceil(df["precio_maximo"].max()))

    rango_precio = st.slider(
        "Rango de precio (unid. monetarias)",
        min_value=precio_min,
        max_value=precio_max,
        value=(precio_min, precio_max),
        step=1.0,
        format="%.0f",
    )

    st.caption(
        "Los tres filtros describen dimensiones distintas: tipo de tienda, familia "
        "de producto y nivel de precio. Ninguno repite la partición de otro."
    )

    mostrar_tabla = st.checkbox("Mostrar los datos filtrados", value=False)


if not tipos_elegidos:
    st.warning("Seleccione al menos un tipo de tienda.")
    st.stop()

if not productos_elegidos:
    st.warning("Seleccione al menos un tipo de producto.")
    st.stop()


df_filtrado = df[
    df["tipo_tienda"].isin(tipos_elegidos)
    & df["tipo_producto"].isin(productos_elegidos)
    & df["precio_maximo"].between(rango_precio[0], rango_precio[1])
].copy()

if df_filtrado.empty:
    st.error("Ninguna fila cumple los filtros seleccionados. Amplíe el rango de precio.")
    st.stop()


ventas_totales = df_filtrado["ventas_totales"].sum()
venta_mediana = df_filtrado["ventas_totales"].median()
venta_media = df_filtrado["ventas_totales"].mean()
ventas_por_tipo = df_filtrado.groupby("tipo_tienda")["ventas_totales"].sum()
tipo_lider = ventas_por_tipo.idxmax()
participacion_lider = ventas_por_tipo.max() / ventas_totales * 100

mediana_global = df["ventas_totales"].median()
media_global = df["ventas_totales"].mean()
ventas_global = df["ventas_totales"].sum()

col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)

with col_kpi_1:
    st.metric(
        "Ventas totales (unid. monetarias)",
        f"{ventas_totales:,.0f}",
        border=True,
    )
    st.caption(f"Dataset completo: {ventas_global:,.0f}.")

with col_kpi_2:
    st.metric(
        "Venta mediana (unid. monetarias)",
        f"{venta_mediana:,.0f}",
        delta=f"{venta_mediana - mediana_global:+,.0f} vs. global",
        delta_color="off",
        border=True,
    )
    st.caption(f"Mediana global: {mediana_global:,.0f}.")

with col_kpi_3:
    st.metric(
        "Venta media (unid. monetarias)",
        f"{venta_media:,.0f}",
        delta=f"{venta_media - media_global:+,.0f} vs. global",
        delta_color="off",
        border=True,
    )
    st.caption(f"Media global: {media_global:,.0f}.")

st.caption(f"{len(df_filtrado):,} registros en la vista de {len(df):,}.")


serie_anio = (
    df_filtrado.groupby("anio_apertura")["ventas_totales"]
    .agg(mediana="median", registros="size")
    .reset_index()
    .sort_values("anio_apertura")
)

if len(serie_anio) == 1:
    fila_anio = serie_anio.iloc[0]
    titulo_linea = (
        f"Cohorte {int(fila_anio['anio_apertura'])}: mediana de "
        f"{fila_anio['mediana']:,.0f}"
    )
else:
    anio_bajo = serie_anio.loc[serie_anio["mediana"].idxmin()]
    anio_alto = serie_anio.loc[serie_anio["mediana"].idxmax()]
    titulo_linea = (
        f"La antigüedad no garantiza ventas: {int(anio_bajo['anio_apertura'])} = "
        f"{anio_bajo['mediana']:,.0f} y {int(anio_alto['anio_apertura'])} = "
        f"{anio_alto['mediana']:,.0f}"
    )

fig_linea = px.line(
    serie_anio,
    x="anio_apertura",
    y="mediana",
    markers=True,
    hover_data={"registros": True, "mediana": ":,.0f"},
    title=titulo_linea,
)
fig_linea.update_layout(
    xaxis_title="Año de apertura de la tienda",
    yaxis_title="Venta mediana (unid. monetarias)",
)
fig_linea.update_xaxes(dtick=1)


ranking = (
    df_filtrado.groupby(["id_tienda", "tipo_tienda"])["ventas_totales"]
    .agg(mediana="median")
    .reset_index()
    .sort_values("mediana")
)

if len(ranking) == 1:
    fila_ranking = ranking.iloc[0]
    titulo_barras = (
        f"{fila_ranking['id_tienda']}: única tienda, mediana "
        f"{fila_ranking['mediana']:,.0f}"
    )
else:
    tienda_alta = ranking.iloc[-1]
    tienda_baja = ranking.iloc[0]
    razon = (
        tienda_alta["mediana"] / tienda_baja["mediana"]
        if tienda_baja["mediana"] > 0
        else np.nan
    )
    if pd.notna(razon) and razon >= 1.05:
        titulo_barras = (
            f"{tienda_alta['id_tienda']} tiene una mediana {razon:.1f}× mayor que "
            f"{tienda_baja['id_tienda']}"
        )
    else:
        titulo_barras = (
            f"{tienda_alta['id_tienda']} y {tienda_baja['id_tienda']} empatan en "
            f"{tienda_alta['mediana']:,.0f}"
        )

fig_barras = px.bar(
    ranking,
    x="mediana",
    y="id_tienda",
    color="tipo_tienda",
    orientation="h",
    color_discrete_map=COLORES_TIENDA,
    category_orders={"id_tienda": ranking["id_tienda"].tolist()},
    text_auto=".0f",
    title=titulo_barras,
)
fig_barras.update_layout(
    xaxis_title="Venta mediana (unid. monetarias)",
    yaxis_title="",
    legend_title="",
)
fig_barras.update_traces(textposition="outside")


resumen_tipo = (
    df_filtrado.groupby("tipo_tienda")["ventas_totales"]
    .agg(
        mediana="median",
        q1=lambda s: s.quantile(0.25),
        q3=lambda s: s.quantile(0.75),
    )
    .sort_values("mediana", ascending=False)
)

if len(resumen_tipo) == 1:
    fila_tipo = resumen_tipo.iloc[0]
    titulo_caja = (
        f"{resumen_tipo.index[0]}: mediana {fila_tipo['mediana']:,.0f} y rango "
        f"intercuartílico {fila_tipo['q1']:,.0f}-{fila_tipo['q3']:,.0f}"
    )
else:
    tipo_alto = resumen_tipo.iloc[0]
    tipo_bajo = resumen_tipo.iloc[-1]
    titulo_caja = (
        f"{resumen_tipo.index[0]} lidera la mediana ({tipo_alto['mediana']:,.0f}); "
        f"{resumen_tipo.index[-1]} queda en {tipo_bajo['mediana']:,.0f}"
    )

fig_caja = px.box(
    df_filtrado,
    x="tipo_tienda",
    y="ventas_totales",
    color="tipo_tienda",
    color_discrete_map=COLORES_TIENDA,
    category_orders={"tipo_tienda": list(COLORES_TIENDA)},
    points="outliers",
    title=titulo_caja,
)
fig_caja.update_layout(
    xaxis_title="",
    yaxis_title="Ventas por producto-tienda (unid. monetarias)",
    legend_title="",
    showlegend=False,
)

col_grafico_1, col_grafico_2 = st.columns(2)

with col_grafico_1:
    st.plotly_chart(fig_linea, width="stretch")

with col_grafico_2:
    st.plotly_chart(fig_barras, width="stretch")

st.plotly_chart(fig_caja, width="stretch")


ventas_por_producto = df_filtrado.groupby("tipo_producto")["ventas_totales"].sum()
producto_lider = ventas_por_producto.idxmax()
participacion_producto = ventas_por_producto.max() / ventas_totales * 100

tipos_en_vista = df_filtrado["tipo_tienda"].nunique()
productos_en_vista = df_filtrado["tipo_producto"].nunique()

if tipos_en_vista > 1 and productos_en_vista > 1:
    if participacion_lider >= participacion_producto:
        sintesis = (
            f"El tipo de tienda pesa más que la familia de producto: {tipo_lider} "
            f"concentra el {participacion_lider:.1f}% de las ventas, mientras "
            f"{producto_lider} aporta el {participacion_producto:.1f}%."
        )
    else:
        sintesis = (
            f"La familia de producto pesa más que el tipo de tienda: {producto_lider} "
            f"concentra el {participacion_producto:.1f}% de las ventas, mientras "
            f"{tipo_lider} aporta el {participacion_lider:.1f}%."
        )
elif tipos_en_vista > 1:
    sintesis = (
        f"Dentro de {producto_lider}, el tipo de tienda sí separa las ventas: "
        f"{tipo_lider} concentra el {participacion_lider:.1f}% del total."
    )
elif productos_en_vista > 1:
    sintesis = (
        f"Dentro de {tipo_lider}, la familia de producto separa las ventas: "
        f"{producto_lider} concentra el {participacion_producto:.1f}% del total."
    )
else:
    sintesis = (
        f"La vista aísla una sola combinación: {tipo_lider} + {producto_lider}. "
        "La comparación entre dimensiones ya no aplica."
    )

tienda_lider = ranking.iloc[-1]
if len(ranking) > 1:
    sintesis += (
        f" {tienda_lider['id_tienda']} lidera la mediana con "
        f"{tienda_lider['mediana']:,.0f} unid. monetarias."
    )
else:
    sintesis += (
        f" La tienda {tienda_lider['id_tienda']} tiene una mediana de "
        f"{tienda_lider['mediana']:,.0f} unid. monetarias."
    )

if (
    len(df_filtrado) >= 3
    and df_filtrado["precio_maximo"].nunique() > 1
    and df_filtrado["ventas_totales"].nunique() > 1
):
    correlacion_precio = df_filtrado["precio_maximo"].corr(
        df_filtrado["ventas_totales"]
    )
    if pd.notna(correlacion_precio):
        sintesis += (
            f" El precio se asocia a las ventas con r = {correlacion_precio:.2f}."
        )

st.info(f"**Hallazgo dinámico:** {sintesis}")


with st.expander("Decisiones de limpieza y alcance"):
    st.markdown(
        "- Se eliminó `peso_producto`: tiene 17% de nulos y su correlación con las "
        "ventas es prácticamente cero.\n"
        "- Se unificaron las cinco variantes de `Item_Fat_Content` en dos categorías.\n"
        "- Los nulos de tamaño de tienda se completaron por tienda. Para OUT010 el "
        "respaldo es fuerte; para OUT017 y OUT045 es una hipótesis basada en su tienda "
        "gemela.\n"
        "- Los ceros de visibilidad se trataron como dato no registrado y se "
        "rellenaron con la mediana del mismo producto; si no había, con la mediana de "
        "su tipo de producto y, en último caso, con la mediana global.\n"
        "- El dataset no documenta la moneda. Por eso todas las cifras monetarias se "
        "rotulan como unidades monetarias, sin atribuirles una divisa.\n"
        "- Los outliers de ventas se conservan: son ventas reales de las tiendas que "
        "más venden.\n"
        "- No hay fecha de venta. El eje temporal del primer gráfico es el año de "
        "apertura de la tienda, no la fecha de la transacción.\n"
        "- Las correlaciones que muestra la franja son asociaciones, no relaciones "
        "causales."
    )


if mostrar_tabla:
    st.subheader("Datos filtrados")
    columnas_tabla = [
        "id_producto",
        "tipo_producto",
        "contenido_grasa",
        "precio_maximo",
        "visibilidad_producto",
        "id_tienda",
        "tipo_tienda",
        "tamano_tienda",
        "tipo_ubicacion",
        "anio_apertura",
        "ventas_totales",
    ]
    st.dataframe(
        df_filtrado[columnas_tabla].sort_values("ventas_totales", ascending=False),
        width="stretch",
        hide_index=True,
    )
