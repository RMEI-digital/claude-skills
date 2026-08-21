# claude-skills

Skills de Claude Code del equipo de **RMEI-digital**, instalables como plugin.

Una *skill* es un conjunto de instrucciones que Claude carga solo cuando hacen falta. Sirve
para que un procedimiento que alguien repite —armar una presentación con el formato
institucional, crear un repositorio como toca— quede escrito una vez y lo pueda usar todo el
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

### `/presentacion-irem`

Genera presentaciones en Quarto con el formato institucional **Mesoamérica Malaria (IREM) /
BID** y las compila a PDF: portada oficial, chevron verde, logotipos del BID y de IREM, y la
paleta y tipografía medidas de las plantillas oficiales.

Produce dos PDF por presentación: uno para proyectar y otro con las **notas del presentador**
intercaladas, que es el guion de quien expone.

Pídele una presentación y te va a preguntar tres cosas antes de escribir nada: audiencia,
duración y el mensaje único. Vale la pena contestarlas bien.

### `/repo-irem`

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

## Publicar un cambio

`/plugin update` compara **versiones**, no contenido. Si corriges algo y no subes la versión
en `plugins/irem/.claude-plugin/plugin.json`, el comando responde «ya estás al día» y todo el
equipo se queda con la copia vieja **sin ningún aviso**.

Al publicar cualquier cambio:

1. Sube `version` en `plugin.json` — parche para correcciones, menor para algo nuevo.
2. `claude plugin validate .` debe pasar sin advertencias.
3. Commit y push.
4. Avisa al equipo que corra `/plugin update irem`.

## Cómo aportar

Las skills son archivos de texto. Cada una es una carpeta en `plugins/irem/skills/` con un
`SKILL.md` que dice qué hace, cuándo usarse y cómo trabajar.

Si encuentras que una skill se equivoca o le falta algo, corrige el `SKILL.md` y abre un
pull request. Documentar el *por qué* de cada regla importa más que la regla: es lo que evita
que alguien la deshaga después sin saber qué rompía.
