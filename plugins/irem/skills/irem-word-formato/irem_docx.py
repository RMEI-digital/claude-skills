#!/usr/bin/env python3
"""
Libreria para construir documentos Word con el formato institucional IREM/BID.

El formato no se reconstruye a mano: sale de plantilla.docx, que conserva tal
cual los estilos, el tema tipografico, los margenes, la numeracion y el
encabezado con los logos IDB + mesoamerica MALARIA del documento de referencia.
Aqui solo se escriben los bloques (titulo, secciones, cuerpo, vinetas, tablas)
con las propiedades medidas de ese documento.
"""
from pathlib import Path
import re

try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ModuleNotFoundError:                       # mensaje util para quien no es tecnico
    import sys
    sys.exit(
        "Falta la libreria python-docx, que es la unica dependencia.\n\n"
        "La forma recomendada de ejecutar esto, que la instala sola y no toca\n"
        "tu Python del sistema:\n"
        "    uv run --with python-docx python generar.py FUENTE.md SALIDA.docx\n\n"
        "Si no tienes uv, mira la seccion 'Requisitos' del SKILL.md.\n"
        "Si prefieres instalarla a mano: pip install python-docx"
    )

AQUI = Path(__file__).resolve().parent
PLANTILLA = AQUI / "plantilla.docx"

FUENTE = "Calibri"        # fuente del tema del documento de referencia
PT_CUERPO = 24            # medios puntos: 12 pt
PT_TABLA = 22             # medios puntos: 11 pt
IDIOMA = "es-419"
GRIS_ENCABEZADO = "D9D9D9"
ANCHO_TABLA = 9784        # twips; la tabla es mas ancha que la caja de texto y va centrada
NUM_SECCION = "53"        # numId de la plantilla: numeracion romana I. II. III.
NUM_VINETA = "36"         # numId de la plantilla: vineta Symbol


# ---------------------------------------------------------------- XML crudo

def _e(tag, **attrs):
    el = OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn("w:" + k), str(v))
    return el


def _rpr(negrita=False, cursiva=False, pt=PT_CUERPO, color=None, fuente=FUENTE):
    """rPr con la fuente, el tamano y el idioma del formato IREM."""
    rpr = OxmlElement("w:rPr")
    rpr.append(_e("w:rFonts", ascii=fuente, hAnsi=fuente, cs=fuente))
    if negrita:
        rpr.append(_e("w:b"))
        rpr.append(_e("w:bCs"))
    if cursiva:
        rpr.append(_e("w:i"))
        rpr.append(_e("w:iCs"))
    if color:
        rpr.append(_e("w:color", val=color))
    rpr.append(_e("w:sz", val=pt))
    rpr.append(_e("w:szCs", val=pt))
    rpr.append(_e("w:lang", val=IDIOMA))
    return rpr


def _run(texto, **fmt):
    r = OxmlElement("w:r")
    r.append(_rpr(**fmt))
    t = OxmlElement("w:t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = texto
    r.append(t)
    return r


# ------------------------------------------------- texto con negrita/cursiva

_TROZOS = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*)", re.S)


def trozos(texto):
    """Parte '**negrita** y *cursiva*' en [(texto, negrita, cursiva), ...]."""
    salida = []
    for parte in _TROZOS.split(texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            salida.append((parte[2:-2], True, False))
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            salida.append((parte[1:-1], False, True))
        else:
            salida.append((parte, False, False))
    return salida or [("", False, False)]


def sin_marcas(texto):
    return "".join(t for t, _, _ in trozos(texto))


# -------------------------------------------------------------- el documento

class Documento:
    """Acumula bloques y los escribe en el cuerpo de la plantilla."""

    def __init__(self, plantilla=None, fuente=FUENTE):
        self.doc = Document(str(plantilla or PLANTILLA))
        self.fuente = fuente
        self.body = self.doc.element.body
        self.sect = self.body.find(qn("w:sectPr"))
        for p in list(self.body.findall(qn("w:p"))):
            self.body.remove(p)
        self.anterior = None      # tipo del bloque anterior, para el ritmo vertical

    # --- plumbing

    def _add(self, el):
        if self.sect is not None:
            self.sect.addprevious(el)
        else:
            self.body.append(el)
        return el

    def _p(self, ppr_hijos=(), rpr_marca=None):
        p = OxmlElement("w:p")
        if ppr_hijos or rpr_marca is not None:
            ppr = OxmlElement("w:pPr")
            for h in ppr_hijos:
                ppr.append(h)
            if rpr_marca is not None:
                ppr.append(rpr_marca)
            p.append(ppr)
        return p

    def _texto(self, p, texto, **fmt):
        # texto puede venir como cadena con marcas **negrita**/*cursiva*
        # o ya troceado en [(texto, negrita, cursiva), ...]
        piezas = texto if isinstance(texto, list) else trozos(texto)
        for t, neg, cur in piezas:
            if not t:
                continue
            f = dict(fmt)
            f["negrita"] = f.get("negrita", False) or neg
            f["cursiva"] = f.get("cursiva", False) or cur
            p.append(_run(t, fuente=self.fuente, **f))
        return p

    # --- ritmo vertical (cuando va un parrafo en blanco antes del bloque)

    _NECESITA_BLANCO = {
        "titulo": lambda ant: False,
        "campo":  lambda ant: ant in ("cuerpo", "vineta", "tabla", "titulo"),
        "h1":     lambda ant: ant is not None,
        "h2":     lambda ant: ant not in (None, "titulo"),
        "h3":     lambda ant: ant in ("cuerpo", "campo"),
        "cuerpo": lambda ant: ant in ("cuerpo", "vineta", "tabla", "titulo"),
        "vineta": lambda ant: False,
        "tabla":  lambda ant: ant is not None,
    }

    def _ritmo(self, tipo):
        if self._NECESITA_BLANCO.get(tipo, lambda a: False)(self.anterior):
            self.blanco()
        self.anterior = tipo

    # --- bloques

    def blanco(self, jc=None):
        hijos = [_e("w:jc", val=jc)] if jc else []
        self._add(self._p(hijos, _rpr(fuente=self.fuente)))

    def titulo(self, texto):
        """Titulo del documento: centrado, negrita, sin espaciado extra."""
        self._ritmo("titulo")
        p = self._p(
            [_e("w:keepNext"),
             _e("w:pStyle", val="paragraph0"),
             _e("w:spacing", before=0, beforeAutospacing=0, after=0, afterAutospacing=0),
             _e("w:jc", val="center")],
            _rpr(negrita=True, fuente=self.fuente),
        )
        self._texto(p, texto, negrita=True)
        self._add(p)

    def campo(self, etiqueta, valor):
        """Linea 'Etiqueta: valor' con la etiqueta en negrita."""
        self._ritmo("campo")
        p = self._p([], _rpr(fuente=self.fuente))
        p.append(_run(etiqueta, negrita=True, fuente=self.fuente))
        if valor:
            self._texto(p, valor)
        self._add(p)

    def h1(self, texto):
        """Seccion con numeracion romana automatica: I. II. III."""
        self._ritmo("h1")
        p = self._p(
            [_e("w:keepNext"),
             _e("w:pStyle", val="NormalWeb"),
             self._numpr(NUM_SECCION),
             _e("w:spacing", before=0, beforeAutospacing=0, after=0, afterAutospacing=0),
             _e("w:ind", left=540, hanging=270)],
            _rpr(negrita=True, fuente=self.fuente),
        )
        self._texto(p, texto, negrita=True)
        self._add(p)

    def h2(self, texto):
        """Subtitulo en negrita, al margen (actor, institucion, bloque)."""
        self._ritmo("h2")
        p = self._p([_e("w:keepNext")], _rpr(negrita=True, fuente=self.fuente))
        self._texto(p, texto, negrita=True)
        self._add(p)

    def h3(self, texto):
        """Sub-subtitulo en cursiva, al margen (Recepcion, Consolidacion, ...)."""
        self._ritmo("h3")
        p = self._p([_e("w:keepNext"), _e("w:jc", val="both")],
                    _rpr(cursiva=True, fuente=self.fuente))
        self._texto(p, texto, cursiva=True)
        self._add(p)

    def cuerpo(self, texto):
        """Parrafo de cuerpo, justificado."""
        self._ritmo("cuerpo")
        p = self._p(
            [_e("w:pStyle", val="NormalWeb"),
             _e("w:spacing", before=0, beforeAutospacing=0, after=0, afterAutospacing=0),
             _e("w:jc", val="both")],
            _rpr(fuente=self.fuente),
        )
        self._texto(p, texto)
        self._add(p)

    def vineta(self, texto):
        """Vineta Symbol a 0.5 pulgadas, justificada."""
        self._ritmo("vineta")
        p = self._p(
            [_e("w:pStyle", val="ListParagraph"),
             self._numpr(NUM_VINETA),
             _e("w:jc", val="both")],
            _rpr(fuente=self.fuente),
        )
        self._texto(p, texto)
        self._add(p)

    def salto_pagina(self):
        p = self._p([], _rpr(fuente=self.fuente))
        r = OxmlElement("w:r")
        r.append(_rpr(fuente=self.fuente))
        r.append(_e("w:br", type="page"))
        p.append(r)
        self._add(p)
        self.anterior = None

    def _numpr(self, num_id, ilvl=0):
        numpr = OxmlElement("w:numPr")
        numpr.append(_e("w:ilvl", val=ilvl))
        numpr.append(_e("w:numId", val=num_id))
        return numpr

    # --- tablas

    def tabla(self, filas, encabezados=(0,), pesos=None, alineaciones=None):
        """
        filas         lista de listas de celdas (texto, admite **negrita**)
        encabezados   indices de filas con fondo gris y negrita
        pesos         anchos relativos por columna (por defecto, iguales)
        alineaciones  'both'/'center'/'left'/'right' por columna
                      (por defecto la primera justificada y el resto centradas)
        """
        if not filas:
            return
        self._ritmo("tabla")
        ncol = max(len(f) for f in filas)
        pesos = list(pesos or [1] * ncol)[:ncol] + [1] * max(0, ncol - len(pesos or []))
        total = sum(pesos) or ncol
        anchos = [int(ANCHO_TABLA * p / total) for p in pesos]
        anchos[-1] += ANCHO_TABLA - sum(anchos)
        if alineaciones is None:
            alineaciones = ["both"] + ["center"] * (ncol - 1)
        alineaciones = list(alineaciones)[:ncol] + ["center"] * max(0, ncol - len(alineaciones))

        tbl = OxmlElement("w:tbl")
        pr = OxmlElement("w:tblPr")
        pr.append(_e("w:tblStyle", val="TableGrid"))
        pr.append(_e("w:tblW", w=ANCHO_TABLA, type="dxa"))
        pr.append(_e("w:jc", val="center"))
        pr.append(_e("w:tblLayout", type="fixed"))
        look = _e("w:tblLook", val="04A0", firstRow=1, lastRow=0,
                  firstColumn=1, lastColumn=0, noHBand=0, noVBand=1)
        pr.append(look)
        tbl.append(pr)
        grid = OxmlElement("w:tblGrid")
        for a in anchos:
            grid.append(_e("w:gridCol", w=a))
        tbl.append(grid)

        for i, fila in enumerate(filas):
            es_enc = i in encabezados
            tr = OxmlElement("w:tr")
            trpr = OxmlElement("w:trPr")
            if es_enc and all(k in encabezados for k in range(i + 1)):
                # solo se repiten al cortar pagina las filas de encabezado de arriba
                trpr.append(_e("w:tblHeader"))
            trpr.append(_e("w:jc", val="center"))
            tr.append(trpr)
            for j in range(ncol):
                celda = fila[j] if j < len(fila) else ""
                tc = OxmlElement("w:tc")
                tcpr = OxmlElement("w:tcPr")
                tcpr.append(_e("w:tcW", w=anchos[j], type="dxa"))
                if es_enc:
                    tcpr.append(_e("w:shd", val="clear", color="auto", fill=GRIS_ENCABEZADO))
                else:
                    tcpr.append(_e("w:vAlign", val="center"))
                tc.append(tcpr)
                jc = "center" if es_enc else alineaciones[j]
                fmt = dict(pt=PT_TABLA, color="000000", negrita=es_enc)
                for k, linea in enumerate(str(celda).split("\n")):
                    p = self._p(
                        [_e("w:pStyle", val="ListParagraph"),
                         _e("w:ind", left=0),
                         _e("w:jc", val=jc)],
                        _rpr(fuente=self.fuente, **fmt),
                    )
                    self._texto(p, linea, **fmt)
                    tc.append(p)
                tr.append(tc)
            tbl.append(tr)
        self._add(tbl)
        self.blanco()
        self.anterior = "tabla"

    def guardar(self, ruta):
        self.doc.save(str(ruta))
        return ruta
