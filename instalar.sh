#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Instalador de respaldo. Copia las skills de este repositorio a
# ~/.claude/skills/, para quien tenga problemas con /plugin marketplace add
# (que en un repositorio privado necesita que git sepa autenticarse).
#
# La forma recomendada sigue siendo el plugin, porque se actualiza con un
# comando. Esto hay que volver a correrlo cada vez que el repositorio cambie.
#
# Uso:  ./instalar.sh
# ---------------------------------------------------------------------------
set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/plugins/irem/skills"
DESTINO="$HOME/.claude/skills"

[[ -d "$ORIGEN" ]] || { echo "No encuentro las skills en $ORIGEN" >&2; exit 1; }
mkdir -p "$DESTINO"

echo "Instalando skills en $DESTINO"
for ruta in "$ORIGEN"/*/; do
  nombre="$(basename "$ruta")"
  if [[ -e "$DESTINO/$nombre" ]]; then
    echo "  · $nombre ya existe: reemplazo"
    rm -rf "$DESTINO/$nombre"
  fi
  cp -R "$ruta" "$DESTINO/$nombre"
  chmod +x "$DESTINO/$nombre"/*.sh 2>/dev/null || true
  chmod +x "$DESTINO/$nombre"/plantilla/*.sh 2>/dev/null || true
  echo "  ✓ $nombre"
done

echo
echo "Listo. Abre una sesión nueva de Claude Code para que las reconozca."
echo "Instaladas:"
ls "$DESTINO" | sed 's/^/  /'
