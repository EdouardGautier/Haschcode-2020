import Class.Book as book
import Class.Library as library
import CalculScore as verif
import tqdm as tqdm
import os as os
import platform as plt
import time as time
import datetime as date

fichierAudio = "Post-competion\Python\mario-mushroom.ogg"

pathInputPrincipal = "Input/"
pathOutputPrincipal = "Post-competion/Version1/Output/"
fichier_1 = "a_example.txt"
fichier_2 = "b_read_on.txt"
fichier_3 = "c_incunabula.txt"
fichier_4 = "d_tough_choices.txt"
fichier_5 = "e_so_many_books.txt"
fichier_6 = "f_libraries_of_the_world.txt"

output1 = "A_output.txt"
output2 = "B_output.txt"
output3 = "C_output.txt"
output4 = "D_output.txt"
output5 = "E_output.txt"
output6 = "F_output.txt"

listePath = [[fichier_1, output1], [fichier_2, output2], [fichier_3,  output3], [
    fichier_4, output4], [fichier_5, output5], [fichier_6, output6]]

ECRITURE_DIRECT = False
VERIFIER_OUTPUT = True

listeLivres = []
listeLibrairies = []
listeLibrairiesSelec = []
listeScoreFile = []
listePathSelected = []
nbJours = day = scoreTotal = timeTotal = 0


def recupInput(path):
    """
        Fonction qui extrait les données du fichier dont le chemin d'accé est mis en parametre

        :param path: Chemin d'accé du fichier
        :type path: str
    """
    global nbJours

    with open(path, "r") as file:
        # Récuperation des informations globales
        ligne = [int(i) for i in file.readline().strip().split()]
        nbLivres, nbLibrairies, nbJours = ligne[0], ligne[1], ligne[2]

        # Récupération des données concernants les livres
        ligne = [int(i) for i in file.readline().strip().split()]

        for k in range(nbLivres):
            livre = book.Book(k, ligne[k])
            listeLivres.append(livre)

        # Récuperation des données concernant les librairies
        for k in range(nbLibrairies):
            ligne = [int(i) for i in file.readline().strip().split()]
            nbLivres, jourProcess, livreJour = ligne[0], ligne[1], ligne[2]
            ligne = [int(i)
                     for i in list(set(file.readline().strip().split()))]
            listeLivresLib = []
            for i in ligne:
                listeLivresLib.append(listeLivres[i])

            librairie = library.Library(
                listeLivresLib, jourProcess, livreJour, k, nbLivres)
            listeLibrairies.append(librairie)


def empruntLivre(jourRestant):
    ratioMax = ratioTemp = 0
    depasseLimiteTemps = depasseLimiteTempsMax = False
    librairieSelec = None
    for k in listeLibrairies:
        ratioTemp, depasseLimiteTemps = k.calculRatio(jourRestant)
        if ratioTemp > ratioMax:
            ratioMax = ratioTemp
            librairieSelec = k
            depasseLimiteTempsMax = depasseLimiteTemps

        elif ratioMax == ratioTemp and depasseLimiteTemps < depasseLimiteTempsMax:
            ratioMax = ratioTemp
            librairieSelec = k
            depasseLimiteTempsMax = depasseLimiteTemps

        elif not ratioTemp:
            # Suppresion des librairies qui ne rapporte plus de point
            listeLibrairies.remove(k)

    listeLibrairiesSelec.append(librairieSelec)
    if librairieSelec != None:
        listeLibrairies.remove(librairieSelec)
        for k in librairieSelec.listeLivreEmprunt(limiteTemps=day - librairieSelec.getDelay()):
            k.empruntLivre()


def ecritOutput(path):
    with open(path, "w") as file:
        line = str(len(listeLibrairiesSelec)) + "\n"
        file.write(line)
        for k in listeLibrairiesSelec[:]:
            line = str(k.getId()) + " " + str(len(k.getListeLivre())) + "\n"
            file.write(line)
            line = " ".join(str(i) for i in k.getListeLivre()) + "\n"
            file.write(line)


def cleanTerminal():
    # Nettoye le terminal automatiquement
    if plt.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")


def interface():
    def pauseQuestionBoolean(phrase, suffixe=" (O\\N)\t"):
        answerContinue = str(input(phrase + suffixe))
        answerContinue = answerContinue.upper()

        while answerContinue != "O" and answerContinue != "N":
            print("Saisie incorrecte")
            answerContinue = str(input(phrase + suffixe))
            answerContinue = answerContinue.upper()

        if answerContinue != "O":
            answerContinue = False
        else:
            answerContinue = True
        return answerContinue

    global listePathSelected

    cleanTerminal()
    answer = True
    listePathSelected = []
    answerContinue = True

    while answerContinue and len(listePath) > 0:
        for path in listePath:
            print(listePath.index(path) + 1, ":",
                  path[0])
        print("\n" + str(len(listePath) + 1), ": ALL")
        error = True

        while error:
            try:
                answer = int(
                    input("\nVeuillez sélectionner le fichier à tester \t"))
                listePathSelected.append(listePath[answer - 1])
                error = False
            except IndexError:
                if answer == len(listePath) + 1:
                    listePathSelected.extend(listePath)
                    error = False
                else:
                    print("Saisie incorrecte")
            except ValueError:
                print("Saisie incorrecte")

        if answer != len(listePath) + 1:
            del listePath[answer - 1]
            if len(listePath) > 0:
                answerContinue = pauseQuestionBoolean(
                    "Voulez vous sélectionner un autre fichier ?")
        else:
            answerContinue = False
        cleanTerminal()

    answer = pauseQuestionBoolean(
        "Voulez-vous vérifier les fichiers de sortie ?")
    if answer:
        VERIFIER_OUTPUT = True
    else:
        VERIFIER_OUTPUT = False

    answer = pauseQuestionBoolean(
        "Voulez-vous écrire les fichiers de sortie en direct ?")
    if answer:
        ECRITURE_DIRECT = True
    else:
        ECRITURE_DIRECT = False

    cleanTerminal()


def scanFichier(path):
    global day

    scoreFile = 0
    print(81*"#" + "\n")
    print("Test sur le fichier : " + path[0])
    startTimeFile = time.time()

    recupInput(pathInputPrincipal + path[0])

    bar = tqdm.tqdm(total=nbJours, desc="Progression des jours")
    while day < nbJours:
        empruntLivre(nbJours - day)
        if listeLibrairiesSelec[-1] != None:
            day += listeLibrairiesSelec[-1].getDelay()
            bar.update(listeLibrairiesSelec[-1].getDelay())
            scoreFile += listeLibrairiesSelec[-1].getScore()
            if ECRITURE_DIRECT:
                ecritOutput(pathOutputPrincipal + path[1])
        else:
            del listeLibrairiesSelec[-1]
            break

    if day < nbJours:
        bar.update(nbJours - day)
    bar.close()
    chrono = time.time() - startTimeFile

    if not ECRITURE_DIRECT:
        ecritOutput(pathOutputPrincipal + path[1])
    print("Process terminer du fichier", path[1], ",", len(
        listeLibrairiesSelec), "librairies")
    print("Score du fichier : ", '{0:,}'.format(scoreFile))
    print("Temps ecoule :", time.strftime(
        "%Hh %Mmin %Ss", time.gmtime(chrono)))
    print("\n" + 81*"#" + 2*"\n")

    return scoreFile, chrono


if __name__ == "__main__":
    interface()

    print(28*"+", "Commencement du process", 28*"+", 2*"\n")
    for path in listePathSelected:
        scoreFile, chrono = scanFichier(path)

        listeLivres = []
        listeLibrairies = []
        listeLibrairiesSelec = []
        listeLivresSelec = []
        listeScoreFile.append(scoreFile)
        nbJours = day = 0
        scoreTotal += scoreFile
        timeTotal += chrono

    print(32*"+", "Process termine", 32*"+", "\n")
    print("Score Total: ", '{0:,}'.format(scoreTotal))
    print("Temps Total:", time.strftime(
        "%Hh %Mmin %Ss", time.gmtime(timeTotal)), "\n")
    print(2*"\n")

    if VERIFIER_OUTPUT:
        # verif
        pass
