#!/usr/bin/env -S uv run --with pymupdf --with pillow --script
"""
Fabrica los íconos y los logos de una presentación IREM, en `iconos/`.

    ./iconos.py tabler brand-whatsapp building-bank server
    ./iconos.py marca github heroku postgresql powerbi

Dos clases, porque sirven para cosas distintas:

  tabler  Pictograma de Tabler Icons (licencia MIT) en blanco sobre un círculo
          del verde institucional. Es el ícono de \\filaIcono, el que acompaña
          a cada frase de la lámina de contexto. Sale como iconos/<nombre>.png.
          Los nombres están en https://tabler.io/icons (la versión «outline»).

  marca   Logo de una herramienta o empresa, de Simple Icons, en el color de
          la marca y con fondo transparente. Es el de \\logoFila, en la primera
          columna de una tabla. Sale como iconos/logo-<nombre>.png. Los nombres
          (slugs) están en https://simpleicons.org.

Para guardar con otro nombre: `nombre:archivo`, p. ej. `building-bank:ministerio`
deja iconos/ministerio.png.

Los logos son marcas registradas de sus dueños. Simple Icons los publica en
CC0, pero algunos (los de Microsoft, por ejemplo) traen sus propias condiciones
de uso; el script las imprime cuando las hay.
"""
import json
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

#  Versiones fijas: así un ícono bajado hoy sale igual el año que viene.
TABLER = "https://cdn.jsdelivr.net/npm/@tabler/icons@3/icons/outline/{}.svg"
#  Simple Icons retira logos de una versión a otra cuando la marca lo pide
#  (Heroku y Twilio ya no están en la 16). Se prueba de la más nueva a la más
#  vieja y se usa la primera que lo tenga. El catálogo con los colores cambió de
#  carpeta en la 15.
SIMPLE = "https://cdn.jsdelivr.net/npm/simple-icons@{v}/icons/{slug}.svg"
SIMPLE_VERSIONES = (16, 15, 13, 10)
SIMPLE_DATOS = ("https://cdn.jsdelivr.net/npm/simple-icons@{v}/data/simple-icons.json",
                "https://cdn.jsdelivr.net/npm/simple-icons@{v}/_data/simple-icons.json")

LADO = 240                 # px; a 9 mm en la lámina sobra resolución
VERDE = (0x98, 0xCE, 0x63)  # verde institucional
GRIS_OSCURO = "404040"     # para la marca cuyo color no se vería sobre blanco
GLIFO = 0.5                # el pictograma ocupa la mitad del círculo

SALIDA = Path("iconos")


def bajar(url, obligatorio=True):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        if obligatorio:
            raise SystemExit(f"No pude bajar {url}: {e}")
        return None


def svg_a_png(svg, lado):
    """Rasteriza un SVG a un cuadrado de `lado` px con fondo transparente."""
    doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
    pag = doc[0]
    zoom = lado / max(pag.rect.width, pag.rect.height)
    pix = pag.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    return im.resize((lado, lado), Image.LANCZOS) if im.size != (lado, lado) else im


def tabler(nombre, archivo):
    svg = bajar(TABLER.format(nombre))
    svg = svg.replace('stroke="currentColor"', 'stroke="#FFFFFF"')
    glifo = svg_a_png(svg, int(LADO * GLIFO))
    # El círculo se dibuja al cuádruple y se reduce: sin eso el borde sale
    # dentado, y a 9 mm proyectados se nota.
    grande = Image.new("RGBA", (LADO * 4, LADO * 4), (0, 0, 0, 0))
    ImageDraw.Draw(grande).ellipse((0, 0, LADO * 4 - 1, LADO * 4 - 1), fill=VERDE + (255,))
    im = grande.resize((LADO, LADO), Image.LANCZOS)
    pos = (LADO - glifo.width) // 2
    im.alpha_composite(glifo, (pos, pos))
    im.save(archivo)


_datos = {}


def color_de_marca(slug, version):
    """El color oficial de la marca, del catálogo de Simple Icons. El catálogo
    no trae el slug salvo excepciones: se deriva del título como lo hace la
    propia librería."""
    if version not in _datos:
        for url in SIMPLE_DATOS:
            texto = bajar(url.format(v=version), obligatorio=False)
            if texto:
                d = json.loads(texto)
                _datos[version] = d["icons"] if isinstance(d, dict) else d
                break
        else:
            _datos[version] = []
    reemplazos = {"+": "plus", ".": "dot", "&": "and", "đ": "d", "ħ": "h", "ı": "i",
                  "ĸ": "k", "ŀ": "l", "ł": "l", "ß": "ss", "ŧ": "t", "ø": "o"}
    for icono in _datos[version]:
        s = icono.get("slug")
        if not s:
            t = icono["title"].lower()
            for a, b in reemplazos.items():
                t = t.replace(a, b)
            t = unicodedata.normalize("NFD", t)
            s = re.sub(r"[^a-z0-9]", "", t)
        if s == slug:
            return icono["hex"], icono.get("license")
    return None, None


def marca(slug, archivo):
    for version in SIMPLE_VERSIONES:
        svg = bajar(SIMPLE.format(v=version, slug=slug), obligatorio=False)
        if svg:
            break
    else:
        raise SystemExit(f"«{slug}» no está en Simple Icons. Búscalo en "
                         f"https://simpleicons.org; el nombre es el de la URL.")
    hexa, licencia = color_de_marca(slug, version)
    hexa = hexa or GRIS_OSCURO
    r, g, b = (int(hexa[i:i + 2], 16) for i in (0, 2, 4))
    # Una marca blanca o casi blanca desaparece sobre la lámina.
    if 0.2126 * r + 0.7152 * g + 0.0722 * b > 215:
        hexa = GRIS_OSCURO
    svg = svg.replace("<svg ", f'<svg fill="#{hexa}" ', 1)
    svg_a_png(svg, LADO).save(archivo)
    if licencia:
        print(f"    ojo: {slug} no es CC0, trae condiciones de uso propias: "
              f"{licencia.get('url') or licencia.get('type')}")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("tabler", "marca"):
        sys.exit(__doc__)
    clase, pedidos = sys.argv[1], sys.argv[2:]
    SALIDA.mkdir(exist_ok=True)
    for pedido in pedidos:
        nombre, _, como = pedido.partition(":")
        if clase == "tabler":
            archivo = SALIDA / f"{como or nombre}.png"
            tabler(nombre, archivo)
        else:
            archivo = SALIDA / f"logo-{como or nombre}.png"
            marca(nombre, archivo)
        print(f"  {archivo}")


if __name__ == "__main__":
    main()
