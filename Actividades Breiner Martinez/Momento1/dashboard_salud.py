"""Dashboard exploratorio del Momento 2 sobre datos/indicadores_salud.csv.

Se ejecuta desde la raíz del repositorio con:

    streamlit run Momento1/dashboard_salud.py
"""

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

RUTA_DATOS = (
    Path(__file__).resolve().parents[1] / "datos" / "indicadores_salud.csv"
)

TITULO_APP = "Mortalidad materno-infantil en Colombia"
DESCRIPCION = (
    "497 registros de 32 municipios en 22 departamentos entre 2005 y 2020. "
    "Una fila es un municipio en un año. Fuente: Ministerio de Salud y Protección "
    "Social, datos.gov.co."
)

COLUMNAS_NUMERICAS = [
    "ano",
    "bajo_peso_nacer",
    "controles_prenatales",
    "fecundidad_adolescente",
    "mortalidad_fetal",
    "mortalidad_general",
    "mortalidad_infantil",
    "mortalidad_materna",
    "mortalidad_neonatal",
    "partos_cesarea",
    "partos_institucionales",
]

COLUMNAS_INDICADORES = [columna for columna in COLUMNAS_NUMERICAS if columna != "ano"]
COLUMNAS_PORCENTAJE = ["bajo_peso_nacer", "partos_cesarea", "partos_institucionales"]

def normalizar_departamento(valor):
    if pd.isna(valor):
        return valor
    texto = str(valor).strip().upper().replace("Ñ", "N")
    texto = "".join(
        caracter
        for caracter in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(caracter)
    )
    texto = re.sub(r"[^A-Z0-9 ]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def correlacion_segura(serie_x: pd.Series, serie_y: pd.Series) -> float:
    if len(serie_x) < 3 or serie_x.nunique() < 2 or serie_y.nunique() < 2:
        return np.nan
    return serie_x.corr(serie_y)


st.set_page_config(page_title=TITULO_APP, layout="wide")


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    df = pd.read_csv(RUTA_DATOS)

    df["departamento"] = df["departamento"].map(normalizar_departamento)
    df["departamento"] = df["departamento"].replace({"BOGOTA D C": "BOGOTA D.C."})
    df = df.dropna(subset=["departamento"])

    for columna in COLUMNAS_NUMERICAS:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

    df = df.drop_duplicates(
        subset=["departamento", "municipio", "ano"], keep="first"
    ).copy()

    for columna in COLUMNAS_INDICADORES:
        df[columna] = df[columna].fillna(df[columna].median())

    df["ano"] = df["ano"].astype(int)

    for columna in COLUMNAS_PORCENTAJE:
        df[columna] = df[columna].clip(0, 100)

    df = df.drop(columns=["cod_departamento", "cod_municipio"], errors="ignore")

    return df.sort_values(["ano", "departamento", "municipio"]).reset_index(
        drop=True
    )


try:
    df = cargar_datos()
except FileNotFoundError:
    st.error(f"No se encontró el archivo de datos en {RUTA_DATOS}.")
    st.stop()
except KeyError as error:
    st.error(
        f"El CSV no tiene la columna esperada {error}. Revise que sea el archivo "
        "indicadores_salud.csv del curso."
    )
    st.stop()

if df.empty:
    st.error("El CSV quedó sin filas después de la limpieza. Revise la ruta y el archivo.")
    st.stop()


st.title(TITULO_APP)
st.write(DESCRIPCION)
st.caption(
    f"{len(df):,} filas útiles, {df['departamento'].nunique()} departamentos, "
    f"{df['municipio'].nunique()} municipios y {df['ano'].min()}-{df['ano'].max()}."
)


with st.sidebar:
    st.header("Filtros")

    departamentos = sorted(df["departamento"].unique())
    departamentos_elegidos = st.multiselect(
        "Departamento",
        options=departamentos,
        default=departamentos,
    )

    ano_min = int(df["ano"].min())
    ano_max = int(df["ano"].max())
    rango_ano = st.slider(
        "Rango de años",
        min_value=ano_min,
        max_value=ano_max,
        value=(ano_min, ano_max),
        step=1,
    )

    fecundidad_min = float(np.floor(df["fecundidad_adolescente"].min()))
    fecundidad_max = float(np.ceil(df["fecundidad_adolescente"].max()))
    rango_fecundidad = st.slider(
        "Fecundidad adolescente (tasa por mil)",
        min_value=fecundidad_min,
        max_value=fecundidad_max,
        value=(fecundidad_min, fecundidad_max),
        step=1.0,
        format="%.0f",
    )

    st.caption(
        "Los tres filtros describen dimensiones distintas: territorio, tiempo y "
        "fecundidad adolescente. Ninguno repite la partición de otro."
    )

    mostrar_tabla = st.checkbox("Mostrar los datos filtrados", value=False)


if not departamentos_elegidos:
    st.warning("Seleccione al menos un departamento.")
    st.stop()


df_filtrado = df[
    df["departamento"].isin(departamentos_elegidos)
    & df["ano"].between(rango_ano[0], rango_ano[1])
    & df["fecundidad_adolescente"].between(
        rango_fecundidad[0], rango_fecundidad[1]
    )
].copy()

if df_filtrado.empty:
    st.error("Ninguna fila cumple los filtros seleccionados. Amplíe el rango de años o de fecundidad.")
    st.stop()


infantil_mediana = df_filtrado["mortalidad_infantil"].median()
materna_mediana = df_filtrado["mortalidad_materna"].median()
controles_promedio = df_filtrado["controles_prenatales"].mean()

infantil_global = df["mortalidad_infantil"].median()
materna_global = df["mortalidad_materna"].median()
controles_global = df["controles_prenatales"].mean()

col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)

with col_kpi_1:
    st.metric(
        "Mortalidad infantil mediana (por 1.000)",
        f"{infantil_mediana:,.1f}",
        delta=f"{infantil_mediana - infantil_global:+,.1f} vs. global",
        delta_color="off",
        border=True,
    )
    st.caption(f"Referencia global: {infantil_global:,.1f} por mil.")

with col_kpi_2:
    st.metric(
        "Mortalidad materna mediana (por 100.000)",
        f"{materna_mediana:,.1f}",
        delta=f"{materna_mediana - materna_global:+,.1f} vs. global",
        delta_color="off",
        border=True,
    )
    st.caption(f"Referencia global: {materna_global:,.1f} por 100.000.")

with col_kpi_3:
    st.metric(
        "Controles prenatales promedio (controles)",
        f"{controles_promedio:,.2f}",
        delta=f"{controles_promedio - controles_global:+.2f} vs. global",
        delta_color="off",
        border=True,
    )
    st.caption(f"Referencia global: {controles_global:,.2f} controles.")

st.caption(f"{len(df_filtrado):,} registros en la vista de {len(df):,}.")


serie_ano = (
    df_filtrado.groupby("ano")["mortalidad_infantil"]
    .agg(mediana="median", registros="size")
    .reset_index()
    .sort_values("ano")
)

if len(serie_ano) == 1:
    fila_ano = serie_ano.iloc[0]
    titulo_linea = (
        f"En {int(fila_ano['ano'])}, la mediana es {fila_ano['mediana']:,.1f} por mil"
    )
else:
    primer_ano = serie_ano.iloc[0]
    ultimo_ano = serie_ano.iloc[-1]
    if ultimo_ano["mediana"] < primer_ano["mediana"]:
        titulo_linea = (
            f"La mortalidad infantil bajó de {primer_ano['mediana']:,.1f} a "
            f"{ultimo_ano['mediana']:,.1f} por mil entre {int(primer_ano['ano'])} y "
            f"{int(ultimo_ano['ano'])}"
        )
    elif ultimo_ano["mediana"] > primer_ano["mediana"]:
        titulo_linea = (
            f"La mortalidad infantil subió de {primer_ano['mediana']:,.1f} a "
            f"{ultimo_ano['mediana']:,.1f} por mil entre {int(primer_ano['ano'])} y "
            f"{int(ultimo_ano['ano'])}"
        )
    else:
        titulo_linea = (
            f"La mortalidad infantil se mantuvo cerca de "
            f"{ultimo_ano['mediana']:,.1f} por mil entre "
            f"{int(primer_ano['ano'])} y {int(ultimo_ano['ano'])}"
        )

fig_linea = px.line(
    serie_ano,
    x="ano",
    y="mediana",
    markers=True,
    hover_data={"registros": True, "mediana": ":,.1f"},
    title=titulo_linea,
)
fig_linea.update_layout(
    xaxis_title="Año",
    yaxis_title="Mortalidad infantil mediana (por 1.000)",
)
fig_linea.update_xaxes(dtick=1)


resumen_departamento = (
    df_filtrado.groupby("departamento")["mortalidad_infantil"]
    .agg(mediana="median", registros="size")
    .reset_index()
    .sort_values("mediana", ascending=False)
)

departamento_lider = resumen_departamento.iloc[0]
departamento_ultimo = resumen_departamento.iloc[-1]

if len(resumen_departamento) == 1:
    titulo_barras = (
        f"{departamento_lider['departamento']}: mediana de "
        f"{departamento_lider['mediana']:,.1f} por mil"
    )
elif len(resumen_departamento) > 10:
    titulo_barras = (
        f"Los 10 departamentos con mayor mortalidad infantil: "
        f"{departamento_lider['departamento']} lidera con "
        f"{departamento_lider['mediana']:,.1f} por mil"
    )
else:
    titulo_barras = (
        f"{departamento_lider['departamento']} lidera con "
        f"{departamento_lider['mediana']:,.1f} por mil; "
        f"{departamento_ultimo['departamento']} queda en "
        f"{departamento_ultimo['mediana']:,.1f}"
    )

barras = resumen_departamento.head(10).sort_values("mediana")

fig_barras = px.bar(
    barras,
    x="mediana",
    y="departamento",
    orientation="h",
    text_auto=".1f",
    color_discrete_sequence=["#4c78a8"],
    category_orders={"departamento": barras["departamento"].tolist()},
    title=titulo_barras,
)
fig_barras.update_layout(
    xaxis_title="Mortalidad infantil mediana (por 1.000)",
    yaxis_title="",
    showlegend=False,
)
fig_barras.update_traces(textposition="outside", cliponaxis=False)


correlacion_controles = correlacion_segura(
    df_filtrado["controles_prenatales"], df_filtrado["mortalidad_infantil"]
)
correlacion_fecundidad = correlacion_segura(
    df_filtrado["fecundidad_adolescente"], df_filtrado["mortalidad_infantil"]
)

if pd.isna(correlacion_controles):
    titulo_dispersion = "No hay variación suficiente para calcular la relación"
elif correlacion_controles <= -0.2:
    titulo_dispersion = (
        f"Más controles prenatales, menor mortalidad infantil "
        f"(r = {correlacion_controles:.2f})"
    )
elif correlacion_controles >= 0.2:
    titulo_dispersion = (
        f"En esta vista, más controles no implican menor mortalidad "
        f"(r = {correlacion_controles:.2f})"
    )
else:
    titulo_dispersion = (
        f"La relación entre controles y mortalidad infantil es débil "
        f"(r = {correlacion_controles:.2f})"
    )

fig_dispersion = px.scatter(
    df_filtrado,
    x="controles_prenatales",
    y="mortalidad_infantil",
    color="fecundidad_adolescente",
    color_continuous_scale="Viridis",
    range_color=(
        df["fecundidad_adolescente"].min(),
        df["fecundidad_adolescente"].max(),
    ),
    opacity=0.75,
    hover_data={
        "departamento": True,
        "municipio": True,
        "ano": True,
        "fecundidad_adolescente": ":,.1f",
        "controles_prenatales": ":,.2f",
        "mortalidad_infantil": ":,.1f",
    },
    title=titulo_dispersion,
)
fig_dispersion.update_layout(
    xaxis_title="Controles prenatales promedio (controles)",
    yaxis_title="Mortalidad infantil (por 1.000)",
    coloraxis_colorbar_title="Fecundidad adolescente (por mil)",
)

if (
    len(df_filtrado) >= 3
    and df_filtrado["controles_prenatales"].nunique() > 1
    and pd.notna(correlacion_controles)
):
    coeficientes = np.polyfit(
        df_filtrado["controles_prenatales"],
        df_filtrado["mortalidad_infantil"],
        1,
    )
    eje_x = np.linspace(
        df_filtrado["controles_prenatales"].min(),
        df_filtrado["controles_prenatales"].max(),
        50,
    )
    fig_dispersion.add_scatter(
        x=eje_x,
        y=np.polyval(coeficientes, eje_x),
        mode="lines",
        name="Tendencia",
        line=dict(color="#222222", dash="dash", width=2),
        showlegend=False,
    )

fig_dispersion.update_traces(
    marker=dict(size=8, line=dict(width=0.5, color="white"))
)

col_grafico_1, col_grafico_2 = st.columns(2)

with col_grafico_1:
    st.plotly_chart(fig_linea, width="stretch")

with col_grafico_2:
    st.plotly_chart(fig_barras, width="stretch")

st.plotly_chart(fig_dispersion, width="stretch")


if len(serie_ano) == 1:
    sintesis_tendencia = (
        f"En {int(serie_ano.iloc[0]['ano'])}, la mortalidad infantil mediana es "
        f"{serie_ano.iloc[0]['mediana']:,.1f} por mil."
    )
else:
    sintesis_tendencia = (
        f"Entre {int(serie_ano.iloc[0]['ano'])} y "
        f"{int(serie_ano.iloc[-1]['ano'])}, la mortalidad infantil mediana pasó de "
        f"{serie_ano.iloc[0]['mediana']:,.1f} a "
        f"{serie_ano.iloc[-1]['mediana']:,.1f} por mil."
    )

if len(resumen_departamento) == 1:
    sintesis_territorio = (
        f"La vista se concentra en {departamento_lider['departamento']}, con mediana "
        f"de {departamento_lider['mediana']:,.1f} por mil."
    )
else:
    sintesis_territorio = (
        f"{departamento_lider['departamento']} lidera con "
        f"{departamento_lider['mediana']:,.1f} por mil y "
        f"{departamento_ultimo['departamento']} queda en "
        f"{departamento_ultimo['mediana']:,.1f}."
    )

if pd.notna(correlacion_controles) and pd.notna(correlacion_fecundidad):
    if (
        abs(correlacion_controles) < 0.2
        and abs(correlacion_fecundidad) < 0.2
    ):
        sintesis_asociacion = (
            f" En esta vista, ni los controles prenatales "
            f"(r = {correlacion_controles:.2f}) ni la fecundidad adolescente "
            f"(r = {correlacion_fecundidad:.2f}) muestran una asociación fuerte."
        )
    elif abs(correlacion_controles) >= abs(correlacion_fecundidad):
        sintesis_asociacion = (
            f" La asociación con controles prenatales (r = {correlacion_controles:.2f}) "
            f"es más fuerte que con fecundidad adolescente "
            f"(r = {correlacion_fecundidad:.2f})."
        )
    else:
        sintesis_asociacion = (
            f" La asociación con fecundidad adolescente "
            f"(r = {correlacion_fecundidad:.2f}) es más fuerte que con controles "
            f"prenatales (r = {correlacion_controles:.2f})."
        )
else:
    sintesis_asociacion = ""

st.info(
    f"**Hallazgo dinámico:** "
    f"{sintesis_tendencia} {sintesis_territorio}{sintesis_asociacion}"
)


with st.expander("Decisiones de limpieza y alcance"):
    st.markdown(
        "- Se descartaron 16 filas sin departamento.\n"
        "- Se estandarizó `departamento` (mayúsculas, sin tildes ni puntuación) y se "
        "eliminaron 19 registros duplicados de municipio-año que quedaron al unificar "
        "variantes como `Atlántico` y `ATLÁNTICO`.\n"
        "- Los faltantes se rellenaron con la mediana de cada columna. La columna más "
        "afectada fue `mortalidad_materna`, con 64 faltantes antes de depurar.\n"
        "- Se convirtió `ano` a entero.\n"
        "- Se recortaron a 0-100 solo las tres columnas que son porcentajes: "
        "`bajo_peso_nacer`, `partos_cesarea` y `partos_institucionales`. Las tasas de "
        "mortalidad no se recortaron porque están expresadas por mil o por cien mil.\n"
        "- No se estandarizó `municipio`: ya venía consistente.\n"
        "- Se descartaron los códigos DANE porque el tablero no los usa.\n"
        "- Las correlaciones que muestra la franja son asociaciones, no relaciones "
        "causales."
    )


if mostrar_tabla:
    st.subheader("Datos filtrados")
    columnas_tabla = [
        "departamento",
        "municipio",
        "ano",
        "bajo_peso_nacer",
        "controles_prenatales",
        "fecundidad_adolescente",
        "mortalidad_fetal",
        "mortalidad_general",
        "mortalidad_infantil",
        "mortalidad_materna",
        "mortalidad_neonatal",
        "partos_cesarea",
        "partos_institucionales",
    ]
    st.dataframe(
        df_filtrado[columnas_tabla].sort_values(
            ["ano", "departamento", "municipio"], ascending=False
        ),
        width="stretch",
        hide_index=True,
    )
