@echo off
echo ==============================================
echo Creando ejecutable con entorno virtual
echo ==============================================

:: Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

:: Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

:: Instalar dependencias
echo Instalando dependencias...
pip install -q customtkinter pillow firebase-admin pyinstaller

:: Crear spec file
echo Creando archivo spec temporal...
echo # -*- mode: python -*- > temp_spec.spec
echo block_cipher = None >> temp_spec.spec
echo a = Analysis(['desktop_app/main.py'], >> temp_spec.spec
echo     pathex=['%CD%'], >> temp_spec.spec
echo     binaries=[], >> temp_spec.spec
echo     datas=[('serviceAccountKey.json', '.'), ('shared', 'shared')], >> temp_spec.spec
echo     hiddenimports=['customtkinter', 'PIL', 'firebase_admin'], >> temp_spec.spec
echo     hookspath=[], >> temp_spec.spec
echo     hooksconfig={}, >> temp_spec.spec
echo     runtime_hooks=[], >> temp_spec.spec
echo     excludes=[], >> temp_spec.spec
echo     win_no_prefer_redirects=False, >> temp_spec.spec
echo     win_private_assemblies=False, >> temp_spec.spec
echo     cipher=block_cipher, >> temp_spec.spec
echo     noarchive=False, >> temp_spec.spec
echo ) >> temp_spec.spec
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher) >> temp_spec.spec
echo exe = EXE(pyz, >> temp_spec.spec
echo     a.scripts, >> temp_spec.spec
echo     [], >> temp_spec.spec
echo     exclude_binaries=True, >> temp_spec.spec
echo     name='ControlStock', >> temp_spec.spec
echo     debug=False, >> temp_spec.spec
echo     bootloader_ignore_signals=False, >> temp_spec.spec
echo     strip=False, >> temp_spec.spec
echo     upx=True, >> temp_spec.spec
echo     console=True, >> temp_spec.spec
echo     disable_windowed_traceback=False, >> temp_spec.spec
echo     argv_emulation=False, >> temp_spec.spec
echo     target_arch=None, >> temp_spec.spec
echo     codesign_identity=None, >> temp_spec.spec
echo     entitlements_file=None, >> temp_spec.spec
echo ) >> temp_spec.spec
echo coll = COLLECT(exe, >> temp_spec.spec
echo     a.binaries, >> temp_spec.spec
echo     a.zipfiles, >> temp_spec.spec
echo     a.datas, >> temp_spec.spec
echo     strip=False, >> temp_spec.spec
echo     upx=True, >> temp_spec.spec
echo     upx_exclude=[], >> temp_spec.spec
echo     name='ControlStock', >> temp_spec.spec
echo ) >> temp_spec.spec

:: Limpiar carpetas previas
echo Limpiando compilaciones anteriores...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"

:: Ejecutar PyInstaller
echo Ejecutando PyInstaller...
pyinstaller --clean temp_spec.spec

:: Verificar resultado
if exist "dist\ControlStock\ControlStock.exe" (
    echo ==============================================
    echo Ejecutable creado exitosamente!
    echo Ubicado en: dist\ControlStock\ControlStock.exe
    echo ==============================================
) else (
    echo ERROR: No se pudo crear el ejecutable!
)

:: Limpiar archivo spec temporal
del temp_spec.spec

:: Desactivar entorno virtual
deactivate

echo.
echo Presiona cualquier tecla para salir...
pause >nul