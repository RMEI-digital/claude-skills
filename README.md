# claude-skills

Skills de Claude Code del equipo de **RMEI-digital**, instalables como plugin.

Una *skill* es un conjunto de instrucciones que Claude carga solo cuando hacen falta. Sirve
para que un procedimiento que alguien repite (armar una presentación con el formato
institucional, crear un repositorio como toca) quede escrito una vez y lo pueda usar todo el
equipo, en lugar de vivir en la cabeza de una persona.

En la práctica no cambia la forma de trabajar: se le pide a Claude lo que se necesita, en
lenguaje normal, y la skill se activa sola cuando viene al caso. También se puede invocar por
su nombre. Todas empiezan con `irem-`, así que escribiendo `/irem` en Claude Code aparecen
todas. El prefijo no es decorativo: es lo que las hace encontrables sin recordar el nombre
exacto.

## Las cinco skills

| Skill | Para qué sirve |
|---|---|
| [`/irem-mision-informe`](#informes-de-misión-irem-mision-informe) | Convierte notas, transcripciones o apuntes de una misión de campo en el informe completo, preguntando por lo que falte. |
| [`/irem-word-formato`](#documentos-word-irem-word-formato) | Da a cualquier documento de Word el formato institucional IREM/BID, con los logos en el encabezado. |
| [`/irem-presentacion`](#presentaciones-irem-presentacion) | Presentaciones con el formato institucional IREM/BID, en PDF o en PowerPoint editable, con las notas del presentador incluidas. |
| [`/irem-repo`](#repositorios-irem-repo) | Crea un repositorio nuevo en GitHub, privado y dentro de la organización, lo clona y deja el primer commit hecho. |
| [`/irem-security-audit`](#seguridad-irem-security-audit) | Auditoría de seguridad de un repositorio: busca secretos en todo el historial de git y revisa los controles que faltan. |

## Instalar

Dentro de Claude Code, dos comandos:

```
/plugin marketplace add RMEI-digital/claude-skills
/plugin install irem
```

Listo. Las skills quedan disponibles y se activan solas cuando vienen al caso, o se invocan
por su nombre.

Para actualizar cuando se corrija algo:

```
/plugin update irem
```

Después de actualizar hay que **abrir una sesión nueva**: las instrucciones se cargan al
arrancar, y el propio comando lo avisa.

### Si el plugin no funciona

Como el repositorio es privado, `/plugin marketplace add` necesita que tu `git` sepa
autenticarse con GitHub. Si da problemas, clona y usa el instalador:

```bash
git clone https://github.com/RMEI-digital/claude-skills.git
cd claude-skills && ./instalar.sh
```

Eso copia las skills a `~/.claude/skills/`. Funciona igual, pero hay que volver a correrlo
cada vez que el repositorio cambie.

## Informes de misión: `/irem-mision-informe`

Convierte el material crudo de una misión de campo (una transcripción de reuniones, los
apuntes del cuaderno, un correo largo, o las tres cosas) en el informe de misión completo.
Se ocupa del **contenido**; el formato lo aplica `/irem-word-formato` en el último paso.

Lo que la distingue de pedirle a Claude «resúmeme estas notas» es que conoce la estructura
real de estos informes y, sobre todo, su espina analítica: cada actor visitado se cuenta
siguiendo el **ciclo de vida del dato** (registro, consolidación, análisis, salida), y los
desafíos de la última sección se agrupan por esas mismas etapas. Esa simetría es la que
permite ver en qué eslabón se rompe la cadena, en lugar de tener una lista de visitas.

También sabe qué preguntar. La etapa que más se olvida en las visitas es *Análisis*, porque
en campo se habla de cómo se llena el formato y no de qué se hace después con el dato.

### Cómo pedirla

- «Hazme el informe de la misión a Quibdó, aquí están mis notas.»
- «Pásame esta transcripción a informe de misión.»
- «Tengo los apuntes de la visita, ármame el reporte.»

### Lo que te va a preguntar

Primero lee todo el material y te enseña un mapa de lo que encontró: qué actores se
visitaron, qué días y de qué etapas hay información. Después pregunta solo por los huecos,
en un mensaje y numerado, para que puedas responder de corrido:

- **Siempre**: fechas, lugar, participantes y el disparador de la misión (qué oficio o
  solicitud la originó, con fecha y firmante).
- **Por cada actor**: las etapas del ciclo de las que no hay nada.
- **Al final**: si hubo reunión de cierre y qué anexos existen.

Dos o tres rondas como máximo. Si después de eso sigue faltando algo, lo deja marcado como
pendiente visible en el documento en lugar de alargar el interrogatorio.

Su regla más importante: **nunca inventa contenido**. Estos informes van al INS, al BID y a
contrapartes de gobierno, así que si un dato falta lo pregunta o lo marca, pero no escribe
algo plausible. Y distingue lo observado de lo dicho: si las notas dicen «mencionan que la
positividad es del 67%», el informe dice que lo mencionaron, no que lo sea.

### Lo que entrega

| Archivo | Qué es |
|---|---|
| `INFORME.docx` | El informe con el formato institucional, listo para enviar |
| `CONTENIDO.md` | El contenido en texto plano, que es lo que vas a querer editar la próxima vez |

Te entrega los dos a propósito: corregir contenido en el `.md` es barato, y recompilar el
Word cuesta un comando.

## Documentos Word: `/irem-word-formato`

Da a un documento de Word el formato institucional IREM/BID completo: los logos del BID y de
mesoamérica MALARIA en el encabezado de todas las páginas, Calibri 12 justificado, títulos
de sección numerados en romanos, viñetas, y tablas centradas con el encabezado gris.

Sirve para dos cosas: **formatear** un `.docx` que ya existe, y **generar** uno nuevo desde
texto o Markdown. La usa `/irem-mision-informe` como último paso, pero también vale sola
para cualquier nota técnica o memorando.

El formato no está escrito a mano en un script: vive en una plantilla derivada de un informe
real, que conserva los estilos, el tema tipográfico, los márgenes, la numeración y el
encabezado con los logos. Los scripts solo escriben bloques dentro de ella, así que el
resultado sale igual **por construcción** y no por aproximación. Comparando el documento de
referencia con uno generado, midiendo las coordenadas de cada línea con Word como
renderizador, la primera página coincide exactamente y el documento entero da las mismas 12
páginas.

### Cómo pedirla

- «Dale el formato institucional a este Word.»
- «Unifica la tipografía de este documento.»
- «Pasa estas notas a Word con el formato de la casa.»

### Lo que te va a preguntar

Poco: es la skill menos conversacional de las cinco. Si le das un `.docx`, lo reformatea y te
dice cuántos bloques de cada tipo encontró, que es la forma de detectar una clasificación
mala. Si le das texto suelto, lo primero es decidir qué línea es sección, qué es subtítulo y
qué es viñeta, y eso lo propone antes de compilar.

Si no tienes `uv` instalado (que es lo único que hace falta, porque se descarga Python solo),
te lo dice y te acompaña a instalarlo en lugar de fallar con un error.

### Dos cosas que conviene saber

El documento de referencia usaba **dos grises distintos** en la misma tabla; la skill unifica
a uno. Y añade `keepNext` a todos los títulos, que el original no tenía, para que ningún
título quede solo al pie de una página. Las dos decisiones están anotadas en su `SKILL.md`.

Normaliza además las inconsistencias que traía el original: párrafos que se habían quedado
sin justificar, sangrías de lista sueltas y veinte numeraciones distintas para viñetas
visualmente iguales.

## Presentaciones: `/irem-presentacion`

Genera presentaciones con la identidad visual oficial de **mesoamérica MALARIA** y del
**BID**, replicada del master institucional `ppt_resultados_IREM_2025_master_logos.pptx`:
portada con fotografía a sangre, Montserrat, logotipos en el pie, numerales 01/02/03 y tablas
de cabecera azul.

La presentación se escribe una sola vez, en Quarto, y de ahí sale lo que haga falta: el PDF
para proyectar, el PDF con las notas del presentador o el PowerPoint editable.

### Cómo pedirla

- «Hazme una presentación de 20 minutos sobre los resultados de la primera fase, para el
  equipo de laboratorio.»
- «Convierte este informe en una presentación para el comité.» (adjuntando el informe)
- «Necesito una propuesta de 30 minutos para el ministerio de salud.»
- «Pásame también el PowerPoint, que la contraparte va a editarlo.»
- «En la lámina 7 sobra texto, pártela en dos.»

### Lo que te va a preguntar antes de escribir nada

Tres cosas, en un solo mensaje. Vale la pena contestarlas bien, porque de ellas depende
todo lo demás:

- **Audiencia**, y si es interna o va a un externo (ministerio, donante, comité). De ahí sale
  el nivel técnico y cuánto vocabulario hay que explicar.
- **Duración**, que define el número de láminas.
- **Qué salida hace falta**, PDF o PowerPoint editable.

Después propone un índice de una línea por lámina y **espera aprobación** antes de escribir la
presentación. Ese momento es el bueno para mover cosas: cambiar el índice cuesta un minuto y
cambiar la presentación entera, una tarde.

### Las opciones

| Qué quieres | Cómo lo pides | Qué recibes |
|---|---|---|
| PDF, que es lo normal | No hace falta decir nada | El PDF para proyectar y otro con las **notas del presentador** intercaladas |
| PowerPoint editable | «en PowerPoint», «el pptx», «que lo puedan editar» | Un `.pptx` con las notas en el panel de notas |
| Las dos cosas | «hazme las dos» | Los tres archivos, desde la misma fuente |
| Propuesta a un externo | Di que va a un ministerio, un donante o un comité | La estructura fija de siete secciones que usa la organización |
| Charla con demostraciones en vivo | Di cuántos demos y ejercicios habrá | La mitad de láminas: un demo consume minutos sin consumir láminas |

La decisión entre PDF y PowerPoint **no cierra ninguna puerta**. Si entregaste el PDF y a la
semana el BID pide el archivo editable, es un comando más sobre el mismo `.qmd`. No se
reescribe nada, y no hay dos versiones del contenido que se desincronicen.

**PDF** cuando la presentación la das tú: no se descuadra al cambiar de computadora.
**PowerPoint** en cuanto alguien más tenga que meter mano. El `.pptx` no se dibuja de cero: la
skill lleva el master institucional sin sus láminas de contenido, así que el fondo, los
logotipos del pie, la portada completa y las fuentes Montserrat embebidas vienen del archivo
original. Sale un PowerPoint normal, con formas nativas, que se edita como cualquier otro.

### Lo que entrega

Una carpeta con el `.qmd` (la fuente), los archivos finales y los scripts para volver a
compilar:

| Comando | Qué hace |
|---|---|
| `./renderizar.sh archivo.qmd` | Compila los dos PDF |
| `./renderizar-pptx.py archivo.qmd` | Genera el PowerPoint |
| `./revisar.py archivo.qmd` | Revisa contenido y formato, y avisa de lo que está mal |
| `./pptx-a-pdf.sh archivo.pptx` | Convierte el PowerPoint para poder mirarlo lámina por lámina |

**Requisitos.** Para el PDF: Quarto, LaTeX y Montserrat. Para el PowerPoint no hace falta
ninguno de los tres, solo Python. Montserrat sí hace falta en los dos casos, y hay que
pedírsela también a quien reciba el `.pptx`: si no la tiene instalada, PowerPoint la sustituye
y las líneas se parten en otro sitio. Es gratis, en Google Fonts.

## Repositorios: `/irem-repo`

Crea un repositorio nuevo **dentro de la organización** y **privado**, lo clona y deja el
primer commit hecho, con README y `.gitignore`.

Las dos reglas que automatiza:

1. El repositorio va dentro de `RMEI-digital`, nunca en tu cuenta personal. Así la
   información no se pierde, queda centralizada y el conocimiento permanece en la
   organización aunque las personas roten.
2. Siempre privado.

### Cómo pedirla

- «Crea un repositorio para el tablero de indicadores.»
- «Necesito un repo nuevo para el análisis de la encuesta de hogares, en R.»
- «Súbeme esto a GitHub.» (si la carpeta todavía no es un repositorio)

### Lo que te va a preguntar

- **Nombre**, en minúsculas y con guiones: `tablero-indicadores`, no `Tablero Indicadores`.
- **Descripción de una línea.** No es un trámite: es lo único que otra persona ve en el
  listado de la organización antes de abrirlo, así que tiene que decir qué es, no cómo se
  llama.
- **Lenguaje principal** (`Python`, `R`, `Node`, `Go`), para poner el `.gitignore` oficial de
  GitHub.

Antes de crear nada te muestra un resumen y espera tu aprobación. Crear un repositorio es
visible para todo el equipo y el nombre no se cambia con comodidad.

**Requisitos**: `gh` instalado (`brew install gh`) y autenticado (`gh auth login`, que es
interactivo y lo tienes que correr tú). Si Claude te ofrece instalarlo, acepta; el login sigue
siendo tuyo.

**Lo que no hace, a propósito.** No mueve proyectos que ya existen: si la carpeta ya tiene
commits, ese caso se resuelve a mano y con criterio, porque hacerlo mal tira la historia del
proyecto. Tampoco protege la rama principal, invita colaboradores ni arma la estructura del
proyecto: son decisiones del equipo, y se ofrecen aparte si vienen al caso.

## Seguridad: `/irem-security-audit`

Auditoría de seguridad de un repositorio, código e historial de git. Corre TruffleHog para
buscar secretos vivos en **todo** el historial y en los archivos sin versionar, Bandit y
Semgrep para análisis estático, `pip-audit` para dependencias con vulnerabilidades conocidas,
VVAH como paso opcional, y (esto es lo que la distingue) una revisión manual de **controles
ausentes**: autenticación, validación de firma, límites de tasa.

Esa distinción es la razón de ser de la skill: el análisis automático encuentra lo que está
mal escrito, no lo que falta. Un endpoint sin autenticación no es código defectuoso, es código
que no existe, y ninguna herramienta lo señala sola. En la revisión que la originó, Semgrep dio
cero hallazgos y el repositorio tenía dos críticos y cuatro altos.

Pensada para repos pequeños de salud pública y datos personales, tipo Flask, Django o Node
sobre Heroku o Vercel.

### Cómo pedirla

- «Hazme una auditoría de seguridad de este repositorio.»
- «Revisa si hay secretos en el historial de git.»
- «Corre los scripts de seguridad antes de que esto salga a producción.»

### Lo que te va a preguntar

- **Si hay acceso en vivo** (base de datos, Heroku o Vercel, credenciales). Con acceso puede
  *demostrar* un hallazgo con un ejemplo real, que es lo que convence a un equipo; sin acceso
  la revisión es estática, y lo dice.
- **Qué datos maneja el sistema** (personales, de salud, ubicación). De eso depende la
  gravedad real y las implicaciones legales.
- **Si se corre el paso opcional (VVAH)**, que encadena hallazgos y encuentra cosas que los
  demás no ven, pero es el más lento y el que más tokens consume: va contra tu clave de API si
  usa el SDK, o contra el uso de tu plan de Claude si usa el backend CLI. Si no lo pides, se
  salta y queda anotado en el alcance del reporte.

### Lo que entrega

| Archivo | Qué es |
|---|---|
| `SECURITY-REVIEW.md` | El reporte completo: cada hallazgo, su severidad, dónde está y cómo se corrige |
| `SECURITY-REVIEW-RESUMEN.md` | Resumen ejecutivo en español, con lo urgente en una frase y las acciones para hoy |
| `security-review/` | Las salidas crudas de cada herramienta, que prueban el alcance real de lo que se escaneó |

Dos reglas suyas que vale la pena conocer antes de usarla. El JSON crudo de TruffleHog
**nunca** se escribe dentro del repo auditado, porque trae los secretos en claro y guardarlo
ahí reproduciría el defecto que se busca. Y no se filtra por tipo de resultado, porque
`unverified` no significa falso positivo sino «no hay forma de comprobarlo desde aquí», que es
el caso de una clave privada en el historial.

La auditoría además **no commitea ni sube nada**: deja todo en tu copia de trabajo.

## Publicar un cambio

`/plugin update` compara **versiones**, no contenido. Si corriges algo y no subes la versión
en `plugins/irem/.claude-plugin/plugin.json`, el comando responde «ya estás al día» y todo el
equipo se queda con la copia vieja **sin ningún aviso**.

Al publicar cualquier cambio:

1. Sube `version` en `plugin.json`: parche para correcciones, menor para algo nuevo.
2. `claude plugin validate .` debe pasar sin advertencias.
3. Commit y push.
4. Avisa al equipo que corra `/plugin update irem`.

Si `update` insiste en que ya estás al día justo después de un push, el clon local del
marketplace todavía no trajo el commit. Se fuerza con:

```bash
git -C ~/.claude/plugins/marketplaces/rmei-digital pull
```

Y después de actualizar hay que **abrir una sesión nueva**: el propio comando lo avisa.

## Cómo aportar

Las skills son archivos de texto. Cada una es una carpeta en `plugins/irem/skills/` con un
`SKILL.md` que dice qué hace, cuándo usarse y cómo trabajar.

Si encuentras que una skill se equivoca o le falta algo, corrige el `SKILL.md` y abre un
pull request. Documentar el *por qué* de cada regla importa más que la regla: es lo que evita
que alguien la deshaga después sin saber qué rompía.
