# preparation.py


"""========================================================================
Bibliothèque
    de fonctions pour l'acquisition et la mise en place des données

--> Récupération et centralisation des données du fichier Mesh
    def acquisition(nom_fichierPly):

--> barycentre à l'origine pour centrer le visage sur nos axes
    def barycentre (x,y,z,NbPts):
        
--> Selection des points de devant (de la figure)
    def pointsdevant(X0,Y0,Z0):

--> rotation d'un angle autour de l'axe x sur les données de devant
    def rotationX(xu,yu,xA,yA,zA,X0,Y0,Z0):
        
--> rotation d'un angle autour de l'axe y sur les données en avant
    def rotationY(xu,yu,xA,yA,zA,X1,Y1,Z1):    
========================================================================"""

from tkinter import Y
from ToolsMesh import *
from math import atan, cos, sin, pi
import numpy as np

"""-----------------------------------------------------
MISE EN PLACE
-----------------------------------------------------"""

def acquisition(nom_fichierPly):
    """ 
    On récupère la tête entière, avec probablement des trous à l'arrière
    la sélection de la zone à approximer est faite dans Python
    Input : Nom d'un fichier
    Output : X0,Y0,Z0,Nbtps les points du fichier recentrés
    """

    FilePly = str(nom_fichierPly) # attention au chemin
    x,y,z = CoordonneesFromPly(FilePly) #Liste des pts duy maillage 
    NbPts = len(x)
    print("Nombre de points : ",NbPts)
    return (barycentre(x,y,z,NbPts))


def barycentre (x,y,z,NbPts):
    """
    barycentre à l'origine pour centrer le visage sur nos axes
    Input : x,y,z,Nbtps : des points et le nombre de points associé
    Output : X0,Y0,Z0,NbPts : les points recentrés et le nombre de points
    """
    #TODO: FOR ALL COORDINATES X0  = X - XB
    # Barycentre (xb,yb,zb)
    xb = sum(x)/NbPts
    yb = sum(y)/NbPts
    zb = sum(z)/NbPts
    # translation pour ramener le barycentre à l'origine
    X0 = [x[i] - xb for i in range(NbPts)]
    Y0 = [y[i] - yb for i in range(NbPts)]
    Z0 = [z[i] - zb for i in range(NbPts)]
    return (X0,Y0,Z0,NbPts)
    

"""-----------------------------------------------------
SELECTION DES POINTS DE DEVANT
-----------------------------------------------------"""

def pointsdevant(X0,Y0,Z0):
    """
    Pour mieux visualiser et sélectionner les rotations à effectuer 
    on sélectionne les points de "devant", cad tels que zA > 0.
    Input :  X0,Y0,Z0 = les points 
    Output : xA,yA,zA = les points de "devant"
    """
    NbPts = len(X0)
    xA, yA, zA = [], [], []
    for i in range(NbPts):
        if Z0[i] > 0:
            xA.append(X0[i])
            yA.append(Y0[i])
            zA.append(Z0[i])
    return (xA,yA,zA)


"""-----------------------------------------------------
FONCTIONS DE ROTATIONS
-----------------------------------------------------"""

def rotationX(xu,yu,xA,yA,zA,X0,Y0,Z0):
    """
    rotation autour de l'axe x
    Input : xu,yu (vecteur qui défini l'angle de rotation : 
                   on veut que ce vecteur soit horizontal)
            xA,yA,zA  (les points de devant pour l'affichage)
            X0,Y0,Z0  (l'entièreté des points à faire bouger)
    Output : Xdisp,Ydisp,Zdisp (les points d'affichage)
             X1,Y1,Z1 (l'entiereté des points après rotation)
    """
    
    Vx = xu[1]-xu[0]
    Vy = yu[1]-yu[0]
    # Vx supposé non nul, sinon pas besoin de rotation
    ##Determination de l'angle de rotation
    cos_alpha = Vx/((Vx**2 + Vy**2)**(1/2))
    sin_alpha = Vy/((Vx**2 + Vy**2)**(1/2))
    R_x_matrix = np.matrix([[1, 0, 0], 
                        [0, cos_alpha, -sin_alpha],
                        [0, sin_alpha, cos_alpha]] )
    # on fait d'abord  tourner uniquement la sélection (xA,yA,zA) pour controle
    new_disp = [np.matmul(R_x_matrix, np.array([xA[i], yA[i], zA[i]])).tolist() for i in range(len(xA))]
    Xdisp = [new_disp[i][0][0] for i in range(len(xA))]
    Ydisp = [new_disp[i][0][1] for i in range(len(yA))]
    Zdisp = [new_disp[i][0][2] for i in range(len(zA))]
    #on affichera ces données
    #On fait la rotation maintenant sur l'ensemble des données
    new_1 = [np.matmul(R_x_matrix, np.array([X0[i], Y0[i], Z0[i]])).tolist() for i in range(len(X0))]
    X1 = [new_1[i][0][0] for i in range(len(X0))]
    Y1 = [new_1[i][0][1] for i in range(len(Y0))]
    Z1 = [new_1[i][0][2] for i in range(len(Z0))]    
    return(Xdisp,Ydisp,Zdisp,X1,Y1,Z1)
    

def rotationY(xu,yu,xA,yA,zA,X1,Y1,Z1):
    """
    rotation autour de l'axe y
    Input : xu,yu (vecteur qui défini l'angle de rotation : 
                   on veut que ce vecteur soit vertical)
            xA,yA,zA  (les points de devant pour l'affichage)
            X1,Y1,Z1  (l'entièreté des points à faire bouger)
    Output : Xdisp,Ydisp,Zdisp (les points d'affichage)
             X2,Y2,Z2 (l'entiereté des points après rotation)
    """
    
    Vx = xu[1]-xu[0]
    Vy = yu[1]-yu[0]
    # Vx supposé non nul, sinon pas besoin de rotation
    cos_alpha = Vy/((Vx**2 + Vy**2)**(1/2))
    sin_alpha = Vx/((Vx**2 + Vy**2)**(1/2))
    R_y_matrix = np.matrix([[cos_alpha, 0, sin_alpha], 
                        [0,             1,        0],
                        [-sin_alpha, 0, cos_alpha]])
    # on fait d'abord  tourner uniquement la sélection (xA,yA,zA) pour controle
    new_disp = [np.matmul(R_y_matrix, np.array([xA[i], yA[i], zA[i]])).tolist() for i in range(len(xA))]
    Xdisp = [new_disp[i][0][0] for i in range(len(xA))]
    Ydisp = [new_disp[i][0][1] for i in range(len(yA))]
    Zdisp = [new_disp[i][0][2] for i in range(len(zA))]
    #On fait maintenant la rotation sur l'ensemble des elements
    new_2 = [np.matmul(R_y_matrix, np.array([X1[i], Y1[i], Z1[i]])).tolist() for i in range(len(X1))]
    X2 = [new_2[i][0][0] for i in range(len(X1))]
    Y2 = [new_2[i][0][1] for i in range(len(Y1))]
    Z2 = [new_2[i][0][2] for i in range(len(Z1))]   
    return(Xdisp,Ydisp,Zdisp,X2,Y2,Z2)

