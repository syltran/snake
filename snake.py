import fltk
from time import sleep
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    :param case : tuple

    >>> case_vers_pixel((0,0))
    (7.5, 7.5)
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    """
    Fonction permettant d'afficher les pommes sur le terrain.
    :param pommes: liste
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        fltk.cercle(x, y, taille_case/2,
                    couleur='darkred', remplissage='red')
        fltk.rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                       couleur='darkgreen', remplissage='darkgreen')


def creer_pomme():
    """
    Fonction permettant d'ajouter à la liste pommes un couple
    représentant les coordonnées d'une case qui va contenir une pomme
    donc en soit de créer une pomme sur le terrain
    ssi elle n'apparaît dans le serpent.
    """
    une_pomme = (randint(0, 39), randint(0, 29))
    while une_pomme in serpent:
        une_pomme = (randint(0, 39), randint(0, 29))
    pommes.append(une_pomme)


def affiche_serpent(serpent):
    """
    Fonction permettant d'afficher le serpent sur le terrain
    :param serpent: liste
    """
    for elem in serpent:
        x, y = case_vers_pixel(elem)
        # boule tête
        if elem == serpent[-1]:
            fltk.cercle(x, y, taille_case/2 + 1, remplissage='green')
            fltk.cercle(x+2, y-2, taille_case/4, remplissage='yellow')  # oeil
            fltk.cercle(x+3, y-3, taille_case/8, remplissage='black')  # oeil
            fltk.rectangle(x+1, y+4, x+6, y+6, remplissage='red')  # bouche
        # boule queue
        elif elem == serpent[0]:
            fltk.cercle(x, y, taille_case/2 + 1, remplissage='orange')
        else:  # boules corps
            fltk.cercle(x, y, taille_case/2 + 1,
                        couleur='darkgreen', remplissage='green')


def change_direction(direction, touche):
    """
    Fonction qui renvoie un couple représentant
    les coordonnées qui va servir à changer la direction du serpent.
    4 directions possibles :
    aller en haut, aller en bas, aller à gauche, aller à droite.
    :param direction : tuple
    :param touche : str
    :return value : tuple

    >>> change_direction((0, 0), 'Up')
    (0, -1)
    >>> change_direction((0, 1), None)
    (0, 1)
    """
    if touche == 'Up' and direction != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        # flèche bas
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        # flèche gauche
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        # flèche droite
        return (1, 0)
    else:
        # pas de changement !
        return direction  # ancienne direction


def actualise_serpent(serpent, direction):
    """
    Fonction additionnant les coordonnées de la tête du serpent à celles
    du couple direction donnant ainsi les coordonnées de la futur tête.
    Si celles-ci n'est pas dans la liste pommes, alors on supprime
    la queue et on fait apparaitre la nouvelle tête.
    Dans le cas contraire,
    on ne supprime pas la queue ce qui fait grandir le serpent.
    Donc en soit cette fonction permet de déplacer le serpent
    et de le faire grandir si il mange une pomme.

    :param serpent : liste
    :param direction : liste
    """
    xtete, ytete = serpent[-1]  # coordonée de l'ancienne tête
    x, y = direction
    x_newtete, y_newtete = xtete + x, ytete + y
    new_tete = (x_newtete, y_newtete)  # coordonnées de la nouvelle tête

    if new_tete not in pommes:
        serpent.pop(0)  # suprime la queue
    serpent.append(new_tete)  # faire apparaitre la nouvelle tête


def reactualiser_objet(serpent, pommes):
    """
    Fonction permettant de réactualiser les objets sur le terrain
    si une pomme est mangée.
    Les objets réactualisés sont: 1 pommes et 12 murs
    :param serpent : liste
    :param pommes : liste
    """
    if serpent[-1] in pommes:
        pommes.pop()  # supprimer l'ancienne pomme
        creer_pomme()  # créer une nouvelle pomme

        mur.clear()  # supprimer les anciens murs
        cree_mur()  # créer 12 nouveaux murs


def fin_jeu(serpent, mur):
    """
    Fonction regardant tous les cas mettant fin au jeu.
    il y a 3 cas possibles:
    1)lorsque la tête du serpent sors du terrain
    2)lorsque le serpent se mange
    3)lorsque la tête du serpent rentre dans un mur

    >>> fin_jeu([(0,-1)], [(2, 0)])
    False
    >>> fin_jeu([(2,2), (2,3), (2,4), (3,4),
                 (4,4), (4,3), (3,3), (2,3)], [(10,2)])
    False
    >>> fin_jeu([(2, 0)], [(2, 0)])
    False

    """
    xtete, ytete = serpent[-1]
    # on regarde si la tête du serpent sors du terrain
    if xtete < 0 or xtete >= 40 or ytete < 0 or ytete >= 30:
        return False

    # on regarde si le serpent se mange lui-même
    for pos in range(len(serpent)-1):
        if (xtete, ytete) == serpent[pos]:
            return False

    # on regarde si la tête du serpent rentre dans un mur
    if (xtete, ytete) in mur:
        return False

    return True


def affiche_mur(mur):
    """
    Fonction permettant d'afficher les murs sur le terrain.
    :param mur: liste
    """
    for elem in mur:
        x, y = case_vers_pixel(elem)
        fltk.rectangle(x-15/2, y-15/2, x+15/2, y+15/2,
                       remplissage='darkgray')


def cree_mur():
    """
    Fonction permettant d'ajouter à la liste mur 12 couples représentant les
    coordonnées de 12 cases qui va contenir les murs
    donc en soit de créer 12 murs sur le terrain
    ssi ils n'apparaissent ni dans le serpent
    ni dans une pomme.
    """
    for nbre_mur in range(12):
        m = (randint(5, 35), randint(0, 29))
        while m in serpent or m in pommes:
            m = (randint(5, 35), randint(0, 29))
        mur.append(m)


# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10   # taux de rafraîchissement du jeu en images/s =FPS
    direction = (0, 0)  # direction initiale du serpent
    pommes = []  # liste des coordonnées des cases contenant des pommes
    mur = []  # liste des coordonnées des cases contenant des murs
    # liste des coordonnées de cases adjacentes décrivant le serpent
    serpent = [(0, 0)]
    score = 0

    # faire apparaitre une pomme au debut du jeu
    creer_pomme()

    # faire apparaitre 12 murs au début du jeu
    cree_mur()

    fltk.cree_fenetre(taille_case * largeur_plateau,
                      taille_case * hauteur_plateau)

    # Message début de jeu : sorte de compte à rebours
    fltk.rectangle(0, 0, 600, 450, remplissage='red')  # laser rouge
    fltk.rectangle(2, 2, 598, 448, remplissage='black')  # fond noir
    fltk.texte(300, 225, 'PRESS TO PLAY', taille=20,
               couleur='white', ancrage='center', tag='play')
    fltk.attend_ev()
    fltk.efface('play')
    Start = ['3', '2', '1', 'START !']
    for elem in Start:
        fltk.texte(300, 225, elem, taille=40, couleur='white',
                   ancrage='center', tag='start')
        fltk.attente(0.3)
        fltk.efface('start')

    # boucle principale
    jouer = True
    temps = 0
    while jouer:
        fltk.efface_tout()
        # affichage des objets
        fltk.rectangle(0, 0, 600, 450, remplissage='red')  # laser rouge
        fltk.rectangle(2, 2, 598, 448, remplissage='black')  # fond noir

        affiche_pommes(pommes)
        affiche_serpent(serpent)
        affiche_mur(mur)

        # affichage score et vitesse
        score = len(serpent)-1
        fltk.texte(530, 10, 'Score: ' + str(score), couleur='white', taille=10)
        fltk.texte(450, 10, 'Speed: x' + str(framerate-10),
                   couleur='cyan', taille=10)
        fltk.mise_a_jour()

        # gestion des événements
        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            print(fltk.touche(ev))
            direction = change_direction(direction, fltk.touche(ev))

        actualise_serpent(serpent, direction)
        reactualiser_objet(serpent, pommes)

        if fin_jeu(serpent, mur) is False:
            jouer = False

        # augmente progressivement la vitesse du jeu
        if temps == 250:
            framerate += 3
            temps = 0

        temps += 1
        # attente avant rafraîchissement
        sleep(1/framerate)

    # message fin de jeu
    fltk.texte(300, 225, 'GAME OVER', taille=50,
               ancrage='center', couleur='red')

    # fermeture et sortie
    fltk.attend_clic_gauche()
    fltk.ferme_fenetre()
