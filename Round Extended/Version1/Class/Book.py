class Book ():
    def __init__(self, rang, score):
        self.score = score
        self.rang = rang
        self.emprunter = False

    def __str__(self):
        return str(self.rang)

    def __eq__(self, other):
        return self.rang == other.getRang()

    def getScore(self):
        return self.score

    def estDispo(self):
        return not self.emprunter

    def getRang(self):
        return self.rang

    def empruntLivre(self):
        if not self.emprunter:
            self.emprunter = True
        else:
            print("########Error#######")
