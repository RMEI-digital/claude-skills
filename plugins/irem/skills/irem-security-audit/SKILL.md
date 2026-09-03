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
avisa al usuario) antes de seguir; si una no se puede instalar, sáltala y dilo en el reporte:
no bloquees toda la auditoría por una herramienta.

| Herramienta | Para qué | Instalación |
|---|---|---|
| **TruffleHog** | Secretos vivos en todo el historial de git | `brew install trufflehog` (macOS) · o binario desde github.com/trufflesecurity/trufflehog |
| **Bandit** | SAST para Python | `uv tool install bandit` |
| **Semgrep** | SAST con rulesets Flask/OWASP/secrets | `uv tool install semgrep` |
| **pip-audit** | Dependencias de Python con vulnerabilidades conocidas | `uv tool install pip-audit` |
| **VVAH** (`vvaharness`) | SAST agéntico (encadena hallazgos). **Opcional**: es el paso más lento y el que más tokens consume | `uv tool install vvaharness` |
| **uv** | Gestor para instalar/correr las de arriba | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **git** | Historial y ramas | ya viene con el sistema / Xcode CLT |

Comprobación rápida de qué está instalado (correr al empezar):

```bash
for t in trufflehog bandit semgrep pip-audit uv git; do
  command -v "$t" >/dev/null 2>&1 && printf "%-12s ✓\n" "$t" || printf "%-12s ✗ FALTA\n" "$t"
done
uv tool list 2>/dev/null | grep -i vva || echo "vvaharness ✗ falta (opcional, ver Paso 3)"
```

Instalar todo de una vez (macOS con Homebrew + uv):

```bash
brew install trufflehog
uv tool install bandit
uv tool install semgrep
uv tool install pip-audit
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

## Antes de empezar

Primero **lee**, y solo pregunta lo que no puedas averiguar leyendo. La regla de commits suele estar
en el `CLAUDE.md` del repo, y el stack en el `README` y el `Procfile`: preguntar eso gasta el turno
del usuario en algo que el repo ya dice. En cualquier caso, y aunque no haya regla escrita, **no
commitees** los entregables ni los scripts de apoyo sin confirmación explícita.

Lo que sí hay que preguntar, todo junto en una sola tanda porque cambia el trabajo:

1. **¿Hay acceso en vivo?** (DB, Heroku/Vercel, credenciales). Determina si puedes *verificar*
   hallazgos con ejemplos reales o si es solo revisión estática.
   - Si NO hay acceso o el usuario no está seguro → empieza con código + historial y avisa qué
     acceso haría falta para probar cada hallazgo.
   - Si SÍ hay acceso → puedes hacer pruebas, pero lee la sección "Pruebas seguras" abajo.
3. **Contexto del dominio.** ¿Qué datos maneja? (PII, datos de salud, GPS). Esto define la gravedad
   real y las implicaciones legales (p. ej. Ley 172-13 en RD para datos de salud).
4. **¿Corremos VVAH (Paso 3)?** Es opcional: tarda bastante y consume bastantes tokens. Los Pasos 1, 2
   y 4 son los que sostienen la auditoría. Pregúntalo en la misma tanda que lo anterior y, si el
   usuario no lo pide explícitamente, **sáltalo** y anótalo en el alcance del reporte.

## Paso 0: reconocimiento

- Lee `README`, `Procfile`, `requirements.txt`/`package.json`, `runtime.txt`, y los archivos de
  entrada (`app.py`, `main.py`, `index.js`, rutas). Entiende: framework, qué endpoints expone,
  dónde está la DB, qué webhooks recibe, qué datos guarda.
- `git log --oneline --all | wc -l` y `git branch -a`: cuántos commits y ramas hay. El historial
  y **todas las ramas** entran en el alcance (los secretos filtrados en ramas viejas siguen vivos).

## Paso 1: secretos en TODO el historial (lo más importante)

TruffleHog escanea cada commit de cada rama y **se autentica de verdad** contra el servicio, sin que
haya que pedirlo: `verified=true` significa que la credencial SIGUE VIVA y es CRITICO.

`unverified` **no significa falso positivo**: significa que no existe forma de comprobarlo desde
aqui. Es el caso de una clave privada, de una URL de Postgres o de un token interno. Por eso **no se
filtra por tipo de resultado**: con `--results=verified` una clave RSA privada en el historial da
cero hallazgos (comprobado en un repo de prueba: 0 con ese filtro, 2 con el set por defecto).

```bash
mkdir -p security-review

# El JSON crudo NUNCA se guarda dentro del repo auditado: su campo "Raw" trae el
# valor completo del secreto, y escribirlo ahi reproduce el defecto que buscas.
CRUDO="$(mktemp -d)/trufflehog.json"

# Sin --results: el default de trufflehog ya es verified,unverified,unknown.
trufflehog git file://. --json --no-update > "$CRUDO" 2> security-review/trufflehog.stderr.txt
echo "exit=$?"   # un fallo NO es un repo limpio: si no es 0, para y averigua por que
grep -c 'finished scanning' security-review/trufflehog.stderr.txt   # confirma que escaneo algo
```

El resumen legible se hace **seleccionando campos**, nunca filtrando lineas. Este script imprime
detector, estado, archivo, linea y commit, y no toca `Raw` en ningun caso:

```bash
python3 - "$CRUDO" <<'FIN' | tee security-review/trufflehog-NOTA.txt
import json, sys
filas = []
for linea in open(sys.argv[1]):
    try: d = json.loads(linea)
    except ValueError: continue
    if "DetectorName" not in d: continue
    g = d.get("SourceMetadata", {}).get("Data", {}).get("Git", {})
    filas.append((d["DetectorName"], bool(d.get("Verified")),
                  g.get("file"), g.get("line"), (g.get("commit") or "")[:8]))
print("hallazgos:", len(filas), "| verificados vivos:", sum(1 for f in filas if f[1]))
for f in sorted(filas):
    print(f"  {f[0]:<28} verified={f[1]}  {f[2]}:{f[3]}  commit {f[4]}")
FIN
```

Un `grep` de palabras clave sobre la salida legible **no sirve como redaccion**: es una lista blanca
aplicada a lineas enteras, asi que cualquier linea de secreto que contenga "file" o "line" se cuela,
y los secretos multilinea se cortan de forma impredecible.

Escanea tambien el **working tree**, no solo el historial. El escaneo de git ve unicamente lo
comiteado, asi que un `.env` o un `.pem` sin versionar, con credenciales vivas en la maquina de quien
despliega, seria invisible:

```bash
printf '\\.venv/\n\\.git/\nsecurity-review/\n__pycache__/\n' > "$(dirname "$CRUDO")/excluir.txt"
trufflehog filesystem . -x "$(dirname "$CRUDO")/excluir.txt" --json --no-update \
  > "${CRUDO%.json}-fs.json" 2> security-review/trufflehog-fs.stderr.txt
echo "exit=$?"
```

El resumen se saca con el mismo script de arriba, cambiando el argumento por
`"${CRUDO%.json}-fs.json"` y leyendo `SourceMetadata.Data.Filesystem` en vez de `.Git`. Los dos
crudos se quedan fuera del repo, por la misma razon.

- Para cada hallazgo `verified=true`: es CRÍTICO. La corrección es **rotar la credencial**
  (`heroku pg:credentials:rotate`, regenerar secreto de Azure/OAuth, etc.), no solo borrarla del
  código, porque ya está en el historial para siempre.
- **NUNCA escribas el valor del secreto en ningun archivo que quede dentro del repo**, ni en los
  `.md`, ni en los `.txt`, ni en el JSON de la herramienta. Escribirlo reproduce el mismo defecto que
  estas reportando, y el JSON es donde de verdad se filtra: el campo `Raw` trae el secreto completo
  (una clave RSA aparece integra, 1675 caracteres). El crudo va a un directorio temporal fuera del
  repo; dentro solo entra el resumen sin valores. Referencia commit + archivo + linea.
- **Protege los entregables antes de generarlos.** En el repo auditado, mete `security-review/` y los
  `.md` del informe en `.git/info/exclude` (no en `.gitignore`, que es un archivo versionado del
  proyecto). Sin eso, un `git add -A` distraido del usuario commitea las salidas de la auditoria.
- Revisa también las **puntas de ramas** (`heroku/testing`, etc.): secretos en texto plano ahí.

## Paso 2: SAST estático (Bandit + Semgrep)

```bash
# Python:
bandit -r . -x ./.venv,./venv,./node_modules,./security-review -f txt \
  -o security-review/bandit.txt 2>security-review/bandit.stderr.txt
echo "bandit exit=$?"   # 1 = encontro hallazgos (normal). 2 = fallo de verdad

semgrep --config p/flask --config p/python --config p/owasp-top-ten --config p/secrets \
  --exclude .venv --exclude node_modules --exclude security-review --metrics=off . \
  > security-review/semgrep.txt 2>security-review/semgrep.stderr.txt
echo "semgrep exit=$?"

# Node/JS: usa --config p/javascript --config p/nodejs --config p/owasp-top-ten
```

**Nunca uses `2>/dev/null || true` aquí.** Si la herramienta no esta instalada o revienta, ese patron
deja un archivo vacio y el reporte acaba diciendo "0 hallazgos", que es exactamente lo contrario de
lo que paso. Comprueba siempre que el artefacto existe y no esta vacio:

```bash
for f in security-review/bandit.txt security-review/semgrep.txt; do
  [ -s "$f" ] && printf "%-32s ✓ %s bytes\n" "$f" "$(wc -c <"$f")" \
              || printf "%-32s ✗ VACIO O AUSENTE: la herramienta fallo\n" "$f"
done
```

Si Semgrep da 0 hallazgos, **anotalo explicitamente como resultado negativo con sentido**, no como
"todo bien" (ver Regla de oro). Ese analisis va en el `.md` del reporte, **no dentro de
`semgrep.txt`**: los crudos se quedan como los escribio la herramienta, para que se puedan comparar
con la corrida siguiente.

## Paso 2.5: dependencias con vulnerabilidades conocidas

Ni Bandit ni Semgrep miran esto, y en un repo de salud sobre Heroku suele ser el hallazgo con mas
CVEs detras. Es rapido y no se puede omitir.

```bash
# Python, sobre el entorno instalado:
pip-audit 2>&1 | tee security-review/pip-audit.txt

# Node:
npm audit --omit=dev 2>&1 | tee security-review/npm-audit.txt
```

**Audita lo que corre en produccion, no lo que tienes instalado.** Si el `requirements.txt` del
working tree ya subio versiones que aun no estan desplegadas, `pip-audit` da 0 y el reporte miente.
Compara contra el fijado en el commit desplegado:

```bash
git show HEAD:requirements.txt > /tmp/req-produccion.txt
pip-audit -r /tmp/req-produccion.txt
```

Si `pip-audit -r` falla creando su venv temporal (pasa en entornos restringidos), la alternativa es
consultar OSV directamente con las versiones fijadas, que no necesita instalar nada:

```bash
python3 - <<'FIN'
import json, re, urllib.request
pkgs = []
for linea in open("/tmp/req-produccion.txt"):
    m = re.match(r"^([A-Za-z0-9_.\-]+)==([^\s;#]+)", linea.split("#")[0].strip())
    if m: pkgs.append((m.group(1), m.group(2)))
q = {"queries": [{"package": {"name": n, "ecosystem": "PyPI"}, "version": v} for n, v in pkgs]}
req = urllib.request.Request("https://api.osv.dev/v1/querybatch",
                             data=json.dumps(q).encode(),
                             headers={"Content-Type": "application/json"})
res = json.load(urllib.request.urlopen(req, timeout=60))
for (n, v), r in zip(pkgs, res.get("results", [])):
    ids = [x["id"] for x in r.get("vulns", [])]
    if ids: print(f"{n}=={v}  {len(ids)} avisos: {', '.join(ids[:5])}")
FIN
```

Nota al escribir el reporte: OSV devuelve un id por aviso y un mismo fallo suele tener GHSA y PYSEC a
la vez, asi que ese numero **no es comparable** con el de `pip-audit`. Di cual usaste.

## Paso 3 (OPCIONAL): SAST agéntico (VVAH / vvaharness)

VVAH modela amenazas y **encadena** hallazgos (encontró el takeover por SharePoint y la inyección
de fórmulas Excel que ningún otro tool vio). A cambio es **el paso más lento de toda la auditoría y
el que más tokens consume**, así que **no se corre por defecto**: solo si el usuario lo pidió en la
pregunta 4 de "Antes de empezar".

Dónde se paga ese consumo depende del backend, y conviene decírselo bien al usuario en vez de
hablar de «API de pago» a secas: con el SDK de Anthropic va contra una clave de API, que se
factura por token; con el backend CLI va contra el uso del plan de Claude que la persona ya
tiene. En el segundo caso no hay factura nueva, pero el gasto existe igual y el paso puede
tardar. Sin este paso la auditoría sigue siendo válida:
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

## Paso 4: revisión manual de CONTROLES AUSENTES (la que más encuentra)

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

## Paso 5: pruebas seguras (solo si hay acceso en vivo y el usuario lo pide)

**Probar el sistema encuentra cosas que leer el código no encuentra nunca.** En una auditoría de
septiembre de 2026, escribirle al bot desde un teléfono real destapó que WhatsApp había empezado a
permitir ocultar el número (los usernames y los BSUID de Meta): los usuarios que lo activaban dejaban
de ser reconocidos y sus reportes se perdían en silencio. Ninguna herramienta ni revisión de código
podía verlo, porque el defecto solo existe frente a la plataforma real. Si el sistema habla con un
servicio externo (WhatsApp, Twilio, Graph, un banco), **usa el sistema como lo usa un usuario**, no
solo leas su código.

Dos trampas de método de esa misma auditoría, por si ahorran horas:

- Un `heroku config:get VARIABLE` vacío **no prueba** que la variable no exista: el buildpack puede
  fijarla al arrancar el dyno. Compruébalo en el log de arranque, no en la config.
- Lo que un `.gitignore` esconde puede ser justo lo que el despliegue necesita. Antes de dar por
  hecho que un archivo nuevo viaja al servidor, `git check-ignore -v` sobre él.

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

1. **`SECURITY-REVIEW.md`**: reporte completo. Encabezado con: fecha, alcance (archivos + nº de
   commits + ramas), sistema/stack, y **la base de las líneas citadas** (qué commit = producción).
   Tabla de hallazgos con severidad (🔴 CRÍTICO / 🟠 ALTO / 🟡 MEDIO / 🔵 BAJO), id (F-1, F-2…),
   ubicación `archivo:línea`, estado (abierto / corregido local no desplegado / etc.), y corrección.
   Cada hallazgo: qué es, prueba/evidencia, impacto, fix concreto.
2. **`SECURITY-REVIEW-RESUMEN.md`**: versión corta en español: "lo urgente en una frase", tabla de
   "acciones para hoy" con comandos, y una tabla de todos los hallazgos. Pensada para el equipo.
3. **`security-review/`**: salidas crudas: `trufflehog-NOTA.txt` (el resumen sin valores, con el
   historial y el working tree), los `.stderr.txt` (que prueban el alcance real de cada escaneo),
   `bandit.txt`, `semgrep.txt`, y
   `vvah/` solo si se corrió el Paso 3. **El JSON crudo de TruffleHog se queda fuera del repo**, en el
   temporal: contiene los secretos en claro. Dilo en la nota, para que se sepa que no se omitió por
   descuido. Si el Paso 3 se saltó, el reporte debe decirlo en el alcance, no dejarlo en silencio.

## Convenciones de escritura del reporte

- Español para el resumen (el equipo lo lee). El detalle puede ser bilingüe.
- Distingue **producción vs local**: si un fix existe solo en el working tree sin commit ni deploy, el
  reporte debe decir claramente "producción sigue vulnerable". (Verifica con `git log` que el fix
  no esté en `HEAD` ni en la rama de deploy.)
- Aclara el **alcance de datos** con honestidad: si NO hay registros por-paciente, dilo (tranquiliza);
  si la PII de operadores/voluntarios está más expuesta de lo que creían, dilo (alarma). No infles ni
  minimices.
- Implicaciones legales solo como orientación, marcadas "confirmar con asesoría legal".

## Recordatorio final

No commitear ni pushear nada. Dejar todo en el working tree. Reportar fielmente: si una herramienta
falló o se saltó un paso, decirlo. No declarar "seguro" un repo por un SAST en verde.
