#!/usr/bin/env bash
# Convierte el .pptx a PDF con el propio PowerPoint y deja los PNG de todas las
# láminas en .revision-pptx/, para poder mirarlas.
#
#   ./pptx-a-pdf.sh <archivo>.pptx   ->  <archivo>-desde-pptx.pdf + .revision-pptx/*.png
#
# Es macOS con PowerPoint instalado. En otro sistema, abre el .pptx y míralo:
# `revisar.py` ya comprobó lo que se puede comprobar sin renderizar.
#
# Cuatro cosas que costaron encontrarse, por si algún día deja de funcionar:
#
#   1. El PDF NO se llama <archivo>.pdf. Ese nombre lo usa el camino de Beamer,
#      y exportar aquí con ese nombre le pisa el PDF bueno sin avisar.
#   2. Hay que abrir el archivo con `open -a`. El `open` de AppleScript no lo
#      abre y el guardado posterior falla sin decir por qué.
#   3. Hay que asignar la presentación a una variable antes de guardarla. En
#      línea, `save active presentation in ... as save as PDF` no escribe nada
#      y devuelve «ok» igual.
#   4. El archivo tiene que estar en una carpeta normal del usuario. Desde
#      /tmp, el sandbox de PowerPoint bloquea el guardado en silencio: dice que
#      guardó y no hay archivo.
set -euo pipefail

pptx="${1:?Uso: ./pptx-a-pdf.sh <archivo>.pptx}"
[[ -f "$pptx" ]] || { echo "No existe: $pptx" >&2; exit 1; }
pptx="$(cd "$(dirname "$pptx")" && pwd)/$(basename "$pptx")"

case "$pptx" in
  /tmp/*|/private/tmp/*|/var/folders/*)
    echo "El archivo está en una carpeta temporal y PowerPoint no puede exportar" >&2
    echo "desde ahí: dice que guardó y no escribe nada. Muévelo a Documentos." >&2
    exit 1 ;;
esac

if [[ ! -d "/Applications/Microsoft PowerPoint.app" ]]; then
  echo "No encuentro PowerPoint. Abre el .pptx y míralo a mano;" >&2
  echo "./revisar.py ya comprobó lo que se puede sin renderizar." >&2
  exit 1
fi

pdf="${pptx%.pptx}-desde-pptx.pdf"
hfs="$(osascript -e "return POSIX file \"$pdf\" as text")"
rm -f "$pdf"

osascript -e 'tell application "Microsoft PowerPoint" to close every presentation saving no' >/dev/null 2>&1 || true
# El archivo de bloqueo que deja PowerPoint al abrir: si sobrevivió a una
# corrida anterior, la siguiente abre el archivo en solo lectura y no exporta.
rm -f "$(dirname "$pptx")/~\$$(basename "$pptx")"
open -a "Microsoft PowerPoint" "$pptx"
for _ in $(seq 30); do
  n=$(osascript -e 'tell application "Microsoft PowerPoint" to return (count of presentations) as text' 2>/dev/null || echo 0)
  [ "$n" != "0" ] && break
  sleep 1
done
[ "${n:-0}" != "0" ] || { echo "PowerPoint no abrió el archivo." >&2; exit 1; }

# El `with timeout` no sobra: AppleScript corta a los 60 segundos y una
# presentación con fotografías tarda más, así que el guardado falla con
# «AppleEvent timed out (-1712)» aunque PowerPoint lo esté haciendo bien.
osascript <<AS >/dev/null
with timeout of 900 seconds
  tell application "Microsoft PowerPoint"
    set d to active presentation
    save d in "$hfs" as save as PDF
  end tell
end timeout
AS
for _ in $(seq 30); do [ -f "$pdf" ] && break; sleep 1; done
osascript -e 'tell application "Microsoft PowerPoint" to close every presentation saving no' >/dev/null 2>&1 || true
rm -f "$(dirname "$pptx")/~\$$(basename "$pptx")"
[ -f "$pdf" ] || { echo "PowerPoint no escribió el PDF." >&2; exit 1; }

# Los PNG con PyMuPDF y no con pdftools: el PDF que exporta PowerPoint trae la
# fotografía de portada en JPEG, y el poppler de pdftools la pinta en blanco o
# se cae. Es la misma trampa que documenta la skill para el PDF del master.
carpeta="$(dirname "$pptx")/.revision-pptx"
uv run --with pymupdf python - "$pdf" "$carpeta" <<'PY'
import shutil, sys
from pathlib import Path
import pymupdf
pdf, carpeta = sys.argv[1], Path(sys.argv[2])
if carpeta.exists():
    shutil.rmtree(carpeta)
carpeta.mkdir()
d = pymupdf.open(pdf)
for i in range(d.page_count):
    d[i].get_pixmap(dpi=110).save(carpeta / f"rev-{i + 1:02d}.png")
print(f"{d.page_count} láminas en {carpeta}/")
PY
echo "$pdf"
