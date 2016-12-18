import tkinter as tk

class Sokoban:
    def __init__(self):
        """ Inicializacijska funkcija, ki nastavi osnovne objekte igre """

        # Definirajmo velikost igralca
        self.velikost = 25
        self.igralec = [1, 1]
        # Pripravimo si sezname zidov in ostalih objektov
        self.zid = []
        self.kocke = []
        self.cilj = []

        # Naredimo prazno okno
        self.okno = tk.Tk()
        self.okno.title("Sokoban")
        # Na oknu naredimo platno
        self.platno = tk.Canvas(self.okno, width=300, height=300)
        self.platno.pack()

        # Pvemo katera funkcija naj se kliče, ko pritiksamo tipke
        self.platno.focus_set()
        self.platno.bind("<w>", self.tipka)
        self.platno.bind("<a>", self.tipka)
        self.platno.bind("<s>", self.tipka)
        self.platno.bind("<d>", self.tipka)

    def pretvori(self, x, y):
        """ Pretvorimo koordinate iz mreže v piksle
        npr. 1, 2 -> 25, 50, 50, 75 """

        return [x * self.velikost, y * self.velikost,
                (x + 1) * self.velikost, (y + 1) * self.velikost]

    def tipka(self, event):
        """ Funkcija, ki skrbi pravilno delovanje tipk """
        # Najprej preverimo ali si končal prejšnji level
        zmaga = True
        for kocka in self.kocke:
            # Vse kocke morajo biti na cilju
            if kocka not in self.cilj:
                zmaga = False
                break
        # Če smo zmagali, preberimo drugi level in ga narišemo
        if zmaga:
            self.preberi_level("lvl2.txt")
            self.narisi_level()
            # Potem ignoriramo pritisk tipke
            return

        # Zapomnimo si uporabnikov položaj pred premikom
        prejx, prejy = self.igralec
        # Premaknimo igralca, ko pritisne kakšen znak
        znak = event.char
        if znak == "w":
            self.igralec[1] -= 1
        if znak == "a":
            self.igralec[0] -= 1
        if znak == "s":
            self.igralec[1] += 1
        if znak == "d":
            self.igralec[0] += 1

        # Poglejmo ali je igralec pristal zidu. Potem da postavimo na njegovo
        # prejšnje mesto
        if tuple(self.igralec) in self.zid:
            self.igralec = [prejx, prejy]

        # Ali je uporabnik zadel kocko? Če ja, jo premaknimo
        if tuple(self.igralec) in self.kocke:
            x, y = self.igralec
            novx, novy = x+x-prejx, y+y-prejy
            if (novx, novy) in self.zid or (novx, novy) in self.kocke:
                self.igralec = [prejx, prejy]
            else:
                st_kocke = self.kocke.index((x, y))
                del self.kocke[st_kocke]
                self.kocke.append((novx, novy))

        # Ko smo vse popravili ponovno narišimo level
        self.narisi_level()

    def preberi_level(self, ime_dat):
        """ Iz datoteke `ime_dat` preberemo zemljevid levla in ga shranimo """

        # Pobrišimo star level pred branjem novega
        self.zid = []
        self.kocke = []
        self.cilj = []

        # Odprimo datoteko
        lvl = open(ime_dat, "r")
        # Preberemo vse vrstice
        vrstice = lvl.readlines()

        for i in range(len(vrstice)):
            for j in range(len(vrstice[i])):
                # Poglejmo vsak znak in si shranimo njegov pomen
                if vrstice[i][j] == "#":
                    self.zid.append((j, i))
                elif vrstice[i][j] == "o":
                    self.kocke.append((j, i))
                elif vrstice[i][j] == "x":
                    self.cilj.append((j, i))
                elif vrstice[i][j] == "p":
                    self.igralec = [j, i]

    def narisi_level(self):
        """ Funkcija pobriše prejšnjo sliko in nariše novo """

        # Najprej izbrišimo vse kar je bilo prej na platnu
        self.platno.delete("all")

        # Nariši vse dele zidu
        for x, y in self.zid:
            self.platno.create_rectangle(self.pretvori(x, y), fill="#882211")
        # Nariši vse cilje
        for x, y in self.cilj:
            self.platno.create_oval(self.pretvori(x, y), fill="yellow")
        # Nariši kocke
        for x, y in self.kocke:
            # Naj bo ďrugačne barve, če je na cilju
            if (x, y) in self.cilj:
                self.platno.create_rectangle(self.pretvori(x, y), fill="pink")
            else:
                self.platno.create_rectangle(self.pretvori(x, y), fill="white")

        # Na platno narišemo igralca
        self.platno.create_oval(self.pretvori(*self.igralec), fill="red")


# Naredimo novo igro
igra = Sokoban()
igra.preberi_level("lvl1.txt")
igra.narisi_level()

# Zaženemo igro
igra.okno.mainloop()
