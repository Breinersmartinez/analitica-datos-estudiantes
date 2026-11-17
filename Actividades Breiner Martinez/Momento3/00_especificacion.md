# Momento 3 · Especificación del encargo (escrita antes de entrenar el modelo final)

Fecha de escritura: 2026-11-13. Este archivo no se reescribe después de ver las métricas finales. Si algo
cambia, se agrega una sección "Enmienda" con fecha y motivo, debajo, sin borrar lo anterior.

## Declaración de honestidad sobre el orden

Antes de escribir este criterio se corrió una **exploración rápida** (no el modelo final) para saber si la
formulación era viable. En ella se vio que un Ridge y un árbol superaban al modelo de la media con un R2 de
test cercano a 0,47 y que las ventas esperadas de las tiendas de barrio rondaban 2,0 a 2,1 millones por
encima de las actuales. Los umbrales de abajo se fijaron por la regla de la clase 13 y por la lógica de la
decisión, no para encajar con esas cifras, pero el equipo las conocía. Esa exploración no se reporta como
resultado.

## 1. Formulación

**Qué se predice.** `Item_Outlet_Sales` (ventas anuales de un producto en una tienda), para las 1.083 filas
de las tiendas de abarrotes (OUT019 y OUT010) **como si se vendieran en un Supermercado Tipo 1**.

**Tipo de problema.** Regresión: la variable objetivo es un número continuo y la decisión necesita un monto.

**Por qué esta formulación y no otra.** Es la que continúa el pitch del M2: el pitch afirma que hay "2,1
millones escondidos" y llama a un piloto. El modelo no abre otra discusión; da una segunda estimación
independiente de ese techo, con rango de error, y dice cuán exigentes son las metas del piloto frente a él.
Clasificar productos de ventas altas o segmentar tiendas responden otras preguntas y no sustentan el
llamado a la acción ya presentado.

**Cómo se entrena.** Solo con filas de Supermercado Tipo 1 (5.577). Variables de entrada: atributos del
producto (`Item_MRP`, `Item_Type`, `Item_Fat_Content`, `Item_Visibility`, `Item_Weight`, categoría por
prefijo del código). **Fuera de X:** `Item_Identifier`, todas las `Outlet_*`, y `Item_Outlet_Sales`.
Se predice sobre las filas de abarrotes con las mismas variables.

## 2. Para quién y qué decisión respalda

- **Decisor** (audiencia del pitch): quien aprueba el piloto. Derivado del pitch; confirmar.
- **Responsable de ejecutar:** gerencia de operaciones (así figura en la diapositiva 7 del pitch).
- **Afectados:** quienes operan OUT019 y OUT010.
- **Decisión:** aprobar o no el piloto de 3 meses que opera OUT019 como supermercado Tipo 1. El modelo informa
  cuánto de la brecha es alcanzable y si las metas del piloto (x1,5, x2, x3) son realistas.

**Objetivo SMART.** Específico: convertir OUT019 a formato Tipo 1 y medir su venta por producto contra OUT046 y
OUT049. Medible: de 340 actuales a al menos 510 (x1,5) como piso y 680 (x2) como meta. Alcanzable: el techo de
la brecha es una venta de unos 2.316 por producto (6,8 veces la actual), así que x2 es menos de un tercio del
techo. Relevante: la brecha total es el 11,5 % de las ventas de la cadena. Temporal: 3 meses, este trimestre.

## 3. Piso de comparación

`DummyRegressor(strategy="mean")` entrenado en la misma partición. Si el modelo no le gana, se dice y el
modelo no sustenta nada: la conclusión pasa a ser "solo con estos datos no hay un segundo estimado fiable".

## 4. Criterio de aceptación (todas las condiciones, escritas antes del modelo final)

1. **Partición** 80/20 con `random_state=42` hecha antes de cualquier imputación o codificación; toda
   transformación dentro de un `Pipeline` ajustado solo con train.
2. **Sin fuga:** ninguna columna de `Outlet_*`, `Item_Identifier` ni la respuesta en X. Se documenta cada
   columna descartada.
3. **Le gana al piso:** el MAE de test del modelo elegido es al menos 20 % menor que el del Dummy. Razón: una
   mejora menor no cambia lo que el decisor entiende del techo.
4. **Sin sobreajuste:** gap de R2 (train menos test) menor que 0,10 en el modelo elegido, con la regla de la
   clase (< 0,05 bien, 0,05 a 0,10 aceptable, > 0,10 sobreajuste). Un modelo con gap mayor puede reportarse,
   pero no se elige.
5. **Elección sin mirar el test:** el modelo y sus hiperparámetros se eligen con validación cruzada de 5
   particiones **solo sobre train**; el test se usa una vez por modelo.
6. **Se reporta con rango:** la estimación de ventas esperadas se entrega como rango (percentiles 5 y 95 de
   1.000 remuestreos de los residuos de test, `random_state=42`) y como **escenario** con sus supuestos, nunca
   como cifra única.
7. **Lectura contra el pitch:** si los 2,14 M del M2 caen dentro del rango, el techo queda corroborado; si caen
   fuera, el pitch cambia la cifra y lo dice. No se ajusta nada para que caiga dentro.
8. **Limitaciones dichas:** asociación y no causalidad, extrapolación de un formato a otro, R2 moderado,
   tamaño de test, y que solo el piloto prueba el efecto de convertir la tienda.

## 5. Qué diferencia mínima cambiaría una decisión

- Si el modelo no cumple 3 y 4, no se presenta como respaldo y el llamado a la acción se sostiene solo en el
  piloto, como ya estaba en el M2.
- Si el rango de ventas esperadas deja un incremento anual por debajo de unas 3 veces el costo de operar el
  piloto, la recomendación cambia. El costo del piloto **no está en los datos**: hay que pedirlo o declararlo
  como supuesto abierto.

## 6. Pendientes que no se inventan

- Retroalimentación verbal del profesor al pitch del M2: no existe por escrito. Solo se tiene lo que el equipo
  recuerda (toda cifra debe decir qué procedimiento o ecuación la produjo). Cualquier otra se agrega solo
  cuando el equipo la confirme.
- Guía de entrega, hora de corte y tiempo del turno: se anuncian en clase y por correo.
- Dashboard vigente: "Explorador de Ventas BigMart", artefacto de tipo Dashboard en claude.ai. Su contenido no se
  pudo leer desde fuera; se revisó por las capturas del equipo (2026-11-13). Cumple los mínimos: 4 filtros (tipo de
  tienda, categoría, año de apertura, precio de lista), 4 KPIs (ventas totales, venta promedio por producto,
  unidades por producto, registros) y 3 gráficos (venta por tienda, visibilidad, precio). El artefacto de Claude
  no se puede exportar: el dashboard se entrega solo como enlace, y el informe lo dice. Verificar que abra sin
  iniciar sesión.
- Costo del piloto: **supuesto abierto** por decisión del equipo (2026-11-13). Sin dato; la condición de la
  sección 5 que lo usa se reporta como no evaluable, no se estima un costo.

## Enmienda 1 (2026-11-13): retroalimentación "no revolver peras con manzanas"

No cambia el criterio de aceptación ni la formulación. Cambia cómo se comparan las cosas y qué se declara.
- La base de comparación es siempre **Supermercado Tipo 1**, nunca el promedio de los tres tipos (el modelo ya
  entrenaba solo con Tipo 1). Las comparaciones por ciudad se emparejan por tipo y nivel.
- Se declara que el dataset no tiene un par exacto de una tienda de barrio, y que el techo es la diferencia entre
  formatos, no lo que la tienda recuperaría.
- Propuesta, **pendiente de decisión del equipo** (no está en el pitch del M2): usar OUT010, que no se convierte,
  como tienda de control del piloto, además de medir OUT019 contra OUT046 y OUT049. Medir el cambio de OUT019
  contra el de OUT010 compara tiendas del mismo formato.
