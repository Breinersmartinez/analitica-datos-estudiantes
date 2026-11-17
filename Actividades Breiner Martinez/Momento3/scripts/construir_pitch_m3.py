"""Construye el pitch del Momento 3 a partir del pitch del Momento 2 y de las cifras del notebook.

    .venv/bin/python -I "Actividades Breiner Martinez/Momento3/scripts/construir_pitch_m3.py"

Lee:     Momento2/Pitch_Tiendas_Barrio.html (no se modifica)
         Momento3/datos_procesados/resultados_m3.json (lo escribe momento-3-nuestro.ipynb, seccion 19)
Escribe: Momento3/Pitch_Tiendas_Barrio_M3.html

Cada reemplazo exige que el texto original exista exactamente una vez; si el pitch del M2 cambia, el
script falla en vez de producir un pitch a medias.
"""

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "Momento2" / "Pitch_Tiendas_Barrio.html"
RESULTADOS = RAIZ / "Momento3" / "datos_procesados" / "resultados_m3.json"
SALIDA = RAIZ / "Momento3" / "Pitch_Tiendas_Barrio_M3.html"

html = ORIGEN.read_text(encoding="utf-8")
R = json.loads(RESULTADOS.read_text(encoding="utf-8"))


def una_vez(viejo, nuevo):
    global html
    n = html.count(viejo)
    assert n == 1, f"se esperaba 1 coincidencia y hay {n}: {viejo[:80]!r}"
    html = html.replace(viejo, nuevo)


def regex_una_vez(patron, nuevo):
    global html
    html, n = re.subn(patron, lambda _: nuevo, html, count=1, flags=re.S)
    assert n == 1, f"patron sin coincidencia: {patron[:80]!r}"


# ---------------------------------------------------------------- datos
m = re.search(r"const DATOS = (\{.*?\});\n</script>", html, flags=re.S)
D = json.loads(m.group(1))
D["misma_ciudad"] = {"nivel1_x": R["pares"]["nivel1_razon"], "nivel3_x": R["pares"]["nivel3_razon"], "pct": D["misma_ciudad"]["pct"]}
V = R["vitrina"]
D["vitrina"] = {
    "vis_barrio": V["barrio"] / 100, "vis_super": V["tipo1"] / 100,
    "ventas_barrio": V["ventas_barrio"], "ventas_super": V["ventas_tipo1"],
    "corr_super": V["corr_tipo1"], "corr_barrio": V["corr_barrio"],
}
D["piloto"]["vecinas_por_producto"] = R["piloto"]["vecinas_por_producto"]
D["m3"] = R
una_vez(m.group(0), "const DATOS = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n</script>")

una_vez("<title>Pitch tiendas de barrio</title>", "<title>Pitch tiendas de barrio, Momento 3</title>")

# ---------------------------------------------------------------- estilos nuevos
una_vez("</style>\n</head>", """
/* Momento 3 */
.modelo-rango { margin: 24px 0 0; font-size: 24px; line-height: 1.45; color: var(--gris); }
.modelo-rango b { color: var(--blanco); }
.no-respaldan { margin-top: 36px; padding: 28px 32px; border-radius: var(--radio); background: var(--superficie); border-left: 6px solid var(--amarillo); }
.no-titulo { margin: 0 0 16px; font-size: 26px; font-weight: 700; color: var(--amarillo); }
.no-lista { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 12px 48px; font-size: 24px; line-height: 1.4; color: var(--gris); }
.no-lista b { color: var(--blanco); }
.paso-numero.chico { font-size: 22px; letter-spacing: 0.04em; text-transform: uppercase; }
.paso-verbo.mediano { font-size: 38px; }
.cierre { max-width: 1500px; font-size: 22px; }
.cierre .pide { display: block; margin-top: 10px; font-size: 28px; color: var(--blanco); }
.slide.accion { padding-bottom: 48px; }
.accion .pasos { margin-top: 32px; }
.accion .piloto { margin-top: 24px; }
.columna-datos.compacta { gap: 16px; }
.columna-datos.compacta .tarjeta { padding: 20px 28px; }
.columna-datos.compacta .dato-numero { font-size: 52px; }
</style>
</head>""")

# ---------------------------------------------------------------- lamina 1: contexto
una_vez('Ahí hay <span id="s1-giro-monto"></span> al año escondidos.',
        'Ahí hay alrededor de <span id="s1-giro-monto"></span> al año escondidos.')
una_vez('<p class="giro-nota">Es lo que venderían sus productos si vendieran como en un Supermercado Tipo 1.</p>',
        '<p class="giro-nota">Es la diferencia con un Supermercado Tipo 1, y un modelo que controla por precio y tipo de producto llega al mismo orden de magnitud.</p>')
una_vez("(EDA, sección 7.6)", "(verificado en Momento3/scripts/verificar_cifras_m2.py)")

# ---------------------------------------------------------------- lamina 2 nueva: el problema
PROBLEMA = """
  <!-- 2. EL PROBLEMA -->
  <section class="slide" aria-label="El problema">
    <p class="antetitulo">El problema</p>
    <h2 class="titulo">¿Qué hacemos con las dos tiendas de barrio: cerrarlas, dejarlas igual o transformarlas?</h2>
    <div class="pasos">
      <div class="tarjeta"><p class="paso-numero chico">Quién decide</p><p class="paso-verbo mediano">La dirección</p><p class="paso-texto">Aprueba o no el piloto que se propone hoy.</p></div>
      <div class="tarjeta"><p class="paso-numero chico">Quién ejecuta</p><p class="paso-verbo mediano">Operaciones</p><p class="paso-texto">La gerencia de operaciones convierte y mide OUT019. Los equipos de OUT019 y OUT010 son los afectados.</p></div>
      <div class="tarjeta"><p class="paso-numero chico">Objetivo medible</p><p class="paso-verbo mediano" id="p-meta"></p><p class="paso-texto" id="p-smart"></p></div>
    </div>
    <p class="fuente" id="p-fuente"></p>
  </section>

"""
una_vez("  <!-- 2. HALLAZGO 1 -->", PROBLEMA + "  <!-- 3. HALLAZGO 1 -->")

# ---------------------------------------------------------------- hallazgo 1
una_vez("Vitrina: % del área de exhibición de la tienda.`;",
        "Vitrina: % del área de exhibición de la tienda (en el dashboard se llama visibilidad).`;")

# ---------------------------------------------------------------- hallazgo 2: solo Tipo 1
una_vez("el 100 % de los productos vende más en el supermercado, 7,5 veces más.",
        "el 100 % de los productos vende más en el Supermercado Tipo 1, 7,5 veces más.")
una_vez("productos que están en los dos tipos de tienda vende más en el supermercado`;",
        "productos que están en los dos tipos de tienda vende más en el Supermercado Tipo 1`;")
regex_una_vez(r"\$\('s3-ciudad'\)\.textContent =\s*`.*?`;",
              "$('s3-ciudad').textContent =\n    `Contra el mismo tipo de supermercado y en la misma ciudad pasa igual: ×${f1.format(D.misma_ciudad.nivel1_x)} en Nivel 1 y ×${f1.format(D.misma_ciudad.nivel3_x)} en Nivel 3.`;")
P_ = R["pareada"]


def es(n):
    """Número entero con punto de miles."""
    return f"{n:,.0f}".replace(",", ".")


regex_una_vez(r'<p class="fuente">Fuente: EDA, sección 7\.4\..*?</p>',
              '<p class="fuente">Cómo se calculó: cada punto es un producto, con su venta promedio en las tiendas de barrio contra su venta promedio en los Supermercados Tipo 1. '
              'El ×7,5 es la mediana, sobre los 898 productos, de la razón entre las dos ventas. '
              f'Diferencia media por producto: {es(P_["dif"])}, intervalo de confianza al 95 %: {es(P_["inf"])} a {es(P_["sup"])} (prueba t, n = {P_["n"]}). '
              'Misma ciudad, solo contra Tipo 1: OUT019 contra OUT046 y OUT049; OUT010 contra OUT013. (Notebook del M3, secciones 4 y 4b.)</p>')

# ---------------------------------------------------------------- hallazgo 3
una_vez('<p class="fuente">Fuente: EDA, secciones 3.1 y 6.5. Tamaño según train.csv (pequeña, mediana o grande), sin metros cuadrados. OUT010, OUT017 y OUT045 no tienen tamaño registrado y por eso no aparecen.</p>',
        '<p class="fuente">Cómo se calculó: venta por producto = promedio de las ventas de cada tienda; solo Supermercados Tipo 1 con tamaño registrado. '
        'Tamaño según train.csv (pequeña, mediana o grande), sin metros cuadrados. OUT010, OUT017 y OUT045 no tienen tamaño registrado y por eso no aparecen. '
        'El ×7 es la mediana de la razón OUT046 / OUT019 en los 308 productos que venden las dos.</p>')

# ---------------------------------------------------------------- hallazgo 4: vitrina
una_vez('<h2 class="titulo">Más vitrina no lo arregla: ya tienen 1,7 veces más espacio y venden 7 veces menos.</h2>',
        '<h2 class="titulo" id="s4-titulo"></h2>')
una_vez('<p class="fuente">Fuente: EDA, secciones 6.4 y 7.2. Ventas extra: regresión de ventas sobre vitrina con efecto de cada tienda y del precio.</p>',
        '<p class="fuente">Cómo se calculó: la comparación es solo entre tiendas de barrio y Supermercados Tipo 1. Ventas extra: regresión lineal de ventas sobre vitrina y precio, con efecto fijo por tienda, '
        'multiplicada por la vitrina adicional de las 1.083 filas de tienda de barrio; intervalo al 95 % con el error estándar del coeficiente. Escenario: los datos son observacionales. (Notebook del M3, sección 6b.)</p>')
regex_una_vez(r"// 5\. HALLAZGO 4: vitrina.*?(?=\n  // 5\. SI NO HACEMOS NADA)", """// 5. HALLAZGO 4: vitrina (solo tiendas de barrio y Supermercados Tipo 1)
  const V = D.vitrina;
  const E = D.m3.vitrina.efectos;
  $('s4-titulo').textContent =
    `Más vitrina no lo arregla: ya tienen ${f1.format(V.vis_barrio / V.vis_super)} veces más espacio y venden ${f1.format(V.ventas_super / V.ventas_barrio)} veces menos.`;
  const maxVis = Math.max(V.vis_barrio, V.vis_super);
  barraFila($('s4-vitrina'), { nombre: 'Tienda de barrio', valor: V.vis_barrio, texto: pct1(V.vis_barrio), max: maxVis, ancho: 520, protagonista: true });
  barraFila($('s4-vitrina'), { nombre: 'Supermercados Tipo 1', valor: V.vis_super, texto: pct1(V.vis_super), max: maxVis, ancho: 520 });
  const maxVen = Math.max(V.ventas_barrio, V.ventas_super);
  barraFila($('s4-ventas'), { nombre: 'Tienda de barrio', valor: V.ventas_barrio, texto: f0.format(V.ventas_barrio), max: maxVen, ancho: 520, protagonista: true });
  barraFila($('s4-ventas'), { nombre: 'Supermercados Tipo 1', valor: V.ventas_super, texto: f0.format(V.ventas_super), max: maxVen, ancho: 520 });
  $('s4-correlacion').textContent =
    `Dentro de cada grupo, vitrina y ventas no se relacionan: correlación de ${f2.format(V.corr_super)} en supermercados Tipo 1 y ${f2.format(V.corr_barrio)} en tiendas de barrio.`;
  const conSigno = (v) => (v < 0 ? '−' : '+') + f0.format(Math.abs(v));
  segmentado($('s4-control'), [[25, '+25 %'], [50, '+50 %'], [100, '+100 %']], 50, (extra) => {
    const e = E[String(extra)];
    $('s4-resultado').textContent =
      `Con ${extra} % más vitrina: ${conSigno(e.efecto)} al año (intervalo al 95 %: de ${conSigno(e.inf)} a ${conSigno(e.sup)}), frente a ${millones(total)} de la cadena.`;
  });
""")

una_vez('<span class="dato-numero">≈ 0</span>', '<span class="dato-numero" style="font-size: 52px">Sin efecto claro</span>')

# ---------------------------------------------------------------- si no hacemos nada
una_vez("Sumada, son 2,1 millones al año.", "Sumada, son alrededor de 2,1 millones al año.")
Bm = R["brecha"]; Mo = R["modelo"]
regex_una_vez(r"\$\('s5-fuente'\)\.textContent =\s*`.*?`;",
              "$('s5-fuente').textContent =\n"
              "    `Cómo se calculó: diferencia de medias (${f0.format(B.promedio_super1)} − ${f0.format(B.promedio_barrio)}) × ${f0.format(B.productos)} productos = ${f0.format(B.total)} al año, contra Supermercado Tipo 1. "
              "Un modelo que controla por precio y tipo de producto estima ${f0.format(D.m3.modelo.incremento)} (rango por ruido de predicción: ${f0.format(D.m3.modelo.inc_p5)} a ${f0.format(D.m3.modelo.inc_p95)}). "
              "Es un techo y un escenario: los acumulados a 3 y 5 años suponen la misma brecha cada año, sin crecimiento ni descuento, y que las tiendas de barrio lleguen a vender como un Tipo 1.`;")

# ---------------------------------------------------------------- lamina nueva: el modelo
MODELO = """
  <!-- 7. EL MODELO -->
  <section class="slide" aria-label="El modelo">
    <p class="antetitulo">El modelo</p>
    <h2 class="titulo" id="m-titulo"></h2>
    <div class="cuerpo-tam">
      <div>
        <p class="control-etiqueta">Ventas anuales de las 1.083 filas de tienda de barrio</p>
        <div class="barras" id="m-barras" role="img"></div>
        <p class="modelo-rango" id="m-rango"></p>
      </div>
      <div class="columna-datos compacta">
        <div class="tarjeta dato"><span class="dato-numero" id="m-error"></span><span class="dato-etiqueta" id="m-error-nota"></span></div>
        <div class="tarjeta dato"><span class="dato-numero">El precio</span><span class="dato-etiqueta" id="m-precio-nota"></span></div>
        <div class="tarjeta dato"><span class="dato-etiqueta"><b>Qué significa para decidir</b></span><span class="dato-etiqueta" id="m-significa"></span></div>
      </div>
    </div>
    <p class="fuente" id="m-fuente"></p>
  </section>

"""
una_vez("  <!-- 6. SI NO HACEMOS NADA -->", MODELO + "  <!-- 8. SI NO HACEMOS NADA -->")

# ---------------------------------------------------------------- lamina nueva: recomendaciones
RECOS = """
  <!-- 9. RECOMENDACIONES -->
  <section class="slide" aria-label="Recomendaciones">
    <p class="antetitulo">Recomendaciones</p>
    <h2 class="titulo">Tres decisiones para este trimestre, y lo que los datos no dicen.</h2>
    <div class="pasos">
      <div class="tarjeta"><p class="paso-numero chico">Para la dirección</p><p class="paso-verbo mediano">No cerrar todavía</p><p class="paso-texto" id="r1"></p></div>
      <div class="tarjeta"><p class="paso-numero chico">Para operaciones</p><p class="paso-verbo mediano">Probar con OUT019</p><p class="paso-texto" id="r2"></p></div>
      <div class="tarjeta"><p class="paso-numero chico">Para dirección y finanzas</p><p class="paso-verbo mediano">Medir entre iguales</p><p class="paso-texto" id="r3"></p></div>
    </div>
    <div class="no-respaldan">
      <p class="no-titulo">Lo que los datos no respaldan</p>
      <ul class="no-lista">
        <li id="n1"></li><li id="n2"></li><li id="n3"></li><li id="n4"></li>
      </ul>
    </div>
    <p class="fuente">Cómo se calculó: cada cifra sale de Momento3/momento-3-nuestro.ipynb (secciones 4b, 6b y 9 a 16) y está listada con su procedimiento en cifras_y_procedimientos.md.</p>
  </section>

"""
una_vez("  <!-- 7. ACCIÓN -->", RECOS + "  <!-- 10. ACCIÓN -->")

# ---------------------------------------------------------------- accion (ultima lamina, llamado a la accion)
una_vez('<section class="slide" aria-label="Acción">', '<section class="slide accion" aria-label="Acción">')
una_vez("Este trimestre: operar OUT019 como supermercado y medirla contra sus vecinas.",
        "Este trimestre: operar OUT019 como supermercado y medirla contra OUT010 y sus vecinas.")
una_vez('Su venta por producto contra OUT046 y OUT049, los supermercados de su misma ciudad.',
        'El cambio en su venta por producto contra el de OUT010, que sigue igual (mismo formato), y su nivel contra OUT046 y OUT049, los supermercados de su ciudad.')
una_vez('<p class="cierre"><b>Responsable:</b> gerencia de operaciones. <b>Plazo:</b> 3 meses. <b>Métrica:</b> venta por producto de OUT019 contra OUT046 y OUT049.</p>',
        '<p class="cierre"><b>Responsable:</b> gerencia de operaciones. <b>Plazo:</b> 3 meses. <b>Métrica:</b> cambio en la venta por producto de OUT019 frente al de OUT010, y su nivel frente a OUT046 y OUT049. '
        '<b>Costo del piloto:</b> por definir.<span class="pide">Les pedimos hoy la aprobación de este piloto.</span></p>')
regex_una_vez(r"\$\('s6-nota'\)\.textContent =\s*`.*?`\s*\+\s*`.*?`;",
              "$('s6-nota').textContent =\n"
              "      `Venta por producto: de ${f0.format(P.por_producto)} a ${f0.format(P.por_producto * k)}; un Tipo 1 de su ciudad vende ${f0.format(P.vecinas_por_producto)}. ` +\n"
              "      `Es el ${f1.format(extra / P.total_cadena * 100)} % de la cadena (${f0.format(P.ventas)} × (${f1.format(k)} − 1)). ` +\n"
              "      `El modelo estima que como Tipo 1 vendería ${f1.format(D.m3.piloto.multiplo_modelo)} veces lo actual: esta meta pide el ${f0.format((k - 1) / (D.m3.piloto.multiplo_modelo - 1) * 100)} % de ese salto.`;")

# ---------------------------------------------------------------- JS de las laminas nuevas
JS_NUEVO = """
  // EL PROBLEMA
  $('p-meta').textContent = `${f0.format(P.por_producto)} a ${f0.format(P.por_producto * 2)}`;
  $('p-smart').textContent =
    `Venta por producto de OUT019 en 3 meses: de ${f0.format(P.por_producto)} hoy a ${f0.format(P.por_producto * 1.5)} como piso (×1,5) y ${f0.format(P.por_producto * 2)} como meta (×2), medida contra OUT010 y contra OUT046 y OUT049.`;
  $('p-fuente').textContent =
    `Cómo se compara: cada tienda de barrio contra Supermercados Tipo 1, un solo tipo y la misma ciudad cuando se puede, y contra la otra tienda de barrio. No existe en los datos un par exacto de una tienda de barrio. Venta por producto de OUT019: ${f0.format(P.ventas)} ÷ ${f0.format(P.productos)} productos.`;

  // EL MODELO
  const MM = D.m3.modelo;
  const techoM2 = D.m3.brecha.techo;
  $('m-titulo').textContent =
    `Un modelo que controla por precio estima también alrededor de ${f1.format(MM.incremento / 1e6)} millones al año.`;
  const maxModelo = Math.max(MM.ventas_esperadas, MM.ventas_actuales + techoM2);
  barraFila($('m-barras'), { nombre: 'Ventas actuales', detalle: 'tiendas de barrio', valor: MM.ventas_actuales, texto: millones(MM.ventas_actuales), max: maxModelo, ancho: 440, protagonista: true });
  barraFila($('m-barras'), { nombre: 'Esperadas como Tipo 1', detalle: 'según el modelo', valor: MM.ventas_esperadas, texto: millones(MM.ventas_esperadas), max: maxModelo, ancho: 440 });
  barraFila($('m-barras'), { nombre: 'Techo del M2', detalle: 'diferencia de medias', valor: MM.ventas_actuales + techoM2, texto: millones(MM.ventas_actuales + techoM2), max: maxModelo, ancho: 440 });
  $('m-barras').setAttribute('aria-label',
    `Ventas actuales ${millones(MM.ventas_actuales)}; esperadas como Tipo 1 según el modelo ${millones(MM.ventas_esperadas)}; techo del M2 ${millones(MM.ventas_actuales + techoM2)}.`);
  $('m-rango').innerHTML =
    `Incremento anual: <b>${f0.format(MM.incremento)}</b> según el modelo, contra <b>${f0.format(techoM2)}</b> por diferencia de medias (${f1.format(Math.abs(MM.dif_vs_techo_pct))} % menos). ` +
    `Las dos estimaciones parten de la misma comparación entre formatos: no son independientes.`;
  $('m-error').textContent = `${f0.format(MM.mejora_mae * 100)} % menos error`;
  $('m-error-nota').textContent =
    `que predecir siempre el promedio: el error por producto baja de ${f0.format(MM.mae_dummy)} a ${f0.format(MM.mae_prueba)}, medido en ${f0.format(MM.n_test)} filas que el modelo no vio.`;
  $('m-precio-nota').textContent = 'es casi la única variable que usa. Tipo de producto, peso y vitrina no aportan.';
  $('m-significa').textContent =
    'La brecha no viene de productos más baratos ni de otra categoría. Que convertir la tienda la cierre, solo lo prueba el piloto.';
  $('m-fuente').textContent =
    `Cómo se calculó: modelo lineal con penalización, entrenado con ${f0.format(MM.n_train)} filas Tipo 1 y evaluado en ${f0.format(MM.n_test)}; aplicado a las 1.083 filas de barrio. Incremento = esperadas − actuales (${f0.format(MM.ventas_actuales)}). ` +
    `Rango ${f0.format(MM.inc_p5)} a ${f0.format(MM.inc_p95)}: percentiles 5 y 95 de 1.000 remuestreos de los errores de prueba; solo cubre el ruido de predicción, no la diferencia entre formatos. Escenario. (Notebook, secciones 9 a 16.)`;

  // RECOMENDACIONES
  $('r1').textContent =
    `Las dos tiendas aportan el ${pct(ventasBarrio / total)} de las ventas, pero un producto vende ×${f1.format(D.pares_resumen.mediana_x)} más en un Supermercado Tipo 1. Cerrarlas hoy descarta la prueba.`;
  $('r2').textContent =
    `Operarla 3 meses con el surtido de OUT046: de ${f0.format(P.productos)} a unos 930 productos. Es lo que la separa de una tienda igual de pequeña que sí vende.`;
  $('r3').textContent =
    'Comparar el cambio de OUT019 con el de OUT010, que sigue igual, y con OUT046 y OUT049. No invertir en más vitrina: no hay evidencia de que mueva las ventas.';
  $('n1').innerHTML = '<b>Que convertir la tienda cause el aumento.</b> Son datos de un año y ninguna tienda de barrio convertida.';
  $('n2').innerHTML = `<b>Una cifra anual exacta.</b> ${millones(techoM2)} es un techo con rango, no una promesa.`;
  $('n3').innerHTML = '<b>Una rentabilidad.</b> Todavía no sabemos cuánto cuesta el piloto.';
  $('n4').innerHTML = '<b>Un efecto de la vitrina,</b> ni a favor ni en contra, con estos datos.';

  // Navegación: cada slide puede tener pasos (data-pasos)"""
una_vez("\n  // Navegación: cada slide puede tener pasos (data-pasos)", JS_NUEVO)

SALIDA.write_text(html, encoding="utf-8")
print("escrito", SALIDA, f"({len(html):,} caracteres)")
