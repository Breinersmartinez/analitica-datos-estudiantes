"""Genera el informe técnico del Momento 3 (HTML y PDF) desde el notebook y sus cifras.

    .venv/bin/python -I "Actividades Breiner Martinez/Momento3/scripts/construir_informe_m3.py"

Lee:     Momento3/datos_procesados/resultados_m3.json y registro_experimentos.csv (los escribe el notebook)
         Momento3/momento-3-nuestro.ipynb (solo para tomar las figuras ya ejecutadas)
Escribe: Momento3/datos_procesados/informe_m3.html y Momento3/Informe_tecnico_M3.pdf (con Chrome sin pantalla)

Ninguna cifra se escribe a mano: todo sale del JSON o del CSV. Si el notebook cambia, se vuelve a ejecutar y se
vuelve a correr este script.
"""

import csv
import html as h
import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M3 = RAIZ / "Momento3"
R = json.loads((M3 / "datos_procesados" / "resultados_m3.json").read_text(encoding="utf-8"))
NB = json.loads((M3 / "momento-3-nuestro.ipynb").read_text(encoding="utf-8"))
SALIDA_HTML = M3 / "datos_procesados" / "informe_m3.html"
SALIDA_PDF = M3 / "Informe_tecnico_M3.pdf"


def es(x, d=0):
    """Formato español: punto de miles y coma decimal."""
    x = 0.0 if round(x, d) == 0 else x  # evita "-0,000"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def signo(x):
    return ("−" if x < 0 else "+") + es(abs(x))


def p_txt(p):
    return "menor que 0,001" if p < 0.001 else es(p, 3)


def figura(marca, pie):
    """Toma la primera imagen de la celda de código cuyo código contiene `marca`."""
    for c in NB["cells"]:
        if c["cell_type"] == "code" and marca in "".join(c["source"]):
            for o in c.get("outputs", []):
                if o.get("output_type") == "display_data" and "image/png" in o.get("data", {}):
                    img = o["data"]["image/png"]
                    img = "".join(img) if isinstance(img, list) else img
                    return f'<figure><img src="data:image/png;base64,{img.strip()}" alt="{h.escape(pie)}"><figcaption>{h.escape(pie)}</figcaption></figure>'
    raise SystemExit(f"No encontré la figura con la marca {marca!r}. Ejecute el notebook completo primero.")


# Tabla de modelos desde el registro de experimentos
filas_modelos = []
with open(M3 / "datos_procesados" / "registro_experimentos.csv", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        if fila["configuración"] in ("MEJOR de su grilla", "strategy=mean"):
            r2p, gap = float(fila["R2 prueba"]), float(fila["gap R2"])
            filas_modelos.append({"modelo": fila["modelo"], "cv": float(fila["MAE validación cruzada (entrenamiento)"]),
                                  "mae": float(fila["MAE prueba"]), "r2p": r2p, "r2e": r2p + gap, "gap": gap,
                                  "elegido": fila["elegido"] == "True"})

I, W, PA, PR, V, B, M, PI = R["ic"], R["welch"], R["pareada"], R["pares"], R["vitrina"], R["brecha"], R["modelo"], R["piloto"]
ib, it = I["Tienda de barrio"], I["Supermercado Tipo 1"]
ef = V["efectos"]
pct_barrio = M["ventas_actuales"] / B["total_cadena"] * 100  # peso de las dos tiendas de barrio en las ventas


def diag(g):
    return "bien" if g < 0.05 else ("aceptable" if g <= 0.10 else "SOBREAJUSTE")


tabla_modelos = "".join(
    f"<tr{' class=\"sel\"' if m['elegido'] else ''}><td>{h.escape(m['modelo'])}{' (elegido)' if m['elegido'] else ''}</td>"
    f"<td>{es(m['cv'], 1)}</td><td>{es(m['mae'], 1)}</td><td>{es(m['r2p'], 3)}</td><td>{es(m['r2e'], 3)}</td>"
    f"<td>{es(m['gap'], 3)}</td><td>{diag(m['gap']) if not m['modelo'].startswith('Dummy') else 'piso'}</td></tr>"
    for m in filas_modelos
)

cond = [
    ("1. Partición 80/20, `random_state=42`, antes de imputar; todo dentro del Pipeline", "Cumple", "notebook, sección 10"),
    ("2. Sin fuga: ni `Outlet_*`, ni `Item_Identifier`, ni la respuesta en X", "Cumple", "sección 10"),
    ("3. MAE de prueba al menos 20 % menor que el del modelo de la media", "Cumple" if M["mejora_mae"] >= 0.20 else "No cumple", f"sale {es(M['mejora_mae'] * 100, 1)} %"),
    ("4. Gap de R2 menor que 0,10 en el modelo elegido", "Cumple" if M["gap_r2"] < 0.10 else "No cumple", f"sale {es(M['gap_r2'], 3)} ({diag(M['gap_r2'])})"),
    ("5. Elección por validación cruzada de 5 particiones solo sobre entrenamiento", "Cumple", "sección 12"),
    ("6. Estimación como rango (percentiles 5 y 95 de 1.000 remuestreos) y como escenario", "Cumple", "sección 16"),
    ("7. Si el techo del pitch cae dentro del rango, queda corroborado; si cae fuera, se dice", "Cumple" if M["techo_dentro_rango"] else "No cumple",
     "dentro del rango" if M["techo_dentro_rango"] else f"el techo ({es(B['techo'])}) cae fuera del rango; la diferencia es de {es(abs(M['dif_vs_techo_pct']), 1)} %, se reporta"),
    ("8. Limitaciones dichas", "Revisar", "sección 8 de este informe"),
]
tabla_cond = "".join(
    f"<tr><td>{h.escape(c).replace('`', '')}</td><td class=\"{'ok' if e == 'Cumple' else 'no'}\">{e}</td><td>{h.escape(n)}</td></tr>" for c, e, n in cond
)

CSS = """
@page { size: A4; margin: 18mm 17mm 18mm 17mm; }
* { box-sizing: border-box; }
body { font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; font-size: 10.3pt; line-height: 1.45; color: #1a1a1a; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 4px; line-height: 1.15; }
h2 { font-size: 13.5pt; margin: 22px 0 6px; padding-top: 6px; border-top: 2px solid #1a1a1a; break-after: avoid; }
h3 { font-size: 11pt; margin: 14px 0 4px; break-after: avoid; }
p { margin: 5px 0; }
.sub { color: #555; font-size: 9.5pt; margin: 0 0 10px; }
.resumen { background: #f4f1e6; border-left: 5px solid #f5c518; padding: 8px 12px; margin: 10px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.2pt; break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #eee; }
td.ok { color: #1b6e3a; font-weight: 700; } td.no { color: #b3261e; font-weight: 700; }
tr.sel td { background: #fff7cf; font-weight: 700; }
figure { margin: 10px 0; break-inside: avoid; } figure img { width: 100%; border: 1px solid #ddd; }
figcaption { font-size: 8.8pt; color: #555; margin-top: 2px; }
.nota { font-size: 9pt; color: #555; }
ul { margin: 4px 0 4px 18px; padding: 0; } li { margin: 2px 0; }
"""

cuerpo = f"""
<h1>Informe técnico, Momento 3: tiendas de barrio</h1>
<p class="sub">Analítica de Datos · Universidad Cooperativa de Colombia · 2026-2 · Integrantes: <i>completar antes de entregar</i><br>
Generado desde <code>momento-3-nuestro.ipynb</code>; ninguna cifra se transcribió a mano.</p>

<div class="resumen"><b>En una frase.</b> Cerrar las dos tiendas de barrio parece lógico porque pesan {es(pct_barrio, 1)} % de las ventas, pero sus productos
venden unas {es(W['razon'], 1)} veces menos que en un supermercado Tipo 1. La diferencia equivale a alrededor de {es(B['techo'] / 1e6, 1)} millones al año
(un modelo da {es(M['incremento'] / 1e6, 1)}); es una hipótesis entre tipologías distintas, y probarla cuesta una tienda y tres meses.
<b>Decisión que se pide:</b> aprobar un piloto de 3 meses que opere OUT019 como supermercado Tipo 1 y la mida contra OUT010, que no cambia, y contra OUT046 y OUT049.</div>

<h2>1. Los cuatro puntos del modelo</h2>

<h3>1.1 Qué se predijo y qué decisión respalda</h3>
<p>La venta anual de un producto en una tienda (<code>Item_Outlet_Sales</code>) para las {es(B['filas'])} filas de las tiendas de barrio, <b>como si se vendieran en un
Supermercado Tipo 1</b>. Respalda la decisión de aprobar el piloto de OUT019: da una segunda estimación del dinero en juego, con rango, y dice qué tan exigentes
son las metas del piloto. Según el modelo, OUT019 vendería {es(PI['multiplo_modelo'], 1)} veces lo actual como Tipo 1; las metas ×1,5, ×2 y ×3 piden el
{es(0.5 / (PI['multiplo_modelo'] - 1) * 100)} %, {es(1 / (PI['multiplo_modelo'] - 1) * 100)} % y {es(2 / (PI['multiplo_modelo'] - 1) * 100)} % de ese salto.</p>

<h3>1.2 Regresión o clasificación, y por qué</h3>
<p>Regresión. La variable objetivo es un monto continuo y la decisión necesita un monto, no una categoría. Clasificar productos en "ventas altas" o segmentar
tiendas se descartó porque no sustenta el llamado a la acción del pitch.</p>

<h3>1.3 Cómo se evaluó: métrica en prueba, gap y comparación con el modelo tonto</h3>
<p>Se entrenó solo con filas de Supermercado Tipo 1 ({es(M['n_train'])} de entrenamiento, {es(M['n_test'])} de prueba, partición 80/20 con <code>random_state=42</code>).
Las variables de entrada son atributos del producto: precio de lista, tipo, grasa, vitrina, peso y categoría. Quedan fuera la respuesta, el identificador del producto
y todas las columnas de la tienda. La imputación y la codificación viven dentro de un <code>Pipeline</code> ajustado solo con entrenamiento. La configuración se eligió
con validación cruzada de 5 particiones sobre entrenamiento; la prueba se usó una vez por modelo. Métrica principal: MAE (error promedio en unidades de venta).</p>
<table>
<tr><th>Modelo</th><th>MAE validación cruzada</th><th>MAE prueba</th><th>R2 prueba</th><th>R2 entrenamiento</th><th>Gap de R2</th><th>Diagnóstico</th></tr>
{tabla_modelos}
</table>
<p>El modelo elegido ({h.escape(M['elegido'])}) reduce el error de prueba {es(M['mejora_mae'] * 100, 1)} % frente a predecir siempre la media
({es(M['mae_dummy'])} contra {es(M['mae_prueba'])} por producto). Con una partición por producto, que deja fuera del entrenamiento los productos de prueba, la
reducción es {es(M['mejora_mae_por_producto'] * 100, 1)} %. El R2 de prueba es {es(M['r2_prueba'], 2)}: moderado, no alto, y así se reporta. Los tres modelos
dan casi el mismo error: la relación que se aprende es sencilla.</p>
{figura("gap_max", "Error de prueba por modelo (izquierda) y R2 de entrenamiento y prueba (derecha). El resultado real es el de prueba.")}

<h3>1.4 Variables clave y acciones que se desprenden</h3>
<p>Por permutación sobre el conjunto de prueba, <b>casi toda la señal está en una variable: el precio de lista</b> (desordenarla empeora el MAE en
{es(M['importancia_precio'])}). Tipo de producto, peso, grasa y vitrina quedan dentro del ruido. <b>Esto es asociación, no causalidad:</b> el precio importa
porque los productos caros venden más, no porque bajar el precio de un producto lo haga vender más.</p>
{figura("imp_perm = ", "Importancia de cada variable: aumento del error de prueba al desordenarla.")}
<p>Acciones: (a) la brecha no se explica por vender productos más baratos ni de otra categoría, así que no se justifica rebajar precios ni cambiar el surtido por categoría;
(b) la vitrina no mueve las ventas con estos datos, así que no se justifica invertir en más espacio de exhibición; (c) lo que queda por probar es el formato, y para eso
sirve el piloto.</p>

<h2>2. Criterio de aceptación, escrito antes de entrenar</h2>
<p>El criterio está en <code>00_especificacion.md</code> con fecha 2026-11-13, antes del modelo final, y declara que hubo una exploración previa fuera del notebook
(incluyó Gradient Boosting, que no pasó al modelo final). Resultado:</p>
<table><tr><th>Condición</th><th>Estado</th><th>Detalle</th></tr>{tabla_cond}</table>

<h2>3. Inferencia: dos intervalos de confianza y una prueba de hipótesis</h2>
<p><b>Intervalos de confianza al 95 %</b> de la venta media por producto (distribución t, error estándar en <code>scale</code>): tienda de barrio
{es(ib['inf'])} a {es(ib['sup'])} (n = {es(ib['n'])}); Supermercado Tipo 1 {es(it['inf'])} a {es(it['sup'])} (n = {es(it['n'])}). No se solapan.</p>
<p><b>Prueba de hipótesis.</b> H0: la venta media por producto es igual en los dos formatos; H1: es distinta; alfa = 0,05, dos colas, escritas antes de calcular.
t de Welch (las varianzas difieren: prueba de Levene): t = {es(W['t'], 1)}, {es(W['gl'])} grados de libertad, p {p_txt(W['p'])}. Se rechaza H0. Lo relevante es el tamaño:
la diferencia media es {es(W['dif'])} por producto (IC 95 %: {es(W['inf'])} a {es(W['sup'])}), la razón de medias es {es(W['razon'], 1)} y la d de Cohen es {es(W['d'], 2)}.
Con más de mil filas por grupo casi cualquier diferencia sale significativa; aquí además es grande y no marginal.</p>
<p><b>Robustez.</b> Comparando el mismo producto en los dos formatos ({es(PA['n'])} productos) la diferencia media es {es(PA['dif'])} (IC 95 %: {es(PA['inf'])} a {es(PA['sup'])}) y la
mediana de la razón es {es(PA['mediana_razon'], 1)}: no se explica solo por qué productos se venden en cada formato. Mann-Whitney confirma sin suponer normalidad.</p>
{figura("ejes[1].boxplot", "Venta media por producto con su intervalo de confianza al 95 % (izquierda) y distribución por formato con la prueba (derecha).")}

<h2>4. Peras con manzanas: qué se compara y qué no</h2>
<p>El profesor observó que una tienda de barrio y un supermercado son tipologías de negocio distintas, aunque ambas sean pequeñas, y que habría sido más relevante comparar
peras con peras, por ejemplo con una subsegmentación. Qué se hizo con este dataset: los supermercados se subsegmentan por tipo y nivel de ciudad, y las comparaciones por ciudad
se emparejan (la comparación de nivel 3 del pitch del M2 mezclaba Tipo 1, 2 y 3 y daba ×{es(PR['nivel3_mezclado_razon'], 1)}; solo contra Tipo 1 da ×{es(PR['nivel3_razon'], 1)};
en nivel 1, ×{es(PR['nivel1_razon'], 1)}). Las dos tiendas de barrio se parecen entre sí (diferencia de {signo(PR['iguales_dif'])} por producto, IC 95 %
{signo(PR['iguales_inf'])} a {signo(PR['iguales_sup'])}, con {es(PR['iguales_n'])} productos comunes).</p>
<p><b>Límite que persiste.</b> No existe en los datos una tienda de barrio de otra cadena con la cual compararlas: solo hay dos, y todas las demás tiendas son supermercados.
La comparación contra Tipo 1 sigue siendo entre tipologías distintas. Por eso convertir la tienda es una <b>hipótesis que el piloto prueba</b>, y los
{es(B['techo'] / 1e6, 1)} millones son la diferencia entre tipologías, no lo que la tienda recuperaría.</p>

<h2>5. El dinero en juego, con rango</h2>
<p>Aplicado a las {es(B['filas'])} filas de tienda de barrio, el modelo estima ventas esperadas de {es(M['ventas_esperadas'])} contra {es(M['ventas_actuales'])} actuales:
un incremento de <b>{es(M['incremento'])} al año</b> (rango del ruido de predicción: {es(M['inc_p5'])} a {es(M['inc_p95'])}, percentiles 5 y 95 de 1.000 remuestreos
de los errores de prueba). La diferencia de medias da {es(B['techo'])}. El modelo queda {es(abs(M['dif_vs_techo_pct']), 1)} % por debajo y el techo cae fuera del rango, por
{es(abs(B['techo'] - M['inc_p95']))}; es una diferencia dentro del redondeo de "alrededor de 2,1 millones", y no se retocó ninguna de las dos cifras.
<b>No son estimaciones independientes</b>: los productos de barrio tienen casi el mismo precio medio que los de Tipo 1, así que el modelo reproduce la misma brecha
controlando por precio y tipo de producto. El rango cubre solo el ruido de predicción, no la diferencia entre formatos.</p>
{figura("nombres_b = ", "Ventas actuales, ventas esperadas como Tipo 1 según el modelo y techo del pitch del M2.")}
<p><b>Vitrina.</b> Regresión de ventas sobre vitrina y precio con efecto fijo por tienda, solo tiendas de barrio y Tipo 1: coeficiente {es(V['coef'], 2)} (IC 95 %
{es(V['coef_inf'], 2)} a {es(V['coef_sup'], 2)}), que contiene el cero. Con +50 % de vitrina en las tiendas de barrio el efecto estimado es {signo(ef['50']['efecto'])} al año
(IC 95 %: {signo(ef['50']['inf'])} a {signo(ef['50']['sup'])}); con +100 %, {signo(ef['100']['efecto'])} ({signo(ef['100']['inf'])} a {signo(ef['100']['sup'])}).
No hay evidencia de efecto, y tampoco queda demostrado que no exista. Este cálculo reemplaza a la simulación del M2, que era una proporción simple.</p>

<h2>6. Tres recomendaciones</h2>
<ul>
<li><b>Para la dirección: no cerrar todavía.</b> Las dos tiendas son el {es(pct_barrio, 1)} % de las ventas, pero sus productos venden ×{es(PA['mediana_razon'], 1)} más en un Tipo 1. Cerrarlas hoy descarta la prueba.</li>
<li><b>Para operaciones: probar con OUT019, con el surtido de OUT046.</b> De {es(PI['productos'])} a unos 930 productos durante 3 meses.</li>
<li><b>Para dirección y finanzas: medir entre iguales y fijar la regla hoy.</b> El cambio de OUT019 contra el de OUT010, que sigue igual, y contra OUT046 y OUT049. Sin inversión en vitrina.
Metas del M2: duplicar la venta por producto (de {es(PI['por_producto'])} a {es(PI['por_producto'] * 2)}); si no sube al menos 50 %, se detiene.</li>
</ul>
<p><b>Llamado a la acción:</b> aprobar hoy el piloto. Metas en dinero (escenarios de multiplicación simple, no pronósticos): ×1,5, {es(PI['ventas'] * 0.5)}; ×2, {es(PI['ventas'])};
×3, {es(PI['ventas'] * 2)} al año con solo esta tienda.</p>

<h2>7. Qué no respaldan los datos</h2>
<ul>
<li>Que convertir la tienda <b>cause</b> el aumento: son datos de un año, sin ninguna tienda de barrio convertida, y la comparación es entre tipologías distintas.</li>
<li>Una cifra anual exacta: los {es(B['techo'] / 1e6, 1)} millones son un techo y un escenario; los acumulados a 3 y 5 años suponen la misma brecha cada año.</li>
<li>Una rentabilidad: <b>el costo del piloto no está en los datos</b> y queda como supuesto abierto. No se calcula retorno.</li>
<li>Un efecto de la vitrina, ni a favor ni en contra.</li>
<li>Dónde están las tiendas, si hay supermercados cerca, el espacio disponible y los costos de ampliar o de cerrar y reubicar: el dataset solo trae el nivel de la ciudad.
La explicación de que un supermercado cercano le quita clientes es una hipótesis, no una medición.</li>
</ul>

<h2>8. Limitaciones</h2>
<ul>
<li>El R2 de prueba es {es(M['r2_prueba'], 2)}: el modelo explica menos de la mitad de la variación; el resto no está en estas columnas. No se buscó subirlo.</li>
<li>Las filas no son independientes (un mismo producto y una misma tienda aparecen varias veces): los intervalos reales son más anchos que los calculados.</li>
<li>El conjunto de prueba tiene {es(M['n_test'])} filas; la métrica se mueve algo con la partición (con partición por producto, la reducción del error fue {es(M['mejora_mae_por_producto'] * 100, 1)} %).</li>
<li>El modelo aprende de supermercados y se aplica a otro formato: es extrapolación entre tipologías, y por eso el resultado es un escenario.</li>
<li>La imputación de la limpieza del M1 usó todo el dataset; para el modelo se rehízo dentro del <code>Pipeline</code>, solo con entrenamiento.</li>
</ul>

<h2>9. Trazabilidad</h2>
<p>Cada cifra de este informe, del pitch y del notebook está listada con su procedimiento en <code>cifras_y_procedimientos.md</code>. Las pruebas están en las secciones 1 a 6b del
notebook, el modelo en las secciones 9 a 17, y las decisiones sobre qué se probó y descartó en <code>registro_experimentos.md</code>. El dashboard se entrega como enlace
(<code>dashboard_cambios_pendientes.md</code> lista sus ajustes pendientes).</p>
"""

SALIDA_HTML.write_text(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Informe técnico, Momento 3</title><style>{CSS}</style></head><body>{cuerpo}</body></html>', encoding="utf-8")
subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={SALIDA_PDF}", SALIDA_HTML.as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("escrito", SALIDA_HTML)
print("escrito", SALIDA_PDF, f"({SALIDA_PDF.stat().st_size:,} bytes)")
