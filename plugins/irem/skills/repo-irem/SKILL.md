---
name: repo-irem
description: Crea un repositorio nuevo, privado, dentro de la organización RMEI-digital en GitHub, lo clona y deja el primer commit hecho. Úsala cuando alguien vaya a empezar un proyecto, una aplicación, un análisis o cualquier trabajo que necesite repositorio, o pida "crear un repo", "un repositorio nuevo" o "subir esto a GitHub". No la uses para repositorios personales fuera de la organización.
---

# Repositorio nuevo en RMEI-digital

Organización: **[RMEI-digital](https://github.com/RMEI-digital)**

## Las dos reglas que no se negocian

1. **El repositorio se crea DENTRO de la organización**, nunca en la cuenta personal. La
   razón no es burocrática: así la información no se pierde, queda centralizada y el
   conocimiento permanece en la organización aunque las personas roten.
2. **Siempre privado.** Es un aplicativo en desarrollo.

Si alguien pide un repositorio público o en su cuenta personal, explícale estas dos razones
antes de hacerlo, y hazlo sólo si insiste.

Esta skill crea repositorios nuevos. **No mueve proyectos existentes**: si la carpeta ya
tiene commits, no la trates como un proyecto nuevo, porque eso tiraría su historia. Ese caso
se resuelve a mano y con criterio, no con un script.

## Cómo trabajar

### 1. Comprueba que se puede, y resuelve lo que puedas resolver

```bash
command -v gh && gh auth status
```

De los dos requisitos, uno lo puedes resolver tú y el otro no. No los mezcles en el mismo
mensaje, porque la persona termina sin saber qué le toca hacer.

| Falta | Qué haces |
|---|---|
| `gh` no está instalado | **Ofrécete a instalarlo** y hazlo con su aprobación: `brew install gh`. No es interactivo. Si no hay `brew`, remítela a https://cli.github.com en vez de asumir Homebrew. |
| `gh` no está autenticado | **Detente.** `gh auth login` es interactivo y no lo puedes correr tú. Pídele que lo corra y espera. |
| Falla el alcance de organización | `gh auth refresh -s read:org`, también interactivo. |

Instalar `gh` sin poder autenticarlo no sirve de nada: si vas a instalarlo, adviértele en el
mismo momento que después le toca el `gh auth login`.

### 2. Reúne tres datos

- **Nombre** en minúsculas con guiones: `tablero-indicadores`, no `Tablero Indicadores`.
  GitHub acepta otras formas, pero el guion en minúsculas es lo que usa la organización y
  evita problemas al clonar en distintos sistemas.
- **Descripción** de una línea. Aparece en el listado de la organización y es lo único que
  otra persona ve antes de abrirlo, así que debe decir qué es, no cómo se llama.
- **Lenguaje principal**, para el `.gitignore` oficial de GitHub: `Python`, `R`, `Node`,
  `Go`. Si no aplica, se omite y se usa uno mínimo.

Si la persona no dio la descripción, pídesela. Un repositorio sin descripción en una
organización compartida es exactamente el problema que la organización quiere evitar.

### 3. Muestra el resumen y **espera aprobación**

Crear un repositorio es visible para todo el equipo y su nombre no se cambia con comodidad.
Antes de tocar GitHub, muestra esto y espera respuesta:

```
Voy a crear:
  Repositorio   RMEI-digital/<nombre>
  Visibilidad   PRIVADO
  Descripción   <descripción>
  Contenido     README.md y .gitignore (<lenguaje>)
  Primer commit "Inicializa el repositorio", como <nombre git> <correo git>
  Clon local    <carpeta>/<nombre>
```

No sigas sin aprobación explícita.

### 4. Créalo

Claude Code te informa el directorio base de esta skill al invocarla («Base directory for
this skill»). Úsalo; **no escribas una ruta fija**, porque cambia si la skill está instalada
localmente o distribuida como plugin.

```bash
BASE="<el directorio base que te informó Claude Code>"
"$BASE/crear-repo.sh" <nombre> "<descripción>" [lenguaje] [carpeta-destino]
```

El script hace las comprobaciones previas, crea, clona, escribe README y `.gitignore`, hace
el primer commit, lo empuja y verifica el resultado. Si algo falla, se detiene antes de crear
nada.

### 5. Reporta

Entrega la URL del repositorio y la ruta del clon local. Menciona explícitamente que quedó
privado y dentro de la organización: es la confirmación de que se cumplió el lineamiento.

## Autoría

Un repositorio no tiene autor, tiene **dueño**, y aquí el dueño es la organización. Lo que
lleva autoría son los commits, y esos van con la identidad git de la persona.

**Nunca** agregues `Co-Authored-By: Claude`, ni «Generated with Claude Code», ni ninguna
atribución a Claude, en commits ni en pull requests. El script lo verifica y falla si
aparece. El mensaje del primer commit es de una sola línea y sin cuerpo, igual que el resto
de los commits de la organización.

## Errores que vas a encontrar

| Mensaje | Qué significa |
|---|---|
| `gh no está instalado` | Ofrécete a correr `brew install gh`. |
| `gh no está autenticado` | Falta `gh auth login`. Es interactivo: lo corre la persona. |
| `no puedo ver la organización RMEI-digital` | La cuenta no pertenece a la organización, o al token le falta alcance. Se arregla con `gh auth refresh -s read:org`. |
| `YA EXISTE` | El nombre está tomado. No lo sobreescribas ni le agregues un sufijo por tu cuenta: pregunta cómo quiere llamarlo. |
| `la identidad git apunta a Claude` | `git config --global user.name` quedó mal configurado. Corrígelo antes de seguir. |
| Falla el `push` por permisos | La organización puede exigir aprobación para crear repositorios, y un rol `member` puede no alcanzar. El repositorio quizá quedó creado y vacío: revísalo antes de reintentar. |

## Después de crear

Cosas que la skill deliberadamente **no** hace, para no tomar decisiones que son del equipo.
Ofrécelas si vienen al caso:

- Protección de la rama principal y revisión obligatoria en pull requests.
- Invitar colaboradores o asignar equipos.
- Temas y etiquetas del repositorio.
- Estructura del proyecto más allá de README y `.gitignore`.
