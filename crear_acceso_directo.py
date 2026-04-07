import os
import sys
from PIL import Image
import win32com.client

def create_shortcut():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    jpeg_path = os.path.join(base_dir, "Ado _ Chando fanart♡.jpeg")
    ico_path = os.path.join(base_dir, "Ado.ico")
    bat_path = os.path.join(base_dir, "Voice YT Music.bat")
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop, "Voice YT Music.lnk")
    
    # 1. Convertir JPEG a ICO si no existe
    if not os.path.exists(ico_path):
        if os.path.exists(jpeg_path):
            img = Image.open(jpeg_path)
            img.save(ico_path, format="ICO", sizes=[(256, 256)])
        else:
            print("No se encontro la imagen.")
            
    # 2. Crear Acceso Directo usando Win32
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = shell.SpecialFolders("Desktop")
        shortcut_path = os.path.join(desktop, "Voice YT Music.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Ejecutar silenciosamente usando pythonw en lugar de .bat
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_path):
            pythonw_path = sys.executable # En caso muy raro de no existir
            
        shortcut.Targetpath = pythonw_path
        shortcut.Arguments = f'"{os.path.join(base_dir, "main.py")}"'
        shortcut.WorkingDirectory = base_dir
        if os.path.exists(ico_path):
            shortcut.IconLocation = ico_path
        shortcut.save()
        print("¡Acceso directo creado con éxito en tu ESCRITORIO!")
    except Exception as e:
        print("Error creando shortcut:", e)

if __name__ == "__main__":
    create_shortcut()
