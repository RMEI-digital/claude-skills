-- Lleva al preámbulo de LaTeX lo que el encabezado del .qmd decide y que
-- irem.tex no puede leer por su cuenta, porque LaTeX no ve el YAML.
--
-- Hoy es una sola cosa: la viñeta verde en el primer nivel de las listas.
-- Va encendida con `tipo: resumen`, y cualquier presentación la enciende o la
-- apaga con `vinetas: true` o `vinetas: false`, que manda sobre el tipo.
-- renderizar-pptx.py lee los mismos dos campos, así que las dos salidas
-- deciden igual.

local function valor(v)
  if v == nil then
    return nil
  end
  if type(v) == "boolean" then
    return tostring(v)
  end
  return pandoc.utils.stringify(v)
end

function Meta(meta)
  local con_vinetas = valor(meta.tipo) == "resumen"
  local vinetas = valor(meta.vinetas)
  if vinetas ~= nil then
    con_vinetas = (vinetas == "true" or vinetas == "sí" or vinetas == "si")
  end
  if con_vinetas then
    -- Se define una macro y nada más: irem.tex pregunta por ella en
    -- \AtBeginDocument, así que da igual cuál de los dos llega antes.
    quarto.doc.include_text("in-header", "\\def\\iremConVinetas{}")
  end
end
