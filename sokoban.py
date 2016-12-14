import tkinter as tk

class Sokoban:
    def __init__(self):

        # Definirajmo velikost igralca
        self.velikost = 25
        self.igralec = [0, 0, self.velikost, self.velikost]
        # Pripravimo si sezname zidov in ostalih objektov
        self.zid = []
        self.kocke = []
        self.cilj = []

        # Naredimo prazno okno
        self.okno = tk.Tk()
        # Na oknu naredimo platno
        self.platno = tk.Canvas(self.okno, width=300, height=200)
        # Na platno narišemo krog
        self.krog = self.platno.create_oval(self.igralec, fill="red")
        self.platno.pack()

        # Pvemo katera funkcija naj se kliče, ko pritiksamo tipke
        self.platno.focus_set()
        self.platno.bind("<w>", self.tipka)
        self.platno.bind("<a>", self.tipka)
        self.platno.bind("<s>", self.tipka)
        self.platno.bind("<d>", self.tipka)

    def tipka(self, event):
        # Premaknimo igralca, ko pritisne kakšen znak
        znak = event.char
        print("Pritisnil si", znak)
        if znak == "w":
            self.igralec[1] -= self.velikost
            self.igralec[3] -= self.velikost
        if znak == "a":
            self.igralec[0] -= self.velikost
            self.igralec[2] -= self.velikost
        if znak == "s":
            self.igralec[1] += self.velikost
            self.igralec[3] += self.velikost
        if znak == "d":
            self.igralec[0] += self.velikost
            self.igralec[2] += self.velikost
        self.platno.coords(self.krog, self.igralec)


# Naredimo novo igro
igra = Sokoban()

# Zaženemo igro
igra.okno.mainloop()
