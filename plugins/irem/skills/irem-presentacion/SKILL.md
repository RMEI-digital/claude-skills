---
name: irem-presentacion
description: Genera presentaciones en Quarto con el formato institucional Mesoamérica Malaria (IREM) / BID y las compila a PDF. Úsala cuando alguien pida "una presentación", "unas diapositivas", "un deck" o "unas láminas" para el equipo, para una reunión, para el BID o para un donante; también cuando pida una propuesta para un ministerio, un comité o una contraparte de gobierno, o convertir un informe, unas notas o un documento en presentación. No la uses para documentos que no sean presentaciones.
---

# Presentaciones institucionales IREM / BID

Produce presentaciones en Quarto (`.qmd`) que compilan a PDF con la identidad
visual oficial, replicada de `ppt_resultados_IREM_2025_master_logos.pptx`, que es
el master vigente: portada de piezas sueltas con fotografía a sangre, Montserrat,
logotipos de mesoamérica MALARIA y del BID en el pie, portadillas blancas y tablas
de cabecera azul.

## Regla de oro

**El formato no se negocia, el contenido sí.** Nunca inventes colores, tipografías
ni logotipos: usa la extensión `_extensions/irem/` tal como está. Si el usuario
pide un color distinto, adviértele que rompe la identidad institucional antes de
hacerlo.

## Cómo trabajar

### 1. Antes de escribir nada, consigue tres cosas

Si el usuario no las dio, pregúntalas en un solo mensaje:

- **Audiencia** — de ella depende el nivel técnico y cuánto vocabulario hay que explicar.
  Pregunta también **si es interna o si va a un externo** (ministerio, donante, comité,
  contraparte de gobierno): si es externa, la estructura no la inventas, está fija: la
  trae completa el apartado «Si la presentación es una propuesta a un externo».
- **Duración** — define el número de láminas (ver presupuesto abajo).
- **El mensaje único** — la frase que la audiencia debe recordar si olvida todo lo demás.

Si el usuario trae material de origen (informe, notas, datos), léelo antes de
proponer estructura. No resumas el documento lámina por lámina: eso produce
presentaciones que se leen en voz alta. Extrae el argumento y constrúyelo.

### 2. Propón la estructura y espera aprobación

Entrega un índice de una línea por lámina, con el minutaje por sección. No generes
el `.qmd` hasta que el usuario apruebe el índice. Ahorra reescrituras completas.

Presupuesto de láminas para una charla **conducida por láminas**, a densidad
intermedia:

| Duración | Láminas | Portadillas |
|---|---|---|
| 10 min | 8–10 | 2 |
| 20 min | 16–20 | 3 |
| 30 min | 26–32 | 4–5 |
| 45 min | 38–46 | 5–6 |

Cuenta las portadillas dentro del total: consumen segundos, no minutos.

**Si la charla es conducida por demos, esta tabla no aplica: divídela más o menos a
la mitad.** Un demo en vivo consume varios minutos sin consumir ni una lámina, y un
ejercicio con la audiencia lo mismo. Una charla de 30 minutos con cuatro demos y dos
ejercicios aterriza en 14–22 láminas, no en 30. Antes de fijar el número, cuenta
cuántos minutos se van en pantalla en vivo y réstalos del presupuesto.

Aplicar la tabla a ciegas produce presentaciones infladas que no se alcanzan a dar.

#### Cuántas láminas pueden llevar una frase sola

Es la cuenta que más se descuida, porque cada lámina vacía por separado parece
defendible y solo se nota el abuso al sumarlas. En el master hay 20 láminas: portada,
guía de estilo, tres portadillas, cierre y **catorce de contenido denso**. Una de cada
cuatro lleva una frase o menos.

Y algo que conviene tener presente: **el master no tiene ni una sola lámina de una sola
afirmación.** Ni `\ideaGrande`, ni `\cifra`, ni `\pregunta`. Esos tres comandos vienen
de la plantilla anterior, que era para charlas de capacitación, no para reportar. Siguen
disponibles porque funcionan, pero son un préstamo y hay que tratarlos como tal.

Dos reglas, y las dos se verifican solas con `./revisar.py`:

- **Ninguna sección con menos de dos láminas de contenido lleva portadilla.** Es la misma
  regla de siempre («si una sección tiene una sola lámina, no es sección»), pero ahora
  importa el doble: cada portadilla es una lámina de una frase, y siete secciones son
  siete láminas casi vacías. La sección puede seguir existiendo como argumento con su
  nombre en el título de la lámina, sin `#` y por lo tanto sin divisoria.
- **Como máximo una lámina de una sola afirmación por cada seis de contenido, y nunca dos
  seguidas.** La que sí se gana el lugar es la del final, la que repite el mensaje único.
  `\pregunta` no va en una propuesta a un externo: un comité no levanta la mano.

Entre portadillas, láminas de despliegue y cierre, **no más de un tercio del total** debe
llevar una frase o menos. Si te pasas, casi siempre es porque hay demasiadas secciones
para el tamaño del deck, no porque sobren cifras.

### Si la presentación es una propuesta a un externo

Cuando la presentación va a un ministerio, un donante, un comité o una contraparte de
gobierno, y sirve para **pedir una decisión**, la estructura no se improvisa. Son siete
secciones, en este orden, y cada título es literal: se usa tal cual, sin sinónimos.

| # | Sección | Qué responde |
|---|---|---|
| 1 | **La solicitud** | Qué nos pidieron, quién y cuándo |
| 2 | **Lo que sabemos** | La evidencia que ya existía antes de que entráramos |
| 3 | **Lo que vemos** | Lo que encontramos nosotros, por actor o por nivel |
| 4 | **Lo que consideramos** | Los criterios con los que se descartaron las otras opciones |
| 5 | **Lo que buscamos** | El fin y el objetivo, en lenguaje de marco lógico |
| 6 | **Lo que proponemos** | La solución, y cuánto cuesta |
| 7 | **Siguientes pasos** | Qué se decide hoy, quién lo hace y para cuándo |

Cada una es un `#` de Quarto, así que cada una genera su portadilla.

**La solicitud va primero, antes del contexto.** Es contraintuitivo y es lo que más se
equivoca: uno quiere explicar el problema antes de llegar al encargo. Para quien escucha
desde afuera, el contexto sin el encargo es ruido, porque todavía no sabe por qué le están
hablando.

**«Lo que sabemos» y «lo que vemos» no son lo mismo, y separarlas es lo que da autoridad.**
La primera es la evidencia documentada que cualquiera podía consultar; la segunda es lo que
fuimos a levantar. Si las fundes, la propuesta parece opinión. Es normal que «lo que vemos»
ocupe varias láminas, una por actor o por nivel, y es la sección más larga.

**No te saltes «lo que consideramos».** Es la que convierte la propuesta en una decisión
razonada en vez de en una preferencia: aquí van los criterios y, si hubo alternativas
descartadas, por qué se cayeron. Sin esta sección, un comité pregunta «¿y por qué no hicieron
la otra cosa?» y no hay respuesta en la presentación.

**«Siguientes pasos» no es opcional y es la que más se olvida.** Una propuesta que termina en
el cierre deja la decisión flotando. Tiene que decir qué se aprueba hoy, quién queda
responsable y con qué fecha. Si no hay una fecha, no hay siguiente paso.

#### Reparto de láminas

Para una propuesta de 30 minutos, unas 26 láminas:

| Sección | Láminas |
|---|---|
| La solicitud | 1 |
| Lo que sabemos | 2–3 |
| Lo que vemos | 6–8 |
| Lo que consideramos | 1–2 |
| Lo que buscamos | 1 |
| Lo que proponemos | 5–7 |
| Siguientes pasos | 1–2 |

**Siete secciones cuestan siete portadillas.** Esa es la letra pequeña de esta espina: solo
se paga sola en una propuesta de veinte láminas de contenido para arriba. Por debajo de eso,
las secciones flacas no llevan `#`: su nombre va en el título de la lámina y te ahorras la
divisoria. Una propuesta de trece láminas con siete portadillas es la mitad del deck en
blanco.

«Lo que vemos» y «lo que proponemos» se llevan la mitad del deck entre las dos. Si «lo que
sabemos» crece más que «lo que vemos», estás presentando un informe de escritorio, no una
propuesta.

#### Errores que ya se cometieron

Esto sale de revisar propuestas reales del equipo. Todos son de contenido, no de formato:

- **Repetir el mismo título en tres láminas seguidas.** Si tres láminas se llaman «Lo que
  proponemos para puntos rurales», quien escucha no sabe qué cambió entre una y otra.
  El título dice qué aporta **esa** lámina: la herramienta, luego el costo, luego las
  implicaciones.
- **Rotular una lámina con el título de otra.** Un «flujo actual» y un «flujo propuesto» con
  el mismo título se leen como la misma lámina repetida, y se pierde justamente la
  comparación que era el argumento.
- **Mandar la tabla de costos con columnas vacías.** Una tabla con «Ventajas» y «Desventajas»
  en blanco frente a un donante dice que la comparación no se hizo. O la llenas o quitas la
  columna.
- **Dejar marcadores vivos en las notas.** Cosas como «[poner algo de lo que nos diga
  Fulano]» sobreviven hasta la versión que se envía. Antes de entregar, busca `[` en las
  notas.
- **Escribir notas en dos láminas de veinte.** En una propuesta a un externo las notas
  importan más que en cualquier otra presentación, porque casi siempre la expone alguien que
  no la escribió.
- **69 palabras por lámina.** Es el promedio real de la última propuesta, contra el tope de
  40. La sección «lo que vemos» es la que más se desborda: cada actor trae cinco hallazgos y
  se vuelcan todos. Van los dos que cambian la decisión; el resto, a las notas.

### 3. Monta el proyecto

Claude Code te informa el directorio base de esta skill al invocarla («Base
directory for this skill»). Úsalo como `$BASE`; **no escribas una ruta fija**,
porque cambia según si la skill está instalada localmente o distribuida como
plugin.

```bash
BASE="<el directorio base que te informó Claude Code>"
mkdir -p <carpeta>
cp -R "$BASE/plantilla/_extensions" <carpeta>/
cp "$BASE/plantilla/renderizar.sh" "$BASE/plantilla/revisar.py" <carpeta>/
chmod +x <carpeta>/renderizar.sh <carpeta>/revisar.py
```

Después escribe el `.qmd` en esa carpeta con este encabezado:

```yaml
---
title: "Título"
subtitle: "TALLER DE CAPACITACIÓN, AGOSTO 2026"
author: "Quien presenta"
date: today
date-format: long
lang: es
format: irem-beamer
---
```

Los cuatro campos caen en sitios distintos de la portada, y no son los de siempre:

| Campo | Dónde cae |
|---|---|
| `subtitle` | La **volanta** dentro de la barra verde: evento y mes, en mayúsculas |
| `title` | El título grande, en gris oscuro |
| `author` | El renglón gris de abajo, donde el master pone el país |
| `date` | Debajo de la autoría, más pequeño |

El `subtitle` **no es un subtítulo**: es la volanta. Si le pones una frase
explicativa larga, se encoge para caber en la barra y queda ilegible. Va corto y en
mayúsculas.

**No escribas la fecha a mano.** Quarto intenta parsear el campo `date` y una fecha
en español como `"20 de agosto de 2026"` produce un literal `Invalid Date` impreso
en la portada. Con `date: today` más `date-format: long` y `lang: es`, Quarto la
escribe bien en español. Si necesitas una fecha fija, úsala en ISO
(`date: 2026-08-24`) y deja que `date-format` la traduzca.

**Montserrat tiene que estar instalada.** Es la tipografía que el master trae
embebida y no viene con macOS. Sale del paquete de TeX Live:

```bash
tlmgr install montserrat
```

Sin ella la presentación compila igual pero sale en Arial, y eso ya no es el
formato institucional. Compruébalo con `kpsewhich Montserrat-Regular.otf`.

### 4. Compila y **verifica con tus propios ojos**

```bash
cd <carpeta> && ./renderizar.sh <archivo>.qmd
```

Genera dos PDF: `<archivo>.pdf` para proyectar y `<archivo>-notas.pdf` con las
notas del presentador intercaladas después de cada lámina. Beamer oculta las notas
por omisión, así que sin esa segunda versión el guion no se ve en ninguna parte.

La primera compilación puede tardar varios minutos porque TinyTeX instala paquetes
que falten. Es normal; no la interrumpas.

**Nombra el `.qmd` sin espacios ni acentos.** Quarto convierte los espacios en
guiones al escribir el PDF, así que el archivo de salida deja de coincidir con el
de entrada y los scripts que lo buscan por nombre fallan en silencio. Usa
`lima-demografia.qmd`, no `Lima demografía.qmd`.

Compilar sin errores **no** significa que la presentación esté bien. Pasa primero el
verificador, que revisa lo mecánico:

```bash
./revisar.py <archivo>.qmd
```

Comprueba el **contenido** sobre el `.qmd` (palabras por lámina, viñetas, títulos
repetidos, marcadores `[...]` sin resolver, cobertura de notas y, si es una propuesta a un
externo, que estén las siete secciones y en orden) y el **formato** sobre los PNG (que
nada invada la banda de los logotipos ni se salga por los lados, y que la portada sangre).
Sale con código 1 si encuentra algo.

Lo que el verificador no puede juzgar es si el argumento se entiende, y eso es lo que
importa. Así que después renderiza las láminas y míralas:

```bash
Rscript -e 'n <- pdftools::pdf_info("archivo.pdf")$pages
            pdftools::pdf_convert("archivo.pdf", pages = 1:n, dpi = 110,
                                  format = "png",
                                  filenames = sprintf("rev-%02d.png", 1:n))'
```

El verificador ya dejó estos PNG en `.revision/`. Revísalos y confirma, lámina por lámina:

- Nada de texto cortado, fuera de caja ni encimado.
- Ningún bloque de código desbordado por la derecha.
- Ninguna lámina saturada de texto.
- Nada encima de los logotipos del pie: el área útil termina en **77 mm**.
- Los logotipos en su sitio: **mesoamérica MALARIA abajo a la izquierda, BID abajo
  a la derecha**. Van así, no al revés.
- Ninguna lámina con número de página.
- En la portada: la fotografía tocando el borde superior y el derecho, la volanta
  dentro de la barra verde y en un solo renglón, y el título sin llegar a la foto.

Si algo desborda, la solución casi siempre es **partir la lámina en dos**, no
reducir el tamaño de letra.

#### Lo que va a sangre, se mide; no se mira

Una franja blanca de 2 mm es invisible a simple vista en un PNG pequeño y arruina la
portada proyectada. Comprueba con números que la fotografía llega a los bordes:

```bash
uv run --with pillow python -c "
from PIL import Image
im=Image.open('rev-01.png').convert('RGB'); W,H=im.size; px=im.load()
blanco=lambda p: all(v>246 for v in p)
arriba=sum(1 for x in range(int(0.60*W),W) if not blanco(px[x,0]))
derecha=sum(1 for y in range(0,int(0.93*H)) if not blanco(px[W-1,y]))
print('borde superior:', arriba, ' borde derecho:', derecha, '  (0 = franja blanca)')
"
```

Ambos números deben ser altos. Un cero significa franja blanca y portada mal
montada.

**La franja blanca de abajo sí es del diseño.** La fotografía se detiene a 3,9 mm
del borde inferior, que es el aire donde respira la cintilla de donantes. No la
elimines pensando que es un defecto.

#### La trampa del JPEG

Si alguna vez cambias una imagen del formato, **no la guardes en JPEG**. xelatex lo
incrusta perfectamente, pero el poppler que usa `pdftools::pdf_convert` lo pinta en
blanco: el PDF sale bien y la revisión por PNG lo muestra roto. Es la peor
combinación posible, porque lleva a «arreglar» algo que no estaba mal. Los assets
del formato están todos en PNG por esta razón.

**Y la trampa muerde también al revés, midiendo un PDF ajeno.** El PDF del master trae
su foto de portada en JPEG. Al renderizarlo con `pdftools` para tomarle medidas, la
portada sale sin foto y uno concluye que el master no la lleva. Sí la lleva. Cuando
midas un PDF que no compilaste tú, renderízalo con Quick Look, que no tiene ese defecto:

```bash
qlmanage -t -s 2666 -o <carpeta> <archivo>.pdf
```

Comprueba antes si el PDF trae JPEG, y si trae, no te fíes de poppler:

```bash
python3 -c "import re; print(len(re.findall(rb'/DCTDecode', open('archivo.pdf','rb').read())))"
```

## Elementos del formato

Láminas normales en Markdown: `#` abre sección (genera portadilla automática), `##`
abre lámina.

Para láminas especiales, un encabezado vacío con clase `.plain` y el comando dentro
de un bloque LaTeX crudo:

````markdown
## {.plain}

```{=latex}
\ideaGrande{La afirmación que deben recordar}
\note{Lo que yo digo aquí, no lo que se proyecta.}
```
````

**Nunca escribas `\begin{frame}` a mano.** Quarto ya tiene la lámina abierta y
anidar un frame dentro de otro rompe la compilación con `! Extra }, or forgotten
\endgroup` — el PDF sale truncado, con menos láminas de las que escribiste y sin
mensaje evidente de qué pasó.

| Comando | Para qué sirve |
|---|---|
| `\numerado{01}{texto}` | Fila numerada: cifra verde y caja verde. Va dentro de `numerados` |
| `\realce{...}` | Recuadro azul de contorno a la derecha, acompaña a los numerales |
| `\panelDerecho{...}` | Columna de texto a la derecha de los numerales |
| `\ideaGrande{...}` | Una sola afirmación, texto grande y centrado |
| `\cifra{41\%}{qué significa}` | Un dato que debe golpear |
| `\pregunta{...}` | Momento participativo, con etiqueta visible para la audiencia |
| `\concepto{término}{frase}` | Caja de concepto, para láminas de vocabulario |
| `\notaPie{...}` | Nota en gris pequeño al pie de la lámina: denominadores, salvedades |
| `\laminaGracias` | Cierre. Acepta otro texto: `\laminaGracias[Preguntas]` |
| `\logosPie` | Añade los dos logotipos a una lámina `.plain` |
| `\cintilla{comite}` o `\cintilla{socios}` | Cintilla de logos, solo para público externo |

Las láminas `.plain` no llevan pie, así que tampoco logotipos. **La última lámina de
la presentación sí debe llevarlos**: agrégale `\logosPie` dentro del mismo bloque
LaTeX. `\laminaGracias` ya trae su propia banda de logotipos.

Las portadillas de sección son automáticas: cada `#` genera una lámina blanca con el
título centrado en azul. No las escribas a mano.

Notas del presentador en láminas Markdown:

```markdown
::: {.notes}
Lo que yo digo, no lo que se proyecta.
:::
```

Escribe notas en **toda** lámina que no sea obvia: son el guion de quien presenta.

### Numerales 01 / 02 / 03

El elemento de firma del master: aparece en tres de sus once layouts. Úsalo para
objetivos, criterios o pasos que la audiencia deba contar.

````markdown
## Objetivos de la medición

```{=latex}
\begin{numerados}
\numerado{01}{Verificar el cumplimiento de los indicadores acordados}
\numerado{02}{Diagnosticar la situación de la eliminación de la malaria}
\numerado{03}{Medir el progreso respecto de la línea de base}
\end{numerados}

\realce{El matiz que no cabe en los numerales}
```
````

**El entorno `numerados` no es decorativo, es obligatorio**: es lo que pone el
contador de filas en cero. Sin él, la segunda lámina con numerales empieza a
dibujar en la fila 4, o sea fuera de la lámina, y no da ningún error.

Máximo tres por lámina. El master nunca pone una cuarta, y no cabe: la tercera fila
ya termina a 4,8 mm del logotipo del pie.

Cada caja admite dos renglones de texto. Si tu punto no cabe en dos, acórtalo o no
era un numeral.

### Tablas

El master trae **cuatro layouts de tabla** de once, así que aquí la tabla es un
ciudadano de primera, no un recurso de emergencia. Hay dos caminos:

**Tabla de Markdown.** Sale con la tipografía y los filetes institucionales, pero
sin la banda azul de cabecera. Sirve para tablas pequeñas y de paso.

**Entorno `tablaIrem`.** Es la tabla del master. Úsalo cuando la tabla sea el
contenido de la lámina, que en este formato es casi siempre.

````markdown
```{=latex}
\begin{center}
\begin{tablaIrem}{m{58mm}rr}
\ch{COMPONENTE} & \ch{LÍNEA BASE (2019)} & \ch{PRIMERA FASE (2024)} \\
Evaluación periódica  & 75,0\% & \celdaCalor{medio}{62,5\%} \\
Retroalimentación     & 37,5\% & \celdaCalor{alto}{50,0\%} \\
\end{tablaIrem}
\end{center}

\notaPie{N: establecimientos en la muestra.}
```
````

Tres detalles que ahorran una recompilación:

- `\ch{}` va **celda por celda** en la cabecera. El color y la negrita no cruzan el
  `&`: cada celda de un `tabular` es su propio grupo.
- Usa `m{58mm}` y no `p{58mm}` para la columna ancha. Con `p` el encabezado de esa
  columna se descuelga y queda desalineado respecto de los demás.
- `\celdaCalor{bajo|medio|alto}{...}` pinta la celda con la escala de tres colores
  que el master declara en su lámina 16. Úsala solo donde haya una meta contra la
  cual comparar.

### Láminas de vocabulario

Para explicar varios términos, **rejilla de cajas en vez de lista de puntos**: cada
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

Dos cajas por fila separadas con `\hfill`: 2 × 66 mm caben en el área de texto de
137,6 mm. Para tres conceptos usa dos filas (2 + 1), **no** tres cajas angostas,
para que el ancho no cambie entre láminas. Máximo cuatro por lámina.

#### Cuándo cajas y cuándo puntos

Cuando una lámina tiene tres o cuatro elementos, pregúntate si son **paralelos** o
una **secuencia**:

| Los puntos son… | Usa | Por qué |
|---|---|---|
| Paralelos entre sí — conceptos, lineamientos, ideas de cierre | **Cajas** o **numerales** | Cada uno queda delimitado y se lee de un vistazo |
| Una secuencia — primero esto, después aquello | **Lista** | Las cajas sugieren independencia y borran el orden, que es justo lo que importa |
| Uno depende del anterior | **Lista** | Igual: la caja rompe el hilo |

Ejemplos de la práctica: las láminas de vocabulario van en cajas y las de objetivos
en numerales; la del flujo de trabajo (antes, mientras, al terminar) va en lista,
porque el orden **es** el contenido.

No metas en cajas un punto que necesita más de dos líneas de explicación. Si no cabe
en dos, o lo acortas o la lámina no era de cajas.

Las cajas no parten palabras a propósito, así que una descripción larga produce una
línea corta en lugar de un guion. Si la frase no cabe en dos líneas, acórtala.

## Identidad visual

Todo lo de esta sección sale de `ppt_resultados_IREM_2025_master_logos.pptx`, que
trae su propia guía de estilo en la lámina 2.

**Ojo con lo que el archivo declara y no cumple.** El `fontScheme` del tema dice
Arial y los layouts arrastran restos del export de Google Slides (título de 40 pt en
`#0070C0`). Nada de eso es la identidad: la identidad es la lámina 2 más lo que
aplican de hecho las láminas de contenido. Si alguna vez vuelves a medir el master,
no te fíes de los valores declarados.

### Paleta

| Color | Hex | Uso |
|---|---|---|
| Azul institucional | `#367CBC` | títulos, portadillas, cabecera de tabla, enlaces |
| Verde institucional | `#98CE63` | numerales, cajas, filetes |
| Gris oscuro | `#404040` | texto principal, título de portada |
| Gris de apoyo | `#9B9B9D` | texto secundario, notas al pie |
| Gris suave | `#EFEEEE` | fondos de bloque, texto sobre azul |
| Verde de portada | `#92C14B` | **solo** la barra de la volanta |

El verde de la barra de portada no es el verde institucional: es un punto más
apagado. Es lo que trae el master; no lo unifiques.

Escala de calor de tablas: `#F8696B` bajo, `#FFEB84` medio, `#63BE7B` alto.

### Tipografía

**Montserrat**, que es la que el master trae embebida en sus cuatro variantes. Viene
del paquete `montserrat` de TeX Live. El respaldo automático es Arial. Código en
Menlo.

Escala declarada en la lámina 2 del master, y la que se usa aquí:

| Rol | Master (pt) | Convertido | Aquí |
|---|---|---|---|
| Título de portadilla | 44 | 20,8 | 21 |
| Título de lámina | 32 | 15,1 | 16 |
| Subtítulo | 20 | 9,4 | 10,5 |
| Cuerpo y punteos | 14–16 | 6,6–7,6 | 10 |
| Tabla | 14 | 6,6 | 8,5 |
| Nota al pie | 10,5 | 5,0 | 7 |

La columna «convertido» aplica el factor de lienzo. Se respeta la geometría del
master pero no su escala de cuerpo: 14 pt sobre un lienzo del doble de ancho son
6,6 pt proyectados, que no se leen. Los elementos de despliegue (portada, portadilla,
cierre, numerales) sí usan el valor convertido, porque ahí sí funciona.

### Geometría

Convertida del lienzo de PowerPoint (338,667 × 190,5 mm) al de Beamer
(160 × 90 mm) a razón de **0,472441**.

| Elemento | Posición | Tamaño |
|---|---|---|
| Título de lámina | (11,2 , 5,2) mm | 137,6 mm de ancho |
| Cuerpo, primer renglón | y = 23,95 mm | margen 11,2 mm a cada lado |
| Logotipo mesoamérica | (2,0 , 77,5) mm | 21,0 mm de ancho |
| Logotipo BID | (146,9 , 78,5) mm | 9,8 mm de ancho |
| Franja azul del pie | y = 86,16 mm | a sangre, 2,22 mm de alto |
| Franja verde del pie | y = 88,38 mm | a sangre, 1,62 mm de alto |

**Las láminas no llevan numeración**, por decisión de formato. No la agregues.

**Este master no lleva chevron.** Si vienes de la plantilla anterior de IREM, ese
elemento ya no existe.

**La franja azul y verde del pie no está en el `.pptx`, pero sí en el PDF.** Se buscó en
la lámina, en su layout, en el slide master y en los otros doce `.pptx` del equipo: en
ninguno. En `ppt_resultados_IREM_2025_master_logos.pdf`, exportado del mismo deck, está
en las veinte láminas con el mismo valor al centésimo. Cuando los dos archivos discrepan,
**manda el PDF**, que es lo que la gente ve. Va en todas las láminas, portada incluida.

**Los logotipos del pie van al revés que en las plantillas viejas**: mesoamérica
MALARIA a la izquierda y grande, BID a la derecha y pequeño. El BID del pie va
recortado, sin la palabra «Administrador» que trae el logotipo completo.

Toda esta decoración vive en el `footline`, nunca en el `headline`: el pie se
compone después del título de lámina, cuya caja tiene fondo blanco y recortaría lo
que hubiera. Las láminas `.plain` no la llevan, a propósito, para que las de idea
única respiren.

### Portada

A diferencia del master anterior, **la portada se compone de piezas sueltas**: la
fotografía es un archivo independiente, no una imagen que ya trae el panel del
logotipo incrustado. Por eso aquí sí se posiciona elemento por elemento.

| Pieza | Posición | Tamaño |
|---|---|---|
| Logotipo mesoamérica | (7,7 , 8,4) mm | 35,5 mm de ancho |
| Barra verde | (6,6 , 23,7) mm | 50,6 × 4,4 mm, esquinas de 0,66 mm |
| Volanta | centrada en la barra | máx. 47 mm, en blanco |
| Título | (6,6 , 30,7) mm | 73,5 mm de ancho |
| Autoría y fecha | (7,7 , 67,2) mm | — |
| Cintilla de donantes | (7,1 , 76,0) mm | 66,3 mm de ancho |
| Fotografía | (91,2 , −0,3) mm | 68,9 × 86,4 mm |

La fotografía ya viene recortada al encuadre del master, que se queda con la mitad
derecha de la imagen original. No la recortes otra vez ni la sustituyas por la
original completa: cambia el encuadre.

En la portada las palabras no se parten. El truco de `\hyphenpenalty=10000` no basta
con babel en español, así que la plantilla anula el `\hyphenchar` de cada fuente
después de seleccionarla. Si añades un elemento nuevo a la portada, repite ese
`\hyphenchar` o volverás a ver cortes como "cuan-do".

### Listas

**En este master el primer nivel no lleva viñeta.** El layout declara `buNone` en
el nivel 1 y reserva solo una sangría de 6 mm. El punto aparece recién en el segundo
nivel, y en gris oscuro, no en verde.

Lo que separa un punto del siguiente es el aire, no el glifo. Si escribes puntos
largos que se envuelven a dos y tres renglones, la lámina se lee como un párrafo
partido en trozos y la decisión de no usar viñeta se convierte en un error de
composición. Con este formato, los puntos cortos no son una preferencia de estilo:
son lo que hace que la lámina funcione.

### Logotipos

En `_extensions/irem/logos/`:

| Archivo | Qué es |
|---|---|
| `logo-mesoamerica.png` | mesoamérica MALARIA; pie izquierdo y portada |
| `logo-bid.png` | BID recortado, sin «Administrador»; pie derecho |
| `portada-foto.png` | fotografía de portada, ya recortada al encuadre del master |
| `cintilla-donantes.png` | Carlos Slim, Fondo Mundial, BID, Gates; barra de la portada |
| `cierre-logos.png` | BID y mesoamérica MALARIA; banda de la lámina de cierre |
| `cintilla-comite-esp.png` | Gates, Carlos Slim, Fondo Mundial, BID |
| `cintilla-socios-esp.png` | OPS, CHAI, COMISCA, Proyecto Mesoamérica, BID |

Las dos últimas **no van en el cuerpo** de la presentación. La portada ya trae su
cintilla de donantes; estas se usan solo si el destinatario es externo (donante,
comité), con `\cintilla{comite}` o `\cintilla{socios}`. Para material interno se
omiten.

## Criterios de calidad

Antes de entregar, revisa que se cumpla todo esto:

- Ninguna lámina pasa de 40 palabras, salvo que sea una tabla.
- Ninguna lista pasa de cuatro puntos, ni ningún punto de dos renglones.
- Ningún título de lámina ocupa más de dos líneas.
- Toda sección tiene su portadilla.
- Toda lámina no obvia tiene nota del presentador.
- Hay al menos un momento participativo cada diez minutos de exposición.
- La última lámina repite el mensaje único.
- Nada invade la banda del pie: el área útil termina en 77 mm.
- Todas las láminas menos la portada llevan la franja azul y verde al pie.
- Ninguna sección lleva portadilla con menos de dos láminas de contenido.
- Las láminas de una frase (portadillas, despliegue y cierre) no pasan de un tercio.
- Ningún título de lámina se repite igual en dos láminas distintas.
- No queda ningún marcador `[...]` sin resolver, ni en las láminas ni en las notas.
- Ninguna tabla se entrega con celdas vacías que debieran tener contenido.

Si es una propuesta a un externo, además:

- Están las siete secciones y en su orden, empezando por «La solicitud».
- «Siguientes pasos» dice qué se decide, quién y con qué fecha.

## Errores frecuentes

- **Volcar el informe en láminas.** La presentación es un argumento, no un resumen.
- **Reducir la letra para que quepa.** Si no cabe, son dos láminas.
- **Puntos con oraciones completas.** La oración completa va en las notas.
  En este formato duele el doble, porque el primer nivel no tiene viñeta.
- **Portadillas sin propósito.** Si una sección tiene una sola lámina, no es sección.
- **Olvidar `\begin{numerados}`.** No da error, simplemente dibuja fuera de la lámina.
- **Poner el subtítulo largo.** `subtitle` es la volanta de la barra verde, no un
  subtítulo: si es largo se encoge hasta volverse ilegible.
