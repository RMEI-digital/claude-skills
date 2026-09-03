---
name: irem-mision-informe
description: Convierte notas, transcripciones de reuniones o apuntes sueltos de una misión de campo en un informe de misión IREM completo, preguntando por el contenido que falte antes de generar el Word final. Úsala cuando alguien diga "hazme el informe de la misión", "tengo las notas de la visita", "pásame esta transcripción a informe", "reporte de misión" o "informe de la visita a [lugar]". Se ocupa del contenido; el formato lo aplica irem-word-formato al final.
---

# Informe de misión IREM

Un informe de misión no es un resumen de lo que pasó: es el registro de qué se
fue a averiguar, a quién se visitó, qué se encontró en cada punto, qué problemas
revela eso y qué se propone hacer. Esta skill se ocupa de ese contenido. El
formato institucional (logos, tipografía, tablas) no se toca aquí: lo aplica
`irem-word-formato` en el último paso.

## Regla de oro

**Nunca inventes contenido.** Estos informes van al Instituto Nacional de
Salud, al BID y a contrapartes de gobierno. Un hallazgo inventado, un nombre
mal puesto o una cifra rellenada a ojo es un daño real, no un detalle de estilo.

Si algo falta, hay dos salidas y ninguna más: preguntarle al usuario, o dejarlo
marcado como pendiente en el documento. Nunca la tercera, que es escribir algo
plausible. Lo mismo vale para los verbos: si las notas dicen "mencionan que la
positividad es del 67%", el informe dice que lo mencionaron, no que sea así.

## La estructura, y por qué es esa

Seis secciones numeradas en romanos:

| Sección | Qué contiene |
|---|---|
| I. Contexto | Por qué existe la misión: el marco de la IREM en el país, el disparador concreto (oficio, solicitud, acuerdo, con fecha y firmante) y qué se hizo en respuesta |
| II. Objetivos de Misión | Un objetivo general en infinitivo y entre dos y cuatro específicos, verificables |
| III. Agenda | Tabla de dos columnas (actividad, participantes) agrupada por día. El día es una fila de encabezado |
| IV. Principales hallazgos | Un bloque por actor visitado. Es el cuerpo del informe |
| V. Desafíos identificados | La síntesis: los problemas que revelan los hallazgos, agrupados |
| VI. Propuesta preliminar | Con quién se cerró, qué se presentó, qué se propone y qué pidió la contraparte |

Antes de las secciones van el título (dos líneas: `Reporte Interno` y el título
descriptivo), las fechas, el lugar y los participantes.

### La espina: el ciclo de vida del dato

Esto es lo que hace útil al informe y lo que hay que respetar. Cada actor de la
sección IV se cuenta en dos capas:

1. **Un párrafo que sitúa al actor**: qué es, de qué depende, qué funciones
   cumple y con qué volúmenes trabaja (personal, pruebas al mes, positividad).
   Sin este párrafo los hallazgos no se entienden.
2. **Subsecciones en cursiva que siguen el recorrido del dato**, siempre en
   este orden:

   **Registro → Consolidación → Análisis → Salida**

El nombre de la primera etapa cambia según el papel del actor, y esa elección
tiene significado:

- **Registro** si el actor genera el dato (un puesto rural, una gestora comunitaria)
- **Recolección** si va a buscarlo (la Secretaría que visita los puntos)
- **Recepción de formatos** si se lo entregan (el Laboratorio Departamental)

Y la última: **Reporte** o **Salida de la información**. Si un actor hace
registro y consolidación en el mismo acto, se juntan en
*Registro y consolidación*. **Otros** existe para lo que no cabe en la cadena.

La sección V agrupa los desafíos **por esas mismas etapas**, más *Calidad del
dato*. Esa simetría es deliberada: se levanta la información por etapa y se
sintetiza por etapa, así se ve en qué eslabón se rompe la cadena.

## Cómo trabajar

### 1. Lee todo el material antes de preguntar nada

El usuario puede traer una transcripción de reuniones, apuntes de campo, un
correo, fotos de un cuaderno o las tres cosas. Léelo completo primero. Preguntar
por algo que ya estaba en las notas es la forma más rápida de perder su
confianza.

De esa lectura saca un mapa provisional: qué actores se visitaron, qué días, y
de qué etapas del ciclo hay material para cada actor.

### 2. Enséñale el mapa y pregunta por los huecos, en un solo mensaje

Muéstrale qué actores detectaste y qué falta, en una tabla corta. Después haz
las preguntas **numeradas y agrupadas**, para que pueda responder de corrido.

Prioriza. Una pregunta vale la pena si su respuesta cambia el informe:

- **Siempre**: fechas, lugar, participantes, el disparador de la misión
  (¿qué oficio o solicitud la originó?), y los objetivos si no están explícitos.
- **Por cada actor**: las etapas del ciclo de las que no hay nada. La más
  olvidada es *Análisis*, porque en las visitas se habla de cómo se llena el
  formato y no de qué se hace con el dato.
- **Al final**: si hubo reunión de cierre y qué se acordó, y qué anexos existen.

No preguntes por lo que el usuario puede decidir que no aplica. Si no hubo
agenda formal, no hay tabla de agenda y no pasa nada.

Dos o tres rondas de preguntas como máximo. Si tras la segunda ronda sigue
faltando algo, escríbelo como pendiente visible en el documento y sigue: es
mejor un informe con tres huecos señalados que un interrogatorio sin final.

### 3. Escribe el contenido en un `.md`

Parte de `plantilla/esqueleto.md`, que ya trae el marcado que entiende
`irem-word-formato`. El usuario revisa este archivo, no el Word: corregir
contenido aquí es barato.

Reglas de redacción del informe:

- **Hallazgos en viñetas, contexto en párrafos.** Los hallazgos son
  observaciones sueltas y verificables; el contexto es un argumento encadenado.
- **Atribuye lo que es dicho.** "Mencionan", "se informa", "de acuerdo con la
  enfermera" cuando viene de una entrevista; "se observa" cuando se vio.
- **Cifras con su fuente y su fecha.** "Alrededor de 650 pruebas mensuales"
  está bien si eso es lo que dijeron; no lo conviertas en un dato duro.
- **Nombres completos de las instituciones** la primera vez, con la sigla entre
  paréntesis, y la sigla después.
- **Los desafíos llevan nombre corto y explicación**: "Consolidación manual:
  todos los actores deben sumar la información a mano, lo que afecta la calidad
  de los datos." El nombre corto es lo que se cita luego en reuniones.
- **Nada de guiones largos ni medios.** Paréntesis, dos puntos o coma.

### 4. Pasa el verificador

```sh
python plantilla/revisar.py CONTENIDO.md
```

Busca huecos de contenido, no de estilo: secciones que faltan, actores sin
párrafo de presentación, actores que cubren menos de dos etapas del ciclo,
subsecciones vacías, marcadores sin rellenar y numeración de anexos incoherente.

Lo que salga en `FALTA` se pregunta o se marca antes de compilar. Lo que salga
en `REVISAR` casi siempre es una buena pregunta para el usuario.

### 5. Compila al formato institucional

El formato lo aplica la skill hermana. Desde la carpeta de esta skill:

```sh
uv run --with python-docx python ../irem-word-formato/generar.py CONTENIDO.md INFORME.docx
```

Si algo del formato hay que decidirlo (una tabla ancha, una fuente distinta,
anchos de columna), invoca `irem-word-formato` y sigue sus instrucciones en vez
de improvisar.

### 6. Entrega las dos cosas

Devuélvele el `.docx` y también el `.md`. El `.md` es lo que va a querer editar
la próxima vez, y recompilar cuesta un comando.

Dile explícitamente qué quedó pendiente, si quedó algo. Que no lo descubra el
INS.

## Criterios de calidad

Antes de entregar, comprueba:

- Cada actor visitado tiene su párrafo de presentación y al menos dos etapas
  del ciclo.
- Los desafíos de la sección V se pueden rastrear a hallazgos concretos de la
  sección IV. Un desafío que no sale de ningún hallazgo está inventado.
- Los objetivos específicos de la sección II tienen respuesta en el informe. Si
  un objetivo era "reunir evidencia sobre formularios" y no hay ni un anexo,
  eso se dice.
- Los anexos citados en el texto existen y están numerados sin saltos.
- Ninguna cifra aparece sin saberse de dónde salió.

## Errores frecuentes

- **Contar la visita en vez del hallazgo.** "Se visitó el laboratorio y se
  conversó con dos bacteriólogas" no es un hallazgo. Lo es "el informe se llena
  a mano y no tiene serial, por lo que no es único para cada punto".
- **Saltarse el párrafo de presentación del actor** y empezar directo con las
  viñetas. El lector no sabe de qué tamaño es lo que está leyendo.
- **Desafíos que son quejas.** Un desafío dice a quién afecta y por qué
  importa, no solo que algo está mal.
- **Convertir la agenda en el informe.** La agenda es la sección III y es una
  tabla; los hallazgos no van en orden cronológico, van por actor.
- **Rellenar la propuesta preliminar** cuando la misión no llegó a proponer
  nada. Si no hubo cierre, se dice que no hubo.
