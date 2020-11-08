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
    """
    Class permettant la lecture des fichiers
    """    
    def __init__(self, fichier):
        """
        Initialisation de la classe

        Args:
            fichier (ficheir texte): fichier en entré
        """        
        self.fichier = fichier
        self.nb_days = int()
        self.list_librairie = list()
        self.lecture()

    def lecture(self):
        """
        Lecture du fichier
        """        
        global listBook
        listBook = list()
        f = open(self.fichier, encoding='utf8')
        ligne = f.readline().strip().split()
        nb_lib = int(ligne[1])
        self.nb_days = int((ligne[2]))
        list_score = f.readline().split()
        for j in range(0, len(list_score)):
            listBook.append(Book(j, list_score[j]))
        for i in range(0, nb_lib):
            i += 1
            ligne = f.readline().strip()
            list_book_librairie = f.readline().strip().split()
            ligne = ligne.split()
            self.list_librairie .append(
                Librairie(i, ligne[0], ligne[1], ligne[2], list_book_librairie))


class Book():
    """
    Représentation des livres en classe
    """    
    def __init__(self, num, score):
        """
        Initialisation de la classe

        Args:
            num (int): numéro du livre, ID
            score (int): nombre de point du livre
        """        
        self.num = int(num)
        self.score = int(score)


class Librairie():
    """
    Représentation des librairie en classe
    """    

    def __init__(self, num, nb_book, ship_time, nb_book_per_day, list_book_librairie):
        """
        Initialisation de la classe

        Args:
            num (int): numéro de la librairie, ID
            nb_book (int): nombre de livre dans la librairie
            ship_time (int): temps d'emprunt des livres
            nb_book_per_day (int): nombre de livre emprunté par jour
            list_book_librairie (list): liste des livres
        """        
        self.nb_book = int(nb_book)
        self.ship_time = int(ship_time)
        self.nb_book_per_day = int(nb_book_per_day)
        self.num = num-1
        self.list_book_librairie = list()
        self.list_book_scanned = list()
        for livre in list_book_librairie:
            self.list_book_librairie.append(listBook[int(livre)])
        self.list_book_librairie = sorted(
            self.list_book_librairie, key=lambda livre: livre.score, reverse=True)
        self.calcul_ratio()

    def calcul_ratio(self):
        """
        Ratio scrore des livres / jour d'emprunt
        """        
        self.score = int()
        self.ratio = int()
        for livre in self.list_book_librairie:
            self.score += livre.score
        self.ratio = self.score / self.ship_time

    def update(self, liste_book_out):
        """
        Mise à jour des attribut de la classe

        Args:
            liste_book_out (list): liste des livres empruntés
        """        
        for livre in liste_book_out:
            try:
                self.list_book_librairie.remove(livre)
            except ValueError:
                pass
        self.nb_book = len(self.list_book_librairie)
        self.calcul_ratio()

    def scanned(self, day, nb_days):
        """
        On commence à scanner les livres

        Args:
            day (int): jour que nous sommes
            nb_days ([type]): nombre de jour restant

        Returns:
            list: liste des livre scanné
        """        
        global scoreLib
        day_scanne = self.nb_book // self.nb_book_per_day
        if self.nb_book % self.nb_book_per_day != 0:
            day_scanne += 1
        if day_scanne + day <= nb_days:
            self.list_book_scanned = self.list_book_librairie.copy()
        else:
            for i in range(day, nb_days):
                for j in range(0, self.nb_book_per_day):
                    self.list_book_scanned.append(self.list_book_librairie[j])
                self.update(self.list_book_scanned)
        for livre in self.list_book_scanned:
            scoreLib += livre.score
        return self.list_book_scanned


def ecriture(fichier, list_librairie_output):
    """
    Ecriture du fichier réponse

    Args:
        fichier (fichier texte): fichier de sorti
        list_librairie_output (list): liste des livres scannés
    """    
    f = open("Haschcode 2020\Output\\" + fichier[21:], "w")
    f.write(str(len(list_librairie_output)) + "\n")
    for librairie in list_librairie_output:
        ligne = str(librairie.num) + " " + str(len(librairie.list_book_scanned))
        f.write(ligne + "\n")
        ligne = str()
        for livre in librairie.list_book_scanned:
            ligne += str(livre.num) + " "
        f.write(ligne + "\n")


def progression(iteration, total=100, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Appel en boucle pour créer une barre de progression du terminal

    Args:
        iteration (int): itération actuelle 
        total (int, optional): total des itérations. Defaults to 100.
        prefix (str, optional): chaîne de préfixe. Defaults to ''.
        suffix (str, optional): chaîne de suffix. Defaults to ''.
        decimals (int, optional): nombre positif de décimales en pourcentage d'achèvement. Defaults to 1.
        length (int, optional): longueur de caractères de la barre. Defaults to 100.
        fill (str, optional): caractère de remplissage de la barre. Defaults to '█'.
        print_end (str, optional): caractère de fin. Defaults to "\r".
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration >= total:
        print()


def initialisation(fichier):
    """
    Initialisation du traitement du fichier

    Args:
        fichier (fichier texte): fichier à traiter

    Returns:
        (scoreLib, temps): score de la librairie, temps restant
    """    
    global scoreLib
    debut = time.time()
    lecture = Read(fichier)
    list_librairie = lecture.list_librairie
    nb_days = lecture.nb_days
    day = int()
    scoreLib = int()
    list_librairie_output = list()
    print("Fichier: " + fichier[21:])
    while day < nb_days and len(list_librairie) > 0:
        progression(day, total=nb_days,
                    suffix="\tScore: {:n}".format(scoreLib), length=50)
        list_librairie = sorted(
            list_librairie, key=lambda librairie: librairie.ratio, reverse=True)
        new_librairie = list_librairie[0]
        day += new_librairie.ship_time
        liste_book_out = new_librairie.scanned(day, nb_days)
        list_librairie.remove(new_librairie)
        if len(new_librairie.list_book_scanned) > 0:
            list_librairie_output.append(new_librairie)
        for librairie in list_librairie:
            librairie.update(liste_book_out)
    progression(nb_days, total=nb_days, length=50, suffix=" " *
                len("  \tScore: {:n}".format(scoreLib)))
    ecriture(fichier, list_librairie_output)
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
