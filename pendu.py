import pygame
import random
import sys
import pygame.mixer

pygame.mixer.init()
pygame.init()

LARGEUR = 800
HAUTEUR = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

NIVEAUX = {
    "Facile": 8,
    "Moyen": 6,
    "Difficile": 4
}

menu_actif=True

def gerer_musique():
    global menu_actif

    if menu_actif:
        pygame.mixer.music.load("pendu\Larbre du pendu - Hunger Game.mp3")
        pygame.mixer.music.play(-1)  
    else:
        pygame.mixer.music.stop()  

def arreter_musique():
    pygame.mixer.music.stop()


def choisir_mot(difficulte):
    with open(r"pendu\mots.txt", "r", encoding="utf-8") as fichier:
        mots = [mot.strip().upper() for mot in fichier.readlines() if len(mot) >= difficulte]
    return random.choice(mots)

def afficher_menu_difficulte(fenetre, font):
    fond_menu_difficulte = pygame.image.load(r"c:pendu\diff.png")
    fond_menu_difficulte = pygame.transform.scale(fond_menu_difficulte, (LARGEUR, HAUTEUR))
    fenetre.blit(fond_menu_difficulte, (0, 0))

    titre = font.render("Choisissez le niveau de difficulté", True, NOIR)
    fenetre.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 2 - 100))

    options = list(NIVEAUX.keys())
    y_position = HAUTEUR // 2
    for option in options:
        texte_option = font.render(option, True, NOIR)
        rect_option = pygame.Rect(
            LARGEUR // 2 - texte_option.get_width() // 2 - 10, y_position, texte_option.get_width() + 20, 50
        )
        pygame.draw.rect(fenetre, BLANC, rect_option)
        fenetre.blit(
            texte_option,
            (LARGEUR // 2 - texte_option.get_width() // 2, y_position + rect_option.height // 2 - texte_option.get_height() // 2)
        )
        y_position += 75

    pygame.display.flip()

    attente_selection = True
    while attente_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, option in enumerate(options):
                    rect_option = pygame.Rect(
                        LARGEUR // 2 - font.size(option)[0] // 2 - 10, HAUTEUR // 2 + i * 75, font.size(option)[0] + 20, 50
                    )
                    if rect_option.collidepoint(event.pos):
                        return NIVEAUX[option]

def afficher_ecran_titre(fenetre, font):
    fenetre.fill(BLANC)

    fond = pygame.image.load(r"pendu\pendu_.jpg")  # Remplacez par le chemin correct de votre image de fond
    fenetre.blit(fond, (0, 0))

    titre = font.render("Jeu du Pendu", True, BLANC)
    appuyer_touche = font.render("Appuyez sur une touche pour commencer", True, BLANC)

    fenetre.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 2 - 50))
    fenetre.blit(appuyer_touche, (LARGEUR // 2 - appuyer_touche.get_width() // 2, HAUTEUR // 2 + 50))

    pygame.display.flip()

    attente_touche = True
    while attente_touche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                attente_touche = False

def dessiner_bonhomme(fenetre, erreurs):
    if erreurs == 0:
        return  # Pas d'erreur, pas besoin de dessiner

    # Dessin du pendu en fonction du nombre d'erreurs
    if erreurs >= 1:
        pygame.draw.line(fenetre, NOIR, (150, 100), (150, 80), 2)  # Potence
        pygame.draw.line(fenetre, NOIR, (150, 80), (200, 80), 2)  # Haut de la potence
        pygame.draw.line(fenetre, NOIR, (200, 80), (200, 250), 2)  # Poteau de la potence
        pygame.draw.line(fenetre, NOIR, (200, 100), (200, 120), 2)  # Corde vers le haut
    if erreurs >= 2:
        pygame.draw.circle(fenetre, NOIR, (200, 160), 20, 2)  # Tête
    if erreurs >= 3:
        pygame.draw.line(fenetre, NOIR, (200, 180), (200, 240), 2)  # Corps
    if erreurs >= 4:
        pygame.draw.line(fenetre, NOIR, (200, 200), (180, 180), 2)  # Bras gauche
    if erreurs >= 5:
        pygame.draw.line(fenetre, NOIR, (200, 200), (220, 180), 2)  # Bras droit
    if erreurs >= 6:
        pygame.draw.line(fenetre, NOIR, (200, 240), (180, 280), 2)  # Jambe gauche
        pygame.draw.line(fenetre, NOIR, (200, 240), (220, 280), 2)  # Jambe droite



def jouer_pendu():

    global menu_actif

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu du Pendu")

    # Chargez le logo
    logo = pygame.image.load(r"pendu\logo.png")  # Remplacez par le chemin correct de votre logo
    pygame.display.set_icon(logo)

    font = pygame.font.Font(None, 36)

    afficher_ecran_titre(fenetre, font)

    clock = pygame.time.Clock()

    attente_touche = True
    while attente_touche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                attente_touche = False

        clock.tick(30)
    while True:  # Ajout de la boucle infinie pour le menu principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        menu_actif = True
        gerer_musique()
        menu_principal(fenetre, font)  # Appel du menu principal

        # Ajoutez une condition de sortie si nécessaire
        clock.tick(30)

def detecter_survol_option(options_rect, pos):
    for rect in options_rect:
        if rect.collidepoint(pos):
            return rect
    return None

def menu_principal(fenetre, font):
    while True:
        fond = pygame.image.load(r"pendu\pendu wall.png")  # Remplacez par le chemin correct de votre image de fond
        fenetre.blit(fond, (0, 0))

        texte_bienvenue = font.render("Bienvenue !", True, NOIR)
        fenetre.blit(texte_bienvenue, (LARGEUR // 2 - texte_bienvenue.get_width() // 2, 50))

        texte_menu_jouer = font.render("Jouer", True, NOIR)
        texte_menu_difficulte = font.render("Choisir la difficulté", True, NOIR)
        texte_menu_insérer = font.render("Insérez un mot", True, NOIR)
        texte_menu_quitter = font.render("Quitter le jeu", True, NOIR)

        rect_jouer = pygame.Rect(LARGEUR // 2 - texte_menu_jouer.get_width() // 2 - 10, HAUTEUR // 2 - 125, texte_menu_jouer.get_width() + 20, 50)
        rect_difficulte = pygame.Rect(LARGEUR // 2 - texte_menu_difficulte.get_width() // 2 - 10, HAUTEUR // 2 - 75, texte_menu_difficulte.get_width() + 20, 50)
        rect_insérer = pygame.Rect(LARGEUR // 2 - texte_menu_insérer.get_width() // 2 - 10, HAUTEUR // 2 - 25, texte_menu_insérer.get_width() + 20, 50)
        rect_quitter = pygame.Rect(LARGEUR // 2 - texte_menu_quitter.get_width() // 2 - 10, HAUTEUR // 2 + 25, texte_menu_quitter.get_width() + 20, 50)

        pygame.draw.rect(fenetre, (200, 200, 200), rect_jouer)
        pygame.draw.rect(fenetre, (200, 200, 200), rect_difficulte)
        pygame.draw.rect(fenetre, (200, 200, 200), rect_insérer)
        pygame.draw.rect(fenetre, (200, 200, 200), rect_quitter)

        fenetre.blit(texte_menu_jouer, (LARGEUR // 2 - texte_menu_jouer.get_width() // 2, HAUTEUR // 2 - 125 + rect_jouer.height // 2 - texte_menu_jouer.get_height() // 2))
        fenetre.blit(texte_menu_difficulte, (LARGEUR // 2 - texte_menu_difficulte.get_width() // 2, HAUTEUR // 2 - 75 + rect_difficulte.height // 2 - texte_menu_difficulte.get_height() // 2))
        fenetre.blit(texte_menu_insérer, (LARGEUR // 2 - texte_menu_insérer.get_width() // 2, HAUTEUR // 2 - 25 + rect_insérer.height // 2 - texte_menu_insérer.get_height() // 2))
        fenetre.blit(texte_menu_quitter, (LARGEUR // 2 - texte_menu_quitter.get_width() // 2, HAUTEUR // 2 + 25 + rect_quitter.height // 2 - texte_menu_quitter.get_height() // 2))

        options_rect = [rect_jouer, rect_difficulte, rect_insérer, rect_quitter]

        for rect in options_rect:
            pygame.draw.rect(fenetre, BLANC, rect)

        pos = pygame.mouse.get_pos()
        survol_option = detecter_survol_option(options_rect, pos)

        for i, option_rect in enumerate(options_rect):
            texte_option = [texte_menu_jouer, texte_menu_difficulte, texte_menu_insérer, texte_menu_quitter][i]

            # Appliquer l'effet de zoom si l'option est survolée
            if survol_option == option_rect:
                scale = 1.2
                texte_option = pygame.transform.scale(texte_option, (int(texte_option.get_width() * scale), int(texte_option.get_height() * scale)))

            fenetre.blit(
                texte_option,
                (option_rect.x + option_rect.width // 2 - texte_option.get_width() // 2, option_rect.y + option_rect.height // 2 - texte_option.get_height() // 2)
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_jouer.collidepoint(event.pos):
                    difficulte = afficher_menu_difficulte(fenetre, font)
                    jouer_partie(difficulte)
                elif rect_difficulte.collidepoint(event.pos):
                    difficulte = afficher_menu_difficulte(fenetre, font)
                    jouer_partie(difficulte)
                elif rect_insérer.collidepoint(event.pos):
                    ajouter_mot(fenetre)
                elif rect_quitter.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def jouer_partie(difficulte):
    global menu_actif
    arreter_musique()
    mot_a_deviner = choisir_mot(difficulte).upper()
    lettres_trouvees = set()
    erreurs = 0

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu du Pendu")

    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    lettre = event.unicode.upper()
                    if lettre not in lettres_trouvees:
                        lettres_trouvees.add(lettre)
                        if lettre not in mot_a_deviner:
                            erreurs += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retour_box.collidepoint(event.pos):
                    return  # Retour au menu principal

        fenetre.fill(BLANC)

        mot_affiche = ""
        for lettre_mot in mot_a_deviner:
            if lettre_mot in lettres_trouvees:
                mot_affiche += lettre_mot + " "
            else:
                mot_affiche += "_ "

        texte_mot = font.render(mot_affiche, True, NOIR)
        fenetre.blit(texte_mot, (LARGEUR // 2 - 100, HAUTEUR // 2 - 50))

        dessiner_bonhomme(fenetre, erreurs)

        if erreurs == 6:
            texte_fin = font.render("Perdu ! Le mot était : " + mot_a_deviner, True, ROUGE)
            fenetre.blit(texte_fin, (LARGEUR // 2 - 200, HAUTEUR // 2 + 50))
            pygame.display.flip()
            pygame.time.delay(2000)  # Pause de 2 secondes
            return
        elif "_" not in mot_affiche:
            texte_fin = font.render("Bravo ! Vous avez trouvé le mot : " + mot_a_deviner, True, ROUGE)
            fenetre.blit(texte_fin, (LARGEUR // 2 - 250, HAUTEUR // 2 + 50))
            pygame.display.flip()
            pygame.time.delay(2000)  # Pause de 2 secondes
            return

        retour_box = pygame.Rect(LARGEUR - 100, 0, 100, 50)
        pygame.draw.rect(fenetre, (200, 200, 200), retour_box)
        texte_retour = font.render("Retour", True, NOIR)
        fenetre.blit(texte_retour, retour_box.topleft)

        pygame.display.flip()
        clock.tick(30)
        gerer_musique()

def ajouter_mot(fenetre):
    input_box = pygame.Rect(LARGEUR // 2 - 200, HAUTEUR // 2 - 25, 400, 50)
    retour_box = pygame.Rect(LARGEUR - 100, 0, 100, 50)  # Zone pour le bouton Retour
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_retour = pygame.Color('green')  # Couleur pour le bouton Retour
    color = color_inactive
    retour_color = color_retour  # Couleur pour le bouton Retour
    active = True
    retour_active = False  # Activation du bouton Retour
    text = ''
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif retour_box.collidepoint(event.pos):
                    return  # Retour au menu principal
                else:
                    active = False
                color = color_active if active else color_inactive
                retour_active = True if retour_box.collidepoint(event.pos) else False
                retour_color = color_retour if retour_active else color_retour

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        with open(r"pendu\mots.txt", "a", encoding="utf-8") as fichier:
                            fichier.write("\n" + text + " ")
                        pygame.time.delay(1000)  # Pause de 1 seconde
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    return  # Retour au menu principal

        fenetre.fill(BLANC)
        pygame.draw.rect(fenetre, color, input_box, 2)
        texte_entree = font.render(text, True, NOIR)
        fenetre.blit(texte_entree, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(fenetre, retour_color, retour_box, 2)  # Dessine la zone du bouton Retour
        texte_retour = font.render("Retour", True, NOIR)
        fenetre.blit(texte_retour, retour_box.topleft)

        pygame.display.flip()

if __name__ == "__main__":
    jouer_pendu()
