---
name: irem-presentacion
description: Genera presentaciones en Quarto con el formato institucional Mesoamérica Malaria (IREM) / BID y las compila a PDF. Úsala cuando alguien pida "una presentación", "unas diapositivas", "un deck" o "unas láminas" para el equipo, para una reunión, para el BID o para un donante; también cuando pida convertir un informe, unas notas o un documento en presentación. No la uses para documentos que no sean presentaciones.
---

# Presentaciones institucionales IREM / BID

Produce presentaciones en Quarto (`.qmd`) que compilan a PDF con la identidad visual
oficial: portada institucional con fotografía y panel del logotipo, chevron verde y
logotipo IREM en cada lámina de contenido, y una densidad tipográfica intermedia — más
aire que las plantillas `.pptx` del equipo, sin llegar a una sola frase por lámina.

## Regla de oro

**El formato no se negocia, el contenido sí.** Nunca inventes colores, tipografías ni
logotipos: usa la extensión `_extensions/irem/` tal como está. Si el usuario pide un
color distinto, adviértele que rompe la identidad institucional antes de hacerlo.

## Cómo trabajar

### 1. Antes de escribir nada, consigue tres cosas

Si el usuario no las dio, pregúntalas en un solo mensaje:

- **Audiencia** — de ella depende el nivel técnico y cuánto vocabulario hay que explicar.
- **Duración** — define el número de láminas (ver presupuesto abajo).
- **El mensaje único** — la frase que la audiencia debe recordar si olvida todo lo demás.

Si el usuario trae material de origen (informe, notas, datos), léelo antes de proponer
estructura. No resumas el documento lámina por lámina: eso produce presentaciones que se
leen en voz alta. Extrae el argumento y constrúyelo.

### 2. Propón la estructura y espera aprobación

Entrega un índice de una línea por lámina, con el minutaje por sección. No generes el
`.qmd` hasta que el usuario apruebe el índice. Ahorra reescrituras completas.

Presupuesto de láminas para una charla **conducida por láminas**, a densidad intermedia:

| Duración | Láminas | Divisorias de sección |
|---|---|---|
| 10 min | 8–10 | 2 |
| 20 min | 16–20 | 3 |
| 30 min | 26–32 | 4–5 |
| 45 min | 38–46 | 5–6 |

Cuenta las divisorias dentro del total: consumen segundos, no minutos.

**Si la charla es conducida por demos, esta tabla no aplica: divídela más o menos a la
mitad.** Un demo en vivo consume varios minutos sin consumir ni una lámina, y un ejercicio
con la audiencia lo mismo. Una charla de 30 minutos con cuatro demos y dos ejercicios
aterriza en 14–22 láminas, no en 30. Antes de fijar el número, cuenta cuántos minutos se van
en pantalla en vivo y réstalos del presupuesto.

Aplicar la tabla a ciegas produce presentaciones infladas que no se alcanzan a dar.

### 3. Monta el proyecto

Claude Code te informa el directorio base de esta skill al invocarla («Base directory for
this skill»). Úsalo como `$BASE`; **no escribas una ruta fija**, porque cambia según si la
skill está instalada localmente o distribuida como plugin.

```bash
BASE="<el directorio base que te informó Claude Code>"
mkdir -p <carpeta>
cp -R "$BASE/plantilla/_extensions" <carpeta>/
cp "$BASE/plantilla/renderizar.sh" <carpeta>/
chmod +x <carpeta>/renderizar.sh
```

Después escribe el `.qmd` en esa carpeta con este encabezado:

```yaml
---
title: "Título"
subtitle: "Subtítulo de una línea"
author: "Quien presenta"
date: today
date-format: long
lang: es
format: irem-beamer
---
```

**No escribas la fecha a mano.** Quarto intenta parsear el campo `date` y una fecha en
español como `"20 de agosto de 2026"` produce un literal `Invalid Date` impreso en la
portada. Con `date: today` más `date-format: long` y `lang: es`, Quarto la escribe bien en
español. Si necesitas una fecha fija, úsala en ISO (`date: 2026-08-24`) y deja que
`date-format` la traduzca.

### 4. Compila y **verifica con tus propios ojos**

```bash
cd <carpeta> && ./renderizar.sh <archivo>.qmd
```

Genera dos PDF: `<archivo>.pdf` para proyectar y `<archivo>-notas.pdf` con las notas del
presentador intercaladas después de cada lámina. Beamer oculta las notas por omisión, así
que sin esa segunda versión el guion no se ve en ninguna parte.

La primera compilación puede tardar varios minutos porque TinyTeX instala paquetes que
falten. Es normal; no la interrumpas.

**Nombra el `.qmd` sin espacios ni acentos.** Quarto convierte los espacios en guiones al
escribir el PDF, así que el archivo de salida deja de coincidir con el de entrada y los
scripts que lo buscan por nombre fallan en silencio. Usa `lima-demografia.qmd`, no
`Lima demografía.qmd`.

Compilar sin errores **no** significa que la presentación esté bien. Renderiza las
láminas a imagen y míralas:

```bash
Rscript -e 'n <- pdftools::pdf_info("archivo.pdf")$pages
            pdftools::pdf_convert("archivo.pdf", pages = 1:n, dpi = 110,
                                  format = "png",
                                  filenames = sprintf("rev-%02d.png", 1:n))'
```

Revisa cada PNG y confirma, lámina por lámina:

- Nada de texto cortado, fuera de caja ni encimado.
- Ningún bloque de código desbordado por la derecha.
- Ninguna lámina saturada de texto.
- El chevron verde **completo**, no una astilla: si sale recortado, algo se está pintando
  encima y hay que mover esa decoración al `footline`.
- Los logotipos en su sitio: BID abajo a la izquierda, IREM abajo a la derecha.
- Ninguna lámina con número de página.
- En la portada: el panel del logotipo con su curva intacta, sin ningún resto de otro
  logotipo detrás, y el título sin tocar la foto.

Si algo desborda, la solución casi siempre es **partir la lámina en dos**, no reducir el
tamaño de letra.

#### Lo que va a sangre, se mide; no se mira

Una franja blanca de 2 mm es invisible a simple vista en un PNG pequeño y arruina la
portada proyectada. Comprueba con números que la fotografía llega a los bordes:

```bash
uv run --with pillow python -c "
from PIL import Image
im=Image.open('rev-01.png').convert('RGB'); W,H=im.size; px=im.load()
nb=lambda y: sum(1 for x in range(int(0.55*W),W,3) if not all(v>245 for v in px[x,y]))
print('fila superior:', nb(0), ' fila inferior:', nb(H-1), '  (0 = franja blanca)')
"
```

Ambos números deben ser altos. Un cero significa franja blanca y portada mal montada.

## Elementos del formato

Láminas normales en Markdown: `#` abre sección (genera divisoria azul automática), `##`
abre lámina.

Para láminas especiales, un encabezado vacío con clase `.plain` y el comando dentro de un
bloque LaTeX crudo:

````markdown
## {.plain}

```{=latex}
\ideaGrande{La afirmación que deben recordar}
\note{Lo que yo digo aquí, no lo que se proyecta.}
```
````

**Nunca escribas `\begin{frame}` a mano.** Quarto ya tiene la lámina abierta y anidar un
frame dentro de otro rompe la compilación con `! Extra }, or forgotten \endgroup` — el PDF
sale truncado, con menos láminas de las que escribiste y sin mensaje evidente de qué pasó.

| Comando | Para qué sirve |
|---|---|
| `\ideaGrande{...}` | Una sola afirmación, texto grande y centrado |
| `\cifra{41\%}{qué significa}` | Un dato que debe golpear |
| `\pregunta{...}` | Momento participativo, con etiqueta visible para la audiencia |
| `\laminaGracias` | Cierre. Acepta otro texto: `\laminaGracias[Preguntas]` |
| `\concepto{término}{frase}` | Caja de concepto, para láminas de vocabulario |
| `\logosPie` | Añade los dos logotipos a una lámina `.plain` |

Las láminas `.plain` no llevan pie, así que tampoco logotipos. **La última lámina de la
presentación sí debe llevarlos**: agrégale `\logosPie` dentro del mismo bloque LaTeX.
`\laminaGracias` ya los incluye por su cuenta.

Las divisorias de sección son automáticas: cada `#` genera una lámina azul a sangre. No
las escribas a mano.

Notas del presentador en láminas Markdown:

```markdown
::: {.notes}
Lo que yo digo, no lo que se proyecta.
:::
```

Escribe notas en **toda** lámina que no sea obvia: son el guion de quien presenta.

### Láminas de vocabulario

Para explicar varios términos, **rejilla de cajas en vez de lista de viñetas**: cada
concepto queda delimitado visualmente, que es justo lo que una lista no hace.

````markdown
## Los 4 del día a día

```{=latex}
\vspace{1mm}
\concepto{Repositorio}{La carpeta del proyecto, pero con memoria}\hfill
\concepto{Commit}{La foto, con una nota de qué cambió y por qué}

\vspace{4mm}
\concepto{Push}{Subir tus fotos al álbum compartido}\hfill
\concepto{Pull}{Bajar las fotos que subieron las demás}
```
````

Dos cajas por fila separadas con `\hfill`: 2 × 60 mm caben en el área de texto de 126 mm.
Para tres conceptos usa dos filas (2 + 1), **no** tres cajas angostas, para que el ancho no
cambie entre láminas. Máximo cuatro por lámina.

#### Cuándo cajas y cuándo viñetas

Cuando una lámina tiene tres o cuatro puntos, pregúntate si son **paralelos** o una
**secuencia**:

| Los puntos son… | Usa | Por qué |
|---|---|---|
| Paralelos entre sí — conceptos, lineamientos, ideas de cierre | **Cajas** | Cada uno queda delimitado y se lee de un vistazo, en cualquier orden |
| Una secuencia — primero esto, después aquello | **Viñetas** o lista numerada | Las cajas sugieren independencia y borran el orden, que es justo lo que importa |
| Uno depende del anterior | **Viñetas** | Igual: la caja rompe el hilo |

Ejemplos de la práctica: las láminas de vocabulario y las de recapitulación van en cajas;
la del flujo de trabajo —antes, mientras, al terminar— va en viñetas, porque el orden **es**
el contenido.

No metas en cajas un punto que necesita más de dos líneas de explicación. Si no cabe en dos,
o lo acortas o la lámina no era de cajas.

Las cajas no parten palabras a propósito, así que una descripción larga produce una línea
corta en lugar de un guion. Si la frase no cabe en dos líneas, acórtala.

## Identidad visual

Paleta medida de `BID-IREM-TemplatePPT2025.pptx`. **Ojo**: el tema de Office declarado en
los `.pptx` oficiales es el de omisión (Calibri, `#4472C4`) y no sirve de referencia; la
identidad está aplicada a mano, figura por figura.

| Color | Hex | Uso |
|---|---|---|
| Azul institucional | `#367CBC` | títulos, divisorias, enlaces |
| Verde institucional | `#98CE63` | acento, viñetas, cifras, filetes |
| Gris oscuro | `#404040` | texto principal |
| Gris de apoyo | `#9B9B9D` | texto secundario, numeración |
| Gris suave | `#EFEEEE` | fondos de bloque y de código |

Tipografía: **Uni Sans** (corporativa del BID) si está instalada; si no, **Arial**, que es
la que aplican de hecho las plantillas de IREM. El respaldo es automático, no hay que
tocar nada. Código en Menlo.

Geometría replicada de las plantillas oficiales, convertida del lienzo de PowerPoint
(13,333 × 7,5 in) al de Beamer (160 × 90 mm) a razón de 12 mm por pulgada:

| Elemento | Posición | Tamaño |
|---|---|---|
| Chevron verde | (10,4 , 4,7) mm | 7,3 mm de ancho |
| Título de lámina | 17,8 mm desde el borde izquierdo | — |
| Logotipo BID | (2,2 , 79,3) mm | 13,3 mm de ancho |
| Logotipo IREM | (127,9 , 79,6) mm | 30,4 mm de ancho |

**Las láminas no llevan numeración**, por decisión de formato. No la agregues.

La portada usa `portada-completa.png` **íntegra**, nunca recortada de nuevo: a altura de
lámina y pegada al borde derecho ocupa 131,57 mm, o sea desde x = 28,43 mm. Su tercio
izquierdo es blanco y se funde con la lámina.

El asset **ya viene recortado de sus márgenes blancos**. La imagen original traía 2,07 %
de blanco arriba y 1,64 % abajo, así que colocarla a altura completa dejaba la *imagen* a
sangre pero la *fotografía* con dos franjas blancas de casi 2 mm. No vuelvas a introducir
márgenes: la fotografía debe tocar el borde superior e inferior de la lámina.

**No intentes recomponer la portada** separando la foto del panel del logotipo. Ya se
probó y produce dos defectos difíciles de ver hasta que se amplía: la foto empieza en el
30,12 % de la imagen pero el panel se extiende sobre ella hasta el 44,72 %, así que
cualquier recorte de la foto arrastra un trozo de panel que luego asoma detrás del panel
superpuesto; y recortar el panel por su borde derecho lo corta antes de la curva y lo deja
con esquina cuadrada. La imagen completa evita ambos.

El bloque de texto mide 62 mm y va centrado en la franja blanca que deja la fotografía,
que arranca en x = 68,1 mm: su eje cae en 34,05 mm, no en el centro de la lámina. El panel
del logotipo ocupa de y = 9,3 a 25,2 mm, por eso el título empieza en 33,7 mm.

En la portada las palabras no se parten. El truco de `\hyphenpenalty=10000` no basta con
babel en español, así que la plantilla anula el `\hyphenchar` de cada fuente después de
seleccionarla. Si añades un elemento nuevo a la portada, repite ese `\hyphenchar` o volverás
a ver cortes como "cuan-do".

Toda esta decoración vive en el `footline`, nunca en el `headline`: el pie se compone
después del título de lámina, cuya caja tiene fondo blanco y recortaría el chevron.
Las láminas `.plain` no la llevan, a propósito, para que las de idea única respiren.

Logotipos en `_extensions/irem/logos/`:

| Archivo | Qué es |
|---|---|
| `chevron.png` | chevron verde, marca de esquina superior izquierda |
| `logo-pie-derecha.png` | mesoamérica MALARIA en alta resolución |
| `logo-pie-izquierda.png` | logotipo del BID |
| `portada-completa.png` | imagen oficial de portada, íntegra: panel del logotipo, fotografía y barra de auspiciadores |
| `cintilla-comite-esp.png` | Gates, Carlos Slim, Fondo Mundial, BID |
| `cintilla-socios-esp.png` | OPS, Clinton Health Access Initiative, COMISCA, Proyecto Mesoamérica, BID |

Las cintillas **no van en el cuerpo** de la presentación. Se usan solo si el destinatario
es externo (donante, comité), con `\cintilla{comite}` o `\cintilla{socios}` en portada o
cierre. Para material interno se omiten.

## Criterios de calidad

Antes de entregar, revisa que se cumpla todo esto:

- Ninguna lámina pasa de 40 palabras, salvo que sea una tabla.
- Ninguna lista pasa de cuatro viñetas.
- Ningún título de lámina ocupa más de dos líneas.
- Toda sección tiene su divisoria.
- Toda lámina no obvia tiene nota del presentador.
- Hay al menos un momento participativo cada diez minutos de exposición.
- La última lámina repite el mensaje único.

## Errores frecuentes

- **Volcar el informe en láminas.** La presentación es un argumento, no un resumen.
- **Reducir la letra para que quepa.** Si no cabe, son dos láminas.
- **Viñetas con oraciones completas.** La oración completa va en las notas.
- **Divisorias sin propósito.** Si una sección tiene una sola lámina, no es sección.
