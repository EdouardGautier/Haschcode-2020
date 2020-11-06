import tqdm as tqdm
import platform as plt
import os as os

fichierAudio = "Post-competion\Python\mario-mushroom.ogg"

pathInputPrincipal = "Python/Input/"
pathOutputPrincipal = "Python/Post-competion/Output/"
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


def convertToInt(liste):
    for k in range(len(liste)):
        liste[k] = int(liste[k])


def recupListeLivre(path):
    with open(path, "r") as file:
        file.readline()
        liste = file.readline().strip().split()
        convertToInt(liste)
    return liste



def verificationFichier(path):
    pathInput = pathInputPrincipal + path[0]
    pathOutput = pathOutputPrincipal + path[1]
    score = nbErreurs = nbLib = 0
    listeLivresPrits = []
    listeScoreLivres = []

    listeScoreLivres = recupListeLivre(pathInput)

    with open(pathOutput, "r") as file:
        nbLib = int(file.readline().strip())
        for k in tqdm.tqdm(range(nbLib), desc="Progression de la vérification"):
            file.readline()
            listeLivreLib = file.readline().strip().split()
            convertToInt(listeLivreLib)
            for i in listeLivreLib:
                if i not in listeLivresPrits:
                    listeLivresPrits.append(i)
                    score += listeScoreLivres[i]
                else:
                    nbErreurs += 1
    
    return score, nbErreurs


def cleanTerminal():
    # Nettoye le terminal automatiquement
    if plt.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")


if __name__ == "__main__":
    cleanTerminal()

    print(28*"-", "Debut vérif des Outputs", 28*"-", "\n")

    scoreTotalTest = 0

    for path in listePath[:2]:
        print(81*"#", "\n")
        print("Test sur le fichier", path[1])
        scoreFile, nbErreurs = verificationFichier(path)
        scoreTotalTest += scoreFile
        print("Score du fichier :", '{0:,}'.format(scoreFile))
        print("Nombre de répétitions :", nbErreurs, "\n")
        print(81*"#", 2*"\n")
        continue

    print(29*"-", "Fin vérif des Outputs", 29*"-")
    print("Score final après vérification", '{0:,}'.format(scoreTotalTest), "\n")
