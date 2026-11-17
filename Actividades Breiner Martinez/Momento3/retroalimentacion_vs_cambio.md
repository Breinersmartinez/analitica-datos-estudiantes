# Retroalimentación del profesor y cambio hecho

La retroalimentación al pitch del M2 fue **verbal** y no existe por escrito. La columna "Fuente" distingue lo
que consta en un archivo de lo que recuerda el equipo. Nada aquí es una cita textual salvo lo marcado como
transcripción.

| # | Comentario | Fuente | Cambio hecho o propuesto | Dónde | Estado |
|---|---|---|---|---|---|
| 1 | Toda traza o cifra debe decir qué procedimiento o ecuación se aplicó | Recuerdo del equipo (verbal) | Cada cifra con su procedimiento: `cifras_y_procedimientos.md`, y a la vista en láminas, dashboard e informe | `cifras_y_procedimientos.md` | Hecho en el pitch del M3 (cada lámina trae su 'Cómo se calculó'). Falta el dashboard (solo enlace, no editable desde aquí) y el informe |
| 2 | Cada KPI debe medir algo útil para el objetivo; no "indicadores por indicadores" | Transcripción, sesión de dashboards del M1 | Revisar que cada KPI del dashboard responda al llamado a la acción | Dashboard | Pendiente de revisar |
| 3 | No mostrar estadísticos técnicos al usuario final ("r = -0,32") sin explicarlos | Transcripción, sesión del M1 | El texto de lectura del dashboard muestra "correlación: -0,13": llevarlo a lenguaje llano | Dashboard | Propuesto |
| 4 | Decir cómo está calculado cada número | Transcripción, sesión del M1 | "Unidades por producto" es ventas / precio de lista: dejar la fórmula a la vista | Dashboard | Propuesto |
| 5 | Colores consistentes y con significado; entre más simple, mejor | Transcripción, sesión del M1 | El dashboard ya usa un color fijo por tipo de tienda | Dashboard | Ya cumplido, según capturas |
| 6 | Notas que expliquen qué se suma o qué es excluyente; filtros que no dejen la vista vacía | Transcripción, sesión del M1 | No verificable con capturas: probar combinaciones de filtros en vivo | Dashboard | Pendiente de probar |
| 7 | Abreviar números grandes (9 K, 9 M) | Transcripción, sesión del M1 | El dashboard ya muestra "18,6 M" y "2,5 K" | Dashboard | Ya cumplido, según capturas |
| 8 | Todo dashboard necesita un objetivo declarado | Transcripción, sesión del M1 | El dashboard no declara su objetivo: agregar una línea que lo ate al piloto de OUT019 | Dashboard | Propuesto |
| 9 | Unificar términos entre pitch y dashboard | Hallazgo propio, no del profesor | "Vitrina" en el pitch y "visibilidad" en el dashboard: elegir uno | Pitch y dashboard | Pitch M3: se conserva "vitrina" y la lámina 3 aclara que en el dashboard se llama visibilidad. Dashboard: pendiente |
| 10 | Corregir observaciones de trazabilidad del pitch (mediana, base de comparación, rango, fuentes, escenarios) | Hallazgo propio, ver `cifras_y_procedimientos.md` | Reescribir las notas al pie de las láminas 3, 4, 5, 6 y 7 | Pitch | Hecho en el pitch del M3: láminas 3, 4, 5, 6 y 8 reescritas con "Cómo se calculó"; las fuentes "EDA, sección X" se reemplazaron por el notebook del M3 |
| 12 | "No revolver peras con manzanas": se comparaban supermercados con tiendas de menor nivel, y eso es desigual | Recuerdo del equipo (verbal) | (a) La comparación de nivel 3 del pitch mezclaba OUT010 con supermercados Tipo 1, 2 y 3 (8,5 veces): emparejada solo con Tipo 1 (OUT013) da 7,0. (b) La lámina 5 comparaba 340 con 2.449, el promedio de los tres tipos: la base pasa a ser siempre Tipo 1 (2.316). (c) Las dos tiendas de barrio se comparan entre sí para justificar agruparlas (diferencia no distinta de cero). (d) Se declara que no existe un par exacto de una tienda de barrio en el dataset | Notebook, sección 4b; `cifras_y_procedimientos.md` | Hecho en el notebook y en el pitch del M3 (lámina 4: 8,5 pasa a 7,0; lámina 6: base Tipo 1) |
| 11 | Otros comentarios verbales del profesor al pitch | No recordados | Ninguno todavía | | **Pendiente de confirmar**: aula virtual o correo del profesor |

Los comentarios 2 a 8 vienen de la retroalimentación a los dashboards del M1 (`Momento2/transcript.docx`), no
del pitch. Se aplican porque la clase 14 pide "dashboard con la retroalimentación incorporada".

**Cambios del pitch del M3 que no vienen de un comentario del profesor** (decisiones del equipo o de rigor):

| Cambio | Motivo |
|---|---|
| Lámina 2 nueva, "El problema": quién decide, quién ejecuta, objetivo medible | La clase 14 exige el bloque 1 con stakeholders y objetivos SMART |
| Lámina 7 nueva, "El modelo" | La clase 14 exige un modelo evaluado; el profesor pidió usarlo para respaldar el llamado a la acción |
| Lámina 9 nueva, "Recomendaciones": tres recomendaciones y lo que los datos no respaldan | La clase 14 exige tres recomendaciones y decir qué no respaldan los datos |
| Última lámina: tienda de control OUT010 y costo del piloto "por definir" | Decisión del equipo (2026-11-13) a partir del comentario de comparar entre iguales |
| La simulación de vitrina se rehizo en el notebook y su resultado pasó de "≈ 0" a "sin efecto claro" (intervalo de -98 mil a +24 mil con +100 % de vitrina) | El código del M2 no estaba en el repo; la versión reproducible muestra un intervalo que contiene el cero pero no es despreciable |
| "Un supermercado de su ciudad vende 2.265" pasa a 2.313 | 2.265 no se pudo reproducir; 2.313 es el promedio de OUT046 y OUT049 |
