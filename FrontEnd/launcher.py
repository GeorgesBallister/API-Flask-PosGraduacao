# launcher.py
import threading
import time
import sys
import traceback
import requests

def iniciar_api():
    """
    Sobe o Flask SEM reloader em uma thread daemon, na 127.0.0.1:5000.
    O Index.py já expõe 'app', então é só importar e rodar.
    """
    from Index import app  # usa seu arquivo existente (exporta 'app'). :contentReference[oaicite:2]{index=2}
    # Importante: sem reloader para não criar processo filho
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def esperar_api(url_health="http://127.0.0.1:5000/users/all", timeout_total=15.0):
    """
    Faz polling até a API responder (ou até estourar timeout_total).
    """
    inicio = time.time()
    while time.time() - inicio < timeout_total:
        try:
            r = requests.get(url_health, timeout=1.5)
            # Qualquer 2xx/404 já indica que o servidor está de pé
            if 200 <= r.status_code < 500:
                return True
        except Exception:
            time.sleep(0.3)
    return False

def iniciar_gui():
    """
    Importa e sobe sua GUI Tkinter. Ela consumirá a API já de pé.
    """
    # O arquivo gui_cliente_mba.py já está OK e usa API_BASE = http://127.0.0.1:5000. :contentReference[oaicite:3]{index=3}
    from gui_cliente_mba import App
    app = App()
    app.mainloop()

if __name__ == "__main__":
    # 1) Sobe a API em background
    th = threading.Thread(target=iniciar_api, daemon=True)
    th.start()

    # 2) Espera a API responder antes de abrir a GUI (melhora UX)
    if not esperar_api():
        print("Não consegui iniciar a API em tempo hábil.", file=sys.stderr)
        sys.exit(1)

    try:
        # 3) Inicia a GUI
        iniciar_gui()
    except Exception:
        traceback.print_exc()
        sys.exit(2)
    # Ao fechar a GUI, o processo principal encerra; a thread daemon da API morre junto.
