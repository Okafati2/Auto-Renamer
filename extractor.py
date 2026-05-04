import pytesseract
from pdf2image import convert_from_path
import config
import re

def extract_text(filepath):
    """
    Convierte la primera página de un PDF a imagen y extrae el texto usando OCR (Tesseract).
    """
    try:
        # Configurar la ruta del ejecutable de Tesseract
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
        
        # Convertir solo la primera página del PDF a imagen
        # Se usa un DPI alto (300) para mejorar la precisión del OCR
        images = convert_from_path(
            filepath,
            first_page=1,
            last_page=1,
            dpi=300,
            poppler_path=config.POPPLER_PATH
        )
        
        if not images:
            print(f"Error: No se pudo convertir el archivo {filepath} a imagen.")
            return None
            
        # Realizar OCR sobre la primera imagen (página 1)
        # lang="spa" para español, psm 6 para bloques de texto uniformes
        text = pytesseract.image_to_string(
            images[0],
            lang="spa",
            config="--psm 6"
        )
        
        return text
        
    except Exception as e:
        print(f"Error al extraer texto: {str(e)}")
        return None

def extract_invoice_number(text):
    """
    Extrae el número de factura y devuelve los últimos 4 dígitos.
    """
    match = re.search(r'(?:Número de factura|Factura):\s*([\d-]+)', text, re.IGNORECASE)
    if match:
        number = match.group(1).replace('-', '')
        return number[-4:]
    return None

def extract_date(text):
    """
    Extrae la fecha de emisión en formato DD-MM-YYYY, soportando varios formatos.
    """
    MESES = {
        'enero': '01', 'febrero': '02', 'marzo': '03',
        'abril': '04', 'mayo': '05', 'junio': '06',
        'julio': '07', 'agosto': '08', 'septiembre': '09',
        'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }
    # Formato 1: "25 de abril de 2026"
    match = re.search(
        r'Fecha\s*de\s*emisi[oó]n:\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
        text, re.IGNORECASE
    )
    if match:
        day = match.group(1).zfill(2)
        month = MESES.get(match.group(2).lower())
        year = match.group(3)
        if month:
            return f"{day}-{month}-{year}"

    # Formato 2: "02-01-2025"
    match = re.search(
        r'Fecha\s*Emisi[oó]n:\s*(\d{2}-\d{2}-\d{4})',
        text, re.IGNORECASE
    )
    if match:
        return match.group(1)

    # Formato 3: Fallback "Fecha de impresión: 28 de abril de 2026"
    match = re.search(
        r'Fecha\s*de\s*impresi[oó]n:\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
        text, re.IGNORECASE
    )
    if match:
        day = match.group(1).zfill(2)
        month = MESES.get(match.group(2).lower())
        year = match.group(3)
        if month:
            return f"{day}-{month}-{year}"

    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        texto = extract_text(sys.argv[1])
        if texto:
            print("Texto extraído exitosamente:")
            print(texto)
            numero = extract_invoice_number(texto)
            fecha = extract_date(texto)
            print(f"\nNúmero de factura (últimos 4 dígitos): {numero}")
            print(f"Fecha de emisión: {fecha}")
            if numero and fecha:
                print(f"\nNombre de archivo resultante: F-{numero}_{fecha}.pdf")
            else:
                print("\nNo se pudieron extraer todos los campos.")
        else:
            print("No se pudo extraer texto del archivo.")
    else:
        print("Uso: python extractor.py <ruta_del_pdf>")
