# Prompt para Claude Code · Momento 3 (v3, corto)

Cómo usarlo: abra Claude Code en la raíz del repo (`analitica-datos-estudiantes/`), cree una rama
(`git checkout -b momento3-cierre`) y pegue todo lo que está debajo de la línea. Reemplaza al v1 y al v2:
el v2 asumía que el trabajo estaba por empezar, y ya está hecho en buena parte.

---

## 1. Qué es esto

Momento 3 de Analítica de Datos (UCC, profesor Julián Garzón). No es un trabajo nuevo: es el **mismo proyecto**
("Tiendas de barrio", `train.csv`) = pitch del Momento 2 + retroalimentación incorporada + machine learning
"por un ladito", usado como una herramienta más para sustentar el llamado a la acción. Sigue siendo storytelling.

## 2. Punto de partida: ya existe, no lo rehagas

En `Actividades Breiner Martinez/Momento3/` hay: `00_especificacion.md`, `momento-3-nuestro.ipynb`
(inferencia + modelo), `Pitch_Tiendas_Barrio_M3.html`, `cifras_y_procedimientos.md`, `registro_experimentos.md`,
`retroalimentacion_vs_cambio.md`, `scripts/` y `datos_procesados/`.

**Paso 1, antes de escribir nada:** audita. Lee esos archivos, ejecuta el notebook completo con `.venv/bin/python`
(Restart & Run All) y compara contra las secciones 3 a 5 de este prompt. Dame en 10 líneas qué cumple y qué falta.
**Paso 2:** completa solo lo que falte. Si algo ya está bien, no lo toques.

## 3. Lo que pidió el profesor (transcripción del 12 de noviembre)

- Mismo dataset; lo del M2 + la retroalimentación + machine learning. Nada más.
- Decidir qué predecir o clasificar, y usarlo para **respaldar la decisión**: "si invertimos esto, el retorno
  esperado es tanto". El modelo es una herramienta para vender el entregable.
- **La última lámina es el llamado a la acción.**
- No evalúa que el modelo esté súper afinado ni el R2. Sí importa saber **cuándo y cómo** usarlo.
- Preguntará después "¿por qué decidieron hacer eso?": **no se explica en las láminas**. Las respuestas van en
  `registro_experimentos.md`.
- La competencia que se evalúa: sustentar una decisión con datos en una presentación estructurada.

## 4. Mensaje central (la historia en una frase)

> Cerrar las dos tiendas de barrio parece lógico porque pesan 2 % de las ventas, pero sus productos venden unas
> 7 veces menos de lo que venderían en un supermercado Tipo 1, y probarlo cuesta una tienda y tres meses.

Orden: el problema, los datos, el análisis (el modelo entra en una o dos láminas, sin justificar el algoritmo),
la decisión. El modelo aporta una segunda estimación **con rango** del dinero en juego y dice si las metas del
piloto son realistas. No se vende como prueba de que convertir la tienda funciona: eso solo lo prueba el piloto.

## 5. Retroalimentación que hay que ver aplicada

Fuente real: `Actividades Breiner Martinez/Momento2/retroalimentacion_sustentacion_m2.md` (transcripción de la
sustentación del M2). Léela completa antes de auditar. Lo que dijo el profesor, y qué hacer:

1. **El storytelling estuvo muy bien llevado: conservarlo.** No reordenes la historia ni la rompas para meter el
   modelo. El modelo se agrega al análisis, no reemplaza nada.
2. **Peras con manzanas.** Su objeción no es solo de tamaño: una tienda de barrio y un supermercado, aunque ambos
   sean pequeños, son **tipologías distintas** (otro foco de negocio). Quiere comparar "peras con peras", con una
   subsegmentación. Qué hacer: la base de comparación es siempre Supermercado Tipo 1 y las comparaciones se
   emparejan por tipo y nivel de ciudad; el pitch dice de frente que el dataset no trae un par exacto de una
   tienda de barrio; y la conversión se presenta como **hipótesis que el piloto prueba**, no como hecho.
3. **Las preguntas que él mismo se hizo** (dos tiendas contra ocho supermercados): dónde están ubicadas, si están
   ubicadas estratégicamente, si hay supermercados alrededor, si les sirve ampliarse o conviene cerrar y
   reubicar. Responde con el dataset lo que se pueda (`Outlet_Location_Type` y las tiendas de su misma ciudad) y
   di claramente lo que no se puede (ubicación exacta, espacio, costos). No inventes datos. La explicación del
   equipo en el Q&A (el supermercado cercano le quita clientes) es una hipótesis, no una medición: preséntala así.
4. **La simulación de vitrina.** Le preocupó que fuera "una regla de tres" sin base estadística, y dijo que eso
   puede ser el punto de quiebre de una presentación que va bien. Qué hacer: que la lámina diga con qué
   procedimiento se calculó (modelo, variables y su intervalo; ya está rehecha en la sección 6b del notebook),
   y si no se sostiene, que diga "sin efecto claro" en vez de "cero". Verifica que no quede ninguna cifra
   proveniente de una proporción simple presentada como simulación.
5. **Toda cifra dice cómo se calculó** (procedimiento o ecuación), a la vista en la lámina, y con su fila en
   `cifras_y_procedimientos.md`. Una estimación con supuestos se marca como **escenario**. Ojo con la fuente:
   esta regla no aparece en la transcripción del M2; viene de la sesión de dashboards del M1 y de la pregunta 4.
6. Retroalimentación de los dashboards del M1 (en `Momento2/transcript.docx`): cada KPI sirve al objetivo, sin
   estadísticos técnicos sin explicar, colores con significado, cifras grandes abreviadas.
7. No inventes otros comentarios del profesor. Si falta alguno, queda "pendiente de confirmar". Actualiza
   `retroalimentacion_vs_cambio.md`: las filas del pitch pasan de "recuerdo del equipo" a esta transcripción.

## 6. Reglas técnicas (cortas)

- Split 80/20 antes de todo; imputación y codificación dentro de un `Pipeline`; métrica solo en test, con gap y
  contra `DummyRegressor`. `random_state=42`.
- Nada de mover hiperparámetros ni columnas hasta que "dé bien". Importancias = asociación, no causalidad.
- El criterio de aceptación ya está escrito en `00_especificacion.md`: no se reescribe; si algo cambia, se agrega una
  "Enmienda" con fecha.
- Toda cifra sale de una celda ejecutada. Si algo no se pudo calcular, lo dices.
- No toques `clase01/` a `clase15/`, `datos/`, `README.md`, `INSTALACION.md`, `CLAUDE.md` (son del profesor).
  `dataset/train.csv` es solo lectura. No agregues análisis que no se pidieron.
- Español, términos técnicos en inglés, sin emojis. **No hagas commit ni push** hasta que lo pida.

## 7. Checklist de entrega (clase 14, jueves 19 de noviembre)

Verifica que el repo tenga: EDA corregido (M1); dashboard corregido (M2) con 3 filtros, 3 KPIs y 3 gráficos;
mínimo dos intervalos de confianza y una prueba de hipótesis; un modelo entrenado y evaluado; tres
recomendaciones en lenguaje de negocio que digan también qué no respaldan los datos; y la narrativa de una
pregunta a una decisión. Se evalúa el último commit antes de la hora de corte, que no está en el repo: pregúntame.

## 8. Lo que probablemente falta (confírmalo en la auditoría)

1. Informe técnico en PDF, generado desde el notebook, con los cuatro puntos de `clase13/reto.md`: qué se predijo y
   qué decisión respalda; regresión o clasificación y por qué; métrica en test, gap y comparación contra el modelo
   tonto; variables clave y acciones.
2. `preparacion_sustentacion.md`: respuestas cortas a por qué este problema, por qué regresión, por qué este
   algoritmo y no otro, qué se descartó, qué significa el gap, qué no se puede concluir. Salen del registro.
3. Dashboard "Explorador de Ventas BigMart" (artefacto en claude.ai, solo enlace): unificar "vitrina" y
   "visibilidad", reemplazar "correlación: -0,13" por lenguaje llano, dejar a la vista la fórmula de "unidades por
   producto", declarar su objetivo. Si no puedes editarlo, déjame la lista de cambios. Verifica que el enlace abra
   sin iniciar sesión.
4. Tiempo: el M2 duró 8 minutos y medio con 7 láminas y el pitch del M3 trae 10. El tiempo del turno del M3 no
   se conoce (el corte es duro). Cuenta cuánto toma hablar cada lámina, dime el total estimado y propón qué
   recortar, empezando por "Los datos" y nunca por "La decisión".
5. Decisiones abiertas que son mías, no tuyas: usar OUT010 como tienda de control del piloto, el costo del piloto
   (hoy "por definir") y el orden de las láminas. Pregúntame, no decidas. Antes de proponer qué ofrecer como alternativa a convertir
   OUT019 (cerrar y reubicar, ampliar), recuerda que la sustentación del M2 dejó esa pregunta abierta.

## 9. Al terminar

Resumen en pocas líneas, archivos creados o cambiados con su ruta, lo que debo confirmar con el profesor y qué
queda por commitear. Sin commit.
