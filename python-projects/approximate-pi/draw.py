#!/usr/bin/env python3

"""Approximer Pi à l'aide du méthode de MonteCarlo et l'afficher sous format gif"""""

#Librairies standards de Python
from sys import argv
import subprocess
from copy import deepcopy

#Module crée
from approximate_pi import generer_iterateur_points



def frac_to_pixels(frac, pixels):
    """Pour y dans [0,1] eon le transforme en pixels avec pixels(1-y)//2"""
    return int((pixels*(1-frac))//2)

def generate_ppm_file(pixels, compteur_pi, compteur_genere):
    """Génerer un image"""
    compteur_boucle = 0
    for point in generer_iterateur_points(int(NBR_DE_POINTS*0.10)):
        compteur_genere += 1
        if compteur_boucle == NBR_DE_POINTS*0.10:
            break
        i, j, cercle = frac_to_pixels(point[0], pixels), frac_to_pixels(point[1], pixels), point[2]
        if cercle:
            LISTE_DES_PIXELS[i][j] = COULEUR_CERCLE
            compteur_pi += 1
        else:
            LISTE_DES_PIXELS[i][j] = COULEUR_HORS_CERCLE
        compteur_boucle += 1
    valeur_pi = 4*(compteur_pi/compteur_genere)
    valeur_pi_chaine = f"{valeur_pi:.{VIRGULE+1}f}"
    if K == 0:
        filename = f"img0_{valeur_pi_chaine[0]}-{valeur_pi_chaine[2:-1]}"
    else:
        filename = f"img{str(K)}_{valeur_pi_chaine[0]}-{valeur_pi_chaine[2:-1]}"
    to_draw = deepcopy(LISTE_DES_PIXELS)
    trace_nombre(pixels, to_draw, valeur_pi_chaine[0]+valeur_pi_chaine[2:-1])
    with open(filename+".ppm", "wb")  as file:
        file.write(f"P6 {str(pixels)} {str(pixels)} 255\n".encode("UTF-8"))
        for ligne in to_draw:
            for un_pixel in ligne:
                file.write(un_pixel)


def trace_segment(pt1, pt2, image):
    """Image sous forme d'une liste, et trace un segement entre pt1 et pt2
    On se limite au tracage des segments horizontals et vertical
    COULEUR sous la forme d'un tuple(X,X,X)"""
    #Pour les points on adopte la presentation ligne colonne
    ligne1, col1 = pt1[0], pt1[1]
    ligne2, col2 = pt2[0], pt2[1]
    if ligne1 == ligne2:
        for k in range(min(col1, col2), max(col1, col2)+1):
            image[ligne1][k] = COULEUR
            for i in range(STROKE):
                image[ligne1-i][k] = COULEUR
                image[ligne1+i][k] = COULEUR
    elif col1 == col2:
        for k in range(min(ligne1, ligne2), max(ligne1, ligne2)+1):
            image[k][col1] = COULEUR
            for i in range(STROKE):
                image[k][col1-i] = COULEUR
                image[k][col1+i] = COULEUR
    else:
        print("Only horizontal or vertical")
    return image

def trace_point(position, image):
    """Posiiton sous la forme de (x,y), le pixel initial et au botleft"""
    i, j = position[0], position[1]
    image[i][j] = COULEUR
    for k in range(STROKE*3):
        for k_2 in range(STROKE*3):
            image[i-k][j] = COULEUR
            image[i-k][j+k_2] = COULEUR
            image[i][j+k_2] = COULEUR
    return image

def trace_nombre(pixels, image, nombre):
    """Tracer un nombre"""
    chiffres = list(nombre)
    seg = int((pixels/2)*ALPHA)
    lignes = [int((pixels//2)*(1-ALPHA)), pixels//2, int((pixels//2)*(1+ALPHA))]
    ####Position du premier ord varie selon le nombre de chiffre
    if len(chiffres) == 1:
        col1 = pixels//2 - seg//2
    elif len(chiffres) == 2:
        col1 = pixels//2 - seg - SEP//2
    elif len(chiffres) == 3:
        col1 = pixels//2 - seg//2 - SEP - seg
    elif len(chiffres) == 4:
        col1 = pixels//2 - SEP//2 - seg - SEP - seg
    elif len(chiffres) == 5:
        col1 = pixels//2 - seg//2 - SEP - seg - SEP - seg
    elif len(chiffres) == 6:
        col1 = pixels//2 - SEP//2 - seg - SEP - seg - SEP - seg
    else:
        print("On ne trace que Pi")
    col2 = col1 + seg
    ords = [(col1, col2)]
    for k in range(len(chiffres)-1):
        jp1 = ords[k][1] + SEP
        jp2 = jp1 + seg
        ords.append((jp1, jp2))
    jpoint = (ords[1][0] + ords[0][1]) // 2
    trace_point((lignes[2], jpoint), image)
    for k in enumerate(ords):
        col1 = ords[k[0]][0]
        col2 = ords[k[0]][1]
        pts = [
            (lignes[0], col1),
            (lignes[0], col2),
            (lignes[1], col1),
            (lignes[1], col2),
            (lignes[2], col1),
            (lignes[2], col2)
            ]
        map_segments_points = {
            "top" : (pts[0], pts[1]),
            "topright"  : (pts[1], pts[3]),
            "topleft" : (pts[0], pts[2]),
            "mid" : (pts[2], pts[3]),
            "botright" : (pts[3], pts[5]),
            "bot" : (pts[4], pts[5]),
            "botleft" : (pts[2], pts[4]),
        }
        for segment in MAP_7_SEGMENT[int(chiffres[k[0]])]:
            trace_segment(map_segments_points[segment][0], map_segments_points[segment][1], image)
    return image



if __name__ == "__main__":
    if len(argv) != 4:
        print("Use: ./draw.py nombre_de_pixels nombre_de_points chiffre_après_virgules")
    try:
        int(argv[1])
        int(argv[2])
        int(argv[3])
    except TypeError:
        print("Les entrées sur l'entrée standard doivent être des entiers")

    if int(argv[1]) < 100 or int(argv[2]) < 100 or not 1 <= int(argv[3]) <= 5:
        raise ValueError("Il faut que:PIXELS >= 100 NBR_DE_POINTS >= 1000  1 <= VIRGULE <= 5 ")

    PIXELS, NBR_DE_POINTS, VIRGULE = int(argv[1]), int(argv[2]), int(argv[3])

    #Compteurs pour calculer pi
    COMPTEUR_PI, COMPTEUR_GENERE = 0, 0

    COULEUR_BACKGROUND = b'\xff\xff\xff'
    COULEUR_CERCLE = b'\x00\xff\x00'
    COULEUR_HORS_CERCLE = b'\xff\x00\x00'
    COULEUR = b'\x00\x00\x00'

    #IMAGE
    LISTE_DES_PIXELS = [[COULEUR_BACKGROUND for _ in range(PIXELS)] for _ in range(PIXELS)]

    #Paramètre d'affichage
    ALPHA = 0.08 #Pourcentage que le segment va prendre de pixels//2
    SEP = 10 #Nombre de pixels qui SEParent les chiffres
    STROKE = 2 #Taille des segments de chiffres
    MAP_7_SEGMENT = {
        0 : ["top", "topright", "topleft", "botright", "botleft", "bot"],
        1: ["topright", "botright"],
        2: ["top", "topright", "mid", "botleft", "bot"],
        3: ["top", "topright", "mid", "botright", "bot"],
        4: ["topright", "topleft", "mid", "botright"],
        5: ["top", "topleft", "mid", "botright", "bot"],
        6: ["top", "topleft", "mid", "botright", "botleft", "bot"],
        7: ["top", "topright", "botright"],
        8: ["top", "topright", "topleft", "mid", "botright", "botleft", "bot"],
        9: ["top", "topright", "topleft", "mid", "botright", "bot"]
    }

    #Pour afficher 10 images
    for K in range(10):
        generate_ppm_file(PIXELS, COMPTEUR_PI, COMPTEUR_GENERE) #On prend 10% pour chaque image

    #Convertir en GIF
    subprocess.run("convert -delay 100 img*.ppm animatedpi.gif", check=True, shell=True)
