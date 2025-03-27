# desktop_app/main.py

import os
import sys

# Asegurarnos de que todos los submódulos de firebase_admin estén disponibles
# Esto fuerza a PyInstaller a incluirlos
def ensure_firebase_modules():
    try:
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore
        from firebase_admin import db
        from firebase_admin import storage
        from firebase_admin import messaging
        from firebase_admin import auth
        
        # Importar módulos de Google Cloud para asegurar que estén disponibles
        import google.cloud
        import google.cloud.firestore
        import google.cloud.firestore_v1
        import google.api_core.grpc_helpers
        
        print("Todos los módulos de Firebase cargados correctamente")
        return True
    except ImportError as e:
        print(f"Error importando módulos de Firebase: {e}")
        return False

# Verificar si estamos ejecutando como ejecutable o como script
if getattr(sys, 'frozen', False):
    # Si estamos en un ejecutable
    # Añadir el directorio donde se encuentra el ejecutable al path
    bundle_dir = os.path.dirname(sys.executable)
    sys.path.append(bundle_dir)
    # También podemos configurar dónde buscar el archivo de firebase
    os.environ['FIREBASE_CONFIG'] = os.path.join(bundle_dir, 'serviceAccountKey.json')
    
    # Verificar que el archivo de credenciales existe
    if not os.path.exists(os.environ['FIREBASE_CONFIG']):
        print(f"ADVERTENCIA: No se encontró el archivo de credenciales en {os.environ['FIREBASE_CONFIG']}")
else:
    # Si estamos en desarrollo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    os.environ['FIREBASE_CONFIG'] = os.path.join(parent_dir, 'serviceAccountKey.json')

try:
    # Verificar que podemos cargar los módulos de Firebase
    firebase_ok = ensure_firebase_modules()
    
    # Ahora importamos customtkinter
    import customtkinter as ctk
    
    # Configurar apariencia de CustomTkinter
    ctk.set_appearance_mode("System")  # Modos: "System" (por defecto), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Temas: "blue" (por defecto), "green", "dark-blue"
    
    # Verificar que la carpeta shared está en el path
    shared_found = False
    for path in sys.path:
        if os.path.exists(os.path.join(path, 'shared')):
            shared_found = True
            break
    
    if not shared_found and getattr(sys, 'frozen', False):
        # Si estamos en un ejecutable y no encontramos shared, intentamos añadirlo
        shared_path = os.path.join(bundle_dir, 'shared')
        if os.path.exists(shared_path):
            sys.path.append(shared_path)
            print(f"Carpeta shared añadida al path: {shared_path}")
    
    # Importar la aplicación principal después de configurar las rutas
    print("Importando app.py...")
    from app import StockControlApp
    
    if __name__ == "__main__":
        print("Iniciando aplicación...")
        app = StockControlApp()
        app.run()
except Exception as e:
    # Si hay algún error, mostrarlo y esperar entrada para no cerrar la ventana inmediatamente
    print(f"Error al iniciar la aplicación: {str(e)}")
    print(f"Path de Python: {sys.path}")
    
    # Mostrar información adicional sobre archivos y carpetas
    if getattr(sys, 'frozen', False):
        try:
            bundle_dir = os.path.dirname(sys.executable)
            print(f"\nContenido del directorio de la aplicación ({bundle_dir}):")
            for item in os.listdir(bundle_dir):
                print(f" - {item}")
                
            # Verificar si existe shared
            shared_path = os.path.join(bundle_dir, 'shared')
            if os.path.exists(shared_path):
                print(f"\nContenido de la carpeta shared:")
                for item in os.listdir(shared_path):
                    print(f" - {item}")
            else:
                print("\nLa carpeta shared no existe")
                
            # Verificar firebase_admin
            firebase_path = os.path.join(bundle_dir, 'firebase_admin')
            if os.path.exists(firebase_path):
                print(f"\nContenido de la carpeta firebase_admin:")
                for item in os.listdir(firebase_path):
                    print(f" - {item}")
        except Exception as e2:
            print(f"Error al listar directorios: {e2}")
            
    input("Presiona Enter para salir...")