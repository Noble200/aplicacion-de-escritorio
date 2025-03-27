# desktop_app/build.py
"""
Script para generar un ejecutable de la aplicación de control de stock.
Asegúrate de tener instalado PyInstaller antes de ejecutar este script.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_executable():
    """Crea un ejecutable de la aplicación usando PyInstaller"""
    
    # Obtener la ruta base del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Verificar si existe el archivo de credenciales de Firebase
    cred_file = os.path.join(project_root, 'serviceAccountKey.json')
    if not os.path.exists(cred_file):
        print("⚠️ Advertencia: No se encontró el archivo serviceAccountKey.json")
        print("   El ejecutable no funcionará sin las credenciales de Firebase.")
        input("   Presiona Enter para continuar de todos modos...")
    
    # Crear el directorio de compilación si no existe
    build_dir = os.path.join(script_dir, 'build')
    os.makedirs(build_dir, exist_ok=True)
    
    # Opciones de PyInstaller
    pyinstaller_options = [
        'pyinstaller',
        '--name=ControlStock',
        '--windowed',  # Sin consola en Windows
        '--onedir',    # Crear un directorio con los archivos
        f'--distpath={os.path.join(script_dir, "dist")}',
        f'--workpath={build_dir}',
        f'--specpath={script_dir}',
        '--clean',     # Limpiar caché
        '--noconfirm', # No confirmar sobreescritura
        '--add-data', f'{cred_file}{os.pathsep}.',  # Incluir credenciales
        '--hidden-import=customtkinter',  # Incluir customtkinter explícitamente
        '--collect-all=customtkinter',    # Recolectar todos los archivos de customtkinter
        '--hidden-import=PIL',            # Incluir Pillow (requerido por customtkinter)
        '--collect-all=PIL',              # Recolectar todos los archivos de Pillow
        os.path.join(script_dir, 'main.py')
    ]
    
    # Ejecutar PyInstaller
    print("🔨 Generando ejecutable...")
    subprocess.run(pyinstaller_options)
    
    # Copiar módulos compartidos
    print("📂 Copiando módulos compartidos...")
    shared_dir = os.path.join(project_root, 'shared')
    dist_shared_dir = os.path.join(script_dir, 'dist', 'ControlStock', 'shared')
    
    # Crear el directorio shared en el destino si no existe
    os.makedirs(dist_shared_dir, exist_ok=True)
    
    # Copiar todos los archivos .py de la carpeta shared
    for file in os.listdir(shared_dir):
        if file.endswith('.py'):
            src_file = os.path.join(shared_dir, file)
            dst_file = os.path.join(dist_shared_dir, file)
            shutil.copy2(src_file, dst_file)
    
    # Crear un archivo __init__.py vacío si no existe
    init_file = os.path.join(dist_shared_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Paquete shared\n')
    
    # Verificar si la compilación fue exitosa
    dist_dir = os.path.join(script_dir, 'dist', 'ControlStock')
    if os.path.exists(dist_dir):
        print("✅ ¡Ejecutable generado con éxito!")
        print(f"📂 La aplicación está en: {dist_dir}")
        print("🔥 Asegúrate de que serviceAccountKey.json esté presente para la conexión con Firebase.")
    else:
        print("❌ Error al generar el ejecutable.")

if __name__ == "__main__":
    create_executable()