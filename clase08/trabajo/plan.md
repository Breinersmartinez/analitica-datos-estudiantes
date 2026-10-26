# Plan: reto clase 8 — cinco figuras publication-ready

Construir el cuaderno `reto_mio.ipynb` a partir del oficial, con las diez tareas (T1–T10),
las cinco figuras exportadas a `clase08/figuras/` y las respuestas escritas, y validar el
resultado contra el criterio de aceptación del encargo.

## Alcance

| Entra | No entra |
|-------|----------|
| T1–T10 del cuaderno, cinco figuras, respuestas escritas, exportación PNG | Rediseñar el reto como dashboard; tocar los verificadores |
| Copia `reto_mio.ipynb` con la ruta del dataset corregida | Sobrescribir `reto.ipynb` original |
| Paleta de cinco roles aplicada en las cinco figuras | Crear figuras o tipos de gráfico extra |
| Ejecución completa del cuaderno y validación final | Entregar sin kernel reiniciado ni 10/10 |

## Criterio de exito

- T1–T10 con `comprobar`/`comprobar_grafico` en CORRECTO y punto de control en 10 de 10.
- Cinco PNG en `clase08/figuras/` con los nombres exactos, legibles y no vacíos.
- Cinco figuras con tipo correcto, orden por valor, eje en cero donde aplica, `sharex=True` en
  la fig. 5, referencia en figs. 3 y 5, unidades legibles, fuente citada y título verdadero.
- Todas las celdas `*Tu respuesta:*` completas, apoyadas en resultados calculados.
- Cuaderno corre de principio a fin desde kernel reiniciado.
- Entregable `reto_clase08_Martinez.ipynb` creado.

## Supuestos

- `datos/EJECUCION_PRESUPUESTAL.csv` no cambia durante el trabajo y tiene 3645 × 21.
- El `.venv` ya trae pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2, seaborn 0.13.2.
- La única corrección al cuaderno oficial es la ruta del CSV (`../../datasets/` → `../datos/`);
  verificadores y andamiaje quedan intactos.
- Los PNG van a `clase08/figuras/` y el entregable se llama `reto_clase08_Martinez.ipynb`.
- Existe criterio de aceptación en el encargo (no se inventa ninguno).

## Pasos

### Fase 1 · Preparar y construir las tablas base (T1, T2) — detallada

- [x] 1. Inventariar insumos y estado.
      Produce: confirmación de dataset, cuaderno, skills y entorno.
      Se comprueba: `datos/EJECUCION_PRESUPUESTAL.csv` = 3645 × 21; el `.venv` importa las cuatro
      librerías; `clase08/reto.ipynb` sin modificar.
  > Dataset 3645 × 21 confirmado. `.venv`: pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2,
  > seaborn 0.13.2. `git status` de `reto.ipynb`, `demo.ipynb`, `reto.md` y el CSV: sin cambios.
  > Las cuatro skills del curso están en `.opencode/skills/` (no en el catálogo global).
- [x] 2. Crear la copia de trabajo y adaptar la ruta del dataset.
      Produce: `clase08/reto_mio.ipynb`.
      Se comprueba: `reto.ipynb` original intacto; en la copia `../datos/EJECUCION_PRESUPUESTAL.csv`
      aparece en la celda de verificación y en `read_csv`, y `../../datasets/` ya no aparece.
  > Copia creada con 66 celdas (igual que el original). 3 reemplazos `../../datasets/` → `../datos/`
  > (celdas 1, 2 y 7). `reto.ipynb` con el mismo sha256 antes y después (6602d1a5245c3c41).
  > `git status`: solo `reto_mio.ipynb` y `trabajo/` como archivos nuevos.
- [ ] 3. Ejecutar el Paso 0 y confirmar carga y limpieza.
      Produce: `df_limpio`, conteo de excluidas y `ejecucion_nacional`.
      Se comprueba: 3645 cargadas, 3 excluidas por apropiación 0, 3642 de trabajo, 32 sectores,
      221 entidades, ejecución nacional ≈ 16.9 %; sin excepción.
  > Celdas 1, 6 y 7 ejecutadas con el intérprete del `.venv`: 3645 cargadas, 3 excluidas,
  > 3642 de trabajo, 32 sectores, 221 entidades, ejecución nacional 16.88 %. Sin excepción.
  > La celda 6 creó `clase08/figuras/`. Intérprete apunta al `.venv` y el CSV se encontró.

- [x] 4. Definir la paleta y confirmar el estilo.
      Produce: `PALETA` de cinco roles, `FUENTE`, `limpiar_ejes`, `guardar`, `EXPORTADAS`.
      Se comprueba: las cinco claves tienen hex no vacío y los cuatro colores fijados; una llamada
      de prueba a `limpiar_ejes` no falla.
  > `PALETA` = neutro #5A7B72, enfasis #3EB489, alerta #E76F51, referencia #799790,
  > secundario #B8C4CE; las cinco claves con hex válido. `limpiar_ejes` oculta los spines
  > superior e izquierdo y deja la grilla del eje x. `EXPORTADAS` vacío (aún sin figuras).
  > Respuesta de justificación de la paleta escrita en la celda markdown siguiente.
- [x] 5. Construir y verificar T1.
      Produce: variable `sector`.
      Se comprueba: `comprobar('T1', sector[['Apropiación (billones)', '% Ejecución']], decimales=2)`
      → CORRECTO; `sector` tiene 32 filas y está ordenado por apropiación descendente.
  > `sector` con 32 filas y 7 columnas; `comprobar('T1', ...)` = CORRECTO. Orden descendente por
  > apropiación confirmado. Top 3: Deuda Pública 97.19, Educación 88.24, Salud 78.17 billones.
  > OJO: el % de ejecución por suma es muy distinto según el sector (Deuda 8.5 % vs Educación 28.9 %).
- [x] 6. Construir y verificar T2.
      Produce: variable `entidad`.
      Se comprueba: `comprobar('T2', ...)` → CORRECTO; `entidad` tiene 221 filas.
  > `entidad` con 221 filas y 4 columnas; `comprobar('T2', ...)` = CORRECTO. Orden descendente
  > confirmado. Top: Deuda Pública 97.19, MinEducación 76.54, MinSalud 75.86 billones.
- [x] 7. Cerrar la fase: verificar T1 y T2 y guardar el cuaderno.
      Produce: cuaderno con T1 y T2 correctos.
      Se comprueba: `_RESULTADOS['T1']` y `_RESULTADOS['T2']` en True; el punto de control
      intermedio muestra solo T1 y T2 correctos.
  > Punto de control intermedio: T1 correcto, T2 correcto, T3–T10 pendientes → 2 de 10.
  > `reto_mio.ipynb` guardado con T1 y T2 resueltas.

### Fase 2 · Las cinco figuras (T3–T8) — detallada

Cada figura es una vuelta del bucle: especificar (pregunta, audiencia, título provisional),
planear (tipo, recorte, unidad del eje, resalte), ejecutar (figura + `guardar`), validar (título
contra la tabla) y escribir la respuesta. Comprobación común a las cinco: tipo correcto, orden
por valor, eje en cero donde aplica, unidades legibles, fuente citada y título verdadero.

- [x] 8. T3 · Figura 1: barras horizontales, top 10 (T3).
      Produce: `fig1`, `eje1`, `figuras/fig1_apropiacion_por_sector.png`.
      Se comprueba: `comprobar_grafico('T3', eje1, desde_cero='x', minimo_textos=5)` → CORRECTO.
  > Especificar: pregunta = qué sectores concentran el presupuesto; audiencia = tomador de
  > decisiones; título provisional verificado contra la tabla (top 10 = 87.3 %).
  > `comprobar_grafico('T3', ...)` = CORRECTO; 10 etiquetas directas; PNG 214 KB. `EXPORTADAS`
  > = ['fig1_apropiacion_por_sector']. OJO: el título del demo (38 % con dos sectores) sería
  > falso; los dos primeros suman 33.9 %. La revisión visual queda para el usuario (el modelo
  > no lee imágenes).
- [x] 9. T4 · Figura 2: brecha con barras agrupadas, top 8 (T4).
      Produce: `fig2`, `eje2`, `figuras/fig2_brecha_apropiacion_compromisos.png`.
      Se comprueba: `comprobar_grafico('T4', eje2, desde_cero='x', minimo_textos=4)` → CORRECTO.
  > Especificar: pregunta = dónde es mayor la brecha autorizado/comprometido; audiencia =
  > tomador de decisiones; título con dos cifras verificadas (Deuda 88.95 absoluta, Trabajo
  > 3.49 % relativa). `comprobar_grafico('T4', ...)` = CORRECTO; 8 etiquetas de %; PNG 254 KB.
  > OJO: brecha absoluta y relativa NO coinciden (Deuda vs Trabajo): justifica etiquetar el %.
- [x] 10. T5 · Figura 3: mucho presupuesto y poca ejecución (T5).
      Produce: `fig3`, `eje3`, `figuras/fig3_entidades_presupuesto_vs_ejecucion.png`.
      Se comprueba: `comprobar_grafico('T5', eje3, con_referencia=True, minimo_textos=2)` → CORRECTO.
  > Especificar: pregunta = entidades con mucho presupuesto y poca ejecución; audiencia =
  > tomador de decisiones; título verificado (13 entidades >5 billones bajo el 16.9 % nacional).
  > `comprobar_grafico('T5', ...)` = CORRECTO; referencia + 2 anotaciones; PNG 377 KB.
  > OJO: 13 candidatas; anotadas Deuda Pública (97.19; 8.48 %) y Min. Trabajo (50.23; 0.32 %).
  > Es hipótesis, no causalidad.
- [x] 11. T6 + T7 · Figura 4: composición normalizada y apilada al 100 %.
      Produce: `composicion_pct`, `fig4`, `eje4`, `figuras/fig4_composicion_gasto_por_sector.png`.
      Se comprueba: `comprobar('T6', ...)` CORRECTO (cada fila suma 100) y
      `comprobar_grafico('T7', eje4, desde_cero='x')` → CORRECTO.
  > Especificar: pregunta = cómo cambia la composición del gasto entre sectores; audiencia =
  > analista/tomador; título verificado (Salud 96.6 %, Educación 92.3 %, Transporte 75.8 %
  > inversión). T6 = CORRECTO: las 8 filas suman 100. T7 = CORRECTO; PNG 218 KB.
  > OJO: Deuda Pública es 100 % servicio de deuda; es el sector más distinto.
- [x] 12. T8 · Figura 5: small multiples 2 × 4.
      Produce: `fig5`, `ejes5`, `figuras/fig5_ejecucion_small_multiples.png`.
      Se comprueba: `comprobar_grafico('T8', ejes5, con_ejes=False, escalas_compartidas=True,
      minimo_textos=8)` → CORRECTO.
  > Especificar: pregunta = qué sectores están bajo el promedio; audiencia = tomador de decisiones;
  > título verificado (6 de 8 bajo el 16.9 %). `comprobar_grafico('T8', ...)` = CORRECTO; 8 paneles
  > con escala compartida; PNG 196 KB. OJO: sin sharex la figura se ve bien y engaña.

### Fase 3 · Ensamblaje y exportación (T9, T10) — detallada

- [x] 13. T9 · Tabla de entidades críticas.
      Produce: `entidades_criticas`.
      Se comprueba: `comprobar('T9', ...)` → CORRECTO; entidades con > 5 billones y % Ejecución
      < `ejecucion_nacional`, columnas `'Apropiación (billones)'` y `'% Ejecución'`.
  > Especificar: pregunta = entidades grandes bajo el promedio; el umbral 5 billones es decisión.
  > `comprobar('T9', ...)` = CORRECTO: 13 filas × 2 columnas. OJO: mismas 13 de la figura 3.
- [x] 14. T10 · Confirmar las cinco exportaciones.
      Produce: `EXPORTADAS` con los cinco nombres.
      Se comprueba: `comprobar('T10', sorted(EXPORTADAS))` → CORRECTO; existen los cinco PNG en
      `clase08/figuras/`.
  > Corrida completa de punta a punta: T10 = CORRECTO; cinco PNG en disco. Punto de control:
  > 10 de 10 correctas (T1–T10).
- [x] 15. Escribir las respuestas de T9, T10 y la checklist figura por figura.
      Produce: celdas de texto completas.
      Se comprueba: no queda ningún `*Tu respuesta:*` sin responder en el cuaderno.
  > Respondidas T9 (tabla), T10 (se ve bien y engaña), checklist figura 5 falla más puntos,
  > cuatro preguntas del analista (figura 5 en «¿responde lo que pregunté?»), análisis crítico
  > 1–5. Cero placeholders vacíos. Copiado a `reto_clase08_Martinez.ipynb` y corrido de
  > punta a punta: 10 de 10 correctas, 5 PNG en disco.

### Fase 4 · Validación de la entrega — detallada

- [x] 16. Corrida de punta a punta con espacio de nombres limpio.
      Produce: punto de control y `EXPORTADAS` desde cero.
      Se comprueba: 10 de 10 correctas; los cinco PNG en `clase08/figuras/`; cero celdas
      `*Tu respuesta:*` sin responder.
  > Corrida completa en un solo espacio de nombres (equivale a Kernel → Restart and Run All):
  > T1–T10 correctas, cinco PNG en disco, cero placeholders. Ningún estado dependió de sesión previa.
- [x] 17. Renombrar y dejar el entregable en su ruta final.
      Produce: `clase08/reto_clase08_Martinez.ipynb`.
      Se comprueba: existe en `clase08/` junto a `figuras/`; `reto_mio.ipynb` es la copia de trabajo.
  > Copiado a `clase08/reto_clase08_Martinez.ipynb` (533690 bytes) y el copia suelto en la raíz
  > fue borrado. `reto.ipynb` original sin tocar.
- [ ] 18. Validación visual: los cinco PNG juntos, con los ojos.
      Produce: veredicto de los puntos 1, 7 y 8 por figura.
      Se comprueba: los cinco pasan la prueba de los 5 segundos, la escala de grises y el título
      verdadero. **Lo hace el usuario: el modelo no lee imágenes.**
  > Queda pendiente por el usuario. Es la única comprobación que ningún `comprobar` cubre.

La **Fase 2** (las cinco figuras), y dentro de ella el **título de cada figura**: un título que
afirme algo que los datos no sostienen degrada la dimensión Ser, y una escala sin `sharex` o un
eje truncado engañan sin lanzar ningún error. Dentro de la Fase 1, el paso 2 es el más riesgoso:
una copia mal hecha o una ruta mal adaptada invalida todas las fases siguientes.
Plan B: calcular primero la cifra que el título afirma y, si no se sostiene, volver a especificar
la figura en lugar de parchar el título; si la ruta falla, rehacer la copia desde el original.

## Donde se puede caer

| Paso | Que puede salir mal | Como se nota |
|------|---------------------|--------------|
| 2 | Ruta del dataset mal reescrita o copia hecha sobre un archivo ya editado | `FileNotFoundError` al ejecutar; `reto.ipynb` con cambios en `git status` |
| 3 | Limpieza distinta a la del curso | Falta la exclusión de las 3 filas; cambian sectores/entidades o la ejecución nacional |
| 4 | Clave de `PALETA` vacía o color fuera de la paleta fijada | Hex vacío; figuras con colores por defecto |
| 5–6 | Nombres derivados inexactos (`'% Ejecución'`, `'Apropiación (billones)'`) | `comprobar` dice "todavía no coincide" |
| 7 | Comprobar antes de definir `sector`/`entidad` | `_RESULTADOS` en False con la variable en `None` |
| Fase 2 | Eje en notación científica o barras sin partir de cero | El eje muestra `1e13`; el verificador pide `desde_cero` |
| Fase 2 | Fig. 5 sin `sharex=True` | El verificador reporta "escalas distintas"; se ve bien e igual engaña |
| Fase 2 | Título falso o que describe los ejes | Al contrastarlo con la tabla no se sostiene |
| Fase 4 | Cuaderno con dependencias de sesión anterior | Restart and Run All revienta o deja tareas pendientes |

## Que se entrega

- `clase08/reto_clase08_Martinez.ipynb`: cuaderno completo, ejecutable de arriba a abajo, con las
  diez tareas correctas (10 de 10), las cinco figuras y todas las respuestas escritas.
- `clase08/figuras/`: los cinco PNG a 300 dpi con los nombres exactos
  (`fig1_apropiacion_por_sector`, `fig2_brecha_apropiacion_compromisos`,
  `fig3_entidades_presupuesto_vs_ejecucion`, `fig4_composicion_gasto_por_sector`,
  `fig5_ejecucion_small_multiples`).
