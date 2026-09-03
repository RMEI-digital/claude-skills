# claude-skills

Skills de Claude Code del equipo de **RMEI-digital**, instalables como plugin.

Una *skill* es un procedimiento de la casa escrito una vez para que lo use todo el equipo, en
lugar de vivir en la cabeza de una persona. No cambia la forma de trabajar: le pides a Claude
lo que necesitas en lenguaje normal y la skill se activa sola. También puedes llamarla por su
nombre, y todas empiezan con `irem-`, así que escribiendo `/irem` aparecen todas.

| Skill | Para qué sirve |
|---|---|
| [`/irem-mision-informe`](#informes-de-misión-irem-mision-informe) | Convierte notas o transcripciones de una misión de campo en el informe completo. |
| [`/irem-word-formato`](#documentos-word-irem-word-formato) | Da a un documento de Word el formato institucional, con los logos en el encabezado. |
| [`/irem-presentacion`](#presentaciones-irem-presentacion) | Presentaciones con el formato IREM/BID, en PDF o en PowerPoint editable. |
| [`/irem-repo`](#repositorios-irem-repo) | Crea un repositorio nuevo en GitHub, privado y dentro de la organización. |
| [`/irem-security-audit`](#seguridad-irem-security-audit) | Auditoría de seguridad de un repositorio: secretos en el historial y controles que faltan. |

## Instalar

### En Claude Code

```
/plugin marketplace add RMEI-digital/claude-skills
/plugin install irem
```

Después, **cierra la sesión y abre una nueva**: las instrucciones se cargan al arrancar, así
que sin ese paso las skills no aparecen. Al volver deberías ver las cinco `irem-*`.

**Si el primer comando falla**, casi siempre es lo mismo: el repositorio es privado y tu `git`
no sabe autenticarse con GitHub. Corre `gh auth login` y vuelve a intentarlo.

Hay un plan B, pero úsalo solo si de verdad te atoras:

```bash
git clone https://github.com/RMEI-digital/claude-skills.git
cd claude-skills && ./instalar.sh
```

Copia las skills a `~/.claude/skills/` y **no se actualiza solo**: hay que repetirlo cada vez
que el repositorio cambie. Y si después instalas el plugin, quedan duplicadas, así que borra
antes las copias sueltas (`rm -rf ~/.claude/skills/irem-*`).

### En Claude Cowork

Tres caminos, en este orden.

**1. El marketplace, igual que en Claude Code.** En **Customize > Plugins**, «Add marketplace»,
escribe `RMEI-digital/claude-skills` e instala el plugin `irem`. Para traer cambios
posteriores, el botón «Update» del marketplace. Como el repositorio es privado, tu cuenta de
GitHub tiene que poder verlo; si no aparece, pasa al camino 2.

**2. Descargar el repositorio y subir el plugin entero.** En GitHub, con la sesión iniciada,
«Code» > «Download ZIP». Descomprime, comprime la carpeta `plugins/irem` (clic derecho,
«Comprimir») y súbela en **Customize > Plugins**, con la opción de instalar desde archivo.
Entran las cinco skills de una vez.

**3. Subir una skill suelta.** Igual, pero comprimiendo solo su carpeta dentro de
`plugins/irem/skills/`, y subiéndola en **Customize > Skills** con «+» > «Create skill» >
«Upload a skill». El `.zip` debe contener la carpeta de la skill con su `SKILL.md` dentro. Para
generarlos todos de una vez:

```bash
cd plugins/irem/skills && for s in */; do zip -qr ~/Desktop/"${s%/}.zip" "$s"; done
```

Los caminos 2 y 3 no se actualizan solos: al publicar una versión nueva hay que volver a bajar
y subir. En planes Team o Enterprise, quien suba una skill puede compartirla con toda la
organización desde **Customize > Skills > Share**, y así nadie repite la subida.

Los plugins funcionan en Cowork y en Claude Code, no en el chat normal; las skills subidas como
`.zip` sí funcionan también en el chat.

### Lo que hay que instalar aparte

Las skills son instrucciones: **las herramientas que usan no vienen dentro del plugin**. Cada
una avisa al empezar de lo que le falta y acompaña a instalarlo, en vez de fallar con un error.

| Skill | Necesita |
|---|---|
| Informes de misión y Word | `uv`, que se descarga Python solo |
| Presentaciones | Quarto y LaTeX para el PDF; solo Python para el PowerPoint. La primera compilación tarda varios minutos porque LaTeX baja los paquetes que faltan: es normal, no la interrumpas. Hace falta además Montserrat, también en la máquina de quien reciba el `.pptx` |
| Repositorios | `gh` instalado y `gh auth login` corrido por cada persona: ese login es interactivo y Claude no puede hacerlo |
| Seguridad | TruffleHog, Bandit, Semgrep y `pip-audit` |

### Actualizar

`/plugin update irem`, y otra vez sesión nueva. **Nadie se entera solo de que hay una versión
nueva**: hasta que corran ese comando siguen con la que tienen, así que cuando el cambio
importe hay que avisar por el canal del equipo.

## Informes de misión: `/irem-mision-informe`

Convierte el material crudo de una misión (transcripciones, apuntes, correos) en el informe
completo, con la estructura de siempre: cada actor contado según el ciclo de vida del dato, y
los desafíos agrupados por esas mismas etapas.

**Nunca inventa contenido.** Si un dato falta, lo pregunta o lo deja marcado como pendiente,
pero no escribe algo plausible. Y distingue lo observado de lo dicho.

**Se lo pides así:** «Hazme el informe de la misión a Quibdó, aquí están mis notas», «pásame
esta transcripción a informe de misión».

**Te va a preguntar** solo por los huecos, después de leer todo y enseñarte qué encontró:
fechas, lugar y participantes; el oficio que originó la misión; las etapas del ciclo de las
que no hay información; y si hubo reunión de cierre.

**Recibes** el informe en Word listo para enviar y su contenido en texto plano. Los dos a
propósito: corregir el texto es barato y recompilar el Word cuesta un comando.

## Documentos Word: `/irem-word-formato`

Da a un documento de Word el formato institucional completo: logos del BID y de mesoamérica
MALARIA en el encabezado, Calibri 12 justificado, secciones numeradas en romanos, viñetas y
tablas de encabezado gris. Sirve para **formatear** un `.docx` que ya existe y para **generar**
uno nuevo desde texto. La usa la skill de informes en su último paso, pero vale sola para
cualquier nota o memorando.

**Se lo pides así:** «Dale el formato institucional a este Word», «pasa estas notas a Word con
el formato de la casa».

**Te va a preguntar** casi nada: es la menos conversacional. Si le das texto suelto, propone
qué línea es sección, cuál subtítulo y cuál viñeta antes de compilar.

**Recibes** el documento formateado, sin tocar el original, y el recuento de bloques de cada
tipo que encontró. Vale la pena mirarlo: cero secciones en un documento que sí tiene capítulos
delata una clasificación mala.

## Presentaciones: `/irem-presentacion`

Presentaciones con la identidad visual oficial: portada con fotografía a sangre, Montserrat,
logotipos en el pie, numerales 01/02/03 y tablas de cabecera azul, replicado del master
institucional. Se escribe una sola vez y de ahí sale lo que haga falta, sin reescribir nada.

**Se lo pides así:** «Hazme una presentación de 20 minutos sobre los resultados, para el equipo
de laboratorio», «necesito una propuesta de 30 minutos para el ministerio», «pásame también el
PowerPoint, que la contraparte va a editarlo».

**Te va a preguntar** tres cosas: **audiencia** (y si es interna o va a un externo),
**duración** y **qué salida** hace falta. Después propone el índice, una línea por lámina, y
espera tu aprobación antes de escribir. Ese es el momento de mover cosas: cambiar el índice
cuesta un minuto y cambiar la presentación entera, una tarde.

| Si pides | Recibes |
|---|---|
| Nada en particular | El PDF para proyectar y otro con las notas del presentador intercaladas |
| «en PowerPoint», «el pptx» | Un `.pptx` editable, con las notas en el panel de notas |
| «las dos» | Los tres archivos, desde la misma fuente |

**PDF** cuando la presentación la das tú; **PowerPoint** en cuanto alguien más tenga que
editarla. La decisión no cierra ninguna puerta: si después piden el editable, es un comando más
sobre el mismo `.qmd`. Y dos cosas que conviene decirle, porque cambian el resultado: si va a un
ministerio, un donante o un comité, usa la estructura fija de siete secciones; y si la charla
lleva demostraciones en vivo, hacen falta la mitad de láminas.

En la carpeta quedan los scripts para volver a compilar: `renderizar.sh` (los dos PDF),
`renderizar-pptx.py` (el PowerPoint), `revisar.py` (revisa contenido y formato) y
`pptx-a-pdf.sh` (convierte el PowerPoint para mirarlo lámina por lámina).

## Repositorios: `/irem-repo`

Crea un repositorio nuevo en GitHub, **dentro de la organización** y **privado**, lo clona y
deja el primer commit hecho. Las dos reglas son el punto: en la organización para que el
conocimiento no se pierda cuando alguien rota, y privado siempre.

**Se lo pides así:** «Crea un repositorio para el tablero de indicadores», «necesito un repo
nuevo para el análisis de la encuesta, en R».

**Te va a preguntar** el **nombre** (en minúsculas y con guiones), una **descripción de una
línea** y el **lenguaje principal**. La descripción no es un trámite: es lo único que otra
persona ve en el listado antes de abrirlo. Antes de crear nada te muestra el resumen y espera
tu aprobación.

**Lo que no hace, a propósito:** no mueve proyectos que ya existen, porque si la carpeta ya
tiene commits hacerlo mal tira la historia y eso se resuelve a mano. Tampoco protege ramas ni
invita colaboradores; eso se ofrece aparte.

## Seguridad: `/irem-security-audit`

Auditoría de un repositorio, código e historial. Busca secretos vivos en **todo** el historial
de git, corre análisis estático y revisa a mano los **controles ausentes**: autenticación,
validación de firma, límites de tasa.

Esa última parte es su razón de ser. En la revisión que la originó, el análisis automático dio
cero hallazgos y el repositorio tenía dos críticos y cuatro altos: las herramientas encuentran
código mal escrito, no código que falta.

**Se lo pides así:** «Hazme una auditoría de seguridad de este repositorio», «revisa si hay
secretos en el historial de git».

**Te va a preguntar** si hay **acceso en vivo** (con acceso puede demostrar un hallazgo con un
ejemplo real, que es lo que convence a un equipo), **qué datos maneja** el sistema, y si se
corre el paso opcional de análisis con agentes, que es el más lento y el que más tokens
consume.

**Recibes** el reporte completo, un resumen ejecutivo en español con lo urgente en una frase, y
las salidas crudas de cada herramienta. No commitea ni sube nada: deja todo en tu copia de
trabajo.

## Publicar un cambio

`/plugin update` compara **versiones**, no contenido. Si corriges algo y no subes la versión en
`plugins/irem/.claude-plugin/plugin.json`, el comando responde «ya estás al día» y todo el
equipo se queda con la copia vieja **sin ningún aviso**.

1. Sube `version` en `plugin.json`: parche para correcciones, menor para algo nuevo.
2. `claude plugin validate .` debe pasar sin advertencias.
3. Commit y push.
4. Avisa al equipo que corra `/plugin update irem`.

Si `update` insiste en que ya estás al día justo después de un push, el clon local del
marketplace todavía no trajo el commit. Se fuerza con:

```bash
git -C ~/.claude/plugins/marketplaces/rmei-digital pull
```

## Cómo aportar

Cada skill es una carpeta en `plugins/irem/skills/` con un `SKILL.md` que dice qué hace, cuándo
usarse y cómo trabajar. Si una se equivoca o le falta algo, corrige ese archivo y abre un pull
request. Documentar el *por qué* de cada regla importa más que la regla: es lo que evita que
alguien la deshaga después sin saber qué rompía.

`Guia-de-uso-skills-RMEI-digital.docx` es este mismo README en Word, para mandárselo a quien no
va a abrir GitHub. Se genera desde `guia-de-uso.md`, que es su fuente, con la skill de formato:

```bash
uv run --with python-docx python plugins/irem/skills/irem-word-formato/generar.py \
  guia-de-uso.md Guia-de-uso-skills-RMEI-digital.docx
```

Si cambias uno, cambia el otro: no hay nada que los sincronice solos.
