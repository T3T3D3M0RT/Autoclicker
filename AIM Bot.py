import math
import random
import tkinter as tk

W, H, R = 640, 420, 22


class Jeu:
    def __init__(self, root):
        self.root = root
        root.title("Jeu de cible")
        self.canvas = tk.Canvas(root, width=W, height=H, bg="#1e1e2e",
                                highlightthickness=0)
        self.canvas.pack()
        self.label = tk.Label(root, text="")
        self.label.pack()

        self.score = 0
        self.bot = False
        self.cx, self.cy = W / 2, H / 2          # viseur du bot
        self.vitesse_bot = 8

        self.cible = self.canvas.create_oval(0, 0, 0, 0, fill="tomato", outline="")
        self.viseur_h = self.canvas.create_line(0, 0, 0, 0, fill="lime", width=2)
        self.viseur_v = self.canvas.create_line(0, 0, 0, 0, fill="lime", width=2)
        self.nouvelle_cible()

        self.canvas.bind("<Button-1>", self.clic)
        root.bind("b", self.basculer_bot)
        self.maj_label()
        self.boucle()

    def nouvelle_cible(self):
        self.tx = random.randint(R, W - R)
        self.ty = random.randint(R, H - R)
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = random.choice([-3, -2, 2, 3])

    def maj_label(self):
        mode = "BOT" if self.bot else "MANUEL"
        self.label.config(text=f"Score : {self.score}   |   Mode : {mode}   |   B = changer de mode")

    def basculer_bot(self, _event=None):
        self.bot = not self.bot
        self.maj_label()

    def tir(self, x, y):
        if math.hypot(x - self.tx, y - self.ty) <= R:
            self.score += 1
            self.nouvelle_cible()
            self.maj_label()

    def clic(self, event):
        if not self.bot:
            self.tir(event.x, event.y)

    def boucle(self):
        # déplacement de la cible avec rebond
        self.tx += self.vx
        self.ty += self.vy
        if self.tx < R or self.tx > W - R:
            self.vx = -self.vx
        if self.ty < R or self.ty > H - R:
            self.vy = -self.vy

        # le bot : repère la cible, avance le viseur vers elle, tire
        if self.bot:
            dx, dy = self.tx - self.cx, self.ty - self.cy
            d = math.hypot(dx, dy)
            if d > 1:
                pas = min(d, self.vitesse_bot)
                self.cx += dx / d * pas
                self.cy += dy / d * pas
            if d < R / 2:
                self.tir(self.cx, self.cy)

        # dessin
        self.canvas.coords(self.cible, self.tx - R, self.ty - R, self.tx + R, self.ty + R)
        if self.bot:
            self.canvas.coords(self.viseur_h, self.cx - 12, self.cy, self.cx + 12, self.cy)
            self.canvas.coords(self.viseur_v, self.cx, self.cy - 12, self.cx, self.cy + 12)
        else:
            self.canvas.coords(self.viseur_h, 0, 0, 0, 0)
            self.canvas.coords(self.viseur_v, 0, 0, 0, 0)

        self.root.after(16, self.boucle)


if __name__ == "__main__":
    root = tk.Tk()
    Jeu(root)
    root.mainloop()
