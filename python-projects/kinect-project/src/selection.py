#selection.py

"""========================================================================
Bibliothèque 
    decoupage et récupération des données/points/angles

--> donne les points de la zone choisie et l'angle associé
    ainsi que les points complémentaires et leur angle associé
    def anglepoints(x2,y2,z2,thetaMin,thetaMax,ym,yM):

========================================================================"""

import numpy as np
from math import atan, pi


def anglepoints(x2,y2,z2,thetaMin,thetaMax,ym,yM):
    """
    permet de récuperer les points de la zone choisie, leur indice 
    ainsi que leur angle associé
    de plus permet de recuperer les points complémentaires, leur indice,
    et leur angle associé
    Input : x2,y2,z2 (les coordonnées de tous les points)
            thetaMin,thetaMax (angles minimum et maximum)
            ym,yM (les hauteurs min et max)
    Output : x3,y3,z3 (les coordonnées de la zone choisie)
             t3 (les indices de ces points pour le retour dans Meshlab)
             th3 (les angles theta associés)
             x3c,y3c,z3c (les points complémentaires)
             t3c (les indices de ces points pour le retour dans Meshlab)
    """
    # #------------------------------------
    # # angles des points (x2,y2,z2):
    # # on détermine l'angle theta associé à chaque point (x2,y2,z2)
    # #------------------------------------
    
    theta = []
    for i in range(len(z2)):    
        if z2[i] == 0 :
            print("Danger divZ par 0!!!! La figure a été mal choisie")
            theta.append(0)
        else:
            theta_i = -atan(x2[i]/z2[i]).real
            if z2[i] < 0 : theta_i += np.pi
            theta.append(theta_i)
    
    if ym < min(y2) or yM> max(y2):
        print("La figure a été mal choisie")
    
    #---------------------------------------------------------
    # selection des points selon la coordonnées y et l'angle 
    #---------------------------------------------------------
    Points, Points_c = [], []
    for i in range(len(y2)):
        if y2[i] > ym and y2[i] < yM and theta[i] < thetaMax and theta[i] > thetaMin :
            Points.append((x2[i], y2[i], z2[i], theta[i], i))
        else:
            Points_c.append((x2[i], y2[i], z2[i], theta[i], i))
    x3 = [Points[i][0] for i in range(len(Points))]
    y3 = [Points[i][1] for i in range(len(Points))]
    z3 = [Points[i][2] for i in range(len(Points))]
    th3 = [Points[i][3] for i in range(len(Points))]
    t3 = [Points[i][4] for i in range(len(Points))]
    x3c = [Points_c[i][0] for i in range(len(Points_c))]
    y3c = [Points_c[i][1] for i in range(len(Points_c))]
    z3c = [Points_c[i][2] for i in range(len(Points_c))]
    t3c = [Points_c[i][4] for i in range(len(Points_c))]
  
    return (x3,y3,z3,x3c,y3c,z3c,t3,th3,t3c)