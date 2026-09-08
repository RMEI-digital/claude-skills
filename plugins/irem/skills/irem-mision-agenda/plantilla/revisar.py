#!/usr/bin/env python3
"""
Revisa la agenda de una mision IREM antes de compilarla a Word.

Comprueba dos cosas: que la estructura este completa y que la redaccion cumpla
las reglas de la casa (tercera persona impersonal, sin guiones largos, horas en
formato de 24 horas, objetivos en infinitivo, sin relleno valorativo).

Uso:
    python revisar.py CONTENIDO.md
"""
import re
import sys
from pathlib import Path

SECCIONES_MINIMAS = [
    ("antecedente", "Antecedentes"),
    ("objetivo general", "Objetivo general"),
    ("objetivos especificos", "Objetivos especificos"),
    ("metodologia", "Metodologia"),
    ("participante", "Participantes"),
    ("agenda", "Agenda detallada"),
]
SECCIONES_ESPERADAS = [
    ("productos esperados", "Productos esperados"),
    ("requerimientos tecnicos", "Requerimientos tecnicos y logisticos"),
    ("requerimiento de movilidad", "Requerimiento de movilidad"),
]
COLUMNAS_AGENDA = ["hora", "actividad", "participantes", "lugar"]

PLACEHOLDER = re.compile(r"\[[^\]]{4,}\]|\bTBD\b|\bXXX\b|\bPENDIENTE\b")
POR_CONFIRMAR = re.compile(r"por confirmar", re.I)
GUION_LARGO = re.compile(r"[–—]")
AMPM = re.compile(r"\b\d{1,2}(:\d{2})?\s*(a\.?\s?m\.?|p\.?\s?m\.?)\b", re.I)
RANGO_CON_GUION = re.compile(r"\d{1,2}:\d{2}\s*[-–—]\s*\d{1,2}")
HORA = re.compile(r"\b(\d{1,2}):(\d{2})\b")
PRIMERA_PERSONA = re.compile(
    r"\b(vamos a|iremos|queremos|buscamos|haremos|realizaremos|tenemos|creemos|"
    r"nuestro|nuestra|nuestros|nuestras|nos reunimos|nos permite)\b", re.I)
RELLENO = re.compile(
    r"\b(muy |sumamente |bastante |cabe (mencionar|destacar|resaltar)|"
    r"es importante (destacar|mencionar|resaltar|senalar)|"
    r"exitos[ao]|enriquecedor[a]?|valios[ao]|de gran (importancia|relevancia)|"
    r"como es sabido|en el marco del presente documento|"
    r"a fin de poder|con el objetivo de poder)\b", re.I)
INFINITIVO = re.compile(r"^[a-zñáéíóú]+(ar|er|ir|arse|erse|irse)$", re.I)


def sin_tildes(t):
    for a, b in zip("áéíóúüñ", "aeiouun"):
        t = t.replace(a, b).replace(a.upper(), b.upper())
    return t


def parsea(texto):
    doc = {"titulo": [], "campos": {}, "secciones": [], "lineas": texto.splitlines()}
    seccion = None
    for cruda in doc["lineas"]:
        l = cruda.strip()
        if not l:
            continue
        if m := re.match(r"^#\s+(.*)", l):
            doc["titulo"].append(m.group(1))
            continue
        if m := re.match(r"^##\s+(.*)", l):
            seccion = {"nombre": m.group(1), "subtitulos": [], "vinetas": 0,
                       "cuerpo": 0, "tablas": [], "lineas": []}
            doc["secciones"].append(seccion)
            continue
        if m := re.match(r"^#{3,4}\s+(.*)", l):
            if seccion is not None:
                seccion["subtitulos"].append(m.group(1))
            continue
        if m := re.match(r"^\*\*([^*]+):\*\*\s*(.*)", l):
            doc["campos"][m.group(1).rstrip(":")] = m.group(2)
            continue
        if l.startswith("|"):
            celdas = [c.strip() for c in l.strip("|").split("|")]
            if seccion is not None:
                if all(re.match(r"^:?-{2,}:?$", c) for c in celdas if c):
                    continue
                if seccion["tablas"] and seccion["tablas"][-1]["abierta"]:
                    seccion["tablas"][-1]["filas"].append(celdas)
                else:
                    seccion["tablas"].append({"filas": [celdas], "abierta": True})
            continue
        if seccion is not None:
            for t in seccion["tablas"]:
                t["abierta"] = False
        if l.startswith("\\"):
            continue
        if seccion is not None:
            seccion["lineas"].append(l)
            if re.match(r"^[-*•]\s+", l):
                seccion["vinetas"] += 1
            else:
                seccion["cuerpo"] += 1
    return doc


def busca(doc, patron):
    for s in doc["secciones"]:
        if re.search(patron, sin_tildes(s["nombre"].lower())):
            return s
    return None


def revisa(ruta):
    texto = Path(ruta).read_text(encoding="utf-8")
    doc = parsea(texto)
    faltas, avisos = [], []

    # ---- cabecera
    if not doc["titulo"]:
        faltas.append("No hay titulo (linea que empieza por '# ').")
    elif len(doc["titulo"]) < 2:
        avisos.append("El titulo es de una sola linea. El formato usa dos: "
                      "'Agenda de Mision' y el titulo descriptivo de la mision.")
    elif sin_tildes(doc["titulo"][0].lower()) != "agenda de mision":
        avisos.append(f"La primera linea del titulo es {doc['titulo'][0]!r}; "
                      f"se espera 'Agenda de Mision'.")
    for campo in ("Fechas", "Lugar"):
        if campo not in doc["campos"]:
            faltas.append(f"Falta el campo '{campo}:' en la cabecera.")
        elif not doc["campos"][campo].strip():
            faltas.append(f"El campo '{campo}:' esta vacio.")

    # ---- secciones
    for patron, nombre in SECCIONES_MINIMAS:
        if busca(doc, patron) is None:
            faltas.append(f"Falta la seccion obligatoria: {nombre}.")
    for patron, nombre in SECCIONES_ESPERADAS:
        if busca(doc, patron) is None:
            avisos.append(f"No hay seccion de {nombre}. Es habitual: confirma "
                          f"con el usuario si de verdad no aplica.")

    if s := busca(doc, "antecedente"):
        if s["cuerpo"] == 0:
            faltas.append("Antecedentes esta vacia.")
        elif s["cuerpo"] > 3:
            avisos.append(f"Antecedentes tiene {s['cuerpo']} parrafos. El maximo "
                          f"son dos: el marco y el disparador de la mision.")
        if s["vinetas"]:
            avisos.append("Antecedentes tiene vinetas. Va en parrafos.")

    if s := busca(doc, "objetivo general"):
        if s["cuerpo"] != 1:
            avisos.append(f"El objetivo general ocupa {s['cuerpo']} parrafos. "
                          f"Debe ser una sola frase.")
        for l in s["lineas"]:
            primera = sin_tildes(re.sub(r"^\W+", "", l).split(" ")[0].lower())
            if primera and not INFINITIVO.match(primera):
                avisos.append(f"El objetivo general no empieza en infinitivo: "
                              f"{l[:60]!r}")

    if s := busca(doc, "objetivos especificos"):
        if s["vinetas"] < 3:
            avisos.append(f"Hay {s['vinetas']} objetivos especificos. Se esperan "
                          f"entre tres y seis.")
        elif s["vinetas"] > 6:
            avisos.append(f"Hay {s['vinetas']} objetivos especificos. Mas de seis "
                          f"suele indicar que algunos son actividades.")
        for l in s["lineas"]:
            if m := re.match(r"^[-*•]\s+(.*)", l):
                primera = sin_tildes(m.group(1).split(" ")[0].lower())
                if primera and not INFINITIVO.match(primera):
                    faltas.append(f"Objetivo especifico que no empieza en "
                                  f"infinitivo: {m.group(1)[:60]!r}")

    if s := busca(doc, "resultados esperados"):
        faltas.append(f"La seccion se titula {s['nombre']!r}. En las agendas de "
                      f"mision se titula siempre 'Productos esperados'.")
    if s := busca(doc, "productos esperados"):
        if not s["vinetas"]:
            faltas.append("Los productos esperados no estan en vinetas.")
        if s["vinetas"] < 2:
            avisos.append(f"Hay {s['vinetas']} productos esperados. Se esperan "
                          f"al menos dos.")

    if s := busca(doc, "metodologia"):
        if s["vinetas"]:
            faltas.append(f"La metodologia tiene {s['vinetas']} vinetas. Va en "
                          f"parrafos narrativos, no en lista.")
        if s["cuerpo"] < 2:
            avisos.append("La metodologia tiene menos de dos parrafos. Deberia "
                          "cubrir el enfoque, cada linea de trabajo y el cierre.")

    if s := busca(doc, "participante"):
        if not s["vinetas"]:
            faltas.append("Los participantes no estan en vinetas por institucion.")
        if not re.search(r"IREM", "\n".join(s["lineas"])):
            avisos.append("Los participantes no incluyen la linea de IREM/BID.")

    # ---- agenda
    if s := busca(doc, "agenda"):
        if not s["tablas"]:
            faltas.append("La agenda detallada no tiene ninguna tabla.")
        dias = [t for t in s["subtitulos"] if re.match(r"^d[ií]a\s", t, re.I)]
        if not dias:
            avisos.append("La agenda no tiene subtitulos de dia ('### Dia 1, ...'). "
                          "Cada dia lleva su subtitulo y su tabla.")
        elif len(dias) != len(s["tablas"]):
            avisos.append(f"Hay {len(dias)} subtitulos de dia y {len(s['tablas'])} "
                          f"tablas. Debe haber una tabla por dia.")
        for i, t in enumerate(s["tablas"], 1):
            cab = [sin_tildes(c.lower()) for c in t["filas"][0]]
            if cab != COLUMNAS_AGENDA:
                faltas.append(f"Tabla {i} de la agenda: el encabezado es {cab} y "
                              f"debe ser {COLUMNAS_AGENDA}.")
            if len(t["filas"]) < 2:
                faltas.append(f"Tabla {i} de la agenda: no tiene actividades.")
            for fila in t["filas"][1:]:
                if fila and not fila[0].strip():
                    avisos.append(f"Tabla {i} de la agenda: una fila sin hora.")
                elif fila and not HORA.search(fila[0]) and \
                        not POR_CONFIRMAR.search(fila[0]):
                    avisos.append(f"Tabla {i} de la agenda: hora ilegible "
                                  f"{fila[0][:30]!r}.")
        if "anchos" not in texto:
            avisos.append("No hay linea '\\anchos 14 44 26 16' antes de las tablas "
                          "de la agenda. Sin ella las columnas salen iguales.")

    # ---- redaccion
    for i, linea in enumerate(doc["lineas"], 1):
        for m in PLACEHOLDER.finditer(linea):
            faltas.append(f"Linea {i}: marcador sin rellenar {m.group(0)[:60]!r}")
        if GUION_LARGO.search(linea):
            faltas.append(f"Linea {i}: guion largo o medio. Usa parentesis, dos "
                          f"puntos o coma.")
        if m := AMPM.search(linea):
            faltas.append(f"Linea {i}: hora en formato am/pm ({m.group(0)!r}). "
                          f"El formato es de 24 horas.")
        if m := RANGO_CON_GUION.search(linea):
            faltas.append(f"Linea {i}: rango de horas con guion ({m.group(0)!r}). "
                          f"Se escribe '9:00 a 12:00'.")
        if m := PRIMERA_PERSONA.search(linea):
            avisos.append(f"Linea {i}: primera persona o posesivo "
                          f"({m.group(0)!r}). La agenda va en tercera persona "
                          f"impersonal.")
        if m := RELLENO.search(linea):
            avisos.append(f"Linea {i}: relleno valorativo ({m.group(0).strip()!r}). "
                          f"Quitalo.")
        if m := POR_CONFIRMAR.search(linea):
            avisos.append(f"Linea {i}: 'Por confirmar'. Correcto si de verdad no "
                          f"esta cerrado; preguntalo antes de entregar.")

    return faltas, avisos


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    faltas, avisos = revisa(argv[1])
    if faltas:
        print(f"FALTA ({len(faltas)}): hay que corregir antes de compilar")
        for f in faltas:
            print(f"  - {f}")
    if avisos:
        print(f"\nREVISAR ({len(avisos)}): probablemente hay que preguntar o corregir")
        for a in avisos:
            print(f"  - {a}")
    if not faltas and not avisos:
        print("Sin huecos detectados. La agenda esta lista para compilar.")
    elif not faltas:
        print("\nNada obligatorio falta. Puedes compilar, pero mira los avisos.")
    return 1 if faltas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
