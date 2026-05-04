import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from renamer import rename_invoice

class InvoiceHandler(FileSystemEventHandler):
    """
    Manejador de eventos para detectar nuevos archivos PDF.
    """
    def on_created(self, event):
        # Ignorar carpetas y archivos que no sean PDF
        if not event.is_directory and event.src_path.lower().endswith(".pdf"):
            self.process_new_file(event.src_path)

    def process_new_file(self, filepath):
        filename = os.path.basename(filepath)
        print(f"\n[Monitor] Nuevo archivo detectado: {filename}")
        
        # Estabilización del archivo (esperar a que termine de escribirse)
        if self.wait_for_file_stability(filepath):
            # Procesar el archivo usando la lógica de renombrado existente
            rename_invoice(filepath)
        else:
            print(f"Omitido (tiempo de espera agotado): {filename}")

    def wait_for_file_stability(self, filepath, timeout=120):
        """
        Verifica que el archivo haya terminado de escribirse comparando su tamaño.
        """
        last_size = -1
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Verificar si el archivo aún existe
                if not os.path.exists(filepath):
                    return False
                    
                current_size = os.path.getsize(filepath)
                
                # Si el tamaño es el mismo que hace 1 segundo y es mayor a 0, está listo
                if current_size == last_size and current_size > 0:
                    return True
                
                last_size = current_size
            except OSError:
                # El archivo puede estar bloqueado por otro proceso
                pass
            
            time.sleep(1)
            
        return False

def start_watching(folder_path):
    """
    Inicia el monitoreo de la carpeta especificada.
    """
    if not os.path.exists(folder_path):
        print(f"Error: La carpeta no existe: {folder_path}")
        return

    event_handler = InvoiceHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    
    print(f"Modo monitor activado en: {folder_path}")
    print("Presiona Ctrl+C para detener...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nDeteniendo monitor...")
    
    observer.join()
    print("Monitor detenido.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        start_watching(sys.argv[1])
    else:
        print("Uso: python watcher.py <ruta_de_carpeta>")
