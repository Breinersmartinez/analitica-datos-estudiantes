# Registro de experimentos del modelo

Qué se probó, qué salió y por qué se mantuvo o se descartó. Las cifras salen de `momento-3-nuestro.ipynb`
(secciones 12 a 16); cada configuración de la grilla está en `datos_procesados/registro_experimentos.csv`.
Todo con `random_state=42`. Entrenamiento 4.461 filas, prueba 1.116 (Supermercado Tipo 1, partición 80/20).

## 0. Lo que ocurrió antes del modelo final (hay que decirlo)

Antes de escribir el criterio de aceptación se corrió una **exploración rápida**, fuera del notebook, con
cinco modelos con hiperparámetros por defecto o de ejemplo: Dummy, Ridge, árbol de profundidad 3, Random Forest
y Gradient Boosting. Resultó viable (R2 de prueba cerca de 0,47). **Gradient Boosting no pasó al modelo final**: no
mejoraba al Ridge en esa exploración (R2 0,45) y se prefirió una comparación más corta (árbol, Ridge, Random
Forest) para limitar las configuraciones probadas. No se retomó después de ver resultados finales. Esa
exploración no se reporta como resultado; el criterio de aceptación declara que existió.

## 1. Experimentos del modelo final

| Modelo | Grilla probada (5 particiones, MAE, solo entrenamiento) | Elegida | MAE de validación cruzada | R2 prueba | MAE prueba | Gap de R2 |
|---|---|---|---|---|---|---|
| Dummy (media) | sin parámetros | strategy = mean | 1.196,5 | -0,000 | 1.229,2 | 0,000 |
| Árbol de decisión | `max_depth` en {2, 3, 5, 8} x `min_samples_leaf` en {1, 20, 50} (12 configuraciones) | profundidad 3, hoja mínima 20 | 822,0 | 0,468 | 836,0 | -0,004 |
| Ridge | `alpha` en {0,1, 1, 10, 100} (4) | alpha = 100 | 816,0 | 0,476 | 825,4 | -0,011 |
| Random Forest | `max_depth` en {5, 10, None} x `min_samples_leaf` en {5, 20}, 200 árboles (6) | profundidad 5, hoja mínima 5 | 816,2 | 0,471 | 827,3 | 0,024 |

**Elegido: Ridge (alpha = 100).** Los tres modelos quedaron a menos de 1 % del mejor MAE de validación cruzada (816,0 a
822,0), así que por la regla fijada antes de entrenar ganó el más simple. Ninguno tiene gap de R2 de 0,05 o más.

## 2. Lo que no funcionó o no aportó

- **Los modelos complejos no le ganan al lineal.** Random Forest y árbol dan el mismo error que Ridge. La relación
  que el modelo aprende es sencilla: casi toda la señal está en el precio de lista (correlación de 0,68 con las
  ventas en entrenamiento). Un algoritmo más sofisticado no tiene más que aprender con estas variables.
- **Las demás variables no aportan.** Por permutación, solo `Item_MRP` empeora el MAE al desordenarse (unos 635).
  El resto queda entre -0,4 y 0,8, dentro del ruido (desviación de 0,2 a 0,8). Peso, vitrina y tipo de producto
  no se relacionan con las ventas dentro de Tipo 1.
- **R2 moderado.** Alrededor de 0,47: el modelo explica menos de la mitad de la variación. El resto es variación
  entre productos y tiendas que estas columnas no capturan. No se buscó subirlo (moverlo no era el objetivo).
- **Gap negativo.** El R2 de prueba es ligeramente mayor que el de entrenamiento en Ridge y árbol. Es ruido de la
  partición (1.116 filas), no una virtud: no se interpreta como que el modelo generaliza mejor que ajusta.

## 3. Pruebas de robustez

- **Partición por producto** (ningún producto de prueba aparece en entrenamiento; entrenamiento 4.438, prueba
  1.139): Ridge reduce el MAE 35,2 % frente al Dummy (32,9 % en la partición aleatoria), gap de R2 de -0,019. La
  métrica no depende de haber visto el producto en otra tienda.
- **Los tres modelos dan casi lo mismo al aplicarse a las tiendas de barrio:** incremento anual esperado de
  2.102.148 (Ridge), 2.127.093 (árbol) y 2.125.152 (Random Forest). El rango entre modelos es de 25 mil.

## 4. Hipótesis que se dejaron de probar a propósito

- Subir o bajar hiperparámetros hasta mejorar la prueba: no se hizo. La prueba se usó una vez por modelo.
- Agregar variables de la tienda (`Outlet_*`) o el identificador de producto: dejadas fuera por la regla de fuga y
  de extrapolación (ver sección 9 del notebook).
- Segundo objetivo (clasificar productos de ventas altas, o segmentar tiendas): descartados en la especificación
  porque no sustentan el llamado a la acción del pitch.
