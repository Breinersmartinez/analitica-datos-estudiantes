# Prompt para Claude Code · Momento 3 (v2)

**Cómo usarlo.** Abra Claude Code en la raíz del repositorio (`analitica-datos-estudiantes/`), cree una rama
(`git checkout -b momento3`, la guía `GUIDE_FORK.md` pide no trabajar en `main`) y pegue todo lo que está
debajo de la línea. Esta versión reemplaza al v1: la Fase 0 (reconocimiento) ya se hizo y sus resultados
están incluidos, así que el agente no los vuelve a derivar.

---

## 1. Rol y objetivo

Eres mi asistente técnico para el **Momento 3** de Analítica de Datos (UCC, 2026-2, profesor Julián Garzón).
El Momento 3 es la tercera etapa del **mismo proyecto** (dataset `train.csv`, historia "Tiendas de barrio"),
no un trabajo nuevo:

> Momento 3 = entregable del Momento 2 + retroalimentación incorporada + machine learning "por un ladito",
> como una herramienta más para sustentar el llamado a la acción. Sigue siendo storytelling.

Quiero poder defender cada decisión ante el profesor. Explícame en 1 o 2 líneas el porqué de cada paso
técnico y detente en los puntos de control de la sección 8.

## 2. Dónde se trabaja (esto corrige el v1)

- Carpeta de trabajo: `Actividades Breiner Martinez/`. Todo lo nuevo va en `Actividades Breiner Martinez/Momento3/`.
- **No escribas ni edites** `clase01/` a `clase15/`, `datos/`, `README.md`, `INSTALACION.md`, `CLAUDE.md`:
  son material del profesor (el `CLAUDE.md` del repo explica que se sobrescribe). Si necesitas un notebook de
  clase como referencia, léelo; no lo modifiques.
- Dataset: `Actividades Breiner Martinez/dataset/train.csv`, **solo lectura**. Derivados a `Momento3/datos_procesados/`.
- Entorno: usa `.venv/bin/python` del repo (scikit-learn 1.9.1, pandas, scipy, plotly, streamlit). El Python
  del sistema no tiene scikit-learn. No instales nada sin decírmelo.
- `random_state=42` en todo lo aleatorio. Sin emojis en ningún archivo. Español, con términos técnicos en inglés.
- **No hagas commit ni push** hasta que yo lo pida. Hay cambios míos sin commitear (`momento-1-nuestro.ipynb`,
  `clase13/demo.ipynb`, `Momento2/`): no los toques ni los revuelvas.

## 3. Hechos ya verificados (no los reconstruyas; solo cítalos con su fuente)

**Dataset** (leído con pandas): 8.523 filas x 12 columnas; 10 tiendas; 1.559 productos; `Item_Weight` con 1.463
nulos; `Outlet_Size` con 2.410 nulos (tiendas OUT010, OUT017 y OUT045 completas); `Item_Visibility = 0` en 526
filas (6,2 %); `Item_Fat_Content` con 5 variantes de 2 categorías; sin duplicados. No hay columna de fecha: el
único eje temporal es `Outlet_Establishment_Year`, así que **no es una serie de tiempo** y no se puede
"pronosticar el siguiente mes".

**Cifras del pitch del M2 que se reproducen con el CSV** (calculadas, no tomadas del guion):

| Cifra del pitch | Valor recalculado | Cálculo |
|---|---|---|
| Ventas totales de la cadena | 18.591.125 | `sum(Item_Outlet_Sales)` |
| Ventas de OUT019 + OUT010 | 368.034 (1,98 %) | suma por `Outlet_Type == "Grocery Store"` (179.694 + 188.340) |
| Venta media por producto: Tipo 1 / abarrotes | 2.316,2 / 339,8 | `mean` por `Outlet_Type` |
| Brecha anual | 2.140.390 (11,5 % del total) | (2.316,2 - 339,8) x 1.083 filas de abarrotes |
| Pilotos x1,5 / x2 / x3 de OUT019 | 89.847 / 179.694 / 359.388 | 179.694 x (factor - 1) |

Las cifras de los hallazgos 1 a 4 (gaseosa DRL01, 898 productos, 7,5x, ciudad, tamaño, simulación de vitrina)
**no se recalcularon todavía**: re-verifícalas en la Fase 2 antes de reutilizarlas.

**Contexto de modelado ya explorado** (borrador en memoria, no es resultado final): entrenar solo con filas de
Supermercado Tipo 1 (5.577) y predecir las 1.083 filas de abarrotes da, con imputación dentro de un `Pipeline`:

| Modelo | R2 test | MAE test | Ventas esperadas (abarrotes) |
|---|---|---|---|
| Dummy (media) | 0,00 | 1.229 | 2,51 M |
| Ridge | 0,47 | 825 | 2,49 M |
| Árbol max_depth=3 | 0,47 | 836 | 2,50 M |
| RandomForest | 0,45 (train 0,60) | 844 | 2,51 M |
| GradientBoosting | 0,45 | 836 | 2,37 M |

Lectura honesta: casi todo el poder predictivo viene de `Item_MRP` (el precio); los modelos de árbol no le
ganan al Ridge, y los ensambles sobreajustan algo. Las ventas esperadas menos las actuales (368 k) dan
aproximadamente 2,0 a 2,1 M: **coincide con los 2,14 M del M2**. Es una triangulación, no un descubrimiento.

## 4. Retroalimentación del profesor: qué hay y qué falta

**Encontrada en archivos** (`Momento2/transcript.docx`; ojo, el nombre engaña: es la sesión de
retroalimentación de los **dashboards del M1**, no del pitch del M2; el final trae las instrucciones del M2):

- Cada KPI tiene que medir algo útil para el objetivo del dashboard; no "indicadores por indicadores".
- No mostrar términos técnicos al usuario final (por ejemplo "r = -0,32"); si se muestran, explicarlos en lenguaje llano.
- Decir **cómo está calculado** cada número ("no sé cómo está calculado este rango de años... la media, la
  mediana, ¿histórica o del último año?"). Es el origen de la regla de trazabilidad de cifras.
- Colores consistentes y con significado; entre más simple mejor; sin gráficos que no concluyen nada.
- Notas aclaratorias en los gráficos (qué se suma, qué es excluyente) y filtros que no dejen la vista vacía.
- Número grande abreviado (9 K, 9 M).
- Antes de publicar, tener claro el mensaje y el dataset; todo dashboard necesita un objetivo declarado.

**No está en ningún archivo y la recuerdo yo:** toda traza o cifra debe decir qué procedimiento o ecuación se
aplicó. Hubo más comentarios al pitch del M2 que no tengo escritos. **No los inventes.** Déjalos como
"pendiente de confirmar" en `retroalimentacion_vs_cambio.md`; yo los recupero del aula virtual o del correo
que el profesor dijo que enviaría.

## 5. Reglas del profesor (transcripción del 12 de nov. y `clase13/`, `clase14/`)

**Se pide:** mismo dataset; retroalimentación incorporada + machine learning; decidir qué predecir o clasificar
o qué grupos generar; usar el modelo para **respaldar el llamado a la acción** (ejemplo del profesor: "invertir
en esto porque el retorno esperado es tanto"); **la última diapositiva es el llamado a la acción**; es
storytelling y la competencia evaluada es sustentar una decisión con datos.

**No se pide:** un modelo "súper atuneado", ni perseguir R2, ni explicar la teoría de cada métrica en la
presentación. Sí importa saber **cuándo y cómo** usar cada técnica.

**Lo preguntará después, no se responde en las láminas:** "¿por qué decidieron hacer eso?" y "¿por qué este
algoritmo y no otro, qué probaron y descartaron?".

**Entregable de la clase 14** (`clase14/slides.html`): EDA corregido (M1), dashboard corregido (M2) con 3 filtros,
3 KPIs y 3 gráficos, **mínimo dos intervalos de confianza y una prueba de hipótesis**, un modelo entrenado y
evaluado, **tres recomendaciones en lenguaje de negocio** que digan también qué no respaldan los datos, y la
narrativa de una pregunta a una decisión. Exposición en cuatro bloques y en este orden: el problema (con
stakeholders y objetivos SMART), los datos, el análisis, la decisión. Si falta tiempo se recorta "Los datos",
nunca "La decisión". Se evalúa el último commit antes del inicio de la clase 14 (jueves 19 de noviembre).
La guía de entrega y la hora de corte **no están en el repo**: pregúntame, no las supongas.

**Topes y errores de fondo que debes evitar:** fuga de datos o no hacer split (Hacer = No aceptable); métrica
de train presentada como resultado (Saber = No aceptable); sin heatmap (Hacer no pasa de Aceptable); omitir el
gap; importancias leídas como causalidad; criterio de aceptación escrito después de ver las métricas; entrenar
un algoritmo que no responda al negocio.

**Tensión resuelta entre mis apuntes y las fuentes:** "optimizado lo más que se pueda" no es requisito. Se hace
un ajuste **razonable y documentado** (grilla pequeña, validación cruzada solo sobre train), sin buscar el número.

## 6. Reglas duras

- Toda cifra sale de una celda ejecutada. Si algo no se pudo calcular, lo dices.
- **Trazabilidad:** crea `Momento3/cifras_y_procedimientos.md` con una fila por cifra (dónde aparece,
  procedimiento o ecuación en palabras y fórmula, filtro y `n`, supuestos, celda que la calcula). Y en cada
  entregable la cifra lleva su "Cómo se calculó" a la vista (nota al pie en láminas e informe, `caption` o
  tooltip en el dashboard, celda markdown junto al cálculo). Una estimación con supuestos se marca como
  **escenario** y lista sus supuestos.
- El criterio de aceptación se escribe **antes** de entrenar, en un archivo que no se reescribe después.
- Prohibido mover hiperparámetros, columnas o cortes hasta que "dé bien".
- Imputaciones del M1 (mediana de visibilidad por producto, tamaño de tienda rellenado como "pequeña") se
  calcularon sobre todo el dataset: para el modelo se rehacen **dentro del `Pipeline`, ajustadas solo con
  train**, o se tratan como "no registrado". No cambies el código del M1; documenta la diferencia.
- No agregues análisis que no se pidieron.

## 6b. Decisiones del equipo ya tomadas (actualización posterior al v2 inicial)

- **Formulación A confirmada** (la más alineada con el pitch). El punto de control 1 ya se cumplió para eso.
- **`Momento3/00_especificacion.md` ya existe** con el criterio de aceptación y la declaración de que hubo una
  exploración previa. No lo reescribas; si algo cambia, agrega una "Enmienda" con fecha.
- **Dashboard vigente:** "Explorador de Ventas BigMart", artefacto de tipo Dashboard en claude.ai
  (`https://claude.ai/artifact/8p1y9sXhXY3PJ36WjHdXkB`). Su contenido no se puede leer desde fuera; se conoce por
  capturas. Cumple los mínimos (4 filtros, 4 KPIs, 3 gráficos) y ya aplica varias correcciones del profesor
  (títulos en forma de pregunta, subtítulos que dicen cómo se calcula, color fijo por tipo de tienda, texto de
  lectura). Mejoras pendientes, sin cambiar lo que funciona: (a) el dashboard dice "visibilidad" y el pitch dice
  "vitrina": unificar el término; (b) el texto de lectura muestra "correlación: -0,13", y el profesor pidió no
  mostrar estadísticos técnicos al usuario final sin explicarlos; (c) "Unidades por producto" es una aproximación
  (ventas ÷ precio de lista): dejar su fórmula a la vista y en `cifras_y_procedimientos.md`; (d) como máximo una
  vista breve del modelo. Su código no está en el repo: pregunta al equipo si se exporta o se mantiene solo el
  enlace, y verifica que el enlace abra sin iniciar sesión (el profesor lo preguntó en la sesión del M1).
  `Momento1/dashboard.py` ya no es el vigente; no lo uses como referencia.
- **Retroalimentación del pitch del M2:** fue verbal y no existe por escrito. Lo que figura en este prompt es
  lo que el equipo recuerda, no una cita del profesor. Trátala como recuerdo, no como fuente.

## 7. Formulación de ML (confirmada: A)

**A (recomendada). Regresión: ¿cuánto venderían los productos de las tiendas de barrio si se vendieran como en
un Supermercado Tipo 1?** Se entrena solo con filas Tipo 1 (variables del producto: precio, tipo, grasa,
visibilidad, categoría por prefijo del código; **sin** `Item_Identifier`, `Outlet_*` ni `Item_Outlet_Sales`) y
se predice sobre las 1.083 filas de abarrotes. Sirve al llamado a la acción porque reemplaza "el techo de 2,1 M"
por una estimación **con rango** (error de test del modelo) y justifica la meta del piloto (x1,5, x2, x3).
Riesgos a declarar: extrapola de un formato a otro (los precios sí se solapan, 31 a 267 en ambos); es asociación
y **no prueba que convertir la tienda funcione**, eso lo prueba el piloto; el R2 moderado significa que el
modelo es un apoyo, no un oráculo. Métrica principal: MAE (error en unidades de venta, el decisor lo entiende)
más R2 y gap. Compárese contra `DummyRegressor`.

**B. Clasificación:** "producto de ventas altas" (tercil superior) para priorizar surtido en el piloto.
Menos ligada al hallazgo central; solo si el equipo quiere un segundo ángulo.

**C. Clustering:** perfiles de tienda para decidir si OUT019 u OUT010 es mejor candidata al piloto. Responde la
pregunta que el guion dejó abierta ("¿por qué OUT019 y no OUT010?"), pero con 10 tiendas es frágil.

Algoritmos para A: árbol de decisión (el de la clase), Ridge (contraste lineal interpretable) y
RandomForest o GradientBoosting (ensamble), cada uno con una línea que diga por qué está.

## 8. Fases y puntos de control

Aplica el bucle de `clase03/skills/` (especificar, planear, ejecutar, validar). Al cierre de cada fase, 3 a 5 líneas.

**Fase 1 · Especificar (PUNTO DE CONTROL 1: espera mi confirmación).** Escribe `Momento3/00_especificacion.md`:
objetivo, alcance, insumos, **criterio de aceptación**, piso de comparación, qué diferencia mínima cambiaría una
decisión, stakeholders y objetivos SMART. Presenta A, B y C con su variable objetivo, riesgo de fuga, métrica
y limitación. Recomienda una y **detente**: elegir qué predecir es decisión mía y el profesor va a preguntarla.
Pregúntame también el formato del pitch, el tiempo del turno y quiénes cuentan como stakeholders.

**Fase 2 · Retroalimentación y trazabilidad.** Re-verifica las cifras de los hallazgos 1 a 4 del pitch contra
el CSV y muéstrame cualquier diferencia antes de corregir. Crea `retroalimentacion_vs_cambio.md` (comentario,
cambio, dónde, fuente; los no recordados como "pendiente"). Revisa `Momento1/dashboard.py` (Streamlit sobre
`train.csv`; su docstring dice "Momento 2", confírmame cuál es el dashboard vigente) contra los 3 filtros,
3 KPIs, 3 gráficos y los comentarios de la sección 4.

**Fase 3 · Inferencia.** Verifica qué inferencia ya existe. Si no cumple, agrega **mínimo dos intervalos de
confianza al 95 % y una prueba de hipótesis** siguiendo `clase12/reto.md`: `stats.t.interval` con error estándar
en `scale`, `stats.ttest_ind(..., equal_var=False)` (Welch), `dropna()` antes, `n` reportado, H0 y H1 escritas
antes de ver el resultado, tamaño del efecto, y significancia distinta de relevancia práctica. Propuesta
natural, ligada al problema y no al p-valor: IC de la venta media por producto en abarrotes y en Tipo 1, y
Welch entre ambos grupos. Con 1.083 y 5.577 filas casi todo sale significativo: lo que importa es el tamaño.

**Fase 4 · Machine learning.** Heatmap de correlación conectado con qué entra al modelo. Define `X` e `y` y
documenta cada columna descartada. Split 80/20 antes de todo; imputación y codificación dentro de
`Pipeline`/`ColumnTransformer`. Línea base Dummy. Los tres algoritmos con grilla pequeña y validación cruzada
solo sobre train; el test se usa una vez por modelo. Métricas en test, gap contra train con la regla de clase
(< 0,05 bien, 0,05 a 0,10 aceptable, > 0,10 sobreajuste) y tamaño del test. Como robustez, repite el split
agrupando por producto (`GroupShuffleSplit`) y reporta si cambia algo. `feature_importances_` o coeficientes,
con la frase explícita de que es asociación y no causalidad. `Momento3/registro_experimentos.md` con todo lo
probado, también lo que no funcionó. Traduce el resultado a decisión: estimación con rango, marcada como
**escenario** con sus supuestos. Notebook que corre con `Restart & Run All`, markdown por sección, títulos que
nombran el hallazgo, ejes con nombre y unidad.

**Fase 5 · Dashboard.** Mantén los mínimos y los comentarios de la sección 4. Como máximo una vista breve del
modelo. Debe correr con `streamlit run` y las dependencias de `requirements.txt`.

**Fase 6 · Presentación (PUNTO DE CONTROL 2: confirma formato y tiempo antes de generarla).** Parte del pitch
de 7 diapositivas del M2 (`Momento2/Pitch_Tiendas_Barrio.html`) y extiéndelo, no lo reemplaces: el modelo entra
como **una o dos láminas** en el bloque del análisis (por ejemplo, entre el hallazgo 4 y "si no hacemos nada"),
sin justificar el algoritmo. Añade tres recomendaciones en lenguaje de negocio dirigidas a los stakeholders y una
lámina o frase de **qué no respaldan los datos**. La última lámina es el llamado a la acción, con la cifra que
sale del análisis. Cada cifra con su procedimiento a la vista.

**Fase 7 · Informe técnico (PDF).** Los 4 puntos de `clase13/reto.md`: qué se predijo y qué decisión respalda;
regresión o clasificación y por qué; métrica en test, gap y comparación contra el modelo tonto; variables clave y
acciones. Más criterio de aceptación, inferencia, limitaciones y qué no respaldan los datos. Generado desde el
notebook para que las cifras no se transcriban a mano.

**Fase 8 · Preparación oral (no se entrega).** `Momento3/preparacion_sustentacion.md`: respuestas cortas a por
qué este problema, por qué regresión, por qué este algoritmo y no otro, qué se probó y descartó, qué significa el
gap, qué no se puede concluir, qué pasa si el modelo se equivoca. Salen del registro de experimentos.

**Fase 9 · Validación final.** Contra el criterio de aceptación, condición por condición, y las cuatro
preguntas del analista: ¿la métrica tiene sentido?, ¿la forma cuadra (`n` de train, test y grupos)?, ¿responde
lo que pregunté?, ¿cambió algo frente al modelo tonto? Verifica que cada cifra esté en
`cifras_y_procedimientos.md`, que no haya fuga, que ninguna métrica de train se presente como resultado y que
estén el heatmap, el gap, la línea base y las tres recomendaciones. Si falla, se vuelve a especificar; no se
parcha el resultado.

## 9. Al terminar

Lista los archivos creados con su ruta, lo que quedó pendiente, lo que debo confirmar con el profesor (guía de
entrega, hora de corte, retroalimentación no recuperada) y qué hay que commitear. No commitees.
