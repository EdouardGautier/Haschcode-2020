import unittest as unittest
import sys as sys
import filecmp as fileCompare

sys.path.append("2020/Competition/Post-competion/Class")

import Book as book
import Library as library

livre0 = book.Book(0, 1)
livre1 = book.Book(1, 2)
livre2 = book.Book(2, 3)
livre3 = book.Book(3, 6)
livre4 = book.Book(4, 5)
livre5 = book.Book(5, 4)
listeLivres = [livre0, livre1, livre2, livre5, livre4, livre3]

librairie0 = library.Library([livre0, livre1, livre2, livre3, livre4], 2, 2, 0, 5)
librairie1 = library.Library([livre3, livre2, livre5, livre0], 3, 1, 1, 4)
listeLibrairie = [librairie0, librairie1]

limiteJourMax = 7


class Test_Lib (unittest.TestCase):
    def test_CalculScoreInit(self):
        self.assertEqual(librairie0.getScore(), 17)
        self.assertEqual(librairie1.getScore(), 14)

    def test_RatioPasLimiteTemps(self):
        librairie0.calculRatio(limiteJourMax)
        librairie1.calculRatio(limiteJourMax)
        self.assertEqual(librairie0.calculRatio(limiteJourMax), (17/2, False))
        self.assertEqual(librairie1.calculRatio(limiteJourMax), (14/3, False))

    def test_CalculScoreTempsLimiter(self):
        # Un seul jour
        librairie0.calculScore(2)   # Nombre de livre pouvant etre prit en 1 jours   
        librairie1.calculScore(1)
        self.assertEqual(librairie0.getScore(), 11)
        self.assertEqual(librairie1.getScore(), 6)

        # Deux jours
        librairie0.calculScore(4)   # Nombre de livre pouvant etre prit en 2 jours   
        librairie1.calculScore(2)
        self.assertEqual(librairie0.getScore(), 16)
        self.assertEqual(librairie1.getScore(), 10)

        # Trois jours
        librairie0.calculScore(6)   # Nombre de livre pouvant etre prit en 3 jours (Plus que dispo librairie0) 
        librairie1.calculScore(3)
        self.assertEqual(librairie0.getScore(), 17)
        self.assertEqual(librairie1.getScore(), 13)

    def test_RatioTempsLimiter(self):
        # Pas le temps de s'incrire
        self.assertEqual(librairie0.calculRatio(1), (0, True))
        self.assertEqual(librairie1.calculRatio(1), (0, True))


        # Inscription plus deux jour
        self.assertEqual(librairie0.calculRatio(4), (16/2, True))   # Score / tempsIncription
        self.assertEqual(librairie1.calculRatio(5), (10/3, True))   # Delay depasse pour tout prendre Vrai

        # Incription plus 3 jours
        self.assertEqual(librairie0.calculRatio(5), (17/2, False))
        self.assertEqual(librairie1.calculRatio(6), (13/3, True))

    def test_ListeLivreEmprunter(self):
        # Pas de limite de temps
        self.assertEqual(librairie0.listeLivreEmprunt(limiteTemps=limiteJourMax), [livre3, livre4, livre2, livre1, livre0])
        self.assertEqual(librairie1.listeLivreEmprunt(limiteTemps=limiteJourMax), [livre3, livre5, livre2, livre0])

        # Deux jours
        self.assertEqual(librairie0.listeLivreEmprunt(limiteTemps=2), [livre3, livre4, livre2, livre1])
        self.assertEqual(librairie1.listeLivreEmprunt(limiteTemps=2), [livre3, livre5])

    def test_MajListeLivreEmprumter(self):
        # Librairie 0 initialiser et emprumpte pendant 3 jours (livre 0, 1, 2, 3, 4)
        # Il ne reste que le livre 5 non emprunter a la librairie 1
        listeLivreEmprunter = [livre0, livre1, livre2, livre3, livre4]
        librairie1.majListeLivre(listeLivreEmprunter)
        self.assertEqual(librairie1.listeLivreEmprunt(limiteTemps=limiteJourMax), [livre5])

    def test_EcritureFichier(self):
        path = "2020/Competition/Post-competion/Test/output_test.txt"
        pathReference = "2020/Competition/Post-competion/Test/output_testRef.txt"

        self.ecritureFichier(path)

        self.assertTrue(fileCompare.cmp(path, pathReference))

    def test_LectureFichierInput(self):
        pathReference = "2020/Competition/Input/a_example.txt"
        nbJoursTest, listeLivresTest, listeLibrairiesTest = self.lectureFichierInput(pathReference)

        for k, i in zip(listeLibrairiesTest, listeLibrairie):
            self.assertTrue(self.compareLib(k,i))

        self.assertEqual(nbJoursTest,limiteJourMax)
        self.assertTrue(self.compareListeLivre(listeLivresTest, listeLivres))

    def test_CalculScoreListeLivreSelected(self):
        listeLivresSelected = [[livre3, livre4, livre2, livre1, livre0], [livre5]]
        setListeLivresSelected = []
        for i in listeLivresSelected:
            setListeLivresSelected.extend(i)
        
        setListeLivresSelected = list(set(setListeLivresSelected))

        score = 0
        for k in setListeLivresSelected:
            score += k.getScore()
        
        self.assertEqual(score, 21)

    def test_CalculScoreFichirOutuput(self):
        path = "2020/Competition/Post-competion/Test/output_testRef.txt"

        self.assertEqual(21, self.lectureScoreFichierOutput(path))

    def ecritureFichier(self, path):
        listeLibrairieSelected = [librairie0, librairie1]
        listeLivresSelected = [[livre3, livre4, livre2, livre1, livre0], [livre5]]
        with open (path, "w") as file:
            file.write(str(len(listeLibrairieSelected)) + "\n")
            for k in range (len(listeLibrairieSelected)):
                line = str(listeLibrairieSelected[k].getId()) + " " + str(len(listeLivresSelected[k])) + "\n"
                file.write(line)
                line = " ".join(str(i) for i in listeLivresSelected[k]) + "\n"
                file.write(line)

    def lectureFichierInput(self, path):
        def convertToInt(liste):
            for k in range(len(liste)):
                liste[k] = int(liste[k])

        listeLibrairiesTest = []
        listeLivresTest = []
        
        with open (path, "r") as file:
            # Récuperation des informations globales
            ligne = file.readline().strip().split()
            convertToInt(ligne)
            nbLivres, nbLibrairies, nbJours = ligne[0], ligne[1], ligne[2]
            
            # Récupération des données concernants les livres
            ligne = file.readline().strip().split()
            convertToInt(ligne)
            for k in range (nbLivres):
                livre = book.Book(k, ligne[k])
                listeLivresTest.append(livre)

            # Récuperation des données concernant les librairies
            for k in range (nbLibrairies):
                ligne = file.readline().strip().split()
                convertToInt(ligne)
                nbLivres, jourProcess, livreJour = ligne[0], ligne[1], ligne[2]
                ligne = file.readline().strip().split()
                convertToInt(ligne)
                listeLivresLib = []
                for i in ligne:
                    listeLivresLib.append(listeLivresTest[i])
                librairie = library.Library(listeLivresLib, jourProcess, livreJour, k, nbLivres)
                listeLibrairiesTest.append(librairie)
        
        return nbJours, listeLivresTest, listeLibrairiesTest

    def lectureScoreFichierOutput(self, path):
        listeRangLivres = []
        listeIdLib = []
        score = 0
        with open (path, "r") as file:
            nbLib = int(file.readline().strip())
            for k in range(nbLib):
                line = file.readline().strip().split()
                self.convertToInt(line)
                idLib, nbLivres = line[0], line[1]
                if idLib not in listeIdLib:
                    listeIdLib.append(idLib)
                    listeLivreLigne = file.readline().strip().split()
                    self.convertToInt(listeLivreLigne)
                    for i in listeLivreLigne:
                        if i not in listeRangLivres:
                            score += listeLivres[i].getScore()
                            listeRangLivres.append(i)
        return score

    def compareLib(self, lib1, lib2):
        lib1.trieLivre()
        lib1.calculScore(lib1.getNbLivre())
        lib2.trieLivre()
        lib2.calculScore(lib1.getNbLivre())

        return lib1.getDelay() == lib2.getDelay() and lib1.getId() == lib2.getId() and \
             lib1.getScore() == lib2.getScore() \
                 and lib1.getEmpruntJour() == lib2.getEmpruntJour() and \
                     self.compareListeLivre(lib1.getListeLivre(), lib2.getListeLivre())

    def compareListeLivre(self, liste1, liste2):
        answer = True
        for k in liste1:
            for i in liste2:
                answerTemp = False
                if self.compareLivre(i, k):
                    answerTemp = True
                    break
            if not answerTemp:
                answer = False
                break            
        if answer and len(liste2) == len(liste1):
            return True
        else:
            return False

    def compareLivre(self, book1, book2):
        return book1.getScore() == book2.getScore() and \
            book1.getRang() == book2.getRang() and book1.estDispo() == book2.estDispo()
    
    def convertToInt(self, liste):
        for k in range(len(liste)):
            liste[k] = int(liste[k])



if __name__ == "__main__":
    test = Test_Lib()
    
    test.test_CalculScoreInit()
    test.test_CalculScoreTempsLimiter()
    test.test_RatioPasLimiteTemps()
    test.test_RatioTempsLimiter()
    test.test_ListeLivreEmprunter()
    test.test_MajListeLivreEmprumter()
    test.test_EcritureFichier()
    test.test_CalculScoreFichirOutuput()
    test.test_CalculScoreListeLivreSelected()
    test.test_LectureFichierInput()
