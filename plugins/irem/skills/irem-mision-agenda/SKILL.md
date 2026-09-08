---
name: irem-mision-agenda
description: Redacta la agenda de una misión del equipo digital de la IREM y la entrega en Word con el formato institucional IREM/BID, sea una misión de definición de alcance, de capacitación o de monitoreo y acompañamiento. Úsala cuando alguien diga "hazme la agenda de la misión", "agenda de misión a [país]", "borrador de agenda", "agenda de la capacitación", "necesito la agenda para la misión de [tema]", o traiga notas, correos o una versión anterior para convertirlos en la agenda formal. Se ocupa del contenido y de la estructura; el formato lo aplica irem-word-formato al final. No la uses para el informe posterior a la misión (esa es irem-mision-informe).
---

# Agenda de misión IREM

Una agenda de misión no es un cronograma: es el documento que la contraparte lee
antes de comprometer a su gente, y con el que después se juzga si la misión hizo
lo que dijo que iba a hacer. Por eso lleva objetivos, productos esperados y
metodología, y no solo la tabla de horas. Esta skill se ocupa de ese contenido.
El formato institucional (encabezado con los logos IDB y mesoamerica MALARIA,
Calibri 12, títulos en romanos, tablas con encabezado gris) lo aplica
`irem-word-formato` en el último paso.

## Regla de oro

**Nunca inventes contenido.** Estas agendas se envían a ministerios de salud,
al BID y a contrapartes de gobierno que reservan personal y transporte por lo
que dice el documento. Una hora inventada, un nombre mal puesto o un
participante que nadie confirmó tiene consecuencias reales.

Si algo falta hay dos salidas y ninguna más: preguntárselo al usuario, o
escribir "Por confirmar" en el documento. Nunca la tercera, que es rellenar
algo plausible.

## Los tres tipos de misión, un solo esqueleto

El equipo digital hace tres clases de misión y las tres usan la misma
estructura. Lo que cambia es el énfasis y una o dos secciones añadidas:

| Tipo | Para qué | Qué añade |
|---|---|---|
| Definición de alcance | Levantar cómo funciona hoy un proceso y qué necesita cada actor | Nada: el esqueleto base le basta |
| Capacitación | Formar a facilitadores o a usuarios finales en una herramienta | *Contenido de la capacitación* y, si es formación de formadores, *Rol de los facilitadores* |
| Monitoreo y acompañamiento | Verificar el uso de una herramienta ya desplegada y reforzar donde haga falta | Metodología más extensa, en secuencia |

El detalle de cada variante está en `plantilla/bloques-por-tipo.md`. Léelo cuando
sepas de qué tipo es la misión.

## La estructura

Secciones numeradas en romanos, siempre en este orden:

| # | Sección | Contenido |
|---|---|---|
| — | Cabecera | Título en dos líneas (`Agenda de Misión` y el título descriptivo), **Fechas:** y **Lugar:** |
| I | Antecedentes | Dos párrafos como máximo: el marco de la IREM en ese país y componente, y el disparador concreto de esta misión |
| II | Objetivo general | Una frase en infinitivo que nombre el resultado, no la actividad |
| III | Objetivos específicos | Entre tres y seis viñetas en infinitivo, verificables |
| IV | Productos esperados | Viñetas: qué queda al cerrar la misión. Se titula así en los tres tipos de misión |
| V | Metodología | **Párrafos narrativos, nunca viñetas.** Enfoque, una línea de trabajo por párrafo en el orden en que ocurren, y el cierre |
| VI | Participantes | Viñetas por institución. IREM/BID va en la última, con nombres |
| VII | Agenda detallada | Un subtítulo por día y su tabla: Hora, Actividad, Participantes, Lugar |
| VIII | Requerimientos técnicos y logísticos | Viñetas |
| IX | Requerimiento de movilidad | Frase de entrada y viñetas de traslados, indicando el día de cada uno |
| X | Anexos | Opcional: listas de usuarios, temarios, formatos |

`plantilla/esqueleto.md` ya trae este esqueleto con el marcado que entiende
`irem-word-formato`. Parte siempre de ahí.

### La agenda detallada

Un bloque por día, con subtítulo en negrita y tabla propia:

```
\anchos 14 44 26 16

### Día 1, lunes 20 de octubre. Santo Domingo: CECOVEZ y DTIC
| Hora | Actividad | Participantes | Lugar |
|---|---|---|---|
| 8:30 a 11:00 | Apertura con CECOVEZ: objetivos de la misión y confirmación de la disponibilidad de los participantes<br>Presentación de los avances de la herramienta | CECOVEZ<br>IREM/BID | Oficinas CECOVEZ |
```

Reglas de la tabla:

- Las cuatro columnas son fijas y siempre en ese orden. La columna *Lugar* es la
  que evita las confusiones logísticas cuando la misión se mueve entre oficinas
  y campo; si el lugar no aplica (un traslado, un almuerzo), la celda va vacía.
- El subtítulo del día dice fecha, ciudad y foco del día. Sin guion largo.
- Horas en formato de 24 horas y rangos con la palabra "a": `9:00 a 12:00`.
  Nunca am/pm, nunca guion entre las horas.
- Traslados, almuerzos y la puesta en común interna del equipo son filas de la
  agenda como cualquier otra. Un día que no los incluye está mal planificado.
- El detalle de una actividad va en la misma celda tras `<br>`, no en una fila
  nueva.
- Participantes agrupados por institución, una por línea con `<br>`, y el
  criterio de asignación a grupos se explica una sola vez, no en cada celda.

## Cómo escribir

Estas reglas son el motivo por el que existe la skill. Aplícalas sin excepción.

- **Tercera persona impersonal.** "La misión combina", "se realiza", "se
  presenta". Nunca "vamos a", "queremos", "nuestro equipo".
- **Nada de introducciones largas.** Antecedentes son dos párrafos. Si el tercero
  aparece, sobra.
- **Objetivos en infinitivo,** un verbo principal cada uno. Un objetivo que
  necesita dos verbos son dos objetivos, o es una actividad disfrazada.
- **Nombre completo de la institución la primera vez,** con la sigla entre
  paréntesis, y la sigla de ahí en adelante.
- **Sin guiones largos ni medios.** Paréntesis, dos puntos o coma.
- **Sin relleno valorativo.** Fuera "muy", "sumamente", "cabe destacar", "es
  importante mencionar", "exitosa jornada", "espacio enriquecedor".
- **Un verbo por frase y frases cortas.** Si una frase pasa de tres líneas,
  pártela.
- **Productos esperados como estados verificables,** no como actividades
  cumplidas: "el equipo local utiliza el tablero para el seguimiento del
  piloto", no "se presentó el tablero". Un producto puede ser un entregable (un
  flujo levantado, una hoja de ruta) o una capacidad instalada (un grupo que usa
  la herramienta); las dos formas caben en la sección.
- **Lo no confirmado se escribe "Por confirmar".** Y se le avisa al usuario de
  qué quedó así.

## Cómo trabajar

### 1. Lee todo el material antes de preguntar nada

El usuario puede traer notas de planificación, un correo con la contraparte, la
agenda de una misión anterior o un borrador a medias. Léelo completo primero.
Preguntar por algo que ya estaba en las notas es la forma más rápida de perder
su confianza.

Si hay una agenda anterior del mismo país o de la misma herramienta, úsala: los
participantes institucionales, las sedes y los tiempos de traslado se repiten.

### 2. Identifica el tipo de misión y lee su bloque

Definición de alcance, capacitación o monitoreo. Si el material no lo aclara, es
la primera pregunta. Después lee `plantilla/bloques-por-tipo.md`.

### 3. Pregunta por los huecos, en un solo mensaje

Preguntas numeradas y agrupadas, para que pueda responder de corrido. Una
pregunta vale la pena si su respuesta cambia el documento:

- **Siempre**: fechas, ciudades y sedes, qué instituciones participan y con qué
  unidades, y quién va por la IREM.
- **Del contenido**: el disparador de la misión (una fase nueva, un acuerdo, una
  solicitud), y los objetivos si el material no los trae explícitos.
- **De la logística**: cuántos días, qué se hace cada día, tiempos de traslado
  entre puntos, y si hay que reservar vehículo o sala.
- **De la capacitación, si aplica**: cuántos grupos, qué temario, qué
  dispositivos se necesitan.

Dos rondas de preguntas como máximo. Si tras la segunda sigue faltando algo, va
como "Por confirmar" y se sigue.

### 4. Escribe el contenido en un `.md`

Copia `plantilla/esqueleto.md` y rellénalo. El usuario revisa este archivo, no el
Word: corregir contenido aquí es barato y recompilar cuesta un comando.

### 5. Pasa el verificador

```sh
python plantilla/revisar.py CONTENIDO.md
```

Comprueba la estructura (secciones que faltan, tablas de agenda sin las cuatro
columnas, días sin tabla, objetivos que no empiezan en infinitivo, metodología
en viñetas) y la redacción (guiones largos, horas en am/pm, rangos con guion,
primera persona, relleno valorativo, marcadores sin rellenar).

Lo que salga en `FALTA` se corrige antes de compilar. Lo que salga en `REVISAR`
casi siempre es una buena pregunta para el usuario.

### 6. Compila al formato institucional

Desde la carpeta de esta skill:

```sh
uv run --with python-docx python ../irem-word-formato/generar.py CONTENIDO.md "Agenda mision PAIS MES AÑO.docx"
```

El encabezado con los dos logos viene de la plantilla, así que no hay que
insertar imágenes a mano. Si algo del formato hay que decidirlo (una tabla
demasiado ancha, anchos de columna, una fuente distinta), invoca
`irem-word-formato` y sigue sus instrucciones en vez de improvisar.

### 7. Entrega las dos cosas

Devuélvele el `.docx` y también el `.md`. Dile explícitamente qué quedó como
"Por confirmar", para que lo cierre antes de enviarlo a la contraparte.

## Criterios de calidad

Antes de entregar, comprueba:

- Cada objetivo específico tiene al menos una actividad en la agenda que lo
  cumple. Un objetivo sin actividad es un objetivo que la misión no va a lograr.
- Cada actividad de la agenda responde a algún objetivo. Si no responde a
  ninguno, o falta un objetivo o sobra la actividad.
- Los días cuadran: horas sin solapes, traslados con su duración real, almuerzo
  incluido y ninguna jornada que termine después de las 18:00 sin motivo.
- Los participantes de las celdas existen en la sección VI.
- Los requerimientos de movilidad cubren todos los traslados de la agenda, con
  el día indicado.
- La metodología está en párrafos y explica cada línea de trabajo que aparece en
  la agenda.

## Errores frecuentes

- **Entregar solo la tabla de horas.** Sin objetivos y sin metodología la
  contraparte no sabe qué se le está pidiendo.
- **Metodología en viñetas.** Va en párrafos: es un argumento encadenado, no una
  lista de actividades.
- **Objetivos que son actividades.** "Realizar la capacitación" no es un
  objetivo, es la agenda. El objetivo dice para qué sirve la capacitación.
- **Olvidar los traslados y los almuerzos.** Es lo primero que la contraparte
  mira, porque es lo que tiene que organizar.
- **Copiar la agenda anterior sin cambiar los nombres.** Ha pasado. Revisa cada
  nombre y cada sede.
- **Repetir la lista completa de participantes en cada celda de la tabla.** Se
  agrupa por institución y el criterio se explica una sola vez.
