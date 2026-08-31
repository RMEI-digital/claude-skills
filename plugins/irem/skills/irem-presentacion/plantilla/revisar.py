#!/usr/bin/env -S uv run --with pillow --script
"""
Revisa una presentación IREM antes de entregarla.

    ./revisar.py <archivo>.qmd

Comprueba dos cosas distintas y las reporta por separado:

  FORMATO   sobre los PNG de las láminas: que nada invada la banda de los
            logotipos ni se salga por los lados, y que la portada sangre.
  CONTENIDO sobre el .qmd: palabras por lámina, viñetas, títulos repetidos,
            marcadores sin resolver, cobertura de notas y, si es una propuesta
            a un externo, que estén las siete secciones y en orden.

No sustituye mirar las láminas: detecta lo mecánico, no si la presentación se
entiende. Lo que no puede medir, lo dice.
"""
import re
import subprocess
import sys
from pathlib import Path

TOPE_PALABRAS = 40
TOPE_VINETAS = 4
TOPE_CARACTERES_VINETA = 118  # unos dos renglones a 10 pt en 137.6 mm
MIN_LAMINAS_POR_SECCION = 2   # menos que esto y la sección no se gana su portadilla
LAMINAS_POR_DISPLAY = 6       # una lámina de una sola frase por cada seis de contenido
TOPE_VACIAS = 1 / 3           # portadillas + despliegue + cierre sobre el total

DISPLAY = r"\\(?:ideaGrande|cifra|pregunta)\b"

ESPINA = [
    "La solicitud", "Lo que sabemos", "Lo que vemos", "Lo que consideramos",
    "Lo que buscamos", "Lo que proponemos", "Siguientes pasos",
]

# Comandos del formato cuyo texto SÍ se proyecta y por lo tanto cuenta.
CMD_CON_TEXTO = r"\\(?:numerado|concepto|realce|ideaGrande|pregunta|cifra|panelDerecho)"


def laminas(cuerpo):
    """Trocea el .qmd en láminas. Cada trozo termina donde empieza la lámina o
    la sección siguiente: sin ese corte, el encabezado de la sección siguiente
    se cuenta como texto de la lámina anterior e infla el conteo."""
    partes = re.split(r"^(#{1,2}) ", cuerpo, flags=re.M)[1:]
    for i in range(0, len(partes), 2):
        nivel, resto = partes[i], partes[i + 1]
        titulo, _, cont = resto.partition("\n")
        yield len(nivel), titulo.strip(), cont


def texto_visible(cont):
    """Lo que se proyecta: fuera notas, bloques de código y marcas de bloque.
    El texto que va dentro de los comandos del formato sí se proyecta."""
    en_latex = " ".join(
        m.group(1) or ""
        for m in re.finditer(CMD_CON_TEXTO + r"(?:\[[^\]]*\])?\{[^{}]*\}(?:\{([^{}]*)\})?", cont)
    )
    vis = re.sub(r"::: \{\.notes\}.*?:::", "", cont, flags=re.S)
    vis = re.sub(r"```.*?```", "", vis, flags=re.S)
    vis = re.sub(r"^:::+.*$", "", vis, flags=re.M)
    return vis, en_latex


def palabras(vis, en_latex):
    """Cuenta palabras. Quita la marca «- » de viñeta y la de énfasis, que no
    son palabras que nadie lea."""
    t = re.sub(r"^\s*[-*]\s+", " ", vis, flags=re.M)
    t = (t + " " + en_latex).replace("*", " ").replace("\\%", "%")
    return len([w for w in t.split() if any(c.isalnum() for c in w)])


def revisar_contenido(qmd):
    s = qmd.read_text()
    partes = s.split("---", 2)
    cuerpo = partes[2] if len(partes) > 2 else s
    fallos, avisos = [], []

    secciones = [t for n, t, _ in laminas(cuerpo) if n == 1]
    titulos, con_nota, total = [], 0, 0
    display, seguidas, max_seguidas, por_seccion, actual = 0, 0, 0, {}, None

    for nivel, titulo, cont in laminas(cuerpo):
        if nivel == 1:
            actual = titulo
            por_seccion[actual] = 0
            continue
        total += 1
        if actual:
            por_seccion[actual] += 1
        if re.search(DISPLAY, cont):
            display += 1
            seguidas += 1
            max_seguidas = max(max_seguidas, seguidas)
        else:
            seguidas = 0
        vis, en_latex = texto_visible(cont)
        if "{.notes}" in cont or "\\note{" in cont:
            con_nota += 1
        n = palabras(vis, en_latex)
        if n > TOPE_PALABRAS and "tablaIrem" not in cont:
            fallos.append(f"«{titulo[:40]}»: {n} palabras (tope {TOPE_PALABRAS})")
        vin = [l for l in vis.split("\n") if re.match(r"^\s*[-*] ", l)]
        if len(vin) > TOPE_VINETAS:
            fallos.append(f"«{titulo[:40]}»: {len(vin)} viñetas (tope {TOPE_VINETAS})")
        for v in vin:
            if len(v.strip()) > TOPE_CARACTERES_VINETA:
                fallos.append(f"«{titulo[:40]}»: viñeta de más de dos renglones")
        if titulo and not titulo.startswith("{"):
            titulos.append(titulo)

    for t in sorted({t for t in titulos if titulos.count(t) > 1}):
        fallos.append(f"título repetido en {titulos.count(t)} láminas: «{t}»")

    # Marcadores sin resolver. Se excluyen los enlaces de Markdown y los
    # argumentos opcionales de los comandos del formato, p. ej.
    # \laminaGracias[Preguntas], que no son marcadores.
    limpio = re.sub(r"\[[^\]]*\]\([^)]*\)", "", cuerpo)
    limpio = re.sub(r"\\[a-zA-Z]+\[[^\]]*\]", "", limpio)
    limpio = re.sub(r"```.*?```", lambda m: re.sub(r"\\[a-zA-Z]+\[[^\]]*\]", "", m.group(0)), limpio, flags=re.S)
    for m in re.findall(r"\[[^\]\n]{6,}\]", limpio):
        fallos.append(f"marcador sin resolver: {m}")

    if total and con_nota / total < 0.5:
        avisos.append(f"solo {con_nota} de {total} láminas tienen nota del presentador")

    # Portadillas que no se ganan su lugar.
    for nombre, n in por_seccion.items():
        if n < MIN_LAMINAS_POR_SECCION:
            fallos.append(
                f"«{nombre}» tiene {n} lámina de contenido y aun así lleva portadilla; "
                f"quítale el # o dale una segunda")

    # Láminas de una sola afirmación.
    if display and total // LAMINAS_POR_DISPLAY < display:
        fallos.append(
            f"{display} láminas de una sola frase para {total} de contenido "
            f"(máximo {max(1, total // LAMINAS_POR_DISPLAY)})")
    if max_seguidas > 1:
        fallos.append(f"{max_seguidas} láminas de una sola frase seguidas")

    # Cuánto del deck va casi en blanco: portada + portadillas + despliegue + cierre.
    paginas = 1 + len(secciones) + total
    vacias = len(secciones) + display + 1
    if paginas and vacias / paginas > TOPE_VACIAS:
        fallos.append(
            f"{vacias} de {paginas} láminas llevan una frase o menos "
            f"({100*vacias/paginas:.0f}%, tope {100*TOPE_VACIAS:.0f}%)")

    return secciones, total, con_nota, fallos, avisos


def revisar_formato(pdf):
    from PIL import Image
    carpeta = pdf.parent / ".revision"
    carpeta.mkdir(exist_ok=True)
    for viejo in carpeta.glob("rev-*.png"):
        viejo.unlink()
    r = subprocess.run(
        ["Rscript", "-e",
         f'n <- pdftools::pdf_info("{pdf}")$pages;'
         f'pdftools::pdf_convert("{pdf}", pages=1:n, dpi=110, format="png",'
         f' filenames=file.path("{carpeta}", sprintf("rev-%02d.png", 1:n)))'],
        capture_output=True, text=True)
    pngs = sorted(carpeta.glob("rev-*.png"))
    if not pngs:
        return None, [f"no pude renderizar los PNG: {r.stderr.strip()[:200]}"]

    fallos = []
    for i, f in enumerate(pngs, 1):
        im = Image.open(f).convert("RGB")
        W, H = im.size
        px = im.load()
        mmy, mmx = 90.0 / H, 160.0 / W
        bl = lambda p: all(v > 246 for v in p)
        if i == 1:
            arriba = sum(1 for c in range(int(0.60 * W), W) if not bl(px[c, 0]))
            der = sum(1 for y in range(0, int(0.93 * H)) if not bl(px[W - 1, y]))
            if arriba < 50:
                fallos.append(f"lámina 1: la foto no sangra por arriba")
            if der < 50:
                fallos.append(f"lámina 1: la foto no sangra por la derecha")
            continue
        z = sum(1 for y in range(int(74.0 / mmy), int(77.0 / mmy))
                for c in range(int(0.16 * W), int(0.88 * W)) if not bl(px[c, y]))
        if z > 60:
            fallos.append(f"lámina {i}: hay contenido en la banda de los logotipos")
        # Entre la base de los logotipos y la franja del pie no va nada. La
        # franja misma ocupa de 86 mm al borde, así que la ventana vigilada es
        # la de en medio; si se mirara hasta el borde, la propia franja daría
        # positivo en todas las láminas.
        b = sum(1 for y in range(int(83.5 / mmy), int(85.8 / mmy))
                for c in range(W) if not bl(px[c, y]))
        if b > 60:
            fallos.append(f"lámina {i}: hay contenido pegado a la franja del pie")
        # Y la franja tiene que estar: azul sobre verde, de borde a borde.
        medio = W // 2
        azul = px[medio, int(87.0 / mmy)]
        verde = px[medio, int(89.0 / mmy)]
        cerca = lambda c, r, g, bb: abs(c[0]-r) < 26 and abs(c[1]-g) < 26 and abs(c[2]-bb) < 26
        if not cerca(azul, 0x36, 0x7C, 0xBC) or not cerca(verde, 0x98, 0xCE, 0x63):
            fallos.append(f"lámina {i}: falta la franja azul y verde del pie")
        # 150.5 y no 148.8: el recuadro \realce llega a 149.5 mm por diseño
        # del master, que le da margen derecho de 10.5 mm y no de 11.2.
        d = sum(1 for y in range(int(4.0 / mmy), int(74.0 / mmy))
                for c in range(int(150.5 / mmx), W) if not bl(px[c, y]))
        if d > 40:
            fallos.append(f"lámina {i}: algo se sale por la derecha")
        iz = sum(1 for y in range(int(4.0 / mmy), int(74.0 / mmy))
                 for c in range(0, int(9.5 / mmx)) if not bl(px[c, y]))
        if iz > 40:
            fallos.append(f"lámina {i}: algo se sale por la izquierda")
    return len(pngs), fallos


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: ./revisar.py <archivo>.qmd")
    qmd = Path(sys.argv[1]).resolve()
    if not qmd.exists():
        sys.exit(f"No existe: {qmd}")

    secciones, total, con_nota, fallos_c, avisos = revisar_contenido(qmd)
    externa = secciones[:1] == ESPINA[:1] or set(ESPINA) & set(secciones)

    print(f"\n{qmd.name}   {total} láminas, {con_nota} con nota")
    print(f"secciones: {' → '.join(secciones) if secciones else '(ninguna)'}")

    if externa and secciones != ESPINA:
        fallos_c.append(
            "parece una propuesta a un externo pero la espina no coincide.\n"
            f"    esperada: {' → '.join(ESPINA)}")

    print("\nCONTENIDO")
    for f in fallos_c:
        print(f"  !! {f}")
    for a in avisos:
        print(f"  ·  {a}")
    if not fallos_c and not avisos:
        print("  todo en regla")

    print("\nFORMATO")
    pdf = qmd.with_suffix(".pdf")
    if not pdf.exists():
        print(f"  no hay {pdf.name}; compila primero con ./renderizar.sh")
        n_fmt = None
        fallos_f = []
    else:
        n_fmt, fallos_f = revisar_formato(pdf)
        for f in fallos_f:
            print(f"  !! {f}")
        if not fallos_f:
            print(f"  {n_fmt} láminas, nada fuera de caja")

    print("\nEsto no reemplaza mirar las láminas: revisa que el argumento se")
    print("entienda y que ninguna lámina se lea en voz alta.")
    sys.exit(1 if (fallos_c or fallos_f) else 0)


if __name__ == "__main__":
    main()
