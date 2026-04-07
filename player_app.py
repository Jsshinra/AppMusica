import webview
import time
import threading
import os
import sys

URL_FILE = "current_url.txt"
CMD_FILE = "player_cmd.txt"

def run_player():
    window = webview.create_window(
        'Voice YT Music Player', 
        'https://music.youtube.com', 
        width=1280, 
        height=720, 
        background_color='#030303' # YT Music Dark background
    )
    
    def check_files():
        last_url = ""
        while True:
            try:
                # Revisar si hay un comando de URL nuevo
                if os.path.exists(URL_FILE):
                    with open(URL_FILE, "r") as f:
                        url = f.read().strip()
                    if url and url != last_url:
                        # Anular la alerta de salida antes de cambiar la URL
                        try:
                            window.evaluate_js('window.onbeforeunload = null;')
                        except Exception:
                            pass
                            
                        window.load_url(url)
                        last_url = url
                        # Mostrar la ventana al reproducir algo nuevo
                        window.restore()
                        window.show()
                        
                # Revisar comandos explicitos de show
                if os.path.exists(CMD_FILE):
                    with open(CMD_FILE, "r") as f:
                        cmd = f.read().strip()
                    if cmd == "SHOW":
                        window.restore()
                        window.show()
                    os.remove(CMD_FILE)
            except Exception:
                pass
            time.sleep(0.5)
            
    threading.Thread(target=check_files, daemon=True).start()
    webview.start()

if __name__ == '__main__':
    run_player()
