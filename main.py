import os
import sys
import tkinter as tk
from tkinter import filedialog
from renamer import rename_invoice
from watcher import start_watching

# Inicializar tkinter y ocultar la ventana principal
root = tk.Tk()
root.withdraw()

def process_folder(folder_path):
    """
    Escanea una carpeta en busca de archivos PDF y los procesa uno por uno.
    """
    # 1. Validar la carpeta
    if not os.path.exists(folder_path):
        print(f"Error: La carpeta no existe: {folder_path}")
        return

    # 2. Buscar todos los archivos PDF (insensible a mayúsculas/minúsculas)
    all_files = os.listdir(folder_path)
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)

    if total_files == 0:
        print("No se encontraron archivos PDF en la carpeta.")
        return

    print(f"Se encontraron {total_files} archivo(s) PDF. Iniciando procesamiento...")

    # 3. Procesar cada PDF
    renombrados = 0
    omitidos = 0

    for i, filename in enumerate(pdf_files, 1):
        filepath = os.path.join(folder_path, filename)
        
        # Llamar a la lógica de renombrado
        resultado = rename_invoice(filepath)
        
        if resultado:
            renombrados += 1
        else:
            omitidos += 1
            
        print(f"[{i}/{total_files}] Procesado: {filename}")

    # 4. Resumen final
    print("─────────────────────────────────")
    print("Proceso completado.")
    print(f"✓ Renombrados: {renombrados}")
    print(f"✗ Omitidos: {omitidos}")
    print("─────────────────────────────────")

def main_menu():
    """
    Muestra el menú principal interactivo.
    """
    while True:
        print("\n" + "="*30)
        print("  AUTO-RENAMER DE FACTURAS")
        print("="*30)
        print("1. Procesar carpeta completa")
        print("2. Procesar archivo(s) seleccionado(s)")
        print("3. Modo vigilancia (automático)")
        print("4. Salir")
        print("="*30)
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            folder = filedialog.askdirectory(title="Selecciona la carpeta a procesar")
            if folder:
                process_folder(folder)
            else:
                print("No se seleccionó ninguna carpeta. Operación cancelada.")
                
        elif opcion == "2":
            file_paths = filedialog.askopenfilenames(
                title="Selecciona factura(s) PDF",
                filetypes=[("Archivos PDF", "*.pdf")]
            )
            if file_paths:
                total_files = len(file_paths)
                print(f"Se seleccionaron {total_files} archivo(s). Iniciando procesamiento...")
                renombrados = 0
                omitidos = 0
                
                for i, file_path in enumerate(file_paths, 1):
                    filename = os.path.basename(file_path)
                    resultado = rename_invoice(file_path)
                    if resultado:
                        renombrados += 1
                    else:
                        omitidos += 1
                    print(f"[{i}/{total_files}] Procesado: {filename}")
                
                print("─────────────────────────────────")
                print("Proceso completado.")
                print(f"✓ Renombrados: {renombrados}")
                print(f"✗ Omitidos: {omitidos}")
                print("─────────────────────────────────")
            else:
                print("No se seleccionó ningún archivo. Operación cancelada.")
                
        elif opcion == "3":
            folder = filedialog.askdirectory(title="Selecciona la carpeta a monitorear")
            if folder:
                start_watching(folder)
            else:
                print("No se seleccionó ninguna carpeta. Operación cancelada.")
                
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Si se pasa un argumento, procesar esa carpeta directamente
        process_folder(sys.argv[1])
    else:
        # De lo contrario, mostrar el menú interactivo
        main_menu()
