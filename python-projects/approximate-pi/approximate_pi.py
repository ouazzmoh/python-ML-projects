#!/usr/bin/env python3

"""Ce module sert a approximer la valeur de Pi a l'aide de l'algorithme de Monte-Carlo
    Ce module fournit les points aleatoire genere dans
    le carré et leur apppartenance dans le cercle sous la forme (x,y,True)"""


#Librairies standards de Python
from random import uniform
from sys import argv



def generer_iterateur_points(nbr_de_points):
    """Generer iterateur des points sous la forme (i ,j ,True)"""
    for _ in range(nbr_de_points):
        point = (uniform(-1, 1), uniform(-1, 1))
        cercle = False
        if point[0]**2 + point[1]**2 <= 1:
            cercle = True
        yield (point[0], point[1], cercle)

def approximation(nbr_de_points):
    """Approxime pi """
    compteur = 0
    for point in generer_iterateur_points(nbr_de_points):
        if point[2]: #Test d'appartenance dans le cercle
            compteur += 1
    return 4*(compteur/nbr_de_points)



if __name__ == "__main__":
    try:
        N = int(argv[1])
        assert N > 0
        print(approximation(N))
    except IndexError:
        print("Il faut utiliser le script comme suit : ./approximate.py nombre_de_points")
    except ValueError:
        print("Il faut entrer un entier")
    except AssertionError:
        print("Il faut entrer un entier positif")
