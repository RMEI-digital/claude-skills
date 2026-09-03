---
name: irem-word-formato
description: Da a un documento de Word el formato institucional IREM/BID completo, con los logos IDB y mesoamerica MALARIA en el encabezado, Calibri 12, títulos numerados en romanos, viñetas, tablas con encabezado gris y el espaciado de la casa. Sirve para dos cosas: formatear un .docx que ya existe ("dale formato a este Word", "aplica el formato institucional", "unifica la tipografía del documento") y generar uno nuevo desde texto o Markdown ("hazme un informe de misión", "pásame estas notas a Word con el formato"). No la uses para presentaciones (esa es irem-presentacion).
---

# Formato de documentos Word IREM/BID

El formato no está escrito a mano en un script: vive en `plantilla.docx`, que es
el documento de referencia (`COL - Informe de misión del 18 al 20 de octubre
2023.docx`) vaciado de contenido. La plantilla conserva los estilos, el tema
tipográfico, los márgenes, la numeración y el encabezado con los dos logos. Los
scripts solo escriben bloques dentro de ella, así que el resultado sale igual
por construcción y no por aproximación.

## Regla de oro

**No se toca el contenido, solo el formato.** No se reescribe, no se resume, no
se corrige el texto. Las negritas y las cursivas se conservan tal como estén.

## La hoja de estilo (medida del documento de referencia)

| Elemento | Regla |
|---|---|
| Página | Carta (21.59 x 27.94 cm), márgenes 2.54 cm en los cuatro lados |
| Encabezado | Logos IDB + mesoamerica MALARIA arriba a la izquierda, en todas las páginas |
| Fuente | Calibri (opción `--fuente` para cambiarla) |
| Cuerpo | 12 pt, justificado, interlineado sencillo, sin espacio después |
| Título del documento | 12 pt, negrita, centrado |
| Campo (`Fechas:`, `Lugar:`) | Etiqueta en negrita, valor normal |
| Sección | Numeración romana automática (`I.` `II.` `III.`), negrita, sangría 540 con francesa de 270 |
| Subtítulo de actor | Negrita, al margen |
| Sub-subtítulo | Cursiva, al margen |
| Viñetas | Viñeta Symbol a 720 twips con francesa de 360, justificadas |
| Tablas | Calibri 11 pt, centradas, 9784 twips de ancho, rejilla completa, encabezado gris `D9D9D9` en negrita y centrado, celdas de datos con alineación vertical centrada, primera columna justificada y el resto centradas |
| Separación | Un párrafo en blanco entre bloques, no `space after` |

El ritmo vertical (dónde va un párrafo en blanco y dónde no) lo pone el script
solo. No hay que escribir líneas en blanco a mano.

Paleta IREM por si alguna vez se quiere un acento: azul `#367CBC`, verde
`#98CE63`, gris oscuro `#404040`, gris claro `#9B9B9D`. Por defecto no se usan.

## Los archivos

- `plantilla.docx` es la fuente del formato. No editarla salvo que cambie la
  identidad institucional.
- `irem_docx.py` es la librería: escribe cada tipo de bloque con su XML.
- `generar.py` convierte un Markdown ligero en `.docx`.
- `aplicar_formato.py` reformatea un `.docx` que ya existe.

## Cómo trabajar

Los comandos de abajo necesitan `uv`. Si falla porque no está instalado, no hay
que abandonar la tarea: ver "Si falta algo, guiar la instalación" más abajo,
resolverlo con el usuario y volver aquí.

### Formatear un documento que ya existe

```sh
uv run --with python-docx python aplicar_formato.py ENTRADA.docx [SALIDA.docx] [--fuente Calibri]
```

Si no se da `SALIDA`, escribe `ENTRADA-formateado.docx` al lado del original y
nunca sobre él. Clasifica cada bloque por su papel y lo reescribe sobre la
plantilla, así que el resultado hereda el encabezado con los logos aunque el
original no lo tuviera. Al terminar informa cuántos bloques encontró de cada
tipo: conviene mirar ese recuento, porque delata una clasificación mala (por
ejemplo, cero secciones en un documento que sí tiene capítulos).

### Generar un documento nuevo

Se escribe el contenido en un `.md` con el marcado de abajo y se compila:

```sh
uv run --with python-docx python generar.py FUENTE.md [SALIDA.docx] [--fuente Calibri]
```

Si el usuario trae texto suelto (pegado de un correo, de unas notas, de otro
documento), el trabajo es clasificarlo en este marcado antes de compilar: qué
línea es sección, qué línea es subtítulo, qué es viñeta y qué es cuerpo.

| Marcado | Resultado |
|---|---|
| `# Texto` | Título del documento. Varias líneas `#` seguidas son varias líneas del título |
| `## Texto` | Sección con numeración romana automática |
| `### Texto` | Subtítulo en negrita |
| `#### Texto` | Sub-subtítulo en cursiva |
| `**Etiqueta:** valor` | Línea de campo |
| `**Solo negrita**` | Equivale a `###` |
| `*Solo cursiva*` | Equivale a `####` |
| `- item` | Viñeta (también `*` o `•`) |
| `\| a \| b \|` | Tabla, con fila separadora `\|---\|---\|` |
| `\anchos 66 34` | Anchos relativos de columna de la tabla siguiente |
| `\pagina` | Salto de página |
| `**negrita**`, `*cursiva*` | Dentro de cualquier párrafo |

En las tablas: la primera fila es encabezado; una fila intermedia con todas sus
celdas en negrita también se pinta como encabezado (sirve para tablas de agenda
por días). `<br>` dentro de una celda es un salto de línea. Los dos puntos de
Markdown (`:---:`) fijan la alineación de la columna.

## Dos cosas en las que el formato se aparta del documento de referencia

Son deliberadas, para que el formato sea consistente:

1. El documento de referencia usa dos grises distintos en la misma tabla
   (`D9D9D9` en la primera fila y `D0CECE` en las intermedias). Aquí se usa
   `D9D9D9` en todas.
2. Se añade `keepNext` a todos los títulos, que el documento de referencia no
   tiene, para que ningún título quede solo al pie de una página.

Además se normalizan las inconsistencias del original: párrafos de cuerpo o
viñetas que se habían quedado sin justificar, sangrías de lista sueltas y
listas repartidas en veinte numeraciones distintas.

## Requisitos

Los scripts son Python puro y funcionan igual en macOS, Windows y Linux. El
único requisito es `uv`, que además se descarga Python solo si no lo hay, así
que no hace falta instalar Python aparte. La única dependencia es
`python-docx`, y `uv` la resuelve en cada ejecución sin tocar el Python del
sistema.

La fuente Calibri viene con Windows y con Office, de modo que el documento se
ve igual en cualquiera de los dos.

## Si falta algo, guiar la instalación

Quien pida un documento no tiene por qué ser una persona técnica. Antes de
rendirse con un error, hay que comprobar qué falta y acompañarla hasta que
funcione. Los pasos:

**1. Comprobar.**

```sh
uv --version
```

**2. Si no está, decirlo en claro y ofrecerse a instalarlo.** No instalarlo por
cuenta propia: instalar un gestor de paquetes cambia el sistema del usuario, y
eso se pregunta antes. Basta explicarle que `uv` es el instalador de Python que
usamos, que ocupa poco y que no interfiere con nada de lo que ya tenga.

**3. Ejecutar el comando que corresponda,** una vez haya dicho que sí:

| Sistema | Comando |
|---|---|
| macOS o Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| macOS con Homebrew | `brew install uv` |
| Windows (PowerShell) | `irm https://astral.sh/uv/install.ps1 \| iex` |
| Windows con winget | `winget install astral-sh.uv` |

**4. Comprobar que quedó.** Recién instalado, `uv` suele no estar todavía en el
PATH de la terminal abierta. Si `uv --version` sigue fallando, hay que abrir
una terminal nueva, o en macOS y Linux cargar el entorno sin cerrar nada:

```sh
source $HOME/.local/bin/env
```

**5. Seguir con el documento** como si nada hubiera pasado, sin hacerle repetir
lo que ya había pedido.

Si el entorno no permite ejecutar comandos, se le dan los mismos pasos para
copiar y pegar, diciéndole qué terminal abrir: en macOS, Terminal desde
Aplicaciones y Utilidades; en Windows, PowerShell desde el menú de inicio.

Si ya tiene Python y prefiere no instalar `uv`, sirve igual con la única
dependencia:

```sh
pip install python-docx
python generar.py FUENTE.md SALIDA.docx
```

Los scripts detectan que falta `python-docx` y lo dicen con un mensaje
entendible en vez de soltar un error de Python.

## Cómo comprobar que quedó bien (opcional)

Word es el único renderizador fiable para esto: QuickLook, Preview y los
visores que no resuelven el tema tipográfico muestran otra fuente.

En macOS:

```sh
osascript -e 'tell application "Microsoft Word"
  open POSIX file "/ruta/doc.docx"
  save as document "doc.docx" file name "/ruta/doc.pdf" file format format PDF
  close document "doc.docx" saving no
end tell'
```

Word solo escribe dentro de su sandbox, así que la ruta de salida debe estar en
una carpeta a la que tenga acceso (por ejemplo
`~/Library/Containers/com.microsoft.Word/Data/`) o pedirá permiso por diálogo.

En Windows, con PowerShell:

```powershell
$w = New-Object -ComObject Word.Application
$d = $w.Documents.Open("C:\ruta\doc.docx")
$d.ExportAsFixedFormat("C:\ruta\doc.pdf", 17)   # 17 = PDF
$d.Close(0)                                      # 0 = sin guardar
$w.Quit()
```

En cualquiera de los dos casos, después se comparan con
`uv run --with pymupdf` las coordenadas de cada línea de los dos PDF: si el
formato coincide, las diferencias en x y en y son 0.
