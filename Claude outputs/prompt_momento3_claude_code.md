# Prompt para Claude Code · Momento 3 (Analítica de Datos, UCC 2026-2)

Copie todo lo que está debajo de la línea y péguelo en Claude Code, abierto en la carpeta que contiene
`Actividades Breiner Martinez/`. Si Claude Code está abierto dentro de `analitica-datos-estudiantes/`
(el repositorio del curso), ábralo mejor un nivel más arriba o indíquele la ruta: ese repositorio es de
solo lectura y el trabajo no va ahí.

---

## ROL Y OBJETIVO

Eres mi asistente técnico para construir el entregable del **Momento 3** del curso Analítica de Datos
(Universidad Cooperativa de Colombia, profesor Julián Garzón). Mi equipo y yo ya entregamos los
momentos 1 y 2 sobre el mismo dataset (`train.csv`). El Momento 3 es la tercera etapa del **mismo
proyecto**, no un trabajo nuevo:

> Momento 3 = lo que entregamos en el Momento 2 + la retroalimentación del profesor incorporada +
> machine learning "por un ladito", como una herramienta más para sustentar el llamado a la acción.
> El formato sigue siendo storytelling: de una pregunta a una decisión.

Yo quiero **aprender y poder defender cada decisión** ante el profesor. Por eso trabajas por fases, me
explicas en español por qué haces cada cosa y te detienes en los puntos de control que se marcan abajo.

La entrega se sustenta en la clase 14 (jueves 19 de noviembre, según la transcripción de la clase del
12 de noviembre). Se evalúa el **último commit anterior al inicio de esa clase**. La hora de corte y la
estructura exacta de la entrega están en la "guía de entrega" que el profesor reparte en clase y envía
por correo: no están en el repositorio del curso. Si esa guía está en alguna carpeta, léela; si no, no
inventes su contenido y pregúntame.

## CONTEXTO DEL PROYECTO (lo que ya presentamos en el Momento 2)

Nuestro storytelling del Momento 2 es **"Tiendas de barrio"**. Está en
`Actividades Breiner Martinez/Momento2/Pitch_Tiendas_Barrio.html`, con su guion hablado en
`Guion_del_pitch_Tiendas_de_barrio.docx` (si el .docx no está en la carpeta, pídemelo). La historia, en
corto:

- Cadena de 10 tiendas, 1.559 productos, unos 18,6 millones en ventas al año. Dos tiendas de barrio
  (OUT019 y OUT010) venden apenas 368 mil; lo lógico parecería cerrarlas.
- Hallazgo: ahí hay unos 2,1 millones al año "escondidos", lo que venderían sus productos si se vendieran
  como en un supermercado Tipo 1. Se descartó que lo explicaran el producto (898 productos comparados),
  la ciudad (comparación dentro de la misma ciudad), el tamaño (OUT046, pequeña, vende 7 veces más) y la
  vitrina (más espacio por producto no mueve las ventas).
- Llamado a la acción del M2: aprobar un piloto de tres meses que opere OUT019 como supermercado y la
  mida contra OUT046 y OUT049, con regla de decisión fijada de antemano.
- El propio guion advierte que los 2,1 millones son un **techo** y que con datos históricos no se prueba
  causalidad; para eso existe el piloto.

**Las cifras de arriba vienen del guion, no de código que hayas ejecutado.** Úsalas como mapa, no como
verdad: cada una se re-verifica contra el notebook antes de reutilizarla (fase 0).

El Momento 3 **extiende esta misma historia**. No la reemplazamos ni cambiamos de tema. El modelo debe
servir al mismo llamado a la acción (por ejemplo, dimensionar o respaldar el piloto), no abrir otra
discusión.

## REGLA DE TRAZABILIDAD DE CIFRAS (retroalimentación del profesor, aplica a todo el Momento 3)

El profesor nos pidió que **toda cifra que mencionemos deje claro qué procedimiento o ecuación se
aplicó** para obtenerla. Es una de las correcciones que recordamos del M1 y M2; puede haber otras (ver
sección siguiente). Aplícala así:

- Crea `Momento 3/cifras_y_procedimientos.md`: una tabla con una fila por cifra que aparezca en el
  notebook, el dashboard, las diapositivas o el informe. Columnas: cifra, dónde aparece, **procedimiento
  o ecuación** (en palabras y, si aplica, en fórmula), filtro y `n` usado, supuestos, y la celda o
  archivo donde se calcula.
- En cada entregable la cifra debe llevar su procedimiento a la vista: nota al pie corta o línea
  "Cómo se calculó" en diapositivas e informe, `caption` o tooltip en el dashboard, celda markdown junto
  a la celda de cálculo en el notebook. No basta con tenerlo en el archivo aparte.
- Esto incluye las cifras del modelo: métrica usada y su fórmula (por ejemplo MAE, RMSE, R2, gap =
  score train menos score test), tamaño de train y test, y cómo se estimó cualquier impacto en dinero.
- Una cifra sin procedimiento reproducible no entra. Una estimación con supuestos se marca como
  escenario y lista sus supuestos.
- Las cifras de M2 que se reutilicen se recalculan y se comparan con lo que dijo el guion; si difieren
  (redondeos o diferencias reales), me lo muestras antes de corregir nada.

## OTRA RETROALIMENTACIÓN DEL PROFESOR (incompleta, por favor completa)

Solo recordamos una corrección con certeza (la de trazabilidad de cifras). El profesor hizo otras que
no recordamos. **No las supongas ni las inventes.** Búscalas así: comentarios o rúbricas dentro de
`Actividades Breiner Martinez/`, notas en los notebooks, README o archivos de texto de M1 y M2, y
cualquier guía o correo guardado. Presenta lo que encuentres con su fuente. Lo que no esté en ningún
archivo lo marcas como "pendiente de confirmar" y yo lo recupero del aula virtual o del correo del
profesor, que dijo que enviaría las instrucciones por correo.

## FUENTES DE VERDAD (en este orden de prioridad)

1. **Lo que dijo el profesor en clase** (resumen en la sección "Reglas del profesor").
2. **El repositorio del curso**, solo lectura: `clase13/` (README, `slides.html`, `reto.md`),
   `clase14/slides.html` (criterios de evaluación del Momento 3), `clase12/reto.md` (inferencia) y
   `clase03/skills/` (bucle especificar, planear, ejecutar, validar).
3. **Nuestras entregas anteriores y la retroalimentación recibida**, en la carpeta
   `Actividades Breiner Martinez/`. El dataset está en `Actividades Breiner Martinez/dataset/train.csv`.
4. Mis apuntes: "optimizar el modelo lo más que se pueda" no es un requisito del profesor (ver tensión
   resuelta más abajo). Los apuntes no pesan más que las fuentes 1 y 2.

Si dos fuentes se contradicen, aplica la de menor número y avísame de la contradicción. No asumas
requisitos que no aparezcan en las fuentes.

## REGLAS DURAS (valen en todas las fases)

- **No escribas nada dentro del repositorio del curso** (`analitica-datos-estudiantes/`). No copies
  archivos de ahí a otro sitio sin necesidad, y no edites sus notebooks: si necesitas uno, trabaja sobre
  una copia en nuestra carpeta.
- **El dataset es de solo lectura.** No sobrescribas `train.csv`. Todo dato derivado va a una carpeta
  nueva (por ejemplo `datos_procesados/`).
- **No inventes resultados.** Toda cifra que aparezca en un notebook, diapositiva o informe sale de una
  celda ejecutada. Si algo no se pudo calcular, lo dices.
- **No modifiques código que ya funciona** de los momentos 1 y 2 salvo que la retroalimentación del
  profesor lo exija o haya un error demostrable. Cada cambio queda justificado en una línea.
- **Honestidad por encima de la cifra.** Un modelo modesto bien reportado vale más que uno inflado.
  Prohibido mover hiperparámetros, columnas, cortes o fechas hasta que "dé bien" (eso es p-hacking y
  búsqueda del número que se quería).
- **El criterio de aceptación se escribe antes de entrenar** y no se reescribe después de ver métricas.
  Queda en un archivo con fecha de creación y no se toca.
- Todo en español; librerías, funciones y términos técnicos en inglés (`groupby`, `overfitting`,
  `DataFrame`). Sin emojis en ningún archivo.
- `random_state=42` en todo lo aleatorio, para que los resultados se repitan.
- **No hagas commit ni push** hasta que yo te lo pida. Cuando termines, dime qué cambió y qué falta
  commitear.

## REGLAS DEL PROFESOR (extraídas de la transcripción y de las clases 13 y 14)

**Qué se pide:**
- Mismo dataset de siempre, a menos que decidamos cambiarlo. "No nos compliquemos la vida."
- Enfocarse en la **retroalimentación** que dio el profesor en los momentos anteriores y en meter
  machine learning. No agregar nada más.
- Decidir **qué predecir o clasificar** (o qué nuevos grupos generar) a partir del dataset, y usar el
  modelo para **respaldar un llamado a la acción**. Ejemplo del profesor: "deberíamos invertir en esto
  porque el retorno estimado es tanto". El modelo es una herramienta más para vender la decisión.
- **La última diapositiva es el llamado a la acción.**
- Es storytelling: la competencia que se evalúa es sustentar una decisión con datos mediante una
  presentación estructurada.

**Qué no se pide (y no debes perseguir):**
- No es un curso de ML: no hace falta un modelo "súper atuneado" ni perseguir R cuadrado. El profesor
  lo dijo explícitamente en clase.
- No hace falta explicar en la presentación la teoría de cada métrica. Sí importa saber **cuándo y cómo**
  usar cada cosa.

**Lo que el profesor va a preguntar después (no se responde dentro de la presentación):**
- "¿Por qué decidieron hacer eso?" y, a todos los equipos: "¿Por qué este algoritmo y no otro? ¿Qué
  probaron y descartaron?". Por eso hay un **registro de experimentos** (fase 4) y un documento de
  preparación oral (fase 8). En las diapositivas no se justifica la elección del algoritmo.

**Tensión entre mis apuntes y las fuentes, ya resuelta:** mis apuntes dicen "optimizado lo más que se
pueda"; la transcripción dice que no se evalúa el nivel de optimización; las diapositivas de la clase 14
sí piden "varios algoritmos, cada uno con su razón de ser" e "hiperparámetros ajustados y documentados".
Criterio a seguir: ajuste **razonable y documentado** (grilla pequeña, validación cruzada solo sobre
entrenamiento), sin obsesionarse con subir la métrica.

### Criterios de evaluación del Momento 3 (clase 14, `slides.html`)

La nota es el promedio de tres dimensiones con el mismo peso, una banda por dimensión (Excelente,
Bueno, Aceptable, Insuficiente, No aceptable).

**Entregable:** proyecto de punta a punta con EDA corregido (M1), dashboard corregido (M2), estadística
inferencial (**mínimo dos intervalos de confianza y una prueba de hipótesis**), un modelo de machine
learning entrenado y evaluado, **tres recomendaciones en lenguaje de negocio** y la narrativa que une
todo, de una pregunta a una decisión.

**Estructura de la exposición (cuatro bloques obligatorios, en este orden):**
1. El problema: problema, contexto de negocio, stakeholders, objetivos SMART.
2. Los datos: dataset, hallazgos del EDA, calidad de datos.
3. El análisis: selección, entrenamiento, métricas, comparación.
4. La decisión: insights y recomendaciones accionables.

**Plantilla de los 4 puntos del modelo (clase 13):** (1) qué se predijo y qué decisión respalda;
(2) regresión o clasificación; (3) métrica en **test**, gap contra train y comparación contra el modelo
tonto; (4) variables clave (`feature_importances_`) y qué acciones se desprenden.

**Saber:** pruebas elegidas según pregunta y tipo de dato, con supuestos verificados; p-valor bien
interpretado, tamaño del efecto y diferencia entre significancia estadística y relevancia práctica;
métricas elegidas según el **costo del error**, con diagnóstico explícito de sobreajuste; problema atado
a un impacto real con stakeholders y objetivos SMART.

**Ser:** cadena causal explícita (el problema obliga a mirar esos datos, los datos a ese análisis, el
análisis a esa recomendación); del bloque del análisis se sale diciendo qué significa el modelo **para
el decisor**, no qué métrica dio; al menos tres recomendaciones accionables dirigidas a los
stakeholders del primer bloque, y se dice **qué no respaldan los datos**. Si hay que preguntar "¿y esto
para qué le sirve a quién?", el techo de Ser es Aceptable.

**Hacer:** limpieza corregida con la retroalimentación de M1 y M2; ingeniería de variables con criterio
de dominio; split adecuado y **sin fuga de datos**; correlación con **heatmap** conectada con qué entra
al modelo; gráficos del análisis tan cuidados como los del EDA (títulos que nombran el hallazgo, ejes
con nombre y unidad); dashboard con la retroalimentación del M2 incorporada y los mínimos (3 filtros,
3 KPIs, 3 gráficos); varios algoritmos con su razón de ser; hiperparámetros ajustados y documentados;
`random_state` fijado; el notebook corre de arriba a abajo con markdown por sección.

**Errores que fijan una dimensión en No aceptable:**
- Hacer: fuga de datos (escalar o imputar **antes** del split, incluir como predictora una variable que
  contiene la respuesta) o no haber hecho train/test split.
- Saber: evaluar sobre entrenamiento y presentarlo como desempeño del modelo.

**Topes (techos, no restas):** sin heatmap, Hacer no pasa de Aceptable; sin análisis de correlación, no
pasa de Insuficiente; estadísticos sin interpretar dejan a Saber en Aceptable. Más los de `clase13/reto.md`:
importancia leída como causalidad, omitir el gap, concluir que el mejor modelo es el de R2 de
entrenamiento 1.000, criterio de aceptación escrito después de ver las métricas.

**Banderas rojas de la sustentación:** métricas calculadas sobre train, fuga de datos en X, entrenar un
algoritmo que no responda a las preguntas del negocio.

**Entregables en el repositorio del equipo (clase 13, slide de checklist):** código limpio, modular y
reproducible; informe técnico en PDF con los 4 puntos diligenciados; tablero interactivo operativo en
vivo.

## FASES DE TRABAJO

Usa la lista de tareas para mostrar el avance. Al final de cada fase, resume en 3 a 5 líneas qué hiciste,
qué decidiste y qué falta. Aplica el bucle de `clase03/skills/` (especificar, planear, ejecutar,
validar): puedes leer esos `SKILL.md` y seguirlos.

### Fase 0 · Reconocimiento (solo lectura, no escribas nada)

1. Localiza `Actividades Breiner Martinez/` (puede estar fuera de la carpeta actual; busca por nombre,
   con cuidado con espacios y acentos). Si hay más de una candidata o no la encuentras, pregúntame.
2. Lista la estructura de esa carpeta y lee lo entregado en M1 y M2 (notebooks, dashboard, presentación,
   informes) y **toda retroalimentación del profesor** que haya (comentarios, rúbricas, correos
   guardados, notas mías). Haz un inventario: qué se entregó, en qué formato y con qué herramientas
   (por ejemplo Streamlit o Plotly para el dashboard).
3. Inspecciona `train.csv`: forma, tipos, nulos, duplicados, cardinalidades, rangos, posible variable
   objetivo natural, columnas identificadoras, columnas con fecha. Revisa si ya existe un diccionario de
   datos.
3b. Lee `Momento2/Pitch_Tiendas_Barrio.html` y el guion hablado. Haz un **inventario de cifras**: cada
   número que aparece, en qué diapositiva, y dónde se calcula en el notebook. Marca las que no tienen
   procedimiento visible (son las primeras a corregir por la regla de trazabilidad) y las que no
   coinciden con el código. Revisa también cómo se trataron los datos faltantes en M1: el guion cuenta
   que los ceros de vitrina (526 filas, 6,2 %) se rellenaron con la mediana del mismo producto en otras
   tiendas y que el tamaño de varias tiendas se rellenó como "pequeña" solo como hipótesis. Eso se hizo
   sobre todo el dataset, y para ML puede ser **fuga de datos** (ver fase 4, punto 3).
4. Lee en el repositorio del curso `clase13/slides.html` (o su texto), `clase13/reto.md`,
   `clase14/slides.html`, `clase12/reto.md` y `clase03/skills/`. Verifica que lo que dice mi resumen de
   las reglas del profesor coincide con esas fuentes y avísame de cualquier diferencia.
5. Confirma `requirements.txt` del curso y el entorno (`scikit-learn`, `pandas`, `scipy`, `matplotlib`,
   y la librería del dashboard). No instales nada sin decírmelo.

Entrega de la fase 0: un **inventario** corto (qué hay, qué retroalimentación existe, qué falta) y una
lista de **puntos de la retroalimentación del profesor** que hay que corregir. Si no encuentras
retroalimentación escrita, dímelo y pídeme que te la pase: no la inventes.

### Fase 1 · Especificar el encargo y proponer el problema de ML (PUNTO DE CONTROL)

Con `especifica-encargo`, escribe en `Momento 3/00_especificacion.md` (carpeta nueva dentro de
`Actividades Breiner Martinez/`, imitando la estructura de carpetas de M1 y M2 si existe):

- Objetivo, alcance, insumos y **criterio de aceptación** del modelo, antes de entrenar.
- El **piso contra el que se compara** (modelo tonto) y qué diferencia mínima haría que el modelo
  cambie una decisión.
- Cómo se conecta con el problema de negocio, los stakeholders y los objetivos SMART del M1/M2.

Luego **propón de 2 a 3 formulaciones de ML** posibles sobre `train.csv` (por ejemplo regresión,
clasificación o segmentación con clustering) que **sirvan al llamado a la acción del M2** (el piloto de
OUT019) y para cada una: qué se predice, para quién, qué decisión
respalda, qué variable objetivo se usa, qué riesgo de fuga hay, qué métrica corresponde según el costo
del error, y qué limitaciones tiene. Recomienda una, con razones. **Detente aquí y espera mi
confirmación**: elegir qué predecir es decisión del equipo y es lo que el profesor va a preguntar.

### Fase 2 · Incorporar la retroalimentación de M1 y M2

- Corrige la limpieza y el EDA según los comentarios del profesor del M1. Corrige el dashboard según
  los del M2 y mantén sus mínimos: 3 filtros, 3 KPIs, 3 gráficos.
- Cada corrección queda en una tabla `retroalimentacion_vs_cambio.md`: comentario del profesor, qué
  cambiaste, dónde. Esta tabla es evidencia de evolución del proyecto.
- No agregues análisis nuevos que no se pidieron.

### Fase 3 · Inferencia (requisito de la clase 12)

- Verifica si M1 y M2 ya traen inferencia. Si no, o si no cumple, agrega **mínimo dos intervalos de
  confianza al 95% y una prueba de hipótesis**, siguiendo `clase12/reto.md` (t-test de Welch con
  `equal_var=False`, error estándar en `scale`, `dropna()` antes de calcular, `n` reportado).
- Hipótesis H0 y H1 en español, escritas **antes** de mirar los resultados; reporta descriptivos antes
  del test, tamaño del efecto y la distinción entre significancia y relevancia práctica.
- Interpretación correcta, sin aceptar H0 y sin lenguaje causal.
- Elige las variables y los grupos por su relación con el problema de negocio, no por el p-valor.

### Fase 4 · Machine learning

Sobre la formulación que yo confirme en la fase 1:

1. **Heatmap de correlación** conectado con qué variables entran al modelo y cuáles se descartan.
2. **Variables y fuga de datos:** define `X` e `y`; elimina identificadores y toda columna que contenga
   la respuesta o se calcule a partir de ella. Documenta cada columna descartada y por qué.
3. **Imputaciones del M1 y fuga:** las medianas por producto y los rellenos de tamaño calculados sobre
   todo el dataset usan información de lo que será el conjunto de test. Para el modelo, esas
   imputaciones se rehacen **dentro del Pipeline, ajustadas solo con train** (o se tratan como categoría
   "no registrado"), y lo documentas. Además, si el modelo usa la tienda o el formato como variable,
   dilo con claridad: un modelo que predice ventas por formato solo reaprende la diferencia que ya
   mostramos y **no prueba causalidad**; no lo presentes como prueba de que convertir la tienda
   funcionará.
4. **Split antes que nada:** partición 80/20 con `random_state=42` (estratificada si es clasificación
   desbalanceada). Si hay fecha y el objetivo es pronosticar el futuro, evalúa un split temporal y
   justifica la decisión. Todo escalado, imputación y codificación va dentro de un `Pipeline` /
   `ColumnTransformer` ajustado **solo con train**.
5. **Línea base:** `DummyRegressor(strategy="mean")` o `DummyClassifier`. Si el modelo no le gana, se
   dice.
6. **Algoritmos:** el árbol de decisión (el de la clase) más uno o dos más con razón de ser (por
   ejemplo un modelo lineal regularizado o regresión logística como contraste interpretable, y un
   ensamble como `RandomForest` o `GradientBoosting`). Cada uno con una línea que explique por qué
   está.
7. **Ajuste razonable y documentado:** grilla pequeña con validación cruzada **solo sobre train**; el
   conjunto de test se usa una sola vez al final por modelo. Guarda hiperparámetros probados y elegidos.
8. **Evaluación honesta:** métricas sobre **test**, más el gap contra train con la regla de la clase
   (menor de 0.05 bien, 0.05 a 0.10 aceptable, mayor de 0.10 sobreajuste). Regresión: MAE, RMSE y R2.
   Clasificación: accuracy, precision, recall, F1 y matriz de confusión, y elige la métrica principal
   según el costo del error de este problema. Reporta el tamaño del conjunto de test: una métrica sobre
   pocos casos es frágil.
9. **Importancia de variables:** `feature_importances_` del mejor modelo, gráfico ordenado, e
   interpretación que diga explícitamente que es **asociación y no causalidad** y qué no se puede
   concluir.
10. **Registro de experimentos** en `Momento 3/registro_experimentos.md`: cada algoritmo y configuración
   probada, su resultado y por qué se mantuvo o se descartó. Incluye lo que **no funcionó**. Es la
   materia prima para responder "qué probaron y descartaron".
11. **Traducción a decisión:** convierte el resultado en algo que entienda el decisor (por ejemplo error
    esperado en unidades de negocio, o cuántos casos se priorizan con cierta tasa de acierto). Si
    estimas retorno o impacto, sale de los datos o se marca como **escenario con supuestos explícitos**;
    nunca como cifra inventada.

Todo en un notebook que corra completo de arriba a abajo con `Kernel > Restart & Run All`, con una
celda de markdown por sección, títulos que nombran el hallazgo y ejes con nombre y unidad.

### Fase 5 · Integrar al dashboard

- Mantén el dashboard del M2 con los mínimos (3 filtros, 3 KPIs, 3 gráficos) y la retroalimentación
  incorporada.
- Agrega como máximo una vista breve del resultado del modelo si ayuda al llamado a la acción. El ML
  es apoyo del storytelling, no el protagonista.
- Debe correr en vivo con las dependencias del `requirements.txt` del proyecto.

### Fase 6 · Presentación (storytelling)

- Usa el mismo formato y herramienta del M2 (si no lo sabes, pregúntame; no elijas por tu cuenta).
- Cuatro bloques en orden: el problema, los datos, el análisis, la decisión. Cada bloque existe porque
  el anterior lo hizo necesario. Si hay que recortar por tiempo, se recorta "Los datos", nunca "La
  decisión". El tiempo del turno lo anuncia el profesor el día de la clase: pregúntame cuánto es.
- El bloque del análisis sale diciendo qué significa el modelo **para el decisor**.
- Al menos **tres recomendaciones accionables** en lenguaje de negocio, dirigidas a los stakeholders del
  primer bloque, y una lámina o frase que diga **qué no respaldan los datos**.
- **La última diapositiva es el llamado a la acción**, con la cifra que sale del análisis.
- Cada cifra de las láminas lleva su procedimiento a la vista (regla de trazabilidad), incluidas las del M2 que se reutilicen.
- Sin justificar en las láminas la elección del algoritmo: eso queda para las preguntas.

### Fase 7 · Informe técnico (PDF)

Informe corto con los 4 puntos diligenciados: (1) qué se predijo y qué decisión respalda, (2) regresión
o clasificación y por qué, (3) métrica en test, gap y comparación contra el modelo tonto, (4) variables
clave y acciones que se desprenden. Más: criterio de aceptación escrito antes de entrenar, resumen de
inferencia, limitaciones y qué no respaldan los datos. Genéralo desde el notebook o un markdown para que
las cifras no se transcriban a mano.

### Fase 8 · Preparación oral (no se entrega, es para mí)

Crea `Momento 3/preparacion_sustentacion.md` con respuestas cortas, en lenguaje llano, a: por qué este
problema de ML y no otro; por qué regresión o clasificación; por qué este algoritmo y no otro; qué
probamos y descartamos; qué significa el gap; por qué confiamos (o no) en el modelo; qué no se puede
concluir; qué decisión recomendamos y qué pasa si el modelo se equivoca. Las respuestas salen del
registro de experimentos, no de teoría general.

### Fase 9 · Validación final (antes de decirme que terminaste)

Valida contra el criterio de aceptación de la fase 1 **condición por condición**, con `valida-resultado`,
y responde por escrito las cuatro preguntas del analista:
- ¿La métrica tiene sentido? (un R2 alto se sospecha; uno bajo se dice).
- ¿La forma cuadra? (tamaños de train y test, `n` de cada grupo).
- ¿Responde lo que pregunté? (qué decisión soporta).
- ¿Cambió algo? (¿le ganó al modelo tonto, y por cuánto?).

Verifica que **cada cifra** de notebook, dashboard, láminas e informe esté en `cifras_y_procedimientos.md` con su procedimiento y que el procedimiento también se vea en el entregable. Revisa contra la lista de topes y errores de fondo de la sección "Criterios de evaluación". Ejecuta
`Restart & Run All` y confirma que no hay errores, que ninguna métrica de train se presenta como
resultado, que no hay fuga y que el heatmap, el gap, la línea base y las tres recomendaciones están.
Si la validación falla, se vuelve a especificar; no se parcha el resultado.

## FORMA DE TRABAJAR CONMIGO

- Español claro, sin relleno. Explica el porqué de cada decisión técnica en 1 o 2 líneas para que yo
  pueda defenderla.
- Puntos de control obligatorios: **al final de la fase 0** (muéstrame el inventario), **en la fase 1**
  (espera mi elección del problema de ML) y **antes de generar la presentación** (confirma formato y
  tiempo del turno).
- Si falta información que cambia lo que construyes (formato de las entregas previas, retroalimentación,
  tiempo del turno, qué cuenta como stakeholder), pregúntame; no rellenes con suposiciones.
- Al terminar: lista de archivos creados o modificados con su ruta, qué quedó pendiente, qué debo
  verificar con el profesor (guía de entrega y hora de corte) y qué hay que commitear.
