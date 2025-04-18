import threading

def thread(target):
    threading.Thread(target=target, daemon=True).start()