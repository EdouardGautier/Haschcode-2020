import time as time
import locale

ma_locale = locale.setlocale(locale.LC_ALL, "")

fichier_1 = "Haschcode 2020\Input\\a_example.txt"
fichier_2 = "Haschcode 2020\Input\\b_read_on.txt"
fichier_3 = "Haschcode 2020\Input\c_incunabula.txt"
fichier_4 = "Haschcode 2020\Input\d_tough_choices.txt"
fichier_5 = "Haschcode 2020\Input\e_so_many_books.txt"
fichier_6 = "Haschcode 2020\Input\\f_libraries_of_the_world.txt"

liste_fichier = [fichier_1, fichier_2,
                 fichier_3, fichier_4, fichier_5, fichier_6]


class Read():

    def __init__(self, fichier):
        self.fichier = fichier
        self.nbDays = int()
        self.listLibrairie = list()
        self.lecture()

    def lecture(self):
        global listBook
        listBook = list()
        listScore = list()
        f = open(self.fichier, encoding='utf8')
        ligne = f.readline().strip().split()
        nbLib = int(ligne[1])
        self.nbDays = int((ligne[2]))
        listScore = f.readline().split()
        for j in range(0, len(listScore)):
            listBook.append(Book(j, listScore[j]))
        for i in range(0, nbLib):
            i += 1
            ligne = f.readline().strip()
            listBookLibrairie = f.readline().strip().split()
            ligne = ligne.split()
            self.listLibrairie .append(
                Librairie(i, ligne[0], ligne[1], ligne[2], listBookLibrairie))


class Book():

    def __init__(self, num, score):
        self.num = int(num)
        self.score = int(score)


class Librairie():

    def __init__(self, num, nbBook, shipTime, nbBookPerDay, listBookLibrairie):
        self.nbBook = int(nbBook)
        self.shipTime = int(shipTime)
        self.nbBookPerDay = int(nbBookPerDay)
        self.num = num-1
        self.listBookLibrairie = list()
        self.listBookScanned = list()
        for livre in listBookLibrairie:
            self.listBookLibrairie.append(listBook[int(livre)])
        self.listBookLibrairie = sorted(
            self.listBookLibrairie, key=lambda livre: livre.score, reverse=True)
        self.calculRatio()

    def calculRatio(self):
        self.score = int()
        self.ratio = int()
        for livre in self.listBookLibrairie:
            self.score += livre.score
        self.ratio = self.score / self.shipTime

    def update(self, listeBookout):
        for livre in listeBookout:
            try:
                self.listBookLibrairie.remove(livre)
            except ValueError:
                pass
        self.nbBook = len(self.listBookLibrairie)
        self.calculRatio()

    def scanned(self, day, nbDays):
        global scoreLib
        dayScanne = self.nbBook // self.nbBookPerDay
        if self.nbBook % self.nbBookPerDay != 0:
            dayScanne += 1
        if dayScanne + day <= nbDays:
            self.listBookScanned = self.listBookLibrairie.copy()
        else:
            for i in range(day, nbDays):
                for j in range(0, self.nbBookPerDay):
                    self.listBookScanned.append(self.listBookLibrairie[j])
                self.update(self.listBookScanned)
        for livre in self.listBookScanned:
            scoreLib += livre.score
        return self.listBookScanned


def ecriture(fichier, listLibrairieOutput):
    ligne = str()
    f = open("Haschcode 2020\Output\\" + fichier[21:], "w")
    f.write(str(len(listLibrairieOutput)) + "\n")
    for librairie in listLibrairieOutput:
        ligne = str(librairie.num) + " " + str(len(librairie.listBookScanned))
        f.write(ligne + "\n")
        ligne = str()
        for livre in librairie.listBookScanned:
            ligne += str(livre.num) + " "
        f.write(ligne + "\n")


def progression(iteration, total=100, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Appel en boucle pour créer une barre de progression du terminal

    :param iteration: itération actuelle 
    :type: int
    :param total: total des itérations
    :param prefix: chaîne de préfixe
    :type: str
    :param prefix: chaîne de suffix
    :type: str
    :param decimals: nombre positif de décimales en pourcentage d'achèvement (Int)
    :type: int
    :param length: longueur de caractères de la barre
    :type: int
    :param fill: caractère de remplissage de la barre
    :type: str
    :param printEnd: caractère de fin
    :type: str
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration >= total:
        print()


def initialisation(fichier):
    global scoreLib
    debut = time.time()
    lecture = Read(fichier)
    listLibrairie = lecture.listLibrairie
    nbDays = lecture.nbDays
    day = int()
    scoreLib = int()
    listLibrairieOutput = list()
    listeBookout = list()
    print("Fichier: " + fichier[21:])
    while day < nbDays and len(listLibrairie) > 0:
        modele = "Score: {:,}"
        progression(day, total=nbDays,
                    suffix="\tScore: {:n}".format(scoreLib), length=50)
        listLibrairie = sorted(
            listLibrairie, key=lambda librairie: librairie.ratio, reverse=True)
        newLibrairie = listLibrairie[0]
        day += newLibrairie.shipTime
        listeBookout = newLibrairie.scanned(day, nbDays)
        listLibrairie.remove(newLibrairie)
        if len(newLibrairie.listBookScanned) > 0:
            listLibrairieOutput.append(newLibrairie)
        for librairie in listLibrairie:
            librairie.update(listeBookout)
    progression(nbDays, total=nbDays, length=50, suffix=" " *
                len("  \tScore: {:n}".format(scoreLib)))
    ecriture(fichier, listLibrairieOutput)
    temps = time.time() - debut
    print("Score: {:n}".format(scoreLib))
    print("Temps:", time.strftime("%Hh %Mmin %Ss", time.gmtime(temps)))
    return scoreLib, temps


if __name__ == "__main__":
    score = int()
    temps = float()
    print()
    for fichier in liste_fichier:
        scorelib, tempslib = initialisation(fichier)
        score += scorelib
        temps += tempslib
        print(80 * "-")
    print("\nScore total: {:n}".format(score), "\nTemps total: ",
          time.strftime("%Hh %Mmin %Ss", time.gmtime(temps)))
