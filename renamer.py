import os
import shutil
from extractor import extract_text, extract_invoice_number, extract_date

def rename_invoice(filepath):
    """
    Extrae datos de la factura, genera un nuevo nombre y renombre el archivo de forma segura.
    """
    filename = os.path.basename(filepath)
    directory = os.path.dirname(filepath)
    
    try:
        # 1. Extraer campos
        text = extract_text(filepath)
        if not text:
            print(f"Omitido (no se pudieron extraer los campos): {filename}")
            return None
            
        numero = extract_invoice_number(text)
        fecha = extract_date(text)
        
        if not numero or not fecha:
            print(f"Omitido (no se pudieron extraer los campos): {filename}")
            return None
            
        # 2. Construir el nuevo nombre base
        base_name = f"F-{numero}_{fecha}"
        new_filename = f"{base_name}.pdf"
        new_filepath = os.path.join(directory, new_filename)
        
        # 3. Manejar duplicados
        counter = 2
        while os.path.exists(new_filepath):
            new_filename = f"{base_name}_{counter}.pdf"
            new_filepath = os.path.join(directory, new_filename)
            counter += 1
            
        # 4. Renombrar y eliminar el original (Copia segura)
        # Se usa shutil.copy2 + os.remove para manejar diferentes unidades/volúmenes
        shutil.copy2(filepath, new_filepath)
        
        # Verificar que la copia existe y tiene el mismo tamaño
        if os.path.exists(new_filepath) and os.path.getsize(new_filepath) == os.path.getsize(filepath):
            os.remove(filepath)
            print(f"Renombrado: {filename} → {new_filename}")
            return new_filepath
        else:
            print(f"Error al renombrar {filename}: La copia no coincide con el original.")
            if os.path.exists(new_filepath):
                os.remove(new_filepath) # Limpiar copia fallida
            return None
            
    except Exception as e:
        print(f"Error al renombrar {filename}: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resultado = rename_invoice(sys.argv[1])
        if resultado:
            print(f"Archivo final: {resultado}")
    else:
        print("Uso: python renamer.py <ruta_del_pdf>")
