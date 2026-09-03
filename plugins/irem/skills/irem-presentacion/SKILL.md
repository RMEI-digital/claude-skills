---
name: irem-presentacion
description: Genera presentaciones con el formato institucional Mesoamérica Malaria (IREM) / BID, en PDF o en PowerPoint editable, desde una sola fuente en Quarto. Úsala cuando alguien pida "una presentación", "unas diapositivas", "un deck", "unas láminas", "un PowerPoint" o "un pptx" para el equipo, para una reunión, para el BID o para un donante; cuando pida el archivo editable para que lo modifique una contraparte; también cuando pida una propuesta para un ministerio, un comité o una contraparte de gobierno, o convertir un informe, unas notas o un documento en presentación. No la uses para documentos que no sean presentaciones.
---

# Presentaciones institucionales IREM / BID

Produce presentaciones con la identidad visual oficial, replicada de
`ppt_resultados_IREM_2025_master_logos.pptx`, que es el master vigente: portada de
piezas sueltas con fotografía a sangre, Montserrat, logotipos de mesoamérica
MALARIA y del BID en el pie, portadillas blancas y tablas de cabecera azul.

Se escribe una sola vez, en Quarto (`.qmd`), y de ahí salen **dos entregables**:
el PDF para proyectar y el `.pptx` editable para quien tenga que meterle mano. El
apartado siguiente dice cuál corresponde.

## Regla de oro

**El formato no se negocia, el contenido sí.** Nunca inventes colores, tipografías
ni logotipos: usa la extensión `_extensions/irem/` tal como está. Si el usuario
pide un color distinto, adviértele que rompe la identidad institucional antes de
hacerlo.

## Dos salidas, una sola fuente

El `.qmd` es el mismo para las dos. Lo que cambia es con qué se compila:

| | PDF (Beamer) | PowerPoint (`.pptx`) |
|---|---|---|
| Comando | `./renderizar.sh <archivo>.qmd` | `./renderizar-pptx.py <archivo>.qmd` |
| Deja | `<archivo>.pdf` y `<archivo>-notas.pdf` | `<archivo>.pptx` |
| Notas del presentador | en un PDF aparte, intercaladas después de cada lámina | en el panel de notas, que es donde PowerPoint las espera |
| Lo puede editar quien la recibe | no, necesita Quarto y LaTeX | sí, es un PowerPoint normal |
| Se ve igual en cualquier máquina | siempre | si quien lo abre tiene Montserrat instalada |

**Por omisión, PDF.** Es lo que no se descuadra al cambiar de computadora.

**PowerPoint en cuanto alguien más tenga que meter mano:** una contraparte que va a
editar las láminas, un ministerio que pide el archivo, quien va a exponer desde su
propia máquina, o una reunión donde se va a mover el orden en vivo.

Si no está claro, haz las dos: es el mismo `.qmd` y son dos comandos. Lo que **no**
se hace es escribir dos versiones del contenido.

## Cómo trabajar

### 1. Antes de escribir nada, consigue dos cosas

Si el usuario no las dio, pregúntalas en un solo mensaje:

- **Audiencia**: de ella depende el nivel técnico y cuánto vocabulario hay que explicar.
  Pregunta también **si es interna o si va a un externo** (ministerio, donante, comité,
  contraparte de gobierno): si es externa, la estructura no la inventas, está fija: la
  trae completa el apartado «Si la presentación es una propuesta a un externo».
- **Duración**: define el número de láminas (ver presupuesto abajo).

Y una tercera, que no es de contenido pero cambia lo que entregas: **si hace falta el
PowerPoint editable o basta el PDF.** Ver «Dos salidas, una sola fuente» arriba.

Si el usuario trae material de origen (informe, notas, datos), léelo antes de
proponer estructura. No resumas el documento lámina por lámina: eso produce
presentaciones que se leen en voz alta. Extrae el argumento y constrúyelo.

### 2. Propón la estructura y espera aprobación

Entrega un índice de una línea por lámina, con el minutaje por sección. No generes
el `.qmd` hasta que el usuario apruebe el índice. Ahorra reescrituras completas.

Presupuesto de láminas para una charla **conducida por láminas**, a densidad
intermedia:

| Duración | Láminas |
|---|---|
| 10 min | 8–10 |
| 20 min | 16–20 |
| 30 min | 26–32 |
| 45 min | 38–46 |

Son láminas de contenido. Por omisión no hay portadillas (ver abajo); si excepcionalmente
pones alguna, súmala aparte.

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

**La cuenta se hace midiendo tinta, no contando comandos.** `./revisar.py` calcula qué
porcentaje del área de contenido lleva tinta en cada lámina y marca las que bajan del 2%.
Es la única manera honesta de verlo: contar portadillas y comandos de despliegue se queda
corto, porque no ve la lámina de dos viñetas sueltas que en pantalla también se lee como
vacía. El tope es **15% del deck**.

Dos reglas más, y las dos se verifican solas:

- **Por omisión no se usan portadillas: la estructura va en los títulos.** El nombre de la
  sección es el título de la lámina y se repite en todas las de esa sección, calificado con
  dos puntos cuando hace falta: «Los números: despliegues y reversiones», «Los números:
  cuánto costó cada vuelta atrás». Vale igual para una charla interna que para una
  propuesta. Medido sobre tres presentaciones reales, con una portadilla por sección
  quedaba entre el 38 y el 40% de las láminas casi vacías; con la estructura en los
  títulos, **cero**. Si aun así pones una portadilla, que su sección tenga cuatro láminas
  o más.
- **Como máximo una lámina de una sola afirmación por cada seis de contenido, y nunca dos
  seguidas.** La que sí se gana el lugar es la del final, la que deja la idea con la que
  quieres que se queden. `\pregunta` no va en una propuesta a un externo: un comité no
  levanta la mano.

Si te pasas del tope, casi siempre es porque hay demasiadas secciones para el tamaño del
deck, no porque sobren cifras.

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

### Dos maneras de poner la espina en la lámina, y cuál usar

Esto es lo que más se equivoca, así que va antes que nada.

**Por omisión, la espina va en los TÍTULOS y no lleva portadillas.** El título de cada
lámina es el nombre de la sección, tal cual, y se repite en todas las láminas de esa
sección. Cuando hace falta precisar, se califica con dos puntos o con una preposición:

```
## Lo que vemos
## Lo que vemos
## Lo que vemos: flujo de información de muestras
## Lo que proponemos para puntos urbanos
## Lo que proponemos: implementación
```

Repetir el título **no es un error, es el mecanismo**. Lo que distingue una lámina de la
siguiente es el primer renglón del cuerpo, que hace de subtítulo: «A nivel Departamental»,
«A nivel Municipal», «En puntos rurales», «En gestores comunitarios». El título dice en qué
parte del argumento estamos; el primer renglón dice de qué trata esta lámina.

La ventaja no es solo de estilo. Una propuesta real del equipo tiene 19 láminas y **solo
dos** llevan una frase o menos (la portada y el cierre): un 11%. Con portadillas para las
siete secciones, ese mismo deck se iría a la mitad en blanco.

**Las portadillas son la excepción, no la alternativa.** Medido sobre las mismas tres
presentaciones, con `#` para cada sección quedaban entre el 38 y el 40% de las láminas con
una frase o menos; pasando la espina a los títulos, **cero**. El master de resultados sí
usa tres portadillas, pero para catorce láminas de contenido y en secciones grandes. Si vas
a poner una, que la sección tenga al menos cuatro láminas.

En Quarto: sin portadillas, todo va en `##` y no se usa `#` en absoluto. Esto vale también
para charlas internas, donde el título hace el mismo trabajo («Cómo nos fue: lo que sí
funcionó», «Los números: despliegues y reversiones»).

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

Este reparto es de láminas de contenido. Si decides usar portadillas, súmalas aparte y
relee arriba cuándo se ganan su lugar.

«Lo que vemos» y «lo que proponemos» se llevan la mitad del deck entre las dos. Si «lo que
sabemos» crece más que «lo que vemos», estás presentando un informe de escritorio, no una
propuesta.

#### Errores que ya se cometieron

Esto sale de revisar propuestas reales del equipo. Todos son de contenido, no de formato:

- **Dejar dos láminas indistinguibles.** Repetir el título está bien, es el mecanismo; lo
  que no puede repetirse es el par completo **título más primer renglón**. En una propuesta
  real había tres láminas seguidas con el mismo título y el mismo subtítulo: una traía la
  herramienta, otra el costo y otra las implicaciones, pero quien escuchaba veía tres veces
  el mismo encabezado. La corrección es la que ese mismo deck ya usaba en otra lámina:
  «Lo que proponemos: implementación», «Lo que proponemos: costo», «Lo que proponemos:
  implicaciones».
- **Dos láminas de flujo con el mismo título.** El flujo actual y el propuesto rotulados
  igual se leen como una lámina repetida, y se pierde justo la comparación que era el
  argumento. Califica cada una: «Lo que vemos: el flujo de hoy», «Lo que proponemos: el
  flujo nuevo».
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
cp "$BASE/plantilla/plantilla-irem.pptx" <carpeta>/
cp "$BASE/plantilla/renderizar.sh" "$BASE/plantilla/renderizar-pptx.py" \
   "$BASE/plantilla/pptx-a-pdf.sh" "$BASE/plantilla/revisar.py" <carpeta>/
chmod +x <carpeta>/*.sh <carpeta>/*.py
```

Se copia todo aunque solo vayas a hacer una de las dos salidas: son unos cientos de
kilobytes y así la otra está a un comando de distancia si la piden después.
`_extensions/` es la extensión de Quarto para el PDF, y de ahí saca también el
generador de PowerPoint los logotipos que no vienen en los layouts.

**La carpeta tiene que estar en un sitio normal del usuario** (Documentos, el
escritorio, un repositorio). Si la pones en `/tmp`, PowerPoint no puede exportar
desde ahí: su sandbox lo bloquea, y lo hace en silencio, diciendo que guardó.

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

**Montserrat tiene que estar instalada**, y hacen falta las dos instalaciones,
porque cada salida la busca en un sitio distinto:

```bash
tlmgr install montserrat                 # para el PDF, vía TeX Live
cp $(kpsewhich Montserrat-Regular.otf | xargs dirname)/Montserrat-{Regular,Bold,Italic,BoldItalic}.otf \
   ~/Library/Fonts/                      # para PowerPoint, como fuente del sistema
```

Sin la primera, el PDF compila igual pero sale en Arial, y eso ya no es el formato
institucional; compruébalo con `kpsewhich Montserrat-Regular.otf`. Sin la segunda,
PowerPoint sustituye la tipografía al abrir el `.pptx` y las líneas se parten en
otro sitio.

**Y hay que decírselo a quien lo reciba.** El `.pptx` lleva Montserrat embebida
(viene del master), pero PowerPoint de Mac ignora las fuentes embebidas: en Windows
se ve bien y en Mac no, salvo que la tengan instalada. Es gratis, en Google Fonts.
El verificador no puede comprobar esto: pasa en la máquina del otro.

### 4. Compila y **verifica con tus propios ojos**

**En PDF:**

```bash
cd <carpeta> && ./renderizar.sh <archivo>.qmd
```

Genera dos PDF: `<archivo>.pdf` para proyectar y `<archivo>-notas.pdf` con las
notas del presentador intercaladas después de cada lámina. Beamer oculta las notas
por omisión, así que sin esa segunda versión el guion no se ve en ninguna parte.

La primera compilación puede tardar varios minutos porque TinyTeX instala paquetes
que falten. Es normal; no la interrumpas.

**En PowerPoint:**

```bash
cd <carpeta> && ./renderizar-pptx.py <archivo>.qmd
```

Genera `<archivo>.pptx`. Aquí no hay LaTeX: el generador lee el mismo `.qmd` y va
montando las láminas sobre los layouts de `plantilla-irem.pptx`. Tarda un segundo.

Solo un archivo, no dos: las notas del presentador van al panel de notas de
PowerPoint, que es donde quien expone las va a buscar.

**Nombra el `.qmd` sin espacios ni acentos.** Quarto convierte los espacios en
guiones al escribir el PDF, así que el archivo de salida deja de coincidir con el
de entrada y los scripts que lo buscan por nombre fallan en silencio. Usa
`lima-demografia.qmd`, no `Lima demografía.qmd`.

Compilar sin errores **no** significa que la presentación esté bien. Pasa primero el
verificador, que revisa lo mecánico:

```bash
./revisar.py <archivo>.qmd
```

Comprueba tres cosas y las reporta por separado. El **contenido**, sobre el `.qmd`
(palabras por lámina, viñetas, títulos repetidos, marcadores `[...]` sin resolver,
cobertura de notas y, si es una propuesta a un externo, que estén las siete secciones
y en orden). El **formato**, sobre los PNG del PDF (que nada invada la banda de los
logotipos ni se salga por los lados, que la portada sangre, y que el PDF tenga tantas
láminas como describe el `.qmd`). Y **PowerPoint**, sobre el `.pptx` si existe: que
ninguna forma se salga del área útil, que el texto quepa en su caja y que ningún
renglón se haya quedado con la tipografía o el color que declaran los layouts, que no
son los del formato. Sale con código 1 si encuentra algo.

Lo de PowerPoint lo comprueba leyendo el archivo, sin renderizarlo, así que funciona
en cualquier sistema. Para verlo de verdad hay que convertirlo, y eso ya es macOS con
PowerPoint instalado:

```bash
./pptx-a-pdf.sh <archivo>.pptx
```

Deja `<archivo>-desde-pptx.pdf` y los PNG de todas las láminas en `.revision-pptx/`.
El nombre no es capricho: si el PDF saliera como `<archivo>.pdf` pisaría el de Beamer
sin avisar. Si el script se queda colgado, borra el `~$<archivo>.pptx` que deja
PowerPoint al abrir: con ese archivo presente vuelve a abrir en solo lectura y el
export no termina nunca.

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

Si hiciste el `.pptx`, mira también sus PNG (`.revision-pptx/`) y compáralos con los
del PDF. Tienen que contar lo mismo. Además, tres cosas que solo se ven ahí:

- **Nada en Arial.** Si un renglón salió en otra tipografía, es que se escapó de la
  corrida que fija la fuente a mano, y eso el verificador sí lo caza: hazle caso.
- **Ningún título celeste.** El azul del formato es `#367CBC`; el `#0070C0` que se
  parece viene de los layouts del master y es un resto del export de Google Slides.
- **Las notas, en el panel de notas.** Ábrelo y confirma que están, porque en el
  `.pptx` no hay una segunda versión donde se vean.

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

Láminas normales en Markdown: `##` abre lámina. `#` abre sección y genera una portadilla,
pero **por omisión no se usa**: la estructura va en los títulos de las láminas.

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
\endgroup`, y el PDF sale truncado, con menos láminas de las que escribiste y sin
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

**Todos estos comandos funcionan igual en las dos salidas.** El generador de
PowerPoint los lee del mismo bloque `{=latex}` y los dibuja con formas nativas: la
caja verde de un numeral es una autoforma, la tabla es una tabla de PowerPoint y el
recuadro de realce es un rectángulo redondeado. Quien reciba el archivo puede
editarlos.

Lo único que el `.pptx` no puede hacer es **ejecutar código**: un bloque
` ```{r} ` o ` ```{python} ` que calcule una figura solo corre en el camino del PDF.
Si la lámina lleva una figura calculada y hace falta el PowerPoint, guarda la figura
como `.png` y ponla con `![](figura.png)`, que sí funciona en las dos.

Si decides usar una portadilla, es automática: cada `#` genera una lámina blanca con el
título centrado en azul, y nunca se escribe a mano. Recuerda que cada una es una lámina
con una sola frase, así que tiene que ganarse el lugar.

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
| Paralelos entre sí (conceptos, lineamientos, ideas de cierre) | **Cajas** o **numerales** | Cada uno queda delimitado y se lee de un vistazo |
| Una secuencia: primero esto, después aquello | **Lista** | Las cajas sugieren independencia y borran el orden, que es justo lo que importa |
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

**Y hay una trampa que ya mordió una vez: la plantilla de Quarto encoge Montserrat.**
El LaTeX que genera trae `\defaultfontfeatures{Scale=MatchLowercase}`, que escala toda
fuente cargada después para igualar la altura de x de la romana, que es Latin Modern.
Montserrat tiene la x muy alta, así que la encoge al 82,5 %: la columna «Aquí» de la
tabla decía 16 pt y el PDF componía 13,2. Medido, no supuesto. La corrección de
densidad que argumenta este formato se perdía entera por ahí, y nadie lo vio porque
las medidas se habían tomado sobre posiciones, no sobre tipografía.

Por eso `irem.tex` carga la fuente con `Scale = 1` explícito. **No se lo quites**, y si
alguna vez el PDF se ve más apretado de lo que dice esta tabla, mide antes de tocar
nada:

```bash
uv run --with pymupdf python -c "
import pymupdf; d=pymupdf.open('archivo.pdf')
for b in d[3].get_text('dict')['blocks']:
    for l in b.get('lines',[]):
        for sp in l['spans']:
            print(round(sp['size'],1),'pt', sp['font'], repr(sp['text'][:34]))"
```

### Geometría

Convertida del lienzo de PowerPoint (338,667 × 190,5 mm) al de Beamer
(160 × 90 mm) a razón de **0,472441**.

| Elemento | Posición | Tamaño |
|---|---|---|
| Título de lámina | (11,2 , 5,2) mm | 137,6 mm de ancho |
| Cuerpo, primer renglón | y = 23,95 mm | margen 11,2 mm a cada lado |
| Logotipo mesoamérica | (2,0 , 77,5) mm | 21,0 mm de ancho |
| Logotipo BID | (146,9 , 78,5) mm | 9,8 mm de ancho |
| Franja azul del pie | y = 86,04 mm | a sangre, 2,26 mm de alto |
| Franja verde del pie | y = 88,30 mm | a sangre, 1,70 mm de alto |

**Las láminas no llevan numeración**, por decisión de formato. No la agregues.

**Este master no lleva chevron.** Si vienes de la plantilla anterior de IREM, ese
elemento ya no existe.

**El fondo no es blanco.** Lleva un degradado gris muy tenue en las esquinas (baja a
`#E6E6E6`) y, al pie, la franja azul sobre verde a sangre. Los dos vienen de una sola
imagen, `fondo.png`, que es el fondo del master tal cual.

Ese fondo es el relleno del slide master (`<p:bg>`), no una forma, y ahí es donde no lo
busca uno: buscándolo entre las formas de las láminas y de los layouts no aparece, y de
ahí sale la conclusión falsa de que el `.pptx` no lo trae. Sí lo trae. Si algún elemento
del formato parece no existir, mira el `<p:bg>` del master antes de darlo por ausente.

Consecuencia práctica: **ninguna caja puede llevar fondo blanco a lo ancho de la lámina**,
o borra el degradado. Por eso el título de lámina va sin `bg`.

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
| Autoría y fecha | (7,7 , 67,2) mm | . |
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

**En este master el primer nivel no lleva viñeta ni sangría: va al ras del título.** El
layout declara `buNone` y un `marL` de 12,7 mm, pero eso no es lo que se compone: en el PDF
del master el cuerpo arranca en 26,4 mm y el título en 26,5, o sea alineados. Otra vez lo
mismo, lo declarado no es lo aplicado; manda el render. El punto aparece recién en el
segundo nivel, y en gris oscuro, no en verde.

Las listas numeradas sí llevan 5 mm, porque el número necesita dónde ponerse. Con el
margen en cero se salía de la lámina por la izquierda.

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
| `fondo.png` | fondo de todas las láminas: degradado y franja azul y verde al pie |
| `portada-foto.png` | fotografía de portada, ya recortada al encuadre del master |
| `cintilla-donantes.png` | Carlos Slim, Fondo Mundial, BID, Gates; barra de la portada |
| `cierre-logos.png` | BID y mesoamérica MALARIA; banda de la lámina de cierre |
| `cintilla-comite-esp.png` | Gates, Carlos Slim, Fondo Mundial, BID |
| `cintilla-socios-esp.png` | OPS, CHAI, COMISCA, Proyecto Mesoamérica, BID |

Las dos últimas **no van en el cuerpo** de la presentación. La portada ya trae su
cintilla de donantes; estas se usan solo si el destinatario es externo (donante,
comité), con `\cintilla{comite}` o `\cintilla{socios}`. Para material interno se
omiten.

## El `.pptx` por dentro

Conviene saber de dónde sale, porque explica qué se puede tocar y qué no.

`plantilla-irem.pptx` **es el master institucional** al que se le quitaron las veinte
láminas de contenido. Conserva el slide master, los once layouts con sus nombres
(TAPA, Portadillas, Titulo y contenido, Cierre, los de numerales, los cuatro de
tabla), el tema, los medios y las cuatro variantes de Montserrat embebidas. Se deriva
con `derivar-plantilla-pptx.py`, que solo hay que volver a correr si la institución
publica un master nuevo.

De ahí salen gratis, sin escribir una línea: el fondo con su degradado y su franja
azul y verde (es el relleno del slide master, no una forma), los logotipos del pie en
todas las láminas de contenido, y la portada entera con la fotografía a sangre, la
barra verde y la cintilla de donantes. Por eso la portada del `.pptx` es idéntica a
la del master aunque el generador solo escriba tres textos.

Tres cosas que hay que tener presentes al tocar `renderizar-pptx.py`:

- **Los layouts mienten.** El master arrastra restos del export de Google Slides: el
  título viene declarado en 40 pt y en `#0070C0`, y el `fontScheme` del tema dice
  Arial. Por eso el generador fija a mano tamaño, color y tipografía en cada renglón
  que escribe. Si añades un elemento y no lo haces, saldrá en Arial y nadie lo notará
  hasta verlo al lado de otra lámina.
- **El interlineado no se declara igual.** LaTeX lo da en puntos absolutos
  (`\fontsize{10}{14.5}`) y PowerPoint como múltiplo de la altura natural de línea de
  la fuente, que en Montserrat es 1,219 em. Copiar el 1,45 tal cual separa las líneas
  un 22 % de más. La conversión está en el archivo.
- **Las láminas `.plain` usan `showMasterSp="0"`**, que es «ocultar gráficos de fondo»
  en el menú de PowerPoint: quita los logotipos heredados del layout y deja el fondo,
  que no es una forma. Es lo que hace que una lámina de una sola idea respire igual
  que en el PDF.

La escala es la misma en las dos salidas: el `.pptx` usa los puntos del PDF
multiplicados por el factor de lienzo, **no** los 14-16 pt de cuerpo del master. Así
las dos parten las líneas en las mismas palabras, que es la única forma de que una
corrección hecha sobre una salida valga para la otra.

Diferencias que quedan, medidas y aceptadas: la tabla arranca unos 4 mm más abajo, la
rejilla de conceptos queda 2 mm más apretada y el título cae 0,6 mm más abajo. Nada de
eso se ve salvo poniendo las dos láminas una encima de la otra.

## Criterios de calidad

Antes de entregar, revisa que se cumpla todo esto:

- Ninguna lámina pasa de 40 palabras, salvo que sea una tabla.
- Ninguna lista pasa de cuatro puntos, ni ningún punto de dos renglones.
- Ningún título de lámina ocupa más de dos líneas.
- Toda lámina no obvia tiene nota del presentador.
- En una charla interna, hay al menos un momento participativo cada diez minutos. En una
  propuesta a un externo, no: un comité no levanta la mano.
- Nada invade la banda del pie: el área útil termina en 77 mm.
- Todas las láminas llevan el fondo del master: degradado en las esquinas y franja al pie.
- La estructura va en los títulos, no en portadillas.
- Ninguna lámina baja del 2% de tinta, y las que se acerquen no pasan del 15% del deck.
- No hay dos láminas indistinguibles: el par título más primer renglón no se repite.
  Repetir solo el título es correcto y esperado.
- No queda ningún marcador `[...]` sin resolver, ni en las láminas ni en las notas.
- Ninguna tabla se entrega con celdas vacías que debieran tener contenido.

Si es una propuesta a un externo, además:

- Están las siete secciones y en su orden, empezando por «La solicitud».
- «Siguientes pasos» dice qué se decide, quién y con qué fecha.

Si entregas el `.pptx`, además:

- `./revisar.py` no reporta nada en el bloque POWERPOINT.
- Lo abriste, o miraste los PNG de `.revision-pptx/`, y cuenta lo mismo que el PDF.
- Las notas del presentador están en el panel de notas.
- Le dijiste a quien lo recibe que instale Montserrat, o asumes que lo abrirá en
  Windows, donde la fuente embebida sí funciona.

## Errores frecuentes

- **Volcar el informe en láminas.** La presentación es un argumento, no un resumen.
- **Reducir la letra para que quepa.** Si no cabe, son dos láminas.
- **Puntos con oraciones completas.** La oración completa va en las notas.
  En este formato duele el doble, porque el primer nivel no tiene viñeta.
- **Poner una portadilla por sección.** Es lo que más vacía un deck. La estructura va en
  los títulos; la portadilla es la excepción.
- **Olvidar `\begin{numerados}`.** No da error, simplemente dibuja fuera de la lámina.
- **Poner el subtítulo largo.** `subtitle` es la volanta de la barra verde, no un
  subtítulo: si es largo se encoge hasta volverse ilegible.
- **Dejar un comentario de HTML entre el encabezado y la primera lámina.** Beamer le
  abre una lámina vacía, con los logotipos del pie y nada más. No da ningún error y no
  se nota hasta proyectarla; el verificador lo caza comparando cuántas láminas tiene el
  PDF con cuántas describe el `.qmd`. Los comentarios van dentro del encabezado, con
  `#` delante, que es donde Quarto los descarta.
- **Escribir la presentación dos veces**, una para el PDF y otra para PowerPoint. Es el
  mismo `.qmd` y son dos comandos. Si el contenido se bifurca, a la semana siguiente hay
  dos presentaciones distintas y nadie sabe cuál es la buena.
- **Trabajar en `/tmp` cuando hace falta el `.pptx`.** El sandbox de PowerPoint no
  exporta desde ahí y lo hace en silencio: dice que guardó y no hay archivo.
