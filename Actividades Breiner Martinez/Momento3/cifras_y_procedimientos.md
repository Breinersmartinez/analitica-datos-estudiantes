# Cifras y procedimientos (regla de trazabilidad)

Cada cifra que aparezca en el notebook, el dashboard, las láminas o el informe tiene aquí su procedimiento.
Este archivo se amplía en las fases 3 a 7 (inferencia, modelo, recomendaciones). Hoy cubre las cifras del
pitch del M2, recalculadas con `scripts/verificar_cifras_m2.py` (resultado completo en
`datos_procesados/cifras_m2_recalculadas.csv`, 38 de 38 coinciden con el pitch dentro del redondeo).

Limpieza usada, igual a la del M1: variantes de grasa unificadas; `Item_Visibility = 0` (526 filas) tratada como
dato no registrado y rellenada con la mediana del mismo producto en las otras tiendas (respaldo: mediana del
tipo de producto). Es descriptiva y se calcula sobre todo el dataset. Para el modelo se rehace dentro del
`Pipeline`, ajustada solo con train.

Notación: "Tipo 1" = `Outlet_Type == "Supermarket Type1"` (5.577 filas); "abarrotes" = tienda de barrio =
`Grocery Store` (OUT019 y OUT010, 1.083 filas); "vitrina" = `Item_Visibility` x 100, el % del área de exhibición
que ocupa el producto. Cada fila del dataset es un producto en una tienda, con su venta del año.

## Cifras del pitch del M2

| Lámina | Cifra | Procedimiento | Valor recalculado |
|---|---|---|---|
| 1 | 18,6 M de ventas | suma de `Item_Outlet_Sales` | 18.591.125 |
| 1 | 368 mil en las dos tiendas de barrio | suma de ventas en abarrotes | 368.034 |
| 1 | "solo cae 2 %" | ventas abarrotes / ventas totales x 100 | 1,98 % |
| 2 | DRL01: 935 contra 6.300 | `Item_Outlet_Sales` de la fila DRL01 en OUT019 y en OUT049 | 934,8 y 6.309,8 |
| 2 | Precio 233 contra 235; vitrina 13,5 % contra 7,7 % | `Item_MRP`; `Item_Visibility` x 100 de esas filas | 233,0 / 235,4; 13,5 / 7,7 |
| 3 | 898 productos en ambos formatos | intersección de `Item_Identifier` entre abarrotes y Tipo 1 | 898 |
| 3 | 100 % vende más en el supermercado | por producto, venta media en Tipo 1 > venta media en abarrotes | 100 % |
| 3 | "7,5 veces más" | **mediana**, sobre los 898 productos, de (venta media en Tipo 1) / (venta media en abarrotes) | 7,50 |
| 3 | Misma ciudad: 7,3 (nivel 1) y 8,5 (nivel 3) | igual, contra los supermercados de la misma ciudad: OUT019 contra OUT046 y OUT049 (445 productos); OUT010 contra OUT013, OUT018 y OUT027 (522) | 7,25 y 8,50 |
| 4 | 308 productos comunes; OUT046 vende 7 veces más | mediana de ventas OUT046 / ventas OUT019 en esos 308 | 7,00 |
| 4 | OUT019 vende 340; supermercados entre 2.278 y 2.439 | venta media por tienda; el rango es de los **Tipo 1 con tamaño registrado** (OUT013, OUT035, OUT046, OUT049) | 340,3; 2.277,8 a 2.438,8 |
| 4 | OUT046 maneja 930 productos, OUT019 528 | número de filas de cada tienda | 930; 528 |
| 5 | Vitrina 10,8 % contra 6,5 % (1,7 veces) | media de vitrina en abarrotes y en los tres tipos de supermercado | 10,80; 6,49; 1,66 |
| 5 | 340 contra 2.449 | venta media en abarrotes y en **los tres tipos de supermercado juntos** | 339,8; 2.449,3 |
| 5 | Vitrina extra: ventas extra cercanas a cero | regresión lineal de ventas sobre vitrina y precio, con efecto de cada tienda; vitrina adicional de las filas de abarrotes | -0,09 % de la cadena con +100 % (aproximación) |
| 5 | Correlación vitrina-ventas "prácticamente nula" | Pearson dentro de cada grupo | -0,014 (supermercados), 0,018 (abarrotes) |
| 6 | 1.976 menos por producto | media de ventas Tipo 1 - media de ventas abarrotes | 1.976,4 |
| 6 | 2,1 M al año; 11,5 % de la cadena | 1.976,4 x 1.083 filas; esa cifra / ventas totales | 2.140.390; 11,5 % |
| 6 | 6,4 M a 3 años; 10,7 M a 5 | brecha anual x 3 y x 5. **Escenario**: supone brecha constante, sin crecimiento ni descuento | 6,42 M; 10,70 M |
| 7 | Piloto x1,5, x2, x3: 90 mil, 180 mil, 359 mil | ventas anuales de OUT019 (179.694) x (factor - 1). **Escenario** | 89.847; 179.694; 359.388 |

Comprobación cruzada: la brecha medida solo sobre los 898 productos comunes (promedio de 1.982 por producto,
aplicado a las 1.079 filas de abarrotes con producto común) da 2.139.000. Controlar por producto no cambia los
2,1 M.

## Observaciones de trazabilidad sobre el pitch (para corregir en la versión del M3)

1. **"7,5 veces" es una mediana.** Con otras estadísticas da otro número: cociente de las medias 6,83; media de
   los cocientes 8,94. La lámina debe decir "mediana".
2. **Dos bases de comparación mezcladas.** La lámina 5 compara 340 con 2.449 (los tres tipos de supermercado);
   las láminas 6 y 7 usan Tipo 1 (2.316). Ambas son correctas, pero la lámina 5 debe decir de cuál habla.
3. **El rango 2.278 a 2.439** de la lámina 4 es de los supermercados **Tipo 1** con tamaño registrado. El texto
   dice "los supermercados": OUT018 (1.995) y OUT027 (3.694) quedan fuera del rango.
4. **La simulación de vitrina** no se puede reproducir exactamente: el código del pitch no está en el
   repositorio. La aproximación hecha aquí confirma el orden de magnitud (menos de 0,1 % de la cadena), no la
   especificación. El script la marca como aproximación.
5. **Las fuentes "EDA, secciones 3.1, 6.4, 6.5, 7.2, 7.4"** que cita el pitch no existen en
   `Momento1/momento-1-nuestro.ipynb`: no tiene secciones numeradas. O el EDA citado es otro archivo, o hay que
   cambiar la cita por el notebook y su celda.
6. **Los techos a 3 y 5 años y los pilotos x1,5 a x3** son escenarios; ya el guion lo dice, la lámina debe dejar
   escritos sus supuestos.

7. **Mezcla de tipos (retroalimentación "peras con manzanas").** La lámina 3 compara OUT010 (nivel 3) con OUT013,
   OUT018 y OUT027, que son Tipo 1, 2 y 3: el "8,5 veces" sale inflado por el Tipo 3 (3.694 por producto). Solo
   contra Tipo 1 (OUT013, 335 productos comunes) da **7,0**. La lámina 5 usa 2.449, que es el promedio de los tres
   tipos de supermercado; contra Tipo 1 (2.316) la razón es 6,8 y no 7,2. Corregido en el notebook (sección 4b).
8. **No hay par exacto.** Ningún supermercado es del mismo formato que una tienda de barrio. La comparación contra
   Tipo 1 sigue siendo entre formatos distintos por diseño; se declara así y la prueba justa de si el formato
   importa es el piloto.

## Cifras de inferencia del Momento 3

**Sección 4b: comparación emparejada por tipo y nivel** (productos presentes en ambas tiendas; razón = mediana de
venta en la tienda de destino / venta en la de origen; diferencia con IC 95 % por t de una muestra sobre las
diferencias por producto):

| Comparación | Productos | Mediana de la razón | Diferencia media (IC 95 %) |
|---|---|---|---|
| Pitch M2, nivel 3: OUT010 contra Tipo 1 + 2 + 3 (**mezcla**) | 522 | 8,50 | 2.337 (2.206 a 2.469) |
| Nivel 3 emparejado: OUT010 contra OUT013 (solo Tipo 1) | 335 | 7,00 | 1.935 (1.782 a 2.088) |
| Nivel 1 emparejado: OUT019 contra OUT046 y OUT049 (solo Tipo 1) | 445 | 7,25 | 1.923 (1.803 a 2.042) |
| Nivel 1 y tamaño pequeño: OUT019 contra OUT046 | 308 | 7,00 | 1.955 (1.796 a 2.114) |
| Entre las dos tiendas de barrio: OUT010 contra OUT019 | 182 | 1,00 | -25 (-67 a 17), contiene el cero |

Venta media por producto según tipo de tienda: tienda de barrio 340; Tipo 1 2.316; Tipo 2 1.995; Tipo 3 3.694. El
promedio de los tres supermercados (2.449) es la base que mezclaba la lámina 5; la razón correcta contra Tipo 1 es
6,8 y no 7,2. Consecuencia para el pitch: solo hay **dos** cifras mezcladas. El "8,5 veces" de nivel 3 (lámina 3)
pasa a 7,0, y la base de 2.449 de la lámina 5 pasa a 2.316. Las demás ya comparaban contra Tipo 1 y se mantienen:
"7,5 veces" (898 productos, solo Tipo 1) y "7,3 veces" de nivel 1 (OUT046 y OUT049 son Tipo 1).

Todas salen de `momento-3-nuestro.ipynb`, secciones 1 a 6. `alfa = 0,05`, dos colas. Filas = producto en tienda;
"barrio" = 1.083 filas de abarrotes, "Tipo 1" = 5.577 filas.

| Sección | Cifra | Procedimiento | Valor |
|---|---|---|---|
| 1 | Media, desviación y mediana por formato | `mean`, `std(ddof=1)`, `median` | barrio 339,8 / 260,9 / 257,0; Tipo 1 2.316,2 / 1.516,0 / 1.990,7 |
| 2 | IC 95 % de la venta media, barrio | `stats.t.interval(0.95, df=n-1, loc=media, scale=error_estandar)`; error estándar = desviación / raíz(n) | 324 a 355 (n = 1.083) |
| 2 | IC 95 % de la venta media, Tipo 1 | igual | 2.276 a 2.356 (n = 5.577) |
| 3 | Levene (varianzas) | `stats.levene` | p menor que 0,001: varianzas distintas, justifica Welch |
| 3 | Welch: diferencia 1.976; t = 90,7; gl = 6.614; p menor que 0,001 | `stats.ttest_ind(equal_var=False)`; comprobado a mano: t = dif / raíz(s1²/n1 + s2²/n2), gl de Welch-Satterthwaite | se rechaza H0 |
| 3 | IC 95 % de la diferencia | `welch.confidence_interval()`; igual a la fórmula a mano | 1.934 a 2.019 |
| 3 | d de Cohen = 1,42; razón de medias = 6,8 | diferencia / desviación combinada; media Tipo 1 / media barrio | efecto grande |
| 3 | Mann-Whitney | `stats.mannwhitneyu`, dos colas | p menor que 0,001 |
| 4 | 898 productos comunes: diferencia media 1.982, IC 95 % 1.908 a 2.057 | por producto, media en Tipo 1 menos media en barrio; t de una muestra sobre las diferencias | t pareado = 52,3 |
| 4 | Mediana de la razón por producto = 7,50 | mediana de (media Tipo 1 / media barrio) en los 898; es la cifra "7,5 veces" del pitch | 7,50; 100 % vende más en Tipo 1 |
| 5 | Techo 2.140.390 (11,5 %); rango 2.094.124 a 2.186.656 | diferencia de medias x 1.083; extremos del IC de la diferencia x 1.083. **Escenario**; el rango solo recoge error de muestreo y supone filas independientes | rango angosto de más: el real es más ancho |
| 6 | Vitrina-ventas, barrio: r = 0,018; IC 95 % -0,041 a 0,078; p = 0,547 | `stats.pearsonr`; IC por transformación de Fisher, error estándar 1/raíz(n-3) | no se rechaza H0 |
| 6 | Vitrina-ventas, Tipo 1: r = -0,011; IC 95 % -0,037 a 0,015; p = 0,408 | igual | no se rechaza H0 |

Salvedades que van a la presentación y al informe: las filas no son independientes (un producto y una tienda
se repiten), así que los intervalos reales son más anchos que los calculados; no rechazar H0 en la vitrina es
ausencia de evidencia, no prueba de ausencia; y todo es asociación en datos de un año, no causalidad.

## Cifras del modelo del Momento 3

Todas salen de `momento-3-nuestro.ipynb`, secciones 9 a 17. Modelo elegido: **Ridge (alpha = 100)**, entrenado con
filas de Supermercado Tipo 1 y aplicado a las 1.083 filas de tienda de barrio. `random_state = 42`.

| Sección | Cifra | Procedimiento | Valor |
|---|---|---|---|
| 10 | Entrenamiento / prueba | `train_test_split(test_size=0.2, random_state=42)` sobre 5.577 filas Tipo 1 | 4.461 / 1.116 |
| 11 | Correlación precio-ventas | Pearson sobre las 4.461 filas de entrenamiento | 0,68 |
| 12 | MAE de validación cruzada | `GridSearchCV`, `KFold(5, shuffle, 42)`, scoring menos MAE, solo entrenamiento | Dummy 1.196; árbol 822; Ridge 816; Random Forest 816 |
| 12 | MAE de prueba | promedio de |venta real - predicha|, una vez por modelo | Dummy 1.229; árbol 836; Ridge 825; Random Forest 827 |
| 12 | R2 de prueba | 1 - SS_residual / SS_total | árbol 0,468; Ridge 0,476; Random Forest 0,471 |
| 12 | Gap de R2 | R2 entrenamiento - R2 prueba | árbol -0,004; Ridge -0,011; Random Forest 0,024 |
| 13 | Reducción del MAE frente al Dummy | 1 - MAE prueba del elegido / MAE prueba del Dummy | 32,9 % |
| 14 | Partición por producto | `GroupShuffleSplit(0.2, 42)` por `Item_Identifier`; mismos hiperparámetros | reducción 35,2 %; gap -0,019; prueba 1.139 filas |
| 15 | Importancia del precio | permutación sobre prueba, 20 repeticiones, scoring menos MAE | +635 de MAE; las demás variables entre -0,4 y 0,8 (ruido) |
| 16 | Ventas esperadas de las 1.083 filas como Tipo 1 | suma de la predicción del Ridge | 2.470.182 |
| 16 | Incremento anual esperado (**escenario**) | esa suma - ventas actuales de esas filas (368.034) | 2.102.148 (11,3 % de la cadena) |
| 16 | Rango 5 %-95 % del ruido de predicción | 1.000 remuestreos de residuos de prueba (`default_rng(42)`), sumados a la predicción | 2.010.395 a 2.126.665 de incremento |
| 16 | Incremento según los tres modelos | misma suma, un modelo cada vez | 2.102.148 (Ridge); 2.127.093 (árbol); 2.125.152 (Random Forest) |
| 16 | Diferencia contra el techo del M2 | incremento del modelo - 2.140.390 | -38.242 (-1,8 %); el techo cae 13.725 fuera del rango |
| 16 | OUT019: ventas esperadas / actuales | suma de la predicción sobre sus 528 filas / 179.694 | 1.198.903 / 179.694 = 6,7 veces |
| 16 | Metas del piloto como parte del incremento estimado | (meta - 1) / (6,7 - 1) | x1,5: 9 %; x2: 18 %; x3: 35 % |

Salvedades: el rango de 2,01 a 2,13 millones solo cubre el ruido fila a fila; no cubre que un formato distinto
pueda comportarse distinto. Que el modelo y el M2 coincidan es esperable (los productos de barrio tienen casi el
mismo precio medio, 140 contra 141): no es una confirmación independiente. Es asociación, no causalidad.

**Costo del piloto: supuesto abierto**, no hay dato. Por eso no se calcula retorno ni rentabilidad.

## Cifras nuevas en el pitch del Momento 3

Todas salen de `datos_procesados/resultados_m3.json`, que escribe `momento-3-nuestro.ipynb` (sección 19); el pitch
se genera con `scripts/construir_pitch_m3.py`, que lee ese archivo.

| Lámina | Cifra | Procedimiento | Valor |
|---|---|---|---|
| 2 | Meta de OUT019: 340 a 510 (piso) y 681 (meta) | venta por producto de OUT019 (179.694 / 528 = 340,3) x 1,5 y x 2 | 340; 510; 681 |
| 4 | x7,3 (nivel 1) y x7,0 (nivel 3) | mediana de la razón por producto, solo contra Tipo 1: OUT019 contra OUT046 y OUT049; OUT010 contra OUT013 | 7,25; 7,00 |
| 6 | Vitrina 10,8 % contra 6,5 % (x1,7); venta 340 contra 2.316 (x6,8) | medias en tiendas de barrio y Supermercados Tipo 1 | base Tipo 1 en las dos |
| 6 | Efecto de +50 % de vitrina: -18.523 al año, intervalo 95 % de -48.858 a +11.811 | regresión de ventas sobre vitrina y precio con efecto fijo por tienda, 6.660 filas (barrio y Tipo 1); coeficiente de la vitrina -3,17 (IC 95 % -8,36 a 2,02) x vitrina adicional de las 1.083 filas de barrio. **Escenario, aproximación reproducible; reemplaza al cálculo del M2, que no se pudo reproducir** | contiene el cero |
| 7 | 33 % menos error; 1.229 a 825; 1.116 filas de prueba | ver sección "Cifras del modelo" | 32,9 % |
| 7 | Incremento del modelo 2.102.148 contra 2.140.390 (1,8 % menos) | ver sección "Cifras del modelo" | escenario |
| 10 | Un Tipo 1 de su ciudad vende 2.313 | promedio de ventas de OUT046 y OUT049 (reemplaza 2.265, no reproducible) | 2.313,1 |
| 10 | El modelo estima 6,7 veces lo actual para OUT019; la meta x2 pide el 18 % de ese salto | ventas esperadas de las 528 filas de OUT019 (1.198.903) / 179.694; (2 - 1) / (6,7 - 1) | 6,7; 18 % |
