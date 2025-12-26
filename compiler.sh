set -e

if command -v python3 >/dev/null; then
    python3 -m pip install --upgrade pip

    python3 -m pip install pyinstaller

    python3 -m pip install -r requirements.txt

    pyinstaller --onefile --hidden-import=PIL._tkinter_finder --add-data "icon.png:." --name MaVMPlayer main.py
else
    echo "install python3"
fi
