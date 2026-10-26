# Encargo: cinco figuras publication-ready sobre la ejecución del Presupuesto General de la Nación

Resolver el reto de la clase 8 completando las diez tareas del cuaderno oficial (T1–T10) y
produciendo cinco figuras listas para publicar, con una paleta única, títulos que enuncien
hallazgos verdaderos y todas las comprobaciones en verde.

## Contexto

El reto es el entregable de la clase 8 del curso de Analítica de Datos y se califica con las
dimensiones Saber, Ser y Hacer. Lo que se evalúa no es limpiar datos nuevos sino **criterio
visual**: elegir el gráfico correcto para cada pregunta, redactar un título verdadero y aplicar
un sistema visual consistente. Quien recibe el resultado es el profesor, y lo compara contra la
checklist de diez puntos y contra las cuatro preguntas del analista. La decisión que depende de
este trabajo es la nota de la clase y, más adelante, la calidad de los gráficos del dashboard del
Momento 2 del proyecto del equipo. Se dispara ahora porque la clase ya cubrió el tipo de gráfico
y la paleta, y porque el dataset es, a propósito, el mismo del demo: lo que cambia son las
preguntas.

## Lo que hay que responder o producir

1. Las **diez tareas T1–T10** resueltas en el cuaderno, con las tablas derivadas en las
   variables exigidas y con las columnas `'% Ejecución'` (porcentaje, `Compromisos /
   Apropiación Vigente * 100`) y `'Apropiación (billones)'` (pesos / 1e12).
2. Las **cinco figuras** especificadas por la consigna, cada una con su pregunta analítica, su
   tipo de gráfico, ejes con unidad legible, orden por valor, título que enuncie una conclusión
   verdadera, fuente citada y color con propósito:
   - Fig. 1 — concentración por sector: barras horizontales, top 10, billones de pesos.
   - Fig. 2 — brecha apropiación/compromisos: barras horizontales agrupadas, top 8, con el
     `% Ejecución` etiquetado en cada par.
   - Fig. 3 — mucho presupuesto y poca ejecución: gráfico de dispersión con línea del promedio
     nacional y al menos dos entidades anotadas.
   - Fig. 4 — composición del gasto: barras apiladas al 100 % sobre las tres categorías de
     `Nombre Nivel Uno Rubro`, normalizadas por fila.
   - Fig. 5 — sectores bajo el promedio: small multiples 2 × 4 con `sharex=True`.
3. La **tabla de entidades críticas** (T9): entidades con más de 5 billones de apropiación y
   ejecución por debajo del promedio nacional, con las columnas `'Apropiación (billones)'` y
   `'% Ejecución'`.
4. La **exportación** de las cinco figuras en PNG (`dpi=300`, `bbox_inches='tight'`,
   `facecolor='white'`), dentro de una carpeta `figuras/`, con los nombres exactos.
5. Las **respuestas escritas** del cuaderno: justificación de la paleta, título por figura,
   lecturas por tarea (T4, T5, T6, T8, T9, T10), análisis crítico de cinco preguntas, checklist
   figura por figura y las cuatro preguntas del analista.
6. El **cuaderno de entrega** que corre de principio a fin en el entorno previsto y con el punto
   de control final en 10 de 10.

## Insumos que hace falta tener

| Insumo | Para que se usa | Si no existe |
|--------|-----------------|--------------|
| `clase08/reto.ipynb` | Cuaderno oficial con las diez tareas, los verificadores y las respuestas por escribir | No hay reto: detenerse y reportar |
| `clase08/reto.md` | Consigna detallada: preguntas, checklist, requisitos y nombres de archivo | Guiarse por `reto.ipynb` y reportar la falta |
| `datos/EJECUCION_PRESUPUESTAL.csv` | Dataset real de ejecución presupuestal (3645 × 21) | No inventar datos: detenerse y reportar |
| `.venv` (pandas, numpy, matplotlib, seaborn) | Entorno de ejecución del cuaderno | Usar el intérprete del entorno del curso |
| `clase08/demo.ipynb` | Paleta, convenciones gráficas y estilo del profesor | Reconstruir el estilo desde `reto.ipynb` Paso 0.2 |
| Skills `especifica-encargo`, `planea-trabajo`, `ejecuta-plan`, `valida-resultado` | Método de trabajo obligatorio del reto | No sustituirlas por un flujo propio |

## Criterio de aceptacion

- **Forma del resultado:** un cuaderno Jupyter ejecutable de principio a fin y una carpeta
  `figuras/` con exactamente cinco PNG con los nombres pedidos. El cuaderno conserva sus celdas
  de texto, sus verificadores y trae escritas todas las celdas `*Tu respuesta:*`.
- **Limites razonables:** 32 sectores; 221 entidades; 3 filas excluidas por apropiación en cero;
  ejecución nacional ≈ 16.9 % (suma de compromisos / suma de apropiación vigente × 100, no el
  promedio simple de porcentajes); apropiación total ≈ 547 billones; la mayor entidad ≈ 97
  billones. Cinco figuras, ni cuatro ni seis.
- **Como se sabra que responde (comprobable por otra persona):**
  1. Las diez tareas están completadas.
  2. Los verificadores `comprobar(...)` y `comprobar_grafico(...)` de T1–T10 informan CORRECTO.
  3. El punto de control final dice 10 de 10 correctas.
  4. Existen los cinco PNG con los nombres exactos y son archivos legibles y no vacíos.
  5. Cada figura cumple los requisitos técnicos y visuales: tipo de gráfico correcto, orden por
     valor, eje en cero donde la regla lo exige, `sharex=True` en la fig. 5, línea de referencia
     en las figs. 3 y 5, etiquetas directas donde la tarea lo pide, unidades legibles (billones
     de pesos o porcentaje, nunca `1e13`), fuente citada con `fig.text(...)`.
  6. Cada título enuncia una conclusión que los datos sostienen (verificada contra la tabla).
  7. Las respuestas escritas están completas y se apoyan en los resultados calculados.
  8. El cuaderno corre desde un kernel reiniciado, en orden y sin excepciones.
  9. El archivo de entrega tiene el nombre requerido.
  10. La validación final documenta el cumplimiento o el incumplimiento de cada condición.

## Lo que queda fuera

- No se inventa ni se reemplaza el dataset, ni se simulan resultados para "cerrar" el reto.
- No se modifica la consigna para hacerla más fácil.
- No se eliminan ni se alteran los verificadores ni sus resultados esperados.
- No se cambian las reglas de cálculo para forzar que una comprobación pase.
- No se generan títulos con conclusiones que los datos no demuestren.
- No se rediseñan las diez tareas como un dashboard distinto.
- No se editan las cuatro skills del curso.
- No se instalan dependencias innecesarias ni se toca el entorno global.
- No se sobrescribe el `reto.ipynb` original: el trabajo va en una copia.
- No se marca como terminada ninguna tarea, figura o respuesta sin verificarla.

## Riesgos del resultado

- **Título falso.** Un título que afirme algo que los datos no sostienen (por ejemplo "X
  concentra el 38 %" sin que la suma dé 38 %) es el error más grave: degrada la dimensión Ser.
  Se previene calculando primero y redactando el título después de comprobar la cifra.
- **Eje truncado o en notación científica.** Un eje de barras que no parte de cero, o un eje
  `1e13`, induce una lectura falsa. Se previene con `set_xlim(0, ...)` y billones de pesos.
- **Promedio engañoso.** Usar el promedio simple de `% Ejecución` por fila en vez de la suma
  sobre la suma cambia la referencia nacional. Se declara la definición usada.
- **Correlación leída como causalidad.** La fig. 3 es una foto de un instante: sugiere
  hipótesis, no causas. Se advierte en la respuesta.
- **Escala logarítmica sin declarar.** Comprime las diferencias grandes; si se usa, se anota en
  la etiqueta del eje.
- **Recorte que oculta.** Mostrar solo los sectores grandes deja fuera 24 sectores; la fig. 5 y
  el análisis deben recordarlo.
- **Fig. 5 sin `sharex`.** Se ve bien y engaña: cada panel se autoescala y la comparación es
  falsa. Se fuerza la escala compartida y se verifica.

## Preguntas pendientes

Ninguna. Los tres puntos abiertos (apellido, ubicación de los PNG y color `secundario`) quedaron
resueltos y pasaron al registro de decisiones.

## Registro de decisiones

> **Duda:** la ruta `../../datasets/EJECUCION_PRESUPUESTAL.csv` del cuaderno no existe en este
> repositorio.
> **Decision:** en la copia de trabajo se reescribe a `../datos/EJECUCION_PRESUPUESTAL.csv`, que
> es donde vive el dataset. El `reto.ipynb` original se conserva intacto.

> **Duda:** la copia de trabajo puede heredar un cuaderno que no corre.
> **Decision:** se parte de `clase08/reto.ipynb` y se guarda como `clase08/reto_mio.ipynb`; solo
> se adaptan la ruta del dataset (celdas Paso 0) y las celdas `TU CÓDIGO AQUÍ`, sin tocar
> verificadores ni el resto del andamiaje.

> **Duda:** el reto exige una paleta de cinco roles, pero la instrucción solo da cuatro colores
> (neutro `#5A7B72`, énfasis `#3EB489`, alerta `#E76F51`, referencia `#799790`).
> **Decision:** se usa ese cuarteto y se reserva para `secundario` un gris azulado claro
> `#B8C4CE` (tomado de la paleta de arranque del demo). Es el rol que solo aparece cuando hay
> dos series (figs. 2 y 4); se mantiene grisáceo para no competir con el énfasis y conservar la
> lectura en escala de grises. Reversible si se prefiere otro tono.

> **Duda:** el demo usa una paleta azul institucional (`#1F4E79`, `#C0392B`, ...), distinta de la
> que fija la instrucción.
> **Decision:** prevalece la paleta indicada en la instrucción (verdes neutros + coral), porque
> es la que el trabajo debe aplicar en las cinco figuras; el demo se usa solo como referencia de
> estilo y estructura.

> **Duda:** ¿dónde quedan los cinco PNG?
> **Decision:** en `clase08/figuras/`, junto al cuaderno, como define `reto.md` (entregable =
> cuaderno + carpeta `figuras/`). La carpeta `figuras/` de la raíz queda sin usar.

> **Duda:** ¿se confirma el color del rol `secundario`?
> **Decision:** sí, `#B8C4CE` para el rol `secundario` (gris azulado claro del demo).

> **Duda:** ¿cómo se llama el archivo de entrega?
> **Decision:** `reto_clase08_Martinez.ipynb`, apellido del estudiante Breiner Martinez. La copia
> de trabajo es `clase08/reto_mio.ipynb` y de ahí se genera el entregable con ese nombre.

> **Duda:** el cuaderno original es material generado que este repositorio no edita a mano.
> **Decision:** no se toca `reto.ipynb`; los artefactos de método (encargo, plan, bitácora) y la
> copia de trabajo viven en `clase08/trabajo/` y `clase08/`, respectivamente.

> **Duda:** ¿se redondean los datos antes de calcular?
> **Decision:** no. Los porcentajes y agregaciones se calculan sin redondear; solo se redondea al
> presentar.
