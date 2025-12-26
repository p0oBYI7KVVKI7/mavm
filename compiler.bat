@echo off

where python >nul 2>nul
if %errorlevel%==0 (
    python -m pip install --upgrade pip

    python -m pip install pyinstaller

    python -m pip install -r requirements.txt

    python -m PyInstaller --onefile --hidden-import=PIL._tkinter_finder --windowed --add-data "icon.png;." --name MaVMPlayer main.py
) else (
    echo install python3
)
