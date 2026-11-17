"""Recalcula desde train.csv las cifras del pitch del Momento 2 y las compara con lo que dice el pitch.

Se ejecuta desde cualquier carpeta con el Python del entorno del curso:

    .venv/bin/python -I "Actividades Breiner Martinez/Momento3/scripts/verificar_cifras_m2.py"

Solo lee train.csv. Escribe un CSV en Momento3/datos_procesados/. Todo es determinista (sin azar).
La limpieza replica la del Momento 1: variantes de grasa unificadas y visibilidad = 0 tratada como
dato no registrado (mediana del mismo producto en las otras tiendas; respaldo: mediana del tipo de
producto). Aquí es descriptivo y se calcula sobre todo el dataset, como en el M1. Para el modelo de
ML esa imputación se rehace dentro del Pipeline, ajustada solo con train.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CSV = RAIZ / "dataset" / "train.csv"
SALIDA = RAIZ / "Momento3" / "datos_procesados" / "cifras_m2_recalculadas.csv"

V = "Item_Outlet_Sales"
df = pd.read_csv(CSV)

# Limpieza del M1 (solo lo que afecta a estas cifras)
vis0 = df["Item_Visibility"].replace(0, np.nan)
vis = vis0.fillna(vis0.groupby(df["Item_Identifier"]).transform("median"))
vis = vis.fillna(vis0.groupby(df["Item_Type"]).transform("median"))
df["vitrina"] = vis * 100  # % del area de exhibicion

abarrotes = df[df["Outlet_Type"] == "Grocery Store"]
tipo1 = df[df["Outlet_Type"] == "Supermarket Type1"]
supers = df[df["Outlet_Type"] != "Grocery Store"]
por_tienda = df.groupby("Outlet_Identifier")[V].mean()

filas = []


def registrar(lamina, cifra, pitch, recalculado, procedimiento, tolerancia):
    ok = abs(recalculado - pitch) <= tolerancia
    filas.append(
        {
            "lamina": lamina,
            "cifra": cifra,
            "pitch": pitch,
            "recalculado": round(float(recalculado), 3),
            "coincide": "si" if ok else "NO",
            "procedimiento": procedimiento,
        }
    )


def razon_mediana(a, b):
    """Mediana, sobre los productos presentes en ambos grupos, de (venta media en b) / (venta media en a)."""
    ma = a.groupby("Item_Identifier")[V].mean()
    mb = b.groupby("Item_Identifier")[V].mean()
    comunes = ma.index.intersection(mb.index)
    return len(comunes), (mb[comunes] / ma[comunes]).median(), (mb[comunes] > ma[comunes]).mean()


# Lamina 1
total = df[V].sum()
registrar(1, "Ventas totales de la cadena (millones)", 18.6, total / 1e6, "sum(Item_Outlet_Sales) / 1e6", 0.05)
registrar(1, "Ventas de OUT019 + OUT010 (miles)", 368, abarrotes[V].sum() / 1e3, "sum(ventas) donde Outlet_Type = Grocery Store", 0.5)
registrar(1, "Peso de las dos tiendas de barrio en ventas (%)", 2, abarrotes[V].sum() / total * 100, "ventas abarrotes / ventas totales x 100", 0.05)
registrar(1, "Productos distintos", 1559, df["Item_Identifier"].nunique(), "nunique(Item_Identifier)", 0)

# Lamina 2 (DRL01)
d = df[df["Item_Identifier"] == "DRL01"].set_index("Outlet_Identifier")
registrar(2, "DRL01 en OUT019 (ventas)", 935, d.loc["OUT019", V], "Item_Outlet_Sales de la fila DRL01 x OUT019", 1)
registrar(2, "DRL01 en OUT049 (ventas)", 6300, d.loc["OUT049", V], "Item_Outlet_Sales de la fila DRL01 x OUT049 (el pitch dice 'mas de 6.300')", 20)
registrar(2, "DRL01 precio OUT019", 233, d.loc["OUT019", "Item_MRP"], "Item_MRP", 0.5)
registrar(2, "DRL01 precio OUT049", 235, d.loc["OUT049", "Item_MRP"], "Item_MRP", 0.5)
registrar(2, "DRL01 vitrina OUT019 (%)", 13.5, d.loc["OUT019", "vitrina"], "Item_Visibility x 100", 0.05)
registrar(2, "DRL01 vitrina OUT049 (%)", 7.7, d.loc["OUT049", "vitrina"], "Item_Visibility x 100", 0.05)

# Lamina 3
n, mediana, pct = razon_mediana(abarrotes, tipo1)
registrar(3, "Productos vendidos en ambos formatos", 898, n, "interseccion de Item_Identifier entre abarrotes y Tipo 1", 0)
registrar(3, "Productos que venden mas en Tipo 1 (%)", 100, pct * 100, "share de productos con venta media Tipo 1 > venta media abarrotes", 0)
registrar(3, "Producto tipico vende N veces mas", 7.5, mediana, "mediana, sobre los 898 productos, de (venta media en Tipo 1) / (venta media en abarrotes)", 0.05)
for etiqueta, tienda, pares, pitch_n in [
    ("Nivel 1 (OUT019 vs OUT046 y OUT049)", "OUT019", ["OUT046", "OUT049"], 7.3),
    ("Nivel 3 (OUT010 vs OUT013, OUT018 y OUT027)", "OUT010", ["OUT013", "OUT018", "OUT027"], 8.5),
]:
    _, m, _ = razon_mediana(df[df["Outlet_Identifier"] == tienda], df[df["Outlet_Identifier"].isin(pares)])
    registrar(3, f"Misma ciudad, {etiqueta}", pitch_n, m, "igual que arriba, pero solo contra los supermercados de la misma ciudad", 0.05)

# Lamina 4
o19 = df[df["Outlet_Identifier"] == "OUT019"].set_index("Item_Identifier")[V]
o46 = df[df["Outlet_Identifier"] == "OUT046"].set_index("Item_Identifier")[V]
comunes = o19.index.intersection(o46.index)
registrar(4, "Productos comunes OUT019 y OUT046", 308, len(comunes), "interseccion de Item_Identifier", 0)
registrar(4, "OUT046 vende N veces mas por producto", 7, (o46[comunes] / o19[comunes]).median(), "mediana de ventas OUT046 / ventas OUT019 en los 308 productos comunes", 0.05)
registrar(4, "Venta por producto OUT019", 340, por_tienda["OUT019"], "mean(ventas) por tienda", 0.5)
t1_con_tamano = ["OUT013", "OUT035", "OUT046", "OUT049"]  # Tipo 1 con tamano registrado
registrar(4, "Rango inferior supermercados Tipo 1 con tamano", 2278, por_tienda[t1_con_tamano].min(), "min de mean(ventas) en Tipo 1 con Outlet_Size registrado", 0.5)
registrar(4, "Rango superior supermercados Tipo 1 con tamano", 2439, por_tienda[t1_con_tamano].max(), "max de mean(ventas) en Tipo 1 con Outlet_Size registrado", 0.5)
registrar(4, "Productos en OUT046", 930, (df["Outlet_Identifier"] == "OUT046").sum(), "filas de OUT046", 0)
registrar(4, "Productos en OUT019", 528, (df["Outlet_Identifier"] == "OUT019").sum(), "filas de OUT019", 0)

# Lamina 5
registrar(5, "Vitrina por producto, abarrotes (%)", 10.8, abarrotes["vitrina"].mean(), "mean(vitrina) en abarrotes", 0.05)
registrar(5, "Vitrina por producto, supermercados (%)", 6.5, supers["vitrina"].mean(), "mean(vitrina) en los tres tipos de supermercado", 0.05)
registrar(5, "Razon de vitrina", 1.7, abarrotes["vitrina"].mean() / supers["vitrina"].mean(), "cociente de las dos medias", 0.05)
registrar(5, "Venta por producto, supermercados (los tres tipos)", 2449, supers[V].mean(), "mean(ventas) en Tipo 1, 2 y 3 juntos (no solo Tipo 1)", 0.5)


# Simulacion de vitrina: OLS ventas ~ vitrina + precio + efecto de cada tienda (aproximacion; el codigo del pitch no esta en el repo)
def ols(data):
    x = pd.concat(
        [data[["vitrina", "Item_MRP"]], pd.get_dummies(data["Outlet_Identifier"], drop_first=True, dtype=float)], axis=1
    )
    x.insert(0, "const", 1.0)
    coef, *_ = np.linalg.lstsq(x.values, data[V].values, rcond=None)
    return dict(zip(x.columns, coef))


coef = ols(df)
extra_100 = coef["vitrina"] * abarrotes["vitrina"].sum()
registrar(5, "Ventas extra con +100 % de vitrina (porcentaje de la cadena)", 0, extra_100 / total * 100, "coef de vitrina (OLS con efecto de tienda y precio) x vitrina adicional de las filas de abarrotes / ventas totales x 100. Reproduce 'cercano a cero'; no se conoce la especificacion exacta del pitch", 0.1)
for nombre, datos in [("supermercados", supers), ("abarrotes", abarrotes)]:
    registrar(5, f"Correlacion vitrina-ventas, {nombre}", 0, datos["vitrina"].corr(datos[V]), "Pearson entre vitrina y ventas dentro del grupo ('practicamente nula')", 0.05)

# Lamina 6
brecha_fila = tipo1[V].mean() - abarrotes[V].mean()
brecha = brecha_fila * len(abarrotes)
registrar(6, "Menos que vende cada producto en tienda de barrio", 1976, brecha_fila, "mean(ventas Tipo 1) - mean(ventas abarrotes)", 0.5)
registrar(6, "Productos entre las dos tiendas", 1083, len(abarrotes), "filas de abarrotes", 0)
registrar(6, "Brecha anual (millones)", 2.1, brecha / 1e6, "brecha por producto x 1.083 filas", 0.05)
registrar(6, "Brecha como % de las ventas de la cadena", 11.5, brecha / total * 100, "brecha / ventas totales x 100", 0.05)
registrar(6, "Brecha a 3 anos (millones)", 6.4, brecha * 3 / 1e6, "brecha x 3: supone que se repite igual cada ano, sin crecimiento ni descuento", 0.05)
registrar(6, "Brecha a 5 anos (millones)", 10.7, brecha * 5 / 1e6, "brecha x 5, mismos supuestos", 0.05)

# Lamina 7
v19 = por_tienda["OUT019"] * (df["Outlet_Identifier"] == "OUT019").sum()
for factor, pitch_k in [(1.5, 90), (2, 180), (3, 359)]:
    registrar(7, f"Piloto x{factor} (miles al ano)", pitch_k, v19 * (factor - 1) / 1e3, "ventas anuales de OUT019 x (factor - 1)", 1)

res = pd.DataFrame(filas)
SALIDA.parent.mkdir(parents=True, exist_ok=True)
res.to_csv(SALIDA, index=False)
pd.set_option("display.width", 250, "display.max_colwidth", 70)
print(res.drop(columns="procedimiento").to_string(index=False))
print(f"\n{(res['coincide'] == 'si').sum()} de {len(res)} cifras coinciden. CSV: {SALIDA}")
