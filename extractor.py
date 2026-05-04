import pdfplumber

def extract_text(filepath):
    """
    Abre un archivo PDF y extrae el texto de la primera página.
    """
    try:
        with pdfplumber.open(filepath) as pdf:
            if pdf.pages:
                # Solo leemos la primera página (índice 0)
                primera_pagina = pdf.pages[0]
                texto = primera_pagina.extract_text()
                if texto is None or not texto.strip():
                    if primera_pagina.chars:
                        print(f"Debug: Se encontraron {len(primera_pagina.chars)} caracteres pero no se pudo extraer texto legible.")
                    else:
                        print("Debug: No se encontraron caracteres (es posible que sea una imagen/escaneado).")
                return texto
            print("Debug: El PDF no tiene páginas.")
            return None
    except Exception as e:
        print(f"Debug: Error al abrir el PDF: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(f"Procesando: {sys.argv[1]}")
        texto = extract_text(sys.argv[1])
        if texto is not None:
            if texto.strip():
                print("Texto extraído exitosamente:")
                print(texto)
            else:
                print("El PDF se abrió pero no se encontró texto (está vacío o es una imagen).")
        else:
            print("No se pudo extraer texto del archivo (error al abrir).")
    else:
        print("Uso: python extractor.py <ruta_del_pdf>")
