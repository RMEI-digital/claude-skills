#!/usr/bin/env python3
"""
Genera un .docx con el formato institucional IREM/BID a partir de un Markdown
ligero.

Uso:
    uv run --with python-docx python generar.py FUENTE.md [SALIDA.docx] [--fuente Calibri]

Marcado que se reconoce:
    # Titulo                 titulo del documento (centrado, negrita).
                             Varias lineas '#' seguidas son varias lineas del titulo.
    ## Seccion               seccion con numeracion romana automatica (I. II. III.)
    ### Subtitulo            subtitulo en negrita, al margen
    #### Sub-subtitulo       sub-subtitulo en cursiva, al margen
    **Etiqueta:** valor      linea de campo (etiqueta en negrita)
    **Solo negrita**         equivale a ###
    *Solo cursiva*           equivale a ####
    - item                   vineta (tambien '*' o '•')
    | a | b |                tabla (con fila separadora |---|---|)
    \\anchos 66 34            anchos relativos de columna para la tabla siguiente
    \\pagina                  salto de pagina
    **negrita** *cursiva*    dentro de cualquier parrafo

Los parrafos en blanco de separacion los pone el generador segun el ritmo
vertical del formato: no hay que escribirlos.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from irem_docx import Documento, trozos  # noqa: E402

SEPARADOR = re.compile(r"^:?-{2,}:?$")
CAMPO = re.compile(r"^\*\*([^*]+:)\*\*\s*(.*)$")
VINETA = re.compile(r"^\s*[-*•]\s+(.*)$")


def es_separador(celdas):
    return bool(celdas) and all(SEPARADOR.match(c.strip()) for c in celdas)


def parte_fila(linea):
    linea = linea.strip()
    if linea.startswith("|"):
        linea = linea[1:]
    if linea.endswith("|"):
        linea = linea[:-1]
    return [c.strip() for c in linea.split("|")]


def solo_negrita(t):
    ts = [x for x in trozos(t) if x[0].strip()]
    return bool(ts) and all(neg for _, neg, _ in ts)


def solo_cursiva(t):
    ts = [x for x in trozos(t) if x[0].strip()]
    return bool(ts) and all(cur for _, _, cur in ts)


def bloques(lineas):
    """Agrupa las lineas en bloques (tipo, contenido)."""
    i = 0
    anchos = None
    while i < len(lineas):
        cruda = lineas[i]
        linea = cruda.strip()

        if not linea:
            i += 1
            continue

        if linea in ("\\pagina", "\\pagebreak", "\\newpage"):
            yield ("pagina", None)
            i += 1
            continue

        if linea.startswith("\\anchos"):
            anchos = [float(x) for x in linea.split()[1:]]
            i += 1
            continue

        # tabla: bloque de lineas consecutivas que empiezan por '|'
        if linea.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append(parte_fila(lineas[i]))
                i += 1
            yield ("tabla", (filas, anchos))
            anchos = None
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", linea)
        if m:
            yield ({1: "titulo", 2: "h1", 3: "h2", 4: "h3"}[len(m.group(1))], m.group(2).strip())
            i += 1
            continue

        m = VINETA.match(cruda)
        if m:
            texto = m.group(1).strip()
            i += 1
            # una vineta puede continuar en las lineas siguientes indentadas
            while i < len(lineas) and lineas[i].strip() and not re.match(
                    r"^\s*([-*•]\s|#|\||\\)", lineas[i]) and lineas[i][:1].isspace():
                texto += " " + lineas[i].strip()
                i += 1
            yield ("vineta", texto)
            continue

        m = CAMPO.match(linea)
        if m:
            yield ("campo", (m.group(1), m.group(2)))
            i += 1
            continue

        if solo_negrita(linea):
            yield ("h2", linea)
            i += 1
            continue
        if solo_cursiva(linea):
            yield ("h3", linea)
            i += 1
            continue

        # cuerpo: hasta la siguiente linea en blanco o marca
        texto = linea
        i += 1
        while i < len(lineas) and lineas[i].strip() and not re.match(
                r"^\s*([-*•]\s|#{1,4}\s|\||\\)", lineas[i]):
            texto += " " + lineas[i].strip()
            i += 1
        yield ("cuerpo", texto)


def alineaciones_de(sep):
    salida = []
    for c in sep:
        c = c.strip()
        if c.startswith(":") and c.endswith(":"):
            salida.append("center")
        elif c.endswith(":"):
            salida.append("right")
        elif c.startswith(":"):
            salida.append("left")
        else:
            salida.append(None)
    return salida


def escribe_tabla(doc, filas, anchos):
    sep = next((f for f in filas if es_separador(f)), None)
    cuerpo = [f for f in filas if not es_separador(f)]
    if not cuerpo:
        return
    encabezados = {0}
    for k, fila in enumerate(cuerpo):
        if k and any(c.strip() for c in fila) and all(
                solo_negrita(c) or not c.strip() for c in fila):
            encabezados.add(k)
    cuerpo = [[re.sub(r"\*\*(.*?)\*\*", r"\1", c) if k in encabezados else c
               for c in fila] for k, fila in enumerate(cuerpo)]
    cuerpo = [[c.replace("<br>", "\n").replace("<br/>", "\n") for c in fila] for fila in cuerpo]

    pesos = anchos
    if pesos is None and sep:
        largos = [len(c.strip()) for c in sep]
        pesos = largos if (max(largos) - min(largos)) > 2 else None
    alin = alineaciones_de(sep) if sep else None
    if alin and any(a is None for a in alin):
        alin = [a or ("both" if j == 0 else "center") for j, a in enumerate(alin)]
    doc.tabla(cuerpo, encabezados=encabezados, pesos=pesos, alineaciones=alin)


def construye(texto, fuente):
    doc = Documento(fuente=fuente)
    for tipo, contenido in bloques(texto.splitlines()):
        if tipo == "titulo":
            doc.titulo(contenido)
        elif tipo == "h1":
            doc.h1(contenido)
        elif tipo == "h2":
            doc.h2(contenido)
        elif tipo == "h3":
            doc.h3(contenido)
        elif tipo == "cuerpo":
            doc.cuerpo(contenido)
        elif tipo == "vineta":
            doc.vineta(contenido)
        elif tipo == "campo":
            doc.campo(contenido[0] + " ", contenido[1])
        elif tipo == "tabla":
            escribe_tabla(doc, contenido[0], contenido[1])
        elif tipo == "pagina":
            doc.salto_pagina()
    return doc


def main(argv):
    args = list(argv[1:])
    fuente = "Calibri"
    if "--fuente" in args:
        k = args.index("--fuente")
        if k + 1 >= len(args):
            sys.exit("Falta el nombre de la fuente despues de --fuente")
        fuente = args[k + 1]
        del args[k:k + 2]
    if not args:
        print(__doc__)
        sys.exit(1)
    entrada = Path(args[0])
    salida = Path(args[1]) if len(args) > 1 else entrada.with_suffix(".docx")
    doc = construye(entrada.read_text(encoding="utf-8"), fuente)
    doc.guardar(salida)
    print(f"Generado con fuente '{fuente}': {salida}")


if __name__ == "__main__":
    main(sys.argv)
