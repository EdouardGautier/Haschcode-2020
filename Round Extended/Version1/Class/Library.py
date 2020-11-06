class Library ():

    def __init__(self, listeLivre, jourSingUp, empruntJour, rang, nbLivre):
        self.listeLivre = listeLivre
        self.jourSingUp = jourSingUp
        self.empruntJour = empruntJour
        self.id = rang
        self.nbLivre = nbLivre
        self.score = 0

        self.trieLivre()
        self.calculScore(self.nbLivre)

    def trieLivre(self):
        self.listeLivre.sort(key=lambda p: p.getScore(), reverse=True)

    def calculRatio(self, jourRestant):
        if self.jourSingUp < jourRestant:
            depasseDelay = False
            self.calculLivreLibre()
            jourRestant -= self.jourSingUp

            if self.nbLivre / self.empruntJour >= jourRestant:
                self.calculScore(self.empruntJour * jourRestant)
                depasseDelay = True
            else:
                self.calculScore(self.nbLivre)
            return self.score / self.jourSingUp, depasseDelay
        else:
            return 0, True

    def calculLivreLibre(self):
        self.majListeLivre()
        self.nbLivre = len(self.listeLivre)

    def calculScore(self, nbLivre):
        self.score = 0
        for k in self.listeLivre[:nbLivre]:
            self.score += k.getScore()

    def majListeLivre(self):
        for k in self.listeLivre:
            if not k.estDispo():
                self.listeLivre.remove(k)
                return self.majListeLivre()

    def listeLivreEmprunt(self, limiteTemps=0):
        if limiteTemps <= 0:
            return self.listeLivre[:]
        else:
            return self.listeLivre[:(self.empruntJour * limiteTemps)]

    def getId(self):
        return self.id

    def getDelay(self):
        return self.jourSingUp

    def getListeLivre(self):
        return self.listeLivre

    def getNbLivre(self):
        return len(self.listeLivre)

    def getScore(self):
        return self.score

    def getEmpruntJour(self):
        return self.empruntJour
