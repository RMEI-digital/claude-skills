#!/usr/bin/env -S uv run --with python-pptx --script
"""
Qué cambió a mano en un PowerPoint generado desde el .qmd.

    ./cambios-pptx.py <generado>.pptx <editado>.pptx

Cuando alguien edita el .pptx en PowerPoint, sus cambios mandan, pero viven
solo en ese archivo: si se regenera desde el .qmd sin recogerlos, se pierden.
Este script dice lámina por lámina qué hay que llevar al .qmd antes de volver
a generar:

  TEXTO       renglones quitados (-) y agregados (+), incluidas las celdas
  RESALTADO   lo marcado con color de resaltado: ahí se dejan los comentarios
  FORMA       piezas movidas, agrandadas, nuevas o borradas. El .qmd no guarda
              posiciones, así que esto se pierde al regenerar: hay que decidir
              si se resuelve en el .qmd o se avisa
  FUENTE      renglones que quedaron fuera de Montserrat al escribirlos a mano

Las láminas se emparejan por su título y, si no lo hay, por su orden.
"""
import difflib
import sys
from pathlib import Path

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu

TOLERANCIA_MM = 2.0     # menos que esto no es un cambio, es redondeo


def titulo(lamina):
    t = lamina.shapes.title
    return t.text_frame.text.strip() if t is not None and t.has_text_frame else ""


def parrafos(forma):
    """Los párrafos de una forma: los de su caja de texto o los de su tabla."""
    if forma.has_text_frame:
        yield from forma.text_frame.paragraphs
    if getattr(forma, "has_table", False) and forma.has_table:
        for fila in forma.table.rows:
            for celda in fila.cells:
                yield from celda.text_frame.paragraphs


def renglones(lamina):
    salida = []
    for forma in lamina.shapes:
        for p in parrafos(forma):
            texto = "".join(r.text for r in p.runs).strip()
            if texto:
                salida.append(texto)
    return salida


def resaltados(lamina):
    for forma in lamina.shapes:
        for p in parrafos(forma):
            for r in p.runs:
                rpr = r._r.find(qn("a:rPr"))
                if rpr is not None and rpr.find(qn("a:highlight")) is not None and r.text.strip():
                    yield r.text.strip()


def fuera_de_fuente(lamina):
    for forma in lamina.shapes:
        for p in parrafos(forma):
            for r in p.runs:
                if r.text.strip() and r.font.name not in ("Montserrat", "Menlo"):
                    yield r.text.strip()


def geometria(lamina):
    mm = lambda v: round(Emu(v).mm, 1) if v is not None else None
    return {f.shape_id: (f.name, mm(f.left), mm(f.top), mm(f.width), mm(f.height))
            for f in lamina.shapes}


def emparejar(gen, edi):
    """Por título; las que no lo tienen o no lo encuentran, por orden."""
    libres = list(range(len(edi)))
    pares = []
    for i, lam in enumerate(gen):
        t = titulo(lam)
        j = next((k for k in libres if t and titulo(edi[k]) == t), None)
        if j is None and i in libres:
            j = i
        if j is not None:
            libres.remove(j)
        pares.append((i, j))
    return pares, libres


def main():
    if len(sys.argv) != 3:
        sys.exit("Uso: ./cambios-pptx.py <generado>.pptx <editado>.pptx")
    a, b = Path(sys.argv[1]), Path(sys.argv[2])
    gen, edi = list(Presentation(str(a)).slides), list(Presentation(str(b)).slides)
    print(f"\n{a.name}: {len(gen)} láminas   {b.name}: {len(edi)} láminas")

    pares, sobrantes = emparejar(gen, edi)
    hay_texto = hay_forma = 0
    for i, j in pares:
        if j is None:
            print(f"\n== lámina {i + 1} «{titulo(gen[i])}»: BORRADA en el editado")
            hay_texto += 1
            continue
        lg, le = gen[i], edi[j]
        bloque = []
        tg, te = titulo(lg), titulo(le)
        diff = [d for d in difflib.ndiff(renglones(lg), renglones(le))
                if d.startswith(("- ", "+ "))]
        for d in diff:
            bloque.append(f"  TEXTO      {d}")
        hay_texto += len(diff)
        for t in resaltados(le):
            bloque.append(f"  RESALTADO  «{t}»")
        gg, ge = geometria(lg), geometria(le)
        for sid, (nombre, *caja) in ge.items():
            if sid not in gg:
                bloque.append(f"  FORMA      nueva: «{nombre}»")
                hay_forma += 1
                continue
            antes = gg[sid][1:]
            if any(x is not None and y is not None and abs(x - y) > TOLERANCIA_MM
                   for x, y in zip(antes, caja)):
                bloque.append(f"  FORMA      «{nombre}»: (x, y, ancho, alto) "
                              f"{tuple(antes)} -> {tuple(caja)} mm")
                hay_forma += 1
        for sid, (nombre, *_) in gg.items():
            if sid not in ge:
                bloque.append(f"  FORMA      borrada: «{nombre}»")
                hay_forma += 1
        for t in fuera_de_fuente(le):
            bloque.append(f"  FUENTE     «{t[:40]}» no está en Montserrat")
        if bloque:
            nombre = te if te == tg else f"{tg}» -> «{te}"
            print(f"\n== lámina {i + 1} «{nombre}»")
            print("\n".join(bloque))
    for j in sobrantes:
        print(f"\n== lámina {j + 1} del editado «{titulo(edi[j])}»: NUEVA, no está en el generado")
        hay_texto += 1

    print()
    if not (hay_texto or hay_forma):
        print("Sin cambios: se puede regenerar desde el .qmd sin perder nada.")
        return
    print(f"{hay_texto} cambios de texto: llévalos al .qmd antes de regenerar.")
    if hay_forma:
        print(f"{hay_forma} cambios de posición o tamaño: el .qmd no los guarda, así que")
        print("se pierden al regenerar. Resuélvelos en el .qmd o avisa a quien editó.")
    sys.exit(1)


if __name__ == "__main__":
    main()
