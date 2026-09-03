# claude-skills

Skills de Claude Code del equipo de **RMEI-digital**, instalables como plugin.

Una *skill* es un conjunto de instrucciones que Claude carga solo cuando hacen falta. Sirve
para que un procedimiento que alguien repite (armar una presentación con el formato
institucional, crear un repositorio como toca) quede escrito una vez y lo pueda usar todo el
equipo, en lugar de vivir en la cabeza de una persona.

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

### Si el plugin no funciona

Como el repositorio es privado, `/plugin marketplace add` necesita que tu `git` sepa
autenticarse con GitHub. Si da problemas, clona y usa el instalador:

```bash
git clone https://github.com/RMEI-digital/claude-skills.git
cd claude-skills && ./instalar.sh
```

Eso copia las skills a `~/.claude/skills/`. Funciona igual, pero hay que volver a correrlo
cada vez que el repositorio cambie.

## Qué trae

Las tres empiezan con `irem-`, así que escribiendo `/irem` en Claude Code aparecen todas.
El prefijo no es decorativo: es lo que las hace encontrables sin recordar el nombre exacto.

### `/irem-presentacion`

Genera presentaciones con el formato institucional **Mesoamérica Malaria (IREM) / BID**:
portada oficial con fotografía a sangre, Montserrat, logotipos de mesoamérica MALARIA y del
BID en el pie, numerales 01/02/03 y tablas de cabecera azul, todo replicado del master
vigente `ppt_resultados_IREM_2025_master_logos.pptx`.

**Dos salidas, una sola fuente.** La presentación se escribe una vez, en Quarto, y de ahí
sale lo que haga falta:

- **PDF**, con una segunda versión que lleva las **notas del presentador** intercaladas, que
  es el guion de quien expone.
- **PowerPoint editable** (`.pptx`), para cuando el archivo tiene que poder modificarlo otra
  persona: una contraparte, un ministerio, o quien vaya a exponer desde su máquina. Las notas
  van al panel de notas, que es donde PowerPoint las espera.

El `.pptx` no se dibuja de cero: la skill lleva el master institucional sin sus láminas de
contenido, así que el fondo, los logotipos del pie, la portada completa y las fuentes
Montserrat embebidas vienen del archivo original. Sale un PowerPoint normal, con formas
nativas, que se edita como cualquier otro.

Pídele una presentación y te va a preguntar tres cosas antes de escribir nada: audiencia,
duración y el mensaje único. Vale la pena contestarlas bien.

Para el PDF hacen falta Quarto y LaTeX; para el `.pptx`, nada más que Python. Montserrat
tiene que estar instalada en los dos casos, y la skill dice cómo.

### `/irem-repo`

Crea un repositorio nuevo **dentro de la organización** y **privado**, lo clona y deja el
primer commit hecho. Antes de crear nada te muestra un resumen y espera tu aprobación.

Las dos reglas que automatiza:

1. El repositorio va dentro de `RMEI-digital`, nunca en tu cuenta personal. Así la
   información no se pierde, queda centralizada y el conocimiento permanece en la
   organización aunque las personas roten.
2. Siempre privado.

**Requisitos**: `gh` instalado (`brew install gh`) y autenticado (`gh auth login`, que es
interactivo y lo tienes que correr tú). Si Claude te ofrece instalarlo, acepta; el login
sigue siendo tuyo.

### `/irem-security-audit`

Auditoría de seguridad de un repositorio, código e historial de git. Corre TruffleHog para
buscar secretos vivos en **todo** el historial y en los archivos sin versionar, Bandit y Semgrep
para análisis estático, `pip-audit` para dependencias con vulnerabilidades conocidas, VVAH como
paso opcional, y (esto es lo que la distingue) una revisión manual de **controles ausentes**:
autenticación, validación de firma, límites de tasa.

Esa distinción es la razón de ser de la skill: el análisis automático encuentra lo que está
mal escrito, no lo que falta. Un endpoint sin autenticación no es código defectuoso, es
código que no existe, y ninguna herramienta lo señala sola.

Dos reglas suyas que vale la pena conocer antes de usarla: el JSON crudo de TruffleHog **nunca**
se escribe dentro del repo auditado, porque trae los secretos en claro; y no se filtra por tipo de
resultado, porque `unverified` no significa falso positivo sino "no hay forma de comprobarlo desde
aquí", que es el caso de una clave privada en el historial.

Pensada para repos pequeños de salud pública y datos personales, tipo Flask, Django o Node
sobre Heroku o Vercel. Entrega `SECURITY-REVIEW.md` y un resumen ejecutivo aparte.

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
