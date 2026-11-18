import ctypes
import threading
import time
import tkinter as tk
from tkinter import ttk

user32 = ctypes.windll.user32

BUTTONS = {
    "Gauche": (0x0002, 0x0004),
    "Droit": (0x0008, 0x0010),
    "Milieu": (0x0020, 0x0040),
}
VK_F6 = 0x75


class AutoClicker:
    def __init__(self, root):
        self.root = root
        root.title("Autocliqueur")
        root.geometry("300x230")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        self.running = threading.Event()
        self.f6_was_down = False

        frm = ttk.Frame(root, padding=15)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Intervalle (millisecondes) :").pack(anchor="w")
        self.interval = tk.StringVar(value="100")
        ttk.Entry(frm, textvariable=self.interval).pack(fill="x", pady=(0, 10))

        ttk.Label(frm, text="Bouton :").pack(anchor="w")
        self.button = tk.StringVar(value="Gauche")
        ttk.Combobox(frm, textvariable=self.button, values=list(BUTTONS),
                     state="readonly").pack(fill="x", pady=(0, 10))

        self.toggle_btn = ttk.Button(frm, text="Démarrer (F6)", command=self.toggle)
        self.toggle_btn.pack(fill="x", pady=5)

        self.status = ttk.Label(frm, text="Arrêté")
        self.status.pack()

        threading.Thread(target=self.click_loop, daemon=True).start()
        self.poll_hotkey()

    def get_interval(self):
        try:
            return max(1, int(self.interval.get())) / 1000
        except ValueError:
            return 0.1

    def toggle(self):
        if self.running.is_set():
            self.running.clear()
            self.toggle_btn.config(text="Démarrer (F6)")
            self.status.config(text="Arrêté")
        else:
            self.running.set()
            self.toggle_btn.config(text="Arrêter (F6)")
            self.status.config(text="En cours...")

    def click_loop(self):
        while True:
            if self.running.is_set():
                down, up = BUTTONS.get(self.button.get(), BUTTONS["Gauche"])
                user32.mouse_event(down, 0, 0, 0, 0)
                user32.mouse_event(up, 0, 0, 0, 0)
                time.sleep(self.get_interval())
            else:
                time.sleep(0.05)

    def poll_hotkey(self):
        down = bool(user32.GetAsyncKeyState(VK_F6) & 0x8000)
        if down and not self.f6_was_down:
            self.toggle()
        self.f6_was_down = down
        self.root.after(30, self.poll_hotkey)


if __name__ == "__main__":
    root = tk.Tk()
    AutoClicker(root)
    root.mainloop()
