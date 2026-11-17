# Preparación para las preguntas de la sustentación (no se entrega)

Respuestas cortas, en lenguaje llano, para las preguntas que el profesor hará **después** de la exposición. En las
láminas no se justifica nada de esto. Cada respuesta sale de un archivo del proyecto; si una pregunta no tiene
respuesta aquí, la honesta es "eso los datos no lo dicen". Las preguntas 1 a 4 vienen de lo que el profesor ya dijo en la
sustentación del M2 (`Momento2/retroalimentacion_sustentacion_m2.md`).

## Sobre lo que ya objetó

**1. "¿Cómo saben que una tienda pequeña equivaldría a un supermercado pequeño?"** No lo sabemos, y lo decimos: son
tipologías distintas. No existe en los datos una tienda de barrio de otra cadena para compararlas; solo hay dos y se parecen
entre sí (340 y 339 por producto). Por eso la comparación contra Tipo 1 es una hipótesis y el piloto es lo que la prueba. Lo
que sí hicimos fue no mezclar tipos de supermercado: comparamos solo contra Tipo 1 y emparejando por ciudad.
*Archivo:* notebook, sección 4b.

**2. "¿Dónde están ubicadas, están bien ubicadas, hay más tiendas alrededor?"** No lo sabemos. El dataset solo trae el nivel
de la ciudad, no la ubicación exacta, ni los supermercados cercanos, ni el espacio, ni los costos. Nuestra explicación del Q&A
del M2 (el supermercado cercano le quita clientes) es una hipótesis, no una medición. *Lámina 2.*

**3. "¿Cómo simularon la visibilidad? ¿Tienen un proceso estadístico?"** La simulación del M2 era una proporción simple y la
rehicimos: regresión de ventas sobre vitrina y precio con efecto fijo por tienda, solo tiendas de barrio y Tipo 1. El
coeficiente es -3,17 con intervalo de -8,36 a 2,02, que contiene el cero. Con +50 % de vitrina el efecto estimado es de menos 18
mil al año (de menos 49 mil a más 12 mil): sin efecto claro. Tampoco demuestra que no exista efecto. *Notebook, sección 6b.*

**4. "¿Y si cerráramos y reubicáramos las tiendas, o las ampliáramos?"** Es una alternativa razonable y no la evaluamos: los
datos no traen ubicación, espacio ni costos para compararla con convertir. Proponemos convertir porque es lo que se puede
probar barato (una tienda, tres meses). Esta respuesta debe acordarla el equipo antes de la sustentación.

## Sobre el problema y el modelo

**5. ¿Por qué este problema de machine learning y no otro?** Porque continúa el pitch: el M2 dijo que había "2,1 millones
escondidos" y el modelo da una segunda estimación con rango. Clasificar productos de ventas altas o segmentar tiendas
(clustering) responden otras preguntas y no sustentan el llamado a la acción. *`00_especificacion.md`.*

**6. ¿Por qué regresión y no clasificación?** Porque lo que se predice es un monto y la decisión necesita un monto, no una
categoría.

**7. ¿Por qué este algoritmo y no otro? ¿Qué probaron y descartaron?** Probamos tres con grilla pequeña y validación cruzada
solo sobre entrenamiento: árbol, Ridge y Random Forest. Dieron casi el mismo error (MAE de validación entre 816 y 822), así que
por regla fijada antes de entrenar ganó el más simple, Ridge. Descartamos Gradient Boosting en una exploración previa porque no
mejoraba al Ridge, y la dejamos fuera para no multiplicar configuraciones. No movimos hiperparámetros para mejorar el
resultado. *`registro_experimentos.md`.*

**8. ¿Qué significa el gap?** La diferencia entre el R2 de entrenamiento y el de prueba. Si es grande, el modelo memorizó. Aquí
es de -0,011, es decir, no hay sobreajuste (la regla de la clase: menos de 0,05 es bien). Que sea ligeramente negativo es ruido
de la partición y no una virtud.

**9. ¿Por qué confían (o no) en el modelo?** Confiamos en lo poco que dice: reduce el error 33 % frente a predecir el
promedio y eso se mantiene con una partición por producto (35 %). No confiamos en que sea preciso: el R2 de prueba es 0,48,
explica menos de la mitad. Casi todo lo explica el precio de lista.

**10. ¿Por qué el modelo coincide con el pitch? ¿No es lo mismo dicho dos veces?** Casi. Los productos de barrio tienen casi el
mismo precio medio que los de Tipo 1 (140 contra 141), así que el modelo reproduce la misma brecha controlando por precio y
tipo de producto. No es una confirmación independiente: descarta que la brecha venga de vender productos más baratos o de otra
categoría, nada más.

**11. Una de las condiciones del criterio no se cumplió, ¿cuál?** La 7: el techo del pitch (2.140.390) cae 13.725 por encima
del rango del modelo (2.010.395 a 2.126.665). La diferencia entre las dos estimaciones es de 1,8 %, dentro del redondeo de
"alrededor de 2,1 millones". No retocamos ninguna cifra para que encajaran.

**12. ¿Qué no se puede concluir?** Que convertir la tienda cause el aumento; una cifra anual exacta; una rentabilidad (no
conocemos el costo del piloto); un efecto de la vitrina a favor o en contra; ni nada sobre ubicación, espacio o costos.

**13. ¿Qué pasa si el modelo se equivoca?** El modelo no decide nada por sí solo. Si el rango real fuera más ancho (lo es:
las filas no son independientes y extrapolamos de un formato a otro), la decisión no cambia, porque el llamado es a **probar**
con una tienda y tres meses, con una regla fijada hoy.

## Sobre la inferencia

**14. ¿Qué dice la prueba de hipótesis?** Que la diferencia de venta por producto entre formatos no es azar (Welch, t = 90,7,
p menor que 0,001), pero lo importante es el tamaño: 1.976 por producto, entre 1.934 y 2.019 con 95 % de confianza, d de
Cohen de 1,42. Con tantas filas casi cualquier diferencia sale significativa; aquí además es grande.

**15. ¿Por qué Welch y no una t normal?** Porque las varianzas son distintas (prueba de Levene, p menor que 0,001). Welch no
supone varianzas iguales.

**16. ¿Los datos son independientes?** No del todo: un producto y una tienda aparecen varias veces. Por eso los intervalos
reales son más anchos que los calculados.

## Sobre la decisión

**17. ¿Por qué empezar por OUT019 y no por OUT010?** El pitch no dio la razón explícita. La que se puede defender con los datos:
el tamaño de OUT019 sí está registrado (pequeña) y tiene dos supermercados Tipo 1 en su ciudad para compararla, entre ellos OUT046,
igual de pequeña. El tamaño de OUT010 no está registrado. **Conviene que el equipo acuerde esta respuesta antes.**

**18. ¿Cuánto cuesta el piloto?** No lo sabemos todavía: es un supuesto abierto y por eso no calculamos retorno ni rentabilidad.
La lámina 10 lo dice ("costo del piloto: por definir").

**19. ¿Por qué OUT010 como tienda de control?** Porque es del mismo formato que OUT019 y no cambia: comparar el cambio de
OUT019 con el de OUT010 compara iguales. Las dos tiendas se parecen entre sí (diferencia de -25 por producto, intervalo que
contiene el cero). Es una propuesta del equipo que no estaba en el pitch del M2.

**20. ¿Qué pasa si el piloto no llega a la meta?** La regla se fijó antes: si duplica su venta por producto, el formato pasa
a OUT010; si no sube al menos 50 %, se detiene. Los escenarios ×1,5, ×2 y ×3 (90 mil, 180 mil y 359 mil al año) son
multiplicación simple, no un pronóstico.
