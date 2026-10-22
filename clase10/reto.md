# Clase 10 · Reto — Dashboard dinámico e interactivo con Inteligencia Artificial

## 1. Contexto y propósito

El objetivo de este reto es construir una **herramienta analítica interactiva y dinámica** sobre el dataset de su proyecto Capstone, utilizando **asistencia de Inteligencia Artificial** (Claude, ChatGPT, etc.).

El propósito fundamental de esta sesión es **eliminar la fricción técnica de entornos locales, dependencias y comandos de terminal** durante el reto en aula. Lo que evaluamos hoy no es su capacidad para resolver problemas de puertos o depurar instalaciones de paquetes; lo que evaluamos es su **criterio analítico para dirigir una IA**, diseñar un artefacto reactivo y utilizarlo como un **simulador de vuelo** para descubrir hallazgos reales en sus datos.

> [!NOTE]
> **Conexión con el Momento 2 (Clase 11):**  
> El Momento 2 se sustenta en la Clase 11 mediante un turno estricto de **10 minutos** (7 min de sustentación ejecutiva navegando la herramienta interactiva en vivo + 2 min de preguntas técnicas + 1 min de rotación). El prototipo dinámico que construyan hoy valida las preguntas de investigación, filtros e hipótesis que sustentarán la próxima sesión.

---

## 2. Formato y stack libre: Cero fricción técnica

Para este reto **el stack tecnológico y el formato de despliegue son completamente libres**. Lo indispensable es que el resultado sea **una herramienta dinámica donde se puedan filtrar datos, recalcular métricas y descubrir hallazgos en vivo**:

- **Artifact interactivo en Claude:** Si utilizan Claude y genera un Artifact interactivo (React, HTML/Tailwind, Recharts, Lucide), es 100% válido. Pueden interactuar directamente en el panel de previsualización sin instalar nada.
- **Archivo HTML/JS autocontenido:** Si la IA les genera un archivo `.html` con librerías embebidas vía CDN (Chart.js, Plotly.js, D3) y los datos incrustados en JSON, es 100% válido. Abre con doble clic en cualquier navegador web.
- **Aplicación en Streamlit:** Si su equipo ya tiene el entorno local estabilizado y prefiere programar sobre la plantilla `streamlit_app_starter.py` y correr `streamlit run`, también es 100% válido.

Elijan el camino que les permita tener un **tablero interactivo funcionando en menos de 15 minutos** para dedicar el resto del bloque a explorar los datos.

---

## 3. Lo que deben tener en cuenta al dirigir la IA

Cuando redacten el encargo (*prompt*) para la IA, no pidan un "dashboard bonito". Exijan explícitamente los **5 pilares de calidad interactiva**:

```
                         LOS 5 PILARES DEL DASHBOARD DINÁMICO
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. INTERACTIVIDAD REAL  │ Controles que recalculan datos y gráficos en vivo │
 ├─────────────────────────┼───────────────────────────────────────────────────┤
 │ 2. 3 FILTROS ORTOGONALES│ Categorías independientes, fechas o rangos slider │
 ├─────────────────────────┼───────────────────────────────────────────────────┤
 │ 3. KPIs EN CABECERA     │ 3 tarjetas con unidad que reaccionan al filtrado  │
 ├─────────────────────────┼───────────────────────────────────────────────────┤
 │ 4. GRÁFICOS COORDINADOS │ Múltiples vistas (tendencia, ranking, dispersión) │
 ├─────────────────────────┼───────────────────────────────────────────────────┤
 │ 5. SÍNTESIS DINÁMICA    │ Franja de texto reactiva que enuncia el hallazgo  │
 └─────────────────────────┴───────────────────────────────────────────────────┘
```

### 1. Interactividad reactiva en tiempo real
- Cada interacción sobre los controles debe actualizar inmediatamente las métricas y las visualizaciones en el cliente sin recargas de página completas ni errores de renderizado.

### 2. Mínimo 3 controles/filtros ortogonales
- Deben filtrar dimensiones analíticas independientes:
  - Al menos una dimensión categórica (ej. municipio, categoría de producto, segmento, estado).
  - Al menos un selector de fecha o rango continuo (ej. deslizador de años, rango de edad, quintil de ingreso).
  - Un tercer control relevante (ej. tipo de evento, canal de atención, umbral de corte).
- *Regla de ortogonalidad:* Dos filtros correlacionados o redundantes (como Departamento y Capital) cuentan como uno solo.

### 3. Métricas clave (KPIs) en la cabecera
- Tres tarjetas destacadas en la parte superior con números legibles y unidades de medida explícitas (%, USD, COP, casos, días).
- Los KPIs deben ser **estrictamente reactivos**: deben recalcularse en tiempo real reflejando el subconjunto de datos filtrado.

### 4. Múltiples visualizaciones coordinadas
- Al menos 3 gráficos interactivos que respondan preguntas analíticas complementarias:
  - **Tendencia temporal:** Gráfico de línea o área para observar la trayectoria histórica.
  - **Comparación / Jerarquía:** Gráfico de barras ordenado para contrastar grupos o entidades.
  - **Distribución o dispersión:** Gráfico de caja, dispersión o histograma para revelar variabilidad y anomalías.
- Títulos de gráficos redactados como afirmaciones o conclusiones, no simples nombres de variables.

### 5. Franja de hallazgo o síntesis dinámica
- Un bloque informativo destacado (`st.info`, banner de alerta o tarjeta de texto) que enuncie automáticamente el hallazgo principal derivado de los filtros seleccionados (ej. *"Bajo esta selección, la categoría X concentra el 64% de las incidencias superando la media histórica"*).

---

## 4. Instrucciones de ejecución paso a paso (Bucle con IA)

Apliquen el bucle de trabajo aprendido en la Clase 3:

```
[1. Especificar] ────► [2. Generar con IA] ────► [3. Probar Controles] ────► [4. Descubrir]
(Definir 5 pilares)     (Claude / GPT / etc.)     (Auditar reactividad)      (Extraer insight)
```

### Paso 1 — Especificar el encargo (10 min)
1. Suban su dataset (o una muestra representativa de 100-500 filas con el esquema exacto de columnas) a la herramienta de IA (Claude, ChatGPT, etc.).
2. Envíen un encargo estructurado. Por ejemplo:
   > *"Actúa como un ingeniero y diseñador de dashboards analíticos senior. A partir de este dataset de [tema], genera un dashboard interactivo completo en [Artifact interactivo de React / archivo HTML autocontenido con Tailwind y Chart.js / Streamlit]. Requisitos estrictos: 1) Barra con 3 filtros ortogonales ([nombrar variables]); 2) Cabecera con 3 tarjetas de KPI reactivas con sus unidades ([métrica 1, 2, 3]); 3) 3 gráficos coordinados interactivos: línea temporal, barras comparativas ordenadas y distribución; 4) Franja de síntesis dinámica que resuma el insight de los datos filtrados; 5) Guardas defensivas para que la interfaz nunca se rompa si se desmarcan los filtros. Los controles deben modificar los datos en tiempo real."*

### Paso 2 — Generar y previsualizar (15 min)
1. Permitan que la IA construya el artefacto.
2. Si genera un **Artifact de Claude**: interactúen con él directamente en la ventana de previsualización.
3. Si genera un **HTML autocontenido**: guarden el código en un archivo `dashboard.html` en su máquina y ábranlo con doble clic en Google Chrome o Safari.
4. Si optan por **Streamlit**: peguen el código en `streamlit_app_starter.py` y córranlo con `streamlit run`.

### Paso 3 — Probar los controles y blindaje (15 min)
1. Desmarquen opciones y muevan los deslizadores a valores extremos.
2. Comprueben que los 3 KPIs cambien efectivamente de valor.
3. Si la app se rompe o los gráficos se congelan, pídanle a la IA el ajuste puntual especificando el síntoma exacto.

### Paso 4 — Explorar y documentar hallazgos (10 min)
1. Manipulen el dashboard para aislar combinaciones interesantes de variables.
2. Identifiquen al menos **un hallazgo o patrón inesperado** que no fuera evidente a simple vista en una tabla estática.

---

## 5. Dinámica de presentación y cierre del reto (10 min)

Al finalizar el bloque práctico se realizará la ronda de demostración y retroalimentación:

1. **Pantalla compartida o rotación rápida:** Cada equipo proyecta su dashboard dinámico en pantalla completa.
2. **Interacción en vivo:** Un integrante del equipo manipula los controles en tiempo real frente al docente o a un equipo evaluador (demostrando que los KPIs y gráficos reaccionan de inmediato).
3. **Pitch de descubrimiento (60 a 90 segundos):**
   - El equipo responde: *"¿Qué descubrimos explorando los datos con este simulador que no sabíamos antes?"*.
   - Explican el insight formulado a partir de la franja de síntesis dinámica.

---

## 6. Criterios de calidad y penalizaciones

| Criterio | Nivel Esperado | Penalización / Falla |
| :--- | :--- | :--- |
| **Interactividad y Dinamismo** | Los controles filtran y recalculan gráficos y KPIs en tiempo real de forma fluida. | Gráficos estáticos, imágenes fijas o controles que no tienen efecto sobre los datos. |
| **Regla de 3 Controles** | Mínimo 3 controles ortogonales (categorías y rangos continuos). | Menos de 3 controles o filtros dependientes redundantes. |
| **Reactividad de KPIs** | 3 métricas con unidades explícitas que cambian según el filtro. | KPIs fijos que no varían o métricas sin unidades. |
| **Coordinación Visual** | 3 visualizaciones complementarias (tendencia, ranking, dispersión). | Gráficos repetitivos o escalas aplastadas por falta de limpieza. |
| **Techo de 5 Elementos** | Máximo 5 filtros y 5 gráficos. Foco cognitivo y jerarquía clara. | **Penalización directa:** Interfaces saturadas con más de 5 filtros o más de 5 gráficos. |
| **Capacidad de Descubrimiento** | El equipo articula un hallazgo claro derivado de la interacción con el tablero. | No poder explicar qué revela la herramienta o limitarse a describir la interfaz. |
