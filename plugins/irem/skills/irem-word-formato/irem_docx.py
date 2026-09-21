#!/usr/bin/env python3
"""
Libreria para construir documentos Word con el formato institucional IREM/BID.

El formato no se reconstruye a mano: sale de plantilla.docx, que conserva tal
cual los estilos, el tema tipografico, los margenes, la numeracion y el
encabezado con los logos mesoamerica MALARIA + BID del documento de referencia.
Aqui solo se escriben los bloques (titulo, secciones, cuerpo, vinetas, tablas)
con las propiedades medidas de ese documento.
"""
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape
import copy
import re

try:
    from docx import Document
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement, parse_xml
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
AZUL_ENLACE = "0563C1"    # el azul de hipervinculo de Word
ANCHO_TABLA = 9784        # twips; la tabla es mas ancha que la caja de texto y va centrada
NUM_SECCION = "53"        # numId de la plantilla: numeracion romana I. II. III.
NUM_VINETA = "36"         # numId de la plantilla: vineta Symbol
JUSTIFICAR_DESDE = 60     # caracteres: por debajo de esto, una columna no se justifica

# Secciones apaisadas. El ancho util es el de la pagina menos los dos margenes
# de la plantilla (1440 twips cada uno): 15840 - 2880 = 12960.
PGSZ_VERTICAL = (12240, 15840)
PGSZ_APAISADA = (15840, 12240)
ANCHO_TABLA_APAISADA = 12960
BLANCOS_APAISADO = 2      # a cada lado de la tabla, o arranca pegada al borde de la seccion

# Para saber si una tabla cabe en vertical hay que estimar cuanto ocupa el token
# mas largo de cada columna, que es lo que Word no puede partir sin cortar la
# palabra. Medido sobre los avances de Calibri.ttf a 11 pt, un caracter va de 85
# twips ("Vigilancia") a 117 ("OBSERVACIONES"); los identificadores largos, que
# son los que de verdad fuerzan el giro ("SM-2024-000123-ABC"), caen en 106-110.
TWIPS_POR_CARACTER = 105
MARGEN_CELDA = 216        # twips: los 108 de relleno que Word deja a cada lado de la celda

# Marca de agua de borrador: texto gris girado 315 grados, detras del texto y
# centrado respecto al margen. Va en DrawingML y no en el WordArt VML clasico de
# las marcas de Word porque ese ya no se dibuja: el XML sobrevive al abrir y
# guardar, pero no se ve ni en pantalla ni al exportar a PDF.
ID_MARCA = "MarcaBorrador"
TEXTO_MARCA = "BORRADOR"
GRIS_MARCA = "D9D9D9"
ROT_MARCA = 18900000      # 315 grados, en sesentamilesimas de grado
EMU_POR_PUNTO = 12700
PT_MARCA = 96             # tamano de "BORRADOR"; un texto mas largo se reduce para caber
EM_POR_CARACTER = 0.59    # cuadratines que ocupa una mayuscula de Calibri, medido
# Word no dibuja la forma si su caja sin girar no cabe entre los margenes, asi que
# el tamano se limita por el ancho util de la pagina vertical: 12240 - 2880 twips.
ANCHO_MARGEN_PT = 468


# ---------------------------------------------------------------- XML crudo

def _e(tag, **attrs):
    el = OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn("w:" + k), str(v))
    return el


def _rpr(negrita=False, cursiva=False, pt=PT_CUERPO, color=None, fuente=FUENTE,
         subrayado=False):
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
    if subrayado:
        rpr.append(_e("w:u", val="single"))
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


# --------------------------------- texto con negrita, cursiva e hipervinculos

_ENLACE = re.compile(r"\[([^\[\]]*)\]\(([^)\s]+)\)", re.S)
_TROZOS = re.compile(r"(\[[^\[\]]*\]\([^)\s]+\)|\*\*.+?\*\*|\*[^*]+?\*)", re.S)


@dataclass(frozen=True)
class Trozo:
    """
    Un tramo de texto con su formato.

    Es un objeto y no una tupla porque cada atributo nuevo obligaba a tocar a
    todos los que la abrian: con esto, quien solo mire .texto sigue valiendo.
    """
    texto: str
    negrita: bool = False
    cursiva: bool = False
    enlace: str = None


def trozos(texto, negrita=False, cursiva=False, enlace=None):
    """
    Parte '**negrita**, *cursiva* y [texto](url)' en una lista de Trozo.

    Se llama a si misma para lo que va dentro de cada marca, de modo que las
    marcas se pueden anidar y '**[texto](url)**' sale en negrita y como enlace.
    Un corchete que no lleve detras un parentesis no es un enlace: queda tal cual.
    """
    salida = []
    for parte in _TROZOS.split(texto):
        if not parte:
            continue
        m = _ENLACE.fullmatch(parte)
        if m:
            if m.group(1):        # un enlace sin texto visible no se pinta
                salida.extend(trozos(m.group(1), negrita, cursiva, m.group(2)))
        elif parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            salida.extend(trozos(parte[2:-2], True, cursiva, enlace))
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            salida.extend(trozos(parte[1:-1], negrita, True, enlace))
        else:
            salida.append(Trozo(parte, negrita, cursiva, enlace))
    return salida or [Trozo("", negrita, cursiva, enlace)]


def como_trozo(x):
    """Acepta un Trozo o la tupla (texto, negrita, cursiva) de antes."""
    return x if isinstance(x, Trozo) else Trozo(*x)


def sin_marcas(texto):
    """El texto visible: sin las marcas y sin las URL de los enlaces."""
    return "".join(t.texto for t in trozos(texto))


# ------------------------------------------- cuanto ocupa una tabla en la pagina

def _token_mas_largo(filas, j):
    """El token sin espacios mas largo de una columna, cabecera incluida."""
    largo = 0
    for fila in filas:
        if j < len(fila):
            for token in sin_marcas(str(fila[j])).split():
                largo = max(largo, len(token))
    return largo


def _columna_corta(filas, j, ancho):
    return _token_mas_largo(filas, j) * TWIPS_POR_CARACTER > ancho - MARGEN_CELDA


def _no_cabe_vertical(filas, anchos):
    """
    Una columna se queda corta cuando su token mas largo no cabe en el ancho que
    le toca: ahi Word parte la palabra por la mitad y la tabla se vuelve altisima.
    Solo se gira si alguna columna se queda corta y deja de quedarse al girar, de
    modo que un token absurdo, que tampoco cabria apaisado, no arrastre la tabla a
    una seccion nueva para nada.
    """
    total = sum(anchos)
    for j, ancho in enumerate(anchos):
        girado = int(ANCHO_TABLA_APAISADA * ancho / total)
        if _columna_corta(filas, j, ancho) and not _columna_corta(filas, j, girado):
            return True
    return False


def _reparte(anchos, ancho_total):
    """Lleva los anchos a otro total guardando las proporciones entre columnas."""
    total = sum(anchos)
    nuevos = [int(ancho_total * a / total) for a in anchos]
    nuevos[-1] += ancho_total - sum(nuevos)
    return nuevos


# --------------------------------------------------- marca de agua de borrador

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS_WPS = "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP_DOCPR = "{%s}docPr" % NS_WP


def _marca_xml(texto, fuente, ident):
    """El parrafo con la marca de agua, ya medido para el texto que lleve."""
    largo = max(1, len(texto))
    pt = min(PT_MARCA, ANCHO_MARGEN_PT / (largo * EM_POR_CARACTER))
    cx = int(largo * EM_POR_CARACTER * pt * EMU_POR_PUNTO)
    cy = int(1.4 * pt * EMU_POR_PUNTO)     # alto de linea holgado, para que no recorte
    texto = escape(texto)
    return (
        f'<w:p xmlns:w="{NS_W}"><w:r><w:rPr><w:noProof/></w:rPr>'
        f'<w:drawing xmlns:wp="{NS_WP}">'
        '<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0"'
        ' relativeHeight="251658752" behindDoc="1" locked="0" layoutInCell="0"'
        ' allowOverlap="1"><wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="margin"><wp:align>center</wp:align></wp:positionH>'
        '<wp:positionV relativeFrom="margin"><wp:align>center</wp:align></wp:positionV>'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
        f'<wp:docPr id="{ident}" name="{ID_MARCA}"/>'
        f'<a:graphic xmlns:a="{NS_A}"><a:graphicData uri="{NS_WPS}">'
        f'<wps:wsp xmlns:wps="{NS_WPS}"><wps:cNvSpPr txBox="1"/>'
        f'<wps:spPr><a:xfrm rot="{ROT_MARCA}"><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '<a:noFill/><a:ln><a:noFill/></a:ln></wps:spPr>'
        '<wps:txbx><w:txbxContent><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r>'
        f'<w:rPr><w:rFonts w:ascii="{fuente}" w:hAnsi="{fuente}" w:cs="{fuente}"/>'
        f'<w:color w:val="{GRIS_MARCA}"/><w:sz w:val="{int(pt * 2)}"/>'
        f'<w:szCs w:val="{int(pt * 2)}"/></w:rPr>'
        f'<w:t>{texto}</w:t></w:r></w:p></w:txbxContent></wps:txbx>'
        '<wps:bodyPr rot="0" vert="horz" wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"'
        ' anchor="ctr" anchorCtr="0"><a:noAutofit/></wps:bodyPr>'
        '</wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing></w:r></w:p>'
    )


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
        self.en_apaisado = False  # hay una seccion apaisada abierta, a la espera de cierre
        self._emitiendo = False   # dentro de una tabla apaisada: no cerrar la seccion

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
        # texto puede venir como cadena con marcas **negrita**/*cursiva*/[t](url)
        # o ya troceado en una lista de Trozo
        piezas = texto if isinstance(texto, list) else trozos(texto)
        for pieza in piezas:
            tr = como_trozo(pieza)
            if not tr.texto:
                continue
            f = dict(fmt)
            f["negrita"] = f.get("negrita", False) or tr.negrita
            f["cursiva"] = f.get("cursiva", False) or tr.cursiva
            if tr.enlace:
                p.append(self._enlace(tr.texto, tr.enlace, **f))
            else:
                p.append(_run(tr.texto, fuente=self.fuente, **f))
        return p

    def _enlace(self, texto, url, **fmt):
        """
        El w:hyperlink con su run dentro, en azul y subrayado.

        La relacion se registra en la part del documento, y python-docx
        reutiliza la que ya exista para esa URL: dos enlaces al mismo sitio
        comparten una sola relacion.
        """
        fmt = dict(fmt)
        fmt.pop("color", None)     # el azul del enlace manda sobre el color del bloque
        h = OxmlElement("w:hyperlink")
        h.set(qn("r:id"), self.doc.part.relate_to(url, RT.HYPERLINK, is_external=True))
        h.append(_run(texto, fuente=self.fuente, color=AZUL_ENLACE,
                      subrayado=True, **fmt))
        return h

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
        # cualquier bloque que no sea otra tabla apaisada devuelve el documento a vertical
        if self.en_apaisado and not self._emitiendo:
            self._cierra_apaisado()
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
             _e("w:ind", left=0, hanging=0)],
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
        if self.en_apaisado:
            # cerrar la seccion apaisada ya parte pagina: un salto mas dejaria una en blanco
            self._cierra_apaisado()
            return
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

    # --- secciones apaisadas

    def _parrafo_seccion(self, pgsz):
        """
        Parrafo que cierra una seccion. El sectPr se copia del que ya trae el
        documento y solo se le cambia el tamano de pagina: construido de cero se
        perderian los margenes, el encabezado con los logos y el pie.
        """
        sect = copy.deepcopy(self.sect)
        ancho, alto = pgsz
        pgz = sect.find(qn("w:pgSz"))
        pgz.set(qn("w:w"), str(ancho))
        pgz.set(qn("w:h"), str(alto))
        if ancho > alto:
            pgz.set(qn("w:orient"), "landscape")
        else:
            pgz.attrib.pop(qn("w:orient"), None)
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        ppr.append(_rpr(fuente=self.fuente))
        ppr.append(sect)      # en pPr el sectPr va despues del rPr
        p.append(ppr)
        return p

    def _abre_apaisado(self):
        """Cierra la seccion vertical en curso y abre la apaisada de la tabla."""
        self._add(self._parrafo_seccion(PGSZ_VERTICAL))
        for _ in range(BLANCOS_APAISADO):
            self.blanco()
        self.en_apaisado = True
        self.anterior = None

    def _cierra_apaisado(self):
        """Cierra la seccion apaisada: lo que venga detras vuelve a vertical."""
        self._emitiendo = True
        try:
            for _ in range(BLANCOS_APAISADO):
                self.blanco()
            self._add(self._parrafo_seccion(PGSZ_APAISADA))
        finally:
            self._emitiendo = False
        self.en_apaisado = False
        self.anterior = None

    # --- tablas

    def tabla(self, filas, encabezados=(0,), pesos=None, alineaciones=None,
              orientacion=None):
        """
        filas         lista de listas de celdas (texto, admite **negrita**)
        encabezados   indices de filas con fondo gris y negrita
        pesos         anchos relativos por columna (por defecto, iguales)
        alineaciones  'both'/'center'/'left'/'right' por columna
                      (por defecto la primera justificada y el resto centradas)
        orientacion   'vertical' u 'horizontal' para mandar sobre el criterio
                      automatico, que gira la tabla cuando no cabe en vertical
        """
        if not filas:
            return
        ncol = max(len(f) for f in filas)
        # el relleno se mide sobre la lista ya normalizada: medido sobre la de
        # entrada, una tabla sin anchos explicitos salia con el doble de columnas
        # y se dibujaba a la mitad de ANCHO_TABLA
        pesos = list(pesos or [1] * ncol)[:ncol]
        pesos += [1] * max(0, ncol - len(pesos))
        total = sum(pesos) or ncol
        anchos = [int(ANCHO_TABLA * p / total) for p in pesos]
        anchos[-1] += ANCHO_TABLA - sum(anchos)
        if alineaciones is None:
            alineaciones = ["both"] + ["center"] * (ncol - 1)
        alineaciones = list(alineaciones)[:ncol] + ["center"] * max(0, ncol - len(alineaciones))
        # justificar solo tiene sentido donde hay texto largo: en una celda corta
        # que parte en dos lineas, Word estira los espacios ("10:30      a" y
        # "10:45" debajo), asi que esas columnas van a la izquierda
        for j in range(ncol):
            if alineaciones[j] == "both":
                largo = max((len(str(f[j])) for f in filas if j < len(f)), default=0)
                if largo < JUSTIFICAR_DESDE:
                    alineaciones[j] = "left"

        if orientacion is None:
            orientacion = "horizontal" if _no_cabe_vertical(filas, anchos) else "vertical"
        apaisada = orientacion == "horizontal"
        if apaisada:
            anchos = _reparte(anchos, ANCHO_TABLA_APAISADA)

        # una tabla apaisada seguida de otra comparte seccion con ella: _emitiendo
        # es lo que evita que el ritmo la cierre para volver a abrirla enseguida
        self._emitiendo = apaisada
        try:
            if apaisada and not self.en_apaisado:
                self._abre_apaisado()
            self._ritmo("tabla")
            self._add(self._construye_tabla(filas, encabezados, anchos, alineaciones))
            if not apaisada:
                self.blanco()
        finally:
            self._emitiendo = False
        self.anterior = "tabla"

    def _construye_tabla(self, filas, encabezados, anchos, alineaciones):
        """El w:tbl en si, ya decididos el ancho de cada columna y la alineacion."""
        ncol = len(anchos)
        ancho_total = sum(anchos)
        tbl = OxmlElement("w:tbl")
        pr = OxmlElement("w:tblPr")
        pr.append(_e("w:tblStyle", val="TableGrid"))
        pr.append(_e("w:tblW", w=ancho_total, type="dxa"))
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
            if i == 0:
                # solo la primera fila se repite al cortar pagina: un encabezado de
                # bloque intermedio arrastraria su rotulo a paginas que ya van por otro
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
        return tbl

    # --- marca de agua

    def marca_borrador(self, texto=TEXTO_MARCA):
        """
        Pone la marca de agua de borrador en todos los encabezados. No va por
        omision: la plantilla no la trae y solo se pone cuando se pide. Si el
        encabezado ya la tiene no se repite, asi que aplicarla dos veces no deja
        dos marcas superpuestas.
        """
        puestas = 0
        for parte in self.doc.part.package.iter_parts():
            if not re.match(r"^/word/header\d*\.xml$", str(parte.partname)):
                continue
            hdr = parte.element
            ids = [el.get("id") for el in hdr.iter(WP_DOCPR)]
            if ID_MARCA in [el.get("name") for el in hdr.iter(WP_DOCPR)]:
                continue
            # el id de la forma tiene que ser unico dentro del encabezado
            ident = max([int(x) for x in ids if x and x.isdigit()] or [0]) + 1
            hdr.append(parse_xml(_marca_xml(texto, self.fuente, ident)))
            puestas += 1
        return puestas

    def guardar(self, ruta):
        if self.en_apaisado:
            self._cierra_apaisado()
        self.doc.save(str(ruta))
        return ruta
