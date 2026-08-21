#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Crea un repositorio PRIVADO en la organización RMEI-digital, lo clona y deja
# el primer commit hecho y empujado con la identidad git del usuario.
#
# Uso:
#   ./crear-repo.sh <nombre-del-repo> "<descripción>" [lenguaje] [carpeta-destino]
#
#   lenguaje         opcional, para el .gitignore oficial de GitHub
#                    (Python, R, Node, Go, ...). Si se omite, .gitignore mínimo.
#   carpeta-destino  opcional, por omisión el directorio actual.
#
# Este script NO pide confirmación: se invoca sólo después de que la persona
# aprobó los datos. Toda la validación previa está aquí para que no se cree
# nada por error.
# ---------------------------------------------------------------------------
set -euo pipefail

ORG="RMEI-digital"

nombre="${1:?Uso: ./crear-repo.sh <nombre-del-repo> \"<descripción>\" [lenguaje] [carpeta]}"
descripcion="${2:?Falta la descripción del repositorio}"
lenguaje="${3:-}"
destino="${4:-$PWD}"

err() { echo "  ✗ $*" >&2; exit 1; }
ok()  { echo "  ✓ $*"; }

echo "Comprobaciones previas"

# --- 1. herramientas -------------------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
  echo "  ✗ gh no está instalado. Faltan DOS pasos, no uno:" >&2
  echo "      1. brew install gh    — automatizable, lo puede correr Claude" >&2
  echo "      2. gh auth login      — INTERACTIVO, lo tiene que correr la persona" >&2
  exit 1
fi
command -v git >/dev/null 2>&1 || err "git no está instalado."
ok "gh y git disponibles"

# --- 2. autenticación ------------------------------------------------------
gh auth status >/dev/null 2>&1 \
  || err "gh no está autenticado. La persona debe correr «gh auth login»: es interactivo."
usuario="$(gh api user --jq .login)"
ok "autenticado como $usuario"

# Que gh sea el ayudante de credenciales de git. Sin esto, «git push» por HTTPS
# le pregunta al llavero del sistema, no encuentra nada, y se queda esperando
# usuario y contraseña para siempre: el script parece colgado y el repositorio
# queda creado pero vacío. Es idempotente y no interactivo.
gh auth setup-git >/dev/null 2>&1 || true
ok "gh configurado como ayudante de credenciales de git"

# --- 3. identidad git ------------------------------------------------------
gname="$(git config --global user.name  || true)"
gmail="$(git config --global user.email || true)"
[[ -n "$gname" && -n "$gmail" ]] || err "falta la identidad git. Configura user.name y user.email."
case "$gname$gmail" in
  *[Cc]laude*|*anthropic*) err "la identidad git apunta a Claude ($gname <$gmail>). Corrígela." ;;
esac
ok "identidad git: $gname <$gmail>"

# --- 4. nombre del repositorio --------------------------------------------
[[ "$nombre" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$ ]] \
  || err "«$nombre» no es válido. Usa minúsculas, números y guiones: mi-proyecto-nuevo"
ok "nombre válido: $nombre"

# --- 5. acceso a la organización ------------------------------------------
gh api "orgs/$ORG" >/dev/null 2>&1 \
  || err "no puedo ver la organización $ORG. ¿Pertenece tu cuenta y el token tiene alcance de organización?"
ok "acceso a la organización $ORG"

# --- 6. que no exista ya ---------------------------------------------------
if gh repo view "$ORG/$nombre" >/dev/null 2>&1; then
  err "$ORG/$nombre YA EXISTE: https://github.com/$ORG/$nombre — elige otro nombre."
fi
ok "el nombre está libre"

# --- 7. carpeta destino ----------------------------------------------------
[[ -d "$destino" ]] || err "la carpeta destino no existe: $destino"
[[ -e "$destino/$nombre" ]] && err "ya hay algo en $destino/$nombre"
ok "destino disponible: $destino/$nombre"

# --- crear ----------------------------------------------------------------
echo
echo "Creando el repositorio"
gh repo create "$ORG/$nombre" --private --description "$descripcion" >/dev/null
ok "creado como PRIVADO en $ORG"

cd "$destino"
gh repo clone "$ORG/$nombre" "$nombre" -- --quiet 2>/dev/null || gh repo clone "$ORG/$nombre" "$nombre"
cd "$nombre"
ok "clonado en $destino/$nombre"

# --- README ---------------------------------------------------------------
cat > README.md <<EOF
# $nombre

$descripcion

## Sobre este repositorio

Pertenece a la organización [$ORG](https://github.com/$ORG) y es **privado**.
Se mantiene dentro de la organización para que la información quede
centralizada y el conocimiento permanezca aunque cambien las personas.
EOF
ok "README.md"

# --- .gitignore -----------------------------------------------------------
if [[ -n "$lenguaje" ]] && gh api "gitignore/templates/$lenguaje" --jq .source > .gitignore 2>/dev/null; then
  ok ".gitignore oficial de GitHub para $lenguaje"
else
  [[ -n "$lenguaje" ]] && echo "  ! no encontré plantilla para «$lenguaje», uso una mínima" >&2
  cat > .gitignore <<'EOF'
.DS_Store
.env
.venv/
__pycache__/
node_modules/
*.log
EOF
  ok ".gitignore mínimo"
fi

# --- primer commit --------------------------------------------------------
git add README.md .gitignore
# Mensaje de una sola línea, sin cuerpo y sin atribución a Claude.
git -c commit.gpgsign=false commit -q -m "Inicializa el repositorio"
rama="$(git branch --show-current)"
GIT_TERMINAL_PROMPT=0 git push -q -u origin "$rama" \
  || err "el push falló. Si pide credenciales, corre: gh auth setup-git"
ok "primer commit empujado a $rama"

# --- verificación ---------------------------------------------------------
echo
echo "Verificación"
vis="$(gh repo view "$ORG/$nombre" --json visibility --jq .visibility)"
[[ "$vis" == "PRIVATE" ]] && ok "visibilidad: PRIVATE" || err "visibilidad inesperada: $vis"
autor="$(git log -1 --format='%an <%ae>')"
ok "autor del commit: $autor"
if git log -1 --format='%B' | grep -qi 'claude\|co-authored-by'; then
  err "el mensaje del commit contiene atribución indebida"
fi
ok "sin atribución a Claude en el commit"

echo
echo "Listo: https://github.com/$ORG/$nombre"
echo "Local: $destino/$nombre"
