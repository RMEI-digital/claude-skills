#!/usr/bin/env bash
# Compila una presentación IREM en dos versiones:
#   <nombre>.pdf         para proyectar
#   <nombre>-notas.pdf   con las notas del presentador intercaladas
#
# Uso:  ./renderizar.sh presentacion.qmd
#
# Requiere que el encabezado del .qmd tenga exactamente la línea:
#   format: irem-beamer

set -euo pipefail

qmd="${1:?Uso: ./renderizar.sh <archivo>.qmd}"
[[ -f "$qmd" ]] || { echo "No existe: $qmd" >&2; exit 1; }
base="${qmd%.qmd}"

# Quarto convierte los espacios del nombre en guiones al escribir el PDF, así
# que el nombre de salida deja de coincidir con el de entrada y el resumen
# final no encuentra los archivos. Mejor renombrar antes de compilar.
case "$qmd" in
  *" "*)
    echo "Aviso: «$qmd» tiene espacios en el nombre." >&2
    echo "       Quarto escribirá el PDF como «$(echo "$base" | tr ' ' '-').pdf»," >&2
    echo "       distinto del nombre de entrada. Renombra el .qmd sin espacios." >&2
    echo >&2
    ;;
esac

if ! grep -qx "format: irem-beamer" "$qmd"; then
  echo "Aviso: no encontré la línea 'format: irem-beamer' en $qmd." >&2
  echo "       Solo genero la versión limpia; la de notas necesita ese encabezado." >&2
  quarto render "$qmd"
  exit 0
fi

echo "→ versión para proyectar"
quarto render "$qmd"

echo "→ versión con notas del presentador"
tmp="${base}-notas.qmd"
sed 's|^format: irem-beamer$|format:\
  irem-beamer:\
    include-in-header:\
      text: \|\
        \\setbeameroption{show notes}|' "$qmd" > "$tmp"
quarto render "$tmp"
rm -f "$tmp"

echo
echo "Listo:"
Rscript -e '
  a <- commandArgs(TRUE)
  for (f in a) if (file.exists(f)) cat(sprintf("  %-34s %d páginas\n", f, pdftools::pdf_info(f)$pages))
' "${base}.pdf" "${base}-notas.pdf" 2>/dev/null

echo
echo "Revisa las láminas antes de entregar, TODAS, no las tres primeras:"
echo "  Rscript -e 'n <- pdftools::pdf_info(\"${base}.pdf\")\$pages"
echo "              pdftools::pdf_convert(\"${base}.pdf\", pages = 1:n, dpi = 110,"
echo "                                    format = \"png\","
echo "                                    filenames = sprintf(\"rev-%02d.png\", 1:n))'"
