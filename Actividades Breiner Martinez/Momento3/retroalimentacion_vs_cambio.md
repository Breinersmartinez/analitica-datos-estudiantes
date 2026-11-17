# Retroalimentación del profesor y cambio hecho

**Fuentes.** Los comentarios al pitch del M2 salen de la transcripción de la sustentación
(`Momento2/retroalimentacion_sustentacion_m2.md`). Los comentarios a los dashboards salen de la sesión del M1
(`Momento2/transcript.docx`, tramo final). Lo que no consta en ninguna de las dos se marca como recuerdo del equipo
o como hallazgo propio. Esta versión corrige una anterior que parafraseó mal la observación de "peras con
manzanas".

## Comentarios al pitch del M2 (transcripción de la sustentación)

| # | Lo que dijo el profesor | Cambio hecho | Dónde | Estado |
|---|---|---|---|---|
| P1 | "A nivel de storytelling estuvo muy bien llevada de principio a fin." | Se conserva la historia y su orden. El modelo se agrega al análisis (lámina 7) sin reemplazar ninguna lámina del M2; se suman el problema (2) y las recomendaciones (9) que pide la clase 14 | Pitch M3 | Hecho |
| P2 | Comparar una tienda de barrio con un supermercado, aunque ambos sean pequeños, es comparar peras con manzanas: son **tipologías distintas** (otro foco, otro objetivo, otro tamaño). Habría sido más relevante comparar peras con peras, por ejemplo con una subsegmentación | (a) Los supermercados se subsegmentan por tipo y nivel de ciudad: la base es siempre Tipo 1 y las comparaciones por ciudad se emparejan (el "8,5 veces" de nivel 3 mezclaba Tipo 1, 2 y 3 y pasa a 7,0). (b) Las dos tiendas de barrio se comparan entre sí (diferencia de -25, intervalo que contiene el cero). (c) Se dice de frente que **no existe en los datos una tienda de barrio de otra cadena** para compararlas, y que la comparación contra Tipo 1 es entre tipologías distintas. (d) La conversión pasa de hecho a **hipótesis que el piloto prueba**. Límite que persiste: con solo dos tiendas de barrio no se puede subsegmentar ese grupo | Notebook sección 4b; pitch láminas 2, 4, 6 y 10 | Hecho hasta donde el dataset permite. Es la objeción más fuerte y no se resuelve del todo con estos datos |
| P3 | Le gustó que dos tiendas son el 2 %. Pero "solamente tenemos 2 tiendas, de las cuales todos los demás son supermercados: ahí ya te cambié la conversación". Preguntas: ¿dónde están ubicadas?, ¿estratégicamente?, ¿hay más tiendas alrededor? | El dataset solo trae el **nivel de ciudad** (`Outlet_Location_Type`), no la ubicación exacta, ni los supermercados cercanos, ni el espacio, ni los costos. La lámina 2 dice qué no se sabe de estas dos tiendas. La explicación que dio el equipo en el Q&A (el supermercado de nivel 1 está casi en la misma ubicación y le quita clientes) es una **hipótesis, no una medición**, y así se presenta | Pitch lámina 2 | Hecho. Preparar la respuesta oral en `preparacion_sustentacion.md` |
| P4 | La simulación de la visibilidad "fue simplemente una fórmula matemática, una regla de tres" y puede ser "un punto de quiebre de una conversación que esté yendo muy bien" si no tiene bases sólidas | La simulación se rehizo con un modelo (regresión con efecto fijo por tienda y precio) e intervalo de confianza; el resultado pasó de "≈ 0" a "sin efecto claro" (de -98 mil a +24 mil con +100 % de vitrina). Además, las otras proyecciones que eran aritmética simple (acumulado a 3 y 5 años, metas ×1,5 a ×3 del piloto) dejan de llamarse "simulación" y se rotulan como **escenarios de multiplicación simple, sin pronóstico** | Notebook sección 6b; pitch láminas 6, 8 y 10 | Hecho |

**Q&A de la sustentación.** El profesor planteó una alternativa: puede que ampliarse no sirva por falta de espacio, y
convenga convertir esas tiendas o cerrarlas y llevarlas a otro lugar. El pitch del M3 propone convertir (piloto). Cerrar
y reubicar **no está evaluado** y los datos no traen ubicación ni costos para evaluarlo: es una decisión abierta del
equipo (ver `preparacion_sustentacion.md`).

## Trazabilidad de cifras

| # | Origen | Cambio hecho | Estado |
|---|---|---|---|
| T1 | No está en la transcripción de la sustentación. Viene de la sesión de dashboards del M1 ("cómo está calculado" cada número) y de la pregunta P4. El equipo la recordaba como comentario al pitch | Cada cifra tiene su procedimiento en `cifras_y_procedimientos.md` y su "Cómo se calculó" a la vista en cada lámina | Hecho en el pitch; pendiente en el dashboard y en el informe |

## Comentarios a los dashboards del M1 (sesión de dashboards)

| # | Comentario | Cambio propuesto | Estado |
|---|---|---|---|
| D1 | Cada KPI debe medir algo útil para el objetivo; no "indicadores por indicadores" | Revisar que cada KPI responda al llamado a la acción | Pendiente de revisar |
| D2 | No mostrar estadísticos técnicos al usuario final ("r = -0,32") sin explicarlos | El texto de lectura muestra "correlación: -0,13": pasarlo a lenguaje llano | Pendiente (dashboard) |
| D3 | Decir cómo está calculado cada número | "Unidades por producto" es ventas / precio de lista: dejar la fórmula a la vista | Pendiente (dashboard) |
| D4 | Colores consistentes y con significado; entre más simple, mejor | El dashboard ya usa un color fijo por tipo de tienda | Cumplido, según capturas |
| D5 | Notas que expliquen qué se suma; filtros que no dejen la vista vacía | No verificable con capturas: probar combinaciones de filtros en vivo | Pendiente de probar |
| D6 | Abreviar números grandes (9 K, 9 M) | El dashboard ya muestra "18,6 M" y "2,5 K" | Cumplido, según capturas |
| D7 | Todo dashboard necesita un objetivo declarado | Agregar una línea que lo ate al piloto de OUT019 | Pendiente (dashboard) |
| D8 | (Hallazgo propio) "vitrina" en el pitch y "visibilidad" en el dashboard | El pitch conserva "vitrina" y la lámina 3 aclara que en el dashboard se llama visibilidad; falta unificarlo en el dashboard | Parcial |

El detalle de lo pendiente del dashboard está en `dashboard_cambios_pendientes.md`.

## Cambios del pitch del M3 que no vienen de un comentario del profesor

| Cambio | Motivo |
|---|---|
| Lámina 2 nueva, "El problema" | La clase 14 exige el bloque 1 con stakeholders y objetivos SMART |
| Lámina 7 nueva, "El modelo" | La clase 14 exige un modelo evaluado; el profesor pidió usarlo para respaldar el llamado a la acción |
| Lámina 9 nueva, "Recomendaciones" y lo que los datos no respaldan | La clase 14 exige tres recomendaciones y decir qué no respaldan los datos |
| Última lámina: tienda de control OUT010 y costo del piloto "por definir" | Propuesta del equipo (2026-11-13) a partir de comparar entre iguales. **Decisión abierta del equipo** |
| "Un supermercado de su ciudad vende 2.265" pasa a 2.313 | 2.265 no se pudo reproducir; 2.313 es el promedio de OUT046 y OUT049 |

## Pendiente de confirmar

Otros comentarios del profesor al pitch que no consten en la transcripción: ninguno conocido. No se inventan.
