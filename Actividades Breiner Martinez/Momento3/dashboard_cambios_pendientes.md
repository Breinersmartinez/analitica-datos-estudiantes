# Dashboard "Explorador de Ventas BigMart": cambios pendientes

El dashboard es un artefacto de Claude (tipo Dashboard) que **solo existe como enlace**: no se puede exportar ni
editar desde el repositorio. Enlace: `https://claude.ai/artifact/8p1y9sXhXY3PJ36WjHdXkB`. Esta lista es para quien lo
edite directamente en claude.ai. Se revisó solo por capturas de pantalla (2026-11-13); no se probó en vivo.

## Qué cumple hoy

- Mínimos de la clase 14: 4 filtros (tipo de tienda, categoría, año de apertura, precio de lista), 4 KPIs (ventas
  totales, venta promedio por producto, unidades por producto, registros) y 3 gráficos (venta por tienda,
  visibilidad, precio). Se piden 3, 3 y 3.
- Retroalimentación ya aplicada: títulos en forma de pregunta, subtítulos que dicen cómo se calcula, color fijo por
  tipo de tienda, texto de lectura, cifras abreviadas (18,6 M).

## Qué cambiar (cuatro ajustes de redacción, ninguno toca la lógica)

1. **Unificar el término.** El dashboard dice "visibilidad" y el pitch dice "vitrina". Elegir uno en los dos sitios.
   (Si el dashboard conserva "visibilidad", el pitch ya aclara en la lámina 3 que es lo mismo.)
2. **Quitar el estadístico técnico del texto de lectura.** Hoy dice "Los productos más visibles venden un poco menos
   (correlación: -0,13)". El profesor pidió no mostrar "r = ..." al usuario final sin explicarlo. Alternativa:
   "Dentro de cada tipo de tienda, tener más espacio de exhibición no cambia lo que se vende."
3. **Dejar a la vista la fórmula de "unidades por producto".** Hoy dice "Aproximadas: ventas ÷ precio de lista".
   Añadir que es una estimación, no un conteo de unidades vendidas.
4. **Declarar el objetivo del dashboard** en una línea bajo el título. Propuesta: "Para decidir si las tiendas de
   barrio se transforman: compara cuánto vende cada producto en cada tipo de tienda."

## Comprobaciones que solo se pueden hacer con el dashboard abierto

- **Que el enlace abra sin iniciar sesión.** En la sesión del M1 el profesor preguntó si el enlace permitía ver sin
  autenticarse. Desde la sesión de trabajo el artefacto se pudo leer como público, pero confirmarlo abriéndolo en una
  ventana de incógnito.
- **Filtros que no dejan la vista vacía.** Probar combinaciones (por ejemplo, solo "Tienda de barrio" con un rango
  de precio alto) y comprobar que se muestra un aviso en vez de un gráfico en blanco. El profesor lo señaló en otros
  dashboards.
- **Que "Registros" cambie al mover los filtros** (la nota del panel lo promete).
- **Que cada KPI sirva al objetivo**: si alguno no ayuda a decidir sobre las tiendas de barrio, quitarlo.
