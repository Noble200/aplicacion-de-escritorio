# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import customtkinter
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Rutas del proyecto - Ajusta estas rutas según tu sistema
MAIN_PY_PATH = r'C:\Users\Ruso\Desktop\Aplicacion de Mercedes\desktop_app\main.py'
PROJECT_ROOT = r'C:\Users\Ruso\Desktop\Aplicacion de Mercedes'
CRED_FILE = r'C:\Users\Ruso\Desktop\Aplicacion de Mercedes\serviceAccountKey.json'
SHARED_DIR = r'C:\Users\Ruso\Desktop\Aplicacion de Mercedes\shared'

# Obtener la ruta de customtkinter para añadirla como dato
customtkinter_path = os.path.dirname(customtkinter.__file__)

# Recolectar dependencias
datas = [(customtkinter_path, "customtkinter/")]
binaries = []
hiddenimports = ["customtkinter", "PIL", "PIL._tkinter_finder"]

# Añadir todos los submódulos de customtkinter
hiddenimports.extend(collect_submodules('customtkinter'))

# Añadir firebase_admin y submódulos
hiddenimports.extend(collect_submodules('firebase_admin'))

# Añadir archivos del proyecto
if os.path.exists(CRED_FILE):
    datas.append((CRED_FILE, '.'))
else:
    print(f"ADVERTENCIA: No se encontró el archivo {CRED_FILE}")

# Añadir carpeta shared
if os.path.exists(SHARED_DIR):
    datas.append((SHARED_DIR, 'shared'))
else:
    print(f"ADVERTENCIA: No se encontró la carpeta {SHARED_DIR}")

# Configurar el análisis
a = Analysis(
    [MAIN_PY_PATH],
    pathex=[PROJECT_ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Empaquetar
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Crear el ejecutable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ControlStock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Cambiado a True para ver errores durante el desarrollo
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Crear la colección final
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ControlStock',
)