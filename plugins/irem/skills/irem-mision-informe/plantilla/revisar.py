#!/usr/bin/env python3
"""
Revisa el contenido de un informe de mision IREM antes de compilarlo a Word.

No juzga el estilo ni el formato: busca huecos de contenido. Lo que encuentra
son las preguntas que hay que hacerle al usuario.

Uso:
    python revisar.py CONTENIDO.md
"""
import re
import sys
from pathlib import Path

# etapas del ciclo de vida del dato, que son la espina de los hallazgos
ETAPAS = {
    "registro": "registro",
    "recoleccion": "registro",
    "recepcion": "registro",
    "consolidacion": "consolidacion",
    "analisis": "analisis",
    "reporte": "salida",
    "salida": "salida",
    "otros": "otros",
}
SECCIONES_MINIMAS = ["contexto", "objetivos", "hallazgos", "desafios"]
SECCIONES_ESPERADAS = ["agenda", "propuesta"]
MARCADORES = re.compile(r"\[[^\]]{4,}\]|\bPENDIENTE\b|\bTBD\b|\bXXX\b|\bPOR CONFIRMAR\b", re.I)


def sin_tildes(t):
    for a, b in zip("áéíóúüñ", "aeiouun"):
        t = t.replace(a, b)
    return t


def etapa_de(titulo):
    t = sin_tildes(titulo.lower())
    for clave, grupo in ETAPAS.items():
        if clave in t:
            return grupo
    return None


def parsea(texto):
    """Devuelve la estructura: secciones, actores y sus etapas."""
    doc = {"titulo": [], "campos": {}, "secciones": [], "lineas": texto.splitlines()}
    seccion = actor = None
    for cruda in doc["lineas"]:
        l = cruda.strip()
        if not l:
            continue
        if m := re.match(r"^#\s+(.*)", l):
            doc["titulo"].append(m.group(1)); continue
        if m := re.match(r"^##\s+(.*)", l):
            seccion = {"nombre": m.group(1), "actores": [], "etapas": [],
                       "vinetas": 0, "cuerpo": 0, "tablas": 0, "subtitulos": []}
            doc["secciones"].append(seccion); actor = None; continue
        if m := re.match(r"^###\s+(.*)", l):
            if seccion is not None:
                actor = {"nombre": m.group(1), "etapas": [], "cuerpo": 0, "vinetas": 0}
                seccion["actores"].append(actor)
                seccion["subtitulos"].append(m.group(1))
            continue
        if m := re.match(r"^####\s+(.*)", l):
            destino = actor if actor is not None else seccion
            if destino is not None:
                destino["etapas"].append({"nombre": m.group(1),
                                          "grupo": etapa_de(m.group(1)), "vinetas": 0})
            continue
        if m := re.match(r"^\*\*([^*]+):\*\*\s*(.*)", l):
            doc["campos"][m.group(1).rstrip(":")] = m.group(2); continue
        if m := re.match(r"^\*\*([^*]+)\*\*$", l):
            if seccion is not None:
                actor = {"nombre": m.group(1), "etapas": [], "cuerpo": 0, "vinetas": 0}
                seccion["actores"].append(actor)
                seccion["subtitulos"].append(m.group(1))
            continue
        if l.startswith("|"):
            if seccion is not None:
                seccion["tablas"] += 1
            continue
        if l.startswith("\\"):
            continue
        es_vineta = bool(re.match(r"^[-*•]\s+", l))
        blanco = None
        if actor is not None and actor["etapas"]:
            blanco = actor["etapas"][-1]
        elif actor is not None:
            blanco = actor
        elif seccion is not None and seccion["etapas"]:
            blanco = seccion["etapas"][-1]
        elif seccion is not None:
            blanco = seccion
        if blanco is not None:
            blanco["vinetas" if es_vineta else "cuerpo"] = \
                blanco.get("vinetas" if es_vineta else "cuerpo", 0) + 1
    return doc


def revisa(ruta):
    texto = Path(ruta).read_text(encoding="utf-8")
    doc = parsea(texto)
    faltas, avisos = [], []

    # 1. cabecera
    if not doc["titulo"]:
        faltas.append("No hay titulo (linea que empieza por '# ').")
    elif len(doc["titulo"]) < 2:
        avisos.append("El titulo es de una sola linea. El formato usa dos: "
                      "'Reporte Interno' y el titulo descriptivo.")
    for campo in ("Fechas", "Lugar"):
        if campo not in doc["campos"]:
            faltas.append(f"Falta el campo '{campo}:' en la cabecera.")
        elif not doc["campos"][campo].strip():
            faltas.append(f"El campo '{campo}:' esta vacio.")
    if not any("participante" in sin_tildes(s.lower())
               for sec in doc["secciones"] for s in sec["subtitulos"]) and \
       "Participantes principales" not in texto:
        faltas.append("No aparecen los participantes de la mision.")

    # 2. secciones
    nombres = [sin_tildes(s["nombre"].lower()) for s in doc["secciones"]]
    for clave in SECCIONES_MINIMAS:
        if not any(clave in n for n in nombres):
            faltas.append(f"Falta la seccion obligatoria: {clave}.")
    for clave in SECCIONES_ESPERADAS:
        if not any(clave in n for n in nombres):
            avisos.append(f"No hay seccion de {clave}. Es habitual: confirma "
                          f"con el usuario si de verdad no aplica.")

    for sec in doc["secciones"]:
        n = sin_tildes(sec["nombre"].lower())

        if "contexto" in n and sec["cuerpo"] < 2:
            avisos.append("El contexto tiene menos de dos parrafos. Deberia encadenar "
                          "el marco, el disparador concreto (oficio, solicitud, fecha) "
                          "y la respuesta.")

        if "objetivo" in n:
            generales = [a for a in sec["actores"]
                         if "general" in sin_tildes(a["nombre"].lower())]
            especificos = [a for a in sec["actores"]
                           if "especifico" in sin_tildes(a["nombre"].lower())]
            if not generales:
                faltas.append("Los objetivos no tienen un objetivo general.")
            if not especificos:
                faltas.append("Los objetivos no tienen objetivos especificos.")
            elif sum(a["vinetas"] for a in especificos) < 2:
                avisos.append("Hay menos de dos objetivos especificos.")

        if "agenda" in n and not sec["tablas"]:
            faltas.append("La seccion de agenda no tiene tabla.")

        if "hallazgo" in n:
            if not sec["actores"]:
                faltas.append("Los hallazgos no tienen ningun actor ('### Nombre').")
            for a in sec["actores"]:
                if not a["cuerpo"]:
                    faltas.append(f"'{a['nombre']}': falta el parrafo que describe al "
                                  f"actor antes de sus hallazgos.")
                grupos = {e["grupo"] for e in a["etapas"] if e["grupo"]}
                utiles = grupos - {"otros"}
                if not a["etapas"]:
                    faltas.append(f"'{a['nombre']}': no tiene ninguna etapa del ciclo "
                                  f"del dato.")
                elif len(utiles) < 2:
                    avisos.append(f"'{a['nombre']}': solo cubre "
                                  f"{sorted(utiles) or ['ninguna']} del ciclo del dato. "
                                  f"Pregunta por las que faltan "
                                  f"(registro, consolidacion, analisis, salida).")
                for e in a["etapas"]:
                    if not e["vinetas"] and not e.get("cuerpo"):
                        faltas.append(f"'{a['nombre']}' / '{e['nombre']}': "
                                      f"sin contenido.")
                    if e["grupo"] is None:
                        avisos.append(f"'{a['nombre']}' / '{e['nombre']}': no es una "
                                      f"etapa del ciclo del dato. Puede estar bien, "
                                      f"pero revisa que no sea un nombre suelto.")

        if "desafio" in n:
            if not sec["etapas"]:
                faltas.append("Los desafios no estan agrupados por etapa ('#### Etapa').")
            for e in sec["etapas"]:
                if not e["vinetas"]:
                    faltas.append(f"Desafios / '{e['nombre']}': sin ningun desafio.")

    # 3. marcadores sin rellenar
    for i, linea in enumerate(doc["lineas"], 1):
        for m in MARCADORES.finditer(linea):
            faltas.append(f"Linea {i}: marcador sin rellenar {m.group(0)[:60]!r}")

    # 4. coherencia de anexos
    citados = {int(x) for x in re.findall(r"[Aa]nexos?\s+(\d+)", texto)}
    citados |= {int(x) for m in re.findall(r"[Aa]nexos\s+(\d+)\s+y\s+(\d+)", texto)
                for x in m}
    if citados:
        huecos = set(range(1, max(citados) + 1)) - citados
        if huecos:
            avisos.append(f"Se citan los anexos {sorted(citados)} pero no "
                          f"{sorted(huecos)}. Revisa la numeracion.")

    return faltas, avisos


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    faltas, avisos = revisa(argv[1])
    if faltas:
        print(f"FALTA ({len(faltas)}): hay que preguntar antes de compilar")
        for f in faltas:
            print(f"  - {f}")
    if avisos:
        print(f"\nREVISAR ({len(avisos)}): probablemente hay que preguntar")
        for a in avisos:
            print(f"  - {a}")
    if not faltas and not avisos:
        print("Sin huecos detectados. El contenido esta listo para compilar.")
    elif not faltas:
        print("\nNada obligatorio falta. Puedes compilar, pero mira los avisos.")
    return 1 if faltas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
