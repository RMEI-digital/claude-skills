# Skills de Claude Code del equipo
# Guía de uso

**Repositorio:** RMEI-digital/claude-skills
**Versión del plugin:** 1.10.2
**Fecha:** 4 de septiembre de 2026

## Qué son

Una *skill* es un procedimiento de la casa escrito una vez para que lo use todo el equipo, en lugar de vivir en la cabeza de una persona. No cambia la forma de trabajar: le pides a Claude lo que necesitas en lenguaje normal y la skill se activa sola. También puedes llamarla por su nombre, y todas empiezan con irem-, así que escribiendo /irem aparecen todas.

\anchos 26 74

| Skill | Para qué sirve |
|---|---|
| /irem-mision-informe | Convierte notas o transcripciones de una misión de campo en el informe completo. |
| /irem-word-formato | Da a un documento de Word el formato institucional, con los logos en el encabezado. |
| /irem-presentacion | Presentaciones con el formato IREM/BID, en PDF o en PowerPoint editable. |
| /irem-repo | Crea un repositorio nuevo en GitHub, privado y dentro de la organización. |
| /irem-security-audit | Auditoría de seguridad de un repositorio: secretos en el historial y controles que faltan. |

## Cómo instalarlas

### En Claude Code

Dos comandos, escritos dentro de Claude Code:

- /plugin marketplace add RMEI-digital/claude-skills
- /plugin install irem

Después, **cierra la sesión y abre una nueva**. Las instrucciones se cargan al arrancar, así que sin ese paso no aparecen. Al volver deberías ver las cinco skills irem-.

El repositorio es **público**: no hace falta cuenta de GitHub ni autenticarse para instalarlo. Si el primer comando falla, suele ser que tu git no puede salir a internet (el proxy o la VPN de la oficina), y el plan B de abajo sirve igual para ese caso.

Hay un plan B en el README del repositorio (clonarlo y correr ./instalar.sh), pero úsalo solo si de verdad te atoras: copia las skills a una carpeta local y **no se actualiza solo**, hay que repetirlo cada vez que el repositorio cambie. Y si después instalas el plugin, te quedan las skills duplicadas, así que borra las copias sueltas antes.

### En Claude Cowork

Tres caminos, en este orden. Ninguno necesita terminal salvo que quieras.

**1. El marketplace, igual que en Claude Code.** En Customize (Personalizar) > Plugins, elige «Add marketplace», escribe RMEI-digital/claude-skills e instala el plugin irem. Para traer los cambios que se publiquen después, el botón «Update» del marketplace. El repositorio es público, así que no necesitas conectar tu cuenta de GitHub ni que tu organización tenga habilitado el conector de GitHub. Si aun así no aparece, pasa al camino 2.

**2. Descargar el repositorio y subir el plugin entero.** En GitHub, el botón verde «Code» y «Download ZIP», sin necesidad de cuenta. Descomprime, entra en la carpeta plugins, comprime la carpeta irem (clic derecho, «Comprimir») y sube ese .zip en Customize > Plugins, con la opción de instalar desde archivo. Suben las cinco skills de una vez.

**3. Subir una skill suelta.** Igual que el anterior, pero comprimiendo solo la carpeta de la skill que te interese, dentro de plugins, irem, skills. Se sube en Customize > Skills, con el botón «+», «Create skill» y «Upload a skill». El .zip tiene que contener la carpeta de la skill con su archivo SKILL.md dentro.

Los caminos 2 y 3 no se actualizan solos: cuando se publique una versión nueva hay que volver a bajar y volver a subir. Si el equipo está en un plan Team o Enterprise, quien suba una skill puede compartirla con toda la organización desde Customize > Skills > Share, y así nadie más repite la subida.

Una diferencia que conviene saber: los plugins funcionan en Cowork y en Claude Code, no en el chat normal; las skills subidas como .zip sí funcionan también en el chat.

### Lo que hay que instalar aparte

Las skills son instrucciones: **las herramientas que usan no vienen dentro del plugin**. Cada una avisa al empezar de lo que le falta y te acompaña a instalarlo, en vez de fallar con un error.

\anchos 34 66

| Skill | Necesita |
|---|---|
| Informes de misión y Word | uv, que se descarga Python solo |
| Presentaciones | Quarto y LaTeX para el PDF; para el PowerPoint, solo Python. La primera compilación tarda varios minutos porque LaTeX baja los paquetes que le faltan: es normal, no la interrumpas |
| Repositorios | gh instalado, y gh auth login corrido por ti. Ese login es interactivo: Claude no puede hacerlo por ti |
| Seguridad | TruffleHog, Bandit, Semgrep y pip-audit |

Para las presentaciones hace falta además la tipografía Montserrat, y hay que pedírsela también a quien reciba el PowerPoint: si no la tiene, su computadora la sustituye y las líneas se parten en otro sitio. Es gratis, en Google Fonts.

### Cómo se actualizan

Con /plugin update irem, y otra vez sesión nueva.

**Nadie se entera solo de que hay una versión nueva.** Hasta que corran ese comando siguen con la que tienen, así que cuando el cambio importe hay que avisar por el canal del equipo.

## Informes de misión: /irem-mision-informe

Convierte el material crudo de una misión (transcripciones, apuntes, correos) en el informe completo, con la estructura de siempre: cada actor contado según el ciclo de vida del dato, y los desafíos agrupados por esas mismas etapas.

**Nunca inventa contenido.** Si un dato falta, lo pregunta o lo deja marcado como pendiente, pero no escribe algo plausible. Y distingue lo observado de lo dicho.

### Se lo pides así

- «Hazme el informe de la misión a Quibdó, aquí están mis notas.»
- «Pásame esta transcripción a informe de misión.»

### Te va a preguntar

Primero lee todo y te enseña qué encontró. Después pregunta solo por los huecos, en un mensaje: fechas, lugar y participantes; el oficio que originó la misión; las etapas del ciclo de las que no hay información; y si hubo reunión de cierre.

### Recibes

El informe en Word, listo para enviar, y su contenido en texto plano. Los dos a propósito: corregir el texto es barato y recompilar el Word cuesta un comando.

## Documentos Word: /irem-word-formato

Da a un documento de Word el formato institucional completo: logos del BID y de mesoamérica MALARIA en el encabezado, Calibri 12 justificado, secciones numeradas en romanos, viñetas y tablas de encabezado gris.

Sirve para **formatear** un documento que ya existe y para **generar** uno nuevo desde texto. La usa la skill de informes en su último paso, pero vale sola para cualquier nota o memorando.

### Se lo pides así

- «Dale el formato institucional a este Word.»
- «Pasa estas notas a Word con el formato de la casa.»

### Te va a preguntar

Casi nada: es la menos conversacional. Si le das texto suelto, propone qué línea es sección, cuál subtítulo y cuál viñeta antes de compilar.

### Recibes

El documento formateado, sin tocar el original, y el recuento de bloques de cada tipo que encontró. Vale la pena mirarlo: cero secciones en un documento que sí tiene capítulos delata una clasificación mala.

## Presentaciones: /irem-presentacion

Presentaciones con la identidad visual oficial: portada con fotografía a sangre, Montserrat, logotipos en el pie, numerales 01/02/03 y tablas de cabecera azul, replicado del master institucional. Se escribe una sola vez y de ahí sale lo que haga falta, sin reescribir nada.

### Se lo pides así

- «Hazme una presentación de 20 minutos sobre los resultados, para el equipo de laboratorio.»
- «Necesito una propuesta de 30 minutos para el ministerio de salud.»
- «Pásame también el PowerPoint, que la contraparte va a editarlo.»

### Te va a preguntar

Tres cosas: **audiencia** (y si es interna o va a un externo), **duración** y **qué salida** hace falta. Después propone el índice, una línea por lámina, y espera tu aprobación antes de escribir. Ese es el momento de mover cosas: cambiar el índice cuesta un minuto y cambiar la presentación entera, una tarde.

### Recibes

\anchos 30 70

| Si pides | Recibes |
|---|---|
| Nada en particular | El PDF para proyectar y otro con las notas del presentador intercaladas |
| «en PowerPoint», «el pptx» | Un archivo editable, con las notas en el panel de notas |
| «las dos» | Los tres archivos, desde la misma fuente |

**PDF** cuando la presentación la das tú; **PowerPoint** en cuanto alguien más tenga que editarla. La decisión no cierra ninguna puerta: si después piden el editable, es un comando más sobre el mismo archivo. Y dos cosas que conviene decirle, porque cambian el resultado: si va a un ministerio, un donante o un comité, usa la estructura fija de siete secciones; y si la charla lleva demostraciones en vivo, hacen falta la mitad de láminas.

## Repositorios: /irem-repo

Crea un repositorio nuevo en GitHub, **dentro de la organización** y **privado**, lo clona en tu máquina y deja el primer commit hecho. Las dos reglas son el punto: en la organización para que el conocimiento no se pierda cuando alguien rota, y privado siempre.

### Se lo pides así

- «Crea un repositorio para el tablero de indicadores.»
- «Necesito un repo nuevo para el análisis de la encuesta, en R.»

### Te va a preguntar

El **nombre** (en minúsculas y con guiones), una **descripción de una línea** y el **lenguaje principal**. La descripción no es un trámite: es lo único que otra persona ve en el listado antes de abrirlo. Antes de crear nada te muestra el resumen y espera tu aprobación.

### Lo que no hace, a propósito

No mueve proyectos que ya existen: si la carpeta ya tiene commits, ese caso se resuelve a mano, porque hacerlo mal tira la historia. Tampoco protege ramas ni invita colaboradores; eso se ofrece aparte.

## Seguridad: /irem-security-audit

Auditoría de un repositorio, código e historial. Busca secretos vivos en **todo** el historial de git, corre análisis estático y revisa a mano los **controles ausentes**: autenticación, validación de firma, límites de tasa.

Esa última parte es su razón de ser. En la revisión que la originó, el análisis automático dio cero hallazgos y el repositorio tenía dos críticos y cuatro altos: las herramientas encuentran código mal escrito, no código que falta.

### Se lo pides así

- «Hazme una auditoría de seguridad de este repositorio.»
- «Revisa si hay secretos en el historial de git.»

### Te va a preguntar

Si hay **acceso en vivo** (con acceso puede demostrar un hallazgo con un ejemplo real, que es lo que convence a un equipo), **qué datos maneja** el sistema, y si se corre el paso opcional de análisis con agentes, que es el más lento y el que más tokens consume.

### Recibes

El reporte completo, un resumen ejecutivo en español con lo urgente en una frase, y las salidas crudas de cada herramienta. No commitea ni sube nada: deja todo en tu copia de trabajo.

## Si algo hay que corregir

Cada skill es un archivo de texto dentro del repositorio. Si una se equivoca o le falta algo, se corrige ese archivo y se abre un pull request. Documentar el **porqué** de cada regla importa más que la regla: es lo que evita que alguien la deshaga sin saber qué rompía. Y al publicar hay que subir la versión del plugin: el comando de actualización compara versiones, no contenido, así que sin ese número el equipo se queda con la copia vieja y sin ningún aviso.

## Licencia

Las skills, las plantillas y los scripts se publican bajo Creative Commons Atribución 4.0 (CC BY 4.0): cualquiera puede usarlos y adaptarlos, incluso comercialmente, citando a la IREM. Quedan **fuera** los logotipos institucionales y la fotografía de portada de las presentaciones, que pertenecen a sus titulares; si adaptas estas plantillas para otra organización, sustitúyelos por los tuyos. El detalle está en el archivo LICENSE del repositorio.
