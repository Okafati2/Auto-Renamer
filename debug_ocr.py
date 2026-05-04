import os
import sys
from extractor import extract_text

def select_file():
    """
    Permite al usuario seleccionar un archivo PDF interactivamente.
    """
    path = input("Introduce la ruta de un archivo PDF o una carpeta: ").strip('"')
    
    if not os.path.exists(path):
        print(f"Error: La ruta no existe: {path}")
        return None
        
    if os.path.isfile(path):
        return path
        
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
        if not files:
            print("No se encontraron archivos PDF en esa carpeta.")
            return None
            
        print("\nArchivos PDF encontrados:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
            
        try:
            seleccion = int(input("\nSelecciona el número del archivo: "))
            if 1 <= seleccion <= len(files):
                return os.path.join(path, files[seleccion-1])
            else:
                print("Selección no válida.")
        except ValueError:
            print("Entrada no válida. Debes introducir un número.")
            
    return None

if __name__ == "__main__":
    filepath = None
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = select_file()
        
    if filepath:
        print(f"\nProcesando: {filepath}\n")
        texto = extract_text(filepath)
        if texto:
            print("=" * 50)
            print("TEXTO BRUTO EXTRAÍDO POR OCR:")
            print("=" * 50)
            print(texto)
            print("=" * 50)
        else:
            print("No se pudo extraer texto.")
