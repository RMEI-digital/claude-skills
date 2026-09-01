---
name: irem-security-audit
description: Auditoría de seguridad completa de un repositorio (código + historial de git), pensada para apps pequeñas de salud/datos personales tipo Flask/Django/Node en Heroku/Vercel. Corre TruffleHog (secretos vivos en todo el historial), Bandit y Semgrep (SAST), opcionalmente VVAH (SAST agéntico) y una revisión manual de CONTROLES AUSENTES (auth, validación de firma). Produce SECURITY-REVIEW.md + SECURITY-REVIEW-RESUMEN.md + salidas crudas en security-review/. Úsala cuando el usuario pida "revisión/auditoría de seguridad de este repo", "corre los scripts de seguridad", "revisa secretos", o /irem-security-audit.
---

# Auditoría de seguridad de un repositorio

Replica el proceso de revisión que se hizo en `bot-dominicana-piloto-colvol`. El objetivo es
darle al usuario hallazgos **reales y demostrables** (no teóricos) que pueda mostrar a su equipo,
para repos pequeños de salud pública / datos personales.

## Requisitos e instalación

Esta skill son instrucciones que orquestan **herramientas externas**. Antes de correrla, esas
herramientas deben estar instaladas en la máquina. Si al iniciar falta alguna, instálala (o
avisa al usuario) antes de seguir; si una no se puede instalar, sáltala y dilo en el reporte —
no bloquees toda la auditoría por una herramienta.

| Herramienta | Para qué | Instalación |
|---|---|---|
| **TruffleHog** | Secretos vivos en todo el historial de git | `brew install trufflehog` (macOS) · o binario desde github.com/trufflesecurity/trufflehog |
| **Bandit** | SAST para Python | `uv tool install bandit` |
| **Semgrep** | SAST con rulesets Flask/OWASP/secrets | `uv tool install semgrep` |
| **VVAH** (`vvaharness`) | SAST agéntico (encadena hallazgos). **Opcional**: es el paso más lento y gasta API | `uv tool install vvaharness` |
| **uv** | Gestor para instalar/correr las de arriba | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **git** | Historial y ramas | ya viene con el sistema / Xcode CLT |

Comprobación rápida de qué está instalado (correr al empezar):

```bash
for t in trufflehog bandit semgrep uv git; do
  command -v "$t" >/dev/null 2>&1 && printf "%-12s ✓\n" "$t" || printf "%-12s ✗ FALTA\n" "$t"
done
uv tool list 2>/dev/null | grep -i vva || echo "vvaharness ✗ falta (opcional, ver Paso 3)"
```

Instalar todo de una vez (macOS con Homebrew + uv):

```bash
brew install trufflehog
uv tool install bandit
uv tool install semgrep
uv tool install vvaharness   # opcional, solo si vas a correr el Paso 3
```

> Nota para quien recibe esta skill compartida: el archivo `SKILL.md` viaja solo con las
> instrucciones; las herramientas de arriba NO se instalan solas. Corre los comandos de esta
> sección una vez en tu máquina antes del primer uso.

## Regla de oro (por qué existe este proceso)

**El SAST clásico encuentra código peligroso PRESENTE; NO encuentra controles AUSENTES.**
En la revisión original Semgrep dio **0 hallazgos** y aun así el repo tenía 2 críticos y 4 altos,
porque las vulnerabilidades eran *controles faltantes*: endpoint sin autenticación, webhook sin
validación de firma, sin rate limiting. Por eso **la revisión manual y TruffleHog pesan más que el
SAST automático**. Nunca declares el repo "limpio" solo porque Bandit/Semgrep no encontraron nada.

## Antes de empezar — preguntar SIEMPRE

1. **Regla de commits del repo.** Muchos de estos repos tienen `CLAUDE.md` con "nunca commitear ni
   pushear". Respétalo. Deja todo en el working tree. Si no hay regla, igual **no commitees** los
   entregables ni los scripts de apoyo sin confirmación explícita.
2. **¿Hay acceso en vivo?** (DB, Heroku/Vercel, credenciales). Determina si puedes *verificar*
   hallazgos con ejemplos reales o si es solo revisión estática.
   - Si NO hay acceso o el usuario no está seguro → empieza con código + historial y avisa qué
     acceso haría falta para probar cada hallazgo.
   - Si SÍ hay acceso → puedes hacer pruebas, pero lee la sección "Pruebas seguras" abajo.
3. **Contexto del dominio.** ¿Qué datos maneja? (PII, datos de salud, GPS). Esto define la gravedad
   real y las implicaciones legales (p. ej. Ley 172-13 en RD para datos de salud).
4. **¿Corremos VVAH (Paso 3)?** Es opcional: tarda bastante y consume API de pago. Los Pasos 1, 2
   y 4 son los que sostienen la auditoría. Pregúntalo en la misma tanda que lo anterior y, si el
   usuario no lo pide explícitamente, **sáltalo** y anótalo en el alcance del reporte.

## Paso 0 — Reconocimiento

- Lee `README`, `Procfile`, `requirements.txt`/`package.json`, `runtime.txt`, y los archivos de
  entrada (`app.py`, `main.py`, `index.js`, rutas). Entiende: framework, qué endpoints expone,
  dónde está la DB, qué webhooks recibe, qué datos guarda.
- `git log --oneline --all | wc -l` y `git branch -a` — cuántos commits y ramas hay. El historial
  y **todas las ramas** entran en el alcance (los secretos filtrados en ramas viejas siguen vivos).

## Paso 1 — Secretos en TODO el historial (lo más importante)

TruffleHog escanea cada commit de cada rama y, con `--results=verified`, **se autentica de verdad**
contra el servicio: `verified=true` significa que la credencial SIGUE VIVA.

```bash
mkdir -p security-review
trufflehog git file://. --results=verified,unknown --json > security-review/trufflehog.json 2>/dev/null
# resumen legible (sin volcar los secretos en texto plano):
trufflehog git file://. --results=verified,unknown 2>/dev/null | grep -Ei 'Detector|Verified|File|Line|Commit' 
```

- Para cada hallazgo `verified=true`: es CRÍTICO. La corrección es **rotar la credencial**
  (`heroku pg:credentials:rotate`, regenerar secreto de Azure/OAuth, etc.), no solo borrarla del
  código — ya está en el historial para siempre.
- **NUNCA escribas el valor del secreto en los .md ni en `security-review/*.txt`.** Escribirlo
  reproduce el mismo defecto que estás reportando. Referencia commit + archivo + línea.
- Revisa también las **puntas de ramas** (`heroku/testing`, etc.): secretos en texto plano ahí.

## Paso 2 — SAST estático (Bandit + Semgrep)

```bash
# Python:
bandit -r . -x ./.venv,./venv,./node_modules -f txt -o security-review/bandit.txt 2>/dev/null || true
semgrep --config p/flask --config p/python --config p/owasp-top-ten --config p/secrets \
  --exclude .venv --exclude node_modules . > security-review/semgrep.txt 2>&1 || true
# Node/JS: usa --config p/javascript --config p/nodejs --config p/owasp-top-ten
```

Si Semgrep da 0 hallazgos, **anótalo explícitamente como resultado negativo con sentido**, no como
"todo bien" (ver Regla de oro). Escribe en `security-review/semgrep.txt` qué hallazgos manuales
(controles ausentes) NO puede ver el SAST.

## Paso 3 (OPCIONAL) — SAST agéntico (VVAH / vvaharness)

VVAH modela amenazas y **encadena** hallazgos (encontró el takeover por SharePoint y la inyección
de fórmulas Excel que ningún otro tool vio). A cambio es **el paso más lento de toda la auditoría y
gasta API de pago** (Anthropic SDK o CLI), así que **no se corre por defecto**: solo si el usuario
lo pidió en la pregunta 4 de "Antes de empezar". Sin este paso la auditoría sigue siendo válida:
dilo en el alcance del reporte ("Paso 3 no ejecutado a pedido del usuario") y sigue.

> ⚠️ **Nunca corras `vvaharness scan` sin `--stop-after s9`.** El perfil por defecto trae
> `step_remediate.enabled: true`, así que el agente de remediación (paso s10) **edita los archivos
> fuente del repo que estás auditando**. Eso rompe la regla de no tocar el código, contamina el
> working tree y arruina la distinción entre "producción vulnerable" y "fix local" del reporte.
> `--stop-after s9` es detección sola, sin cambios en el código.

```bash
vvaharness doctor                              # credenciales y conectividad, read-only
vvaharness estimate --repo .                   # alcance y costo aproximado, sin gasto de API
vvaharness scan --repo . --stop-after s9       # detección sola, NO edita código
```

Enséñale al usuario la salida de `estimate` y confirma antes de lanzar el `scan`. Si `doctor` falla
por credenciales (falta `ANTHROPIC_SDK_API_KEY` o el backend CLI), no insistas: salta el paso y
dilo en el reporte.

Las salidas **no** caen en `security-review/vvah/`: VVAH escribe dentro del repo, en
`<repo>/security-scan/` (y en `<repo>/security-remediation/` solo si se dejó correr s10, que aquí
no pasa). Comprueba con `ls security-scan/` qué generó y copia los artefactos al lugar de siempre:

```bash
mkdir -p security-review/vvah
ls security-scan/ && cp -R security-scan/. security-review/vvah/
```

`security-scan/` queda en el working tree del repo auditado: no lo commitees, y menciónalo al
usuario para que lo borre o lo ignore cuando termine.

Si VVAH no está instalado: `uv tool install vvaharness`. Si falla o no aplica al stack, sáltalo y
dilo en el reporte, no bloquees la auditoría por esto.

## Paso 4 — Revisión manual de CONTROLES AUSENTES (la que más encuentra)

Lee el código buscando lo que *falta*. Checklist:

- **Autenticación en endpoints de datos.** ¿Hay rutas (`/odata`, `/api`, `/export`) que devuelven
  PII/datos sin token ni sesión? ¿`$top`/límites sin tope (100k registros)?
- **Validación de firma de webhooks.** Twilio → `RequestValidator` + `X-Twilio-Signature`. Stripe,
  GitHub, etc. → verificar HMAC. **Ojo con proxies TLS** (Heroku/Vercel terminan TLS): el esquema
  debe reconstruirse desde `X-Forwarded-Proto` o la firma siempre falla.
- **Bypass de verificación** por palabras clave de "prueba"/"test" que saltan el control de identidad.
- **Rate limiting / DoS**: `time.sleep()` en un worker único, sin límite de peticiones anónimas.
- **Parseo de input sin guardas** → 500s no autenticados.
- **Validación de datos de negocio** (conteos, montos) nunca chequeada.
- **`.gitignore` ausente** → `.venv`/secretos/artefactos versionados.
- **Rutas de debug públicas** (`/test`, `/pruebados`).
- **Suplantación vía datos externos** (un Excel/hoja editable que define quién es quién → takeover).
- **Inyección de fórmulas** en exports a Excel/CSV (`=`, `+`, `@` al inicio de celda → RCE en la
  máquina de quien lo abre).

## Paso 5 — Pruebas seguras (solo si hay acceso en vivo y el usuario lo pide)

El usuario suele querer un **ejemplo real** para convencer a su equipo. Reglas:

- Prueba **primero de forma no destructiva**: un `curl` de webhook sin firma que devuelve 200 ya
  demuestra la falta de validación, sin escribir datos falsos. Un `GET` a `/odata` sin token que
  devuelve PII ya demuestra la exposición.
- **No escribas datos falsos en producción** ni completes flujos que inserten filas fabricadas bajo
  la identidad de un usuario real. Si hace falta prueba de escritura, usa un número/registro que el
  usuario controle, o un entorno de prueba.
- **No vuelques el valor de secretos vivos** a archivos ni al chat.
- Guarda un pequeño script de apoyo (p. ej. `jobs/security_check.py` de lectura read-only de la DB)
  en la carpeta, **sin commitear**, para que el usuario reproduzca.

## Entregables (siempre, salvo que pidan otra cosa)

1. **`SECURITY-REVIEW.md`** — reporte completo. Encabezado con: fecha, alcance (archivos + nº de
   commits + ramas), sistema/stack, y **la base de las líneas citadas** (qué commit = producción).
   Tabla de hallazgos con severidad (🔴 CRÍTICO / 🟠 ALTO / 🟡 MEDIO / 🔵 BAJO), id (F-1, F-2…),
   ubicación `archivo:línea`, estado (abierto / corregido local no desplegado / etc.), y corrección.
   Cada hallazgo: qué es, prueba/evidencia, impacto, fix concreto.
2. **`SECURITY-REVIEW-RESUMEN.md`** — versión corta en español: "lo urgente en una frase", tabla de
   "acciones para hoy" con comandos, y una tabla de todos los hallazgos. Pensada para el equipo.
3. **`security-review/`** — salidas crudas: `trufflehog.json`, `bandit.txt`, `semgrep.txt`, y
   `vvah/` solo si se corrió el Paso 3. En los .txt de secretos, **omitir los valores** y decir por
   qué. Si el Paso 3 se saltó, el reporte debe decirlo en el alcance, no dejarlo en silencio.

## Convenciones de escritura del reporte

- Español para el resumen (el equipo lo lee). El detalle puede ser bilingüe.
- Distingue **producción vs local**: si un fix existe solo en el working tree sin commit/deploy, el
  reporte debe decir claramente "producción sigue vulnerable". (Verifica con `git log` que el fix
  no esté en `HEAD` ni en la rama de deploy.)
- Aclara el **alcance de datos** con honestidad: si NO hay registros por-paciente, dilo (tranquiliza);
  si la PII de operadores/voluntarios está más expuesta de lo que creían, dilo (alarma). No infles ni
  minimices.
- Implicaciones legales solo como orientación, marcadas "confirmar con asesoría legal".

## Recordatorio final

No commitear ni pushear nada. Dejar todo en el working tree. Reportar fielmente: si una herramienta
falló o se saltó un paso, decirlo. No declarar "seguro" un repo por un SAST en verde.
