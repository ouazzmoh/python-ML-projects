# reconstruction.py

"""========================================================================
Bibliothèque 
    de fonctions pour la reconstruction géométrique
    des données issues de la kinect :

--> Moindres carrées sans contraintes
    def moindres_carres (x3,y3,z3,nb_noeudsT,nb_noeudsY,th3,VnoeudsT,VnoeudsY):

--> Moindres carrées avec contraintes
    def moindres_carres_contrainte(ATA,ATx,ATy,ATz,Bx,By,Bz,H,nb_noeudsT,nb_noeudsY):
        
--> Réseau des points de contrôle
    def point_de_controle(pcxx,pcyy,pczz,nbPC,nb_noeudsY,nb_noeudsT):

========================================================================"""

from ToolsBsplines3D import *


def moindres_carres (x3,y3,z3,nb_noeudsT,nb_noeudsY,th3,VnoeudsT,VnoeudsY):
    """
    approximation moindres carrée sans contraintes:
    Construction du systeme principal : "normal equations"
    Input : x3,y3,z3 (les points sur lesquels on fait les calculs)
            nb_noeudsT,nb_noeudsY (nombre de noeuds)
            th3 (angles associés aux points)
            VnoeudsT,VnoeudsY (vecteur des noeuds)
    Output : ATA,ATx,ATy,ATz (matrices des equations normales)
             nbC (nombre de points de contrôle)
    """
    # matrice moindre carré
    #On cherche a resoudre le probleme Ax = B avec x les points de controle voulu
    # construction de la matrice A pour les moindres carrés
    nbData3 = len(x3)
    nbPC    = (nb_noeudsY + 2) * (nb_noeudsT + 2)
    A = np.zeros((nbData3,nbPC))
    # construction de la matrice A pour les moindres carrés
    for ligne in range(nbData3) :
        col = 0
        for i in range(nb_noeudsT+2):
            for j in range(nb_noeudsY+2):
                A[ligne][col] = Bspline(VnoeudsT, i, th3[ligne]) * Bspline(VnoeudsY, j, y3[ligne])
                col += 1

    
    x3 = np.array(x3)
    y3 = np.array(y3)
    z3 = np.array(z3)
    
    # Equations normales :
    ATA = np.dot(np.transpose(A), A)
    print("Determinant de ATA :", np.linalg.det(ATA))
    ATx = np.dot(np.transpose(A), x3)
    ATy = np.dot(np.transpose(A), y3)
    ATz = np.dot(np.transpose(A), z3)
    
    #Résolution directe des équations normales ( avec linalg.solve)
    pcx = np.linalg.solve(ATA, ATx)
    pcy = np.linalg.solve(ATA, ATy)
    pcz = np.linalg.solve(ATA, ATz)

    #affichage moindre carrées sans contraintes
    fig = plt.figure()
    ax0 = plt.axes(projection='3d')
    ax0.set_xlabel('x axis')
    ax0.set_ylabel('y axis')
    ax0.set_zlabel('z axis')
    ax0.set_title('moindre carrées sans contraintes')
    ax0.scatter(x3, y3, z3, color='r', marker='o', s=0.3)
    ax0.plot3D(pcx,pcy,pcz, 'co--', lw=1, ms=5) 
    
    plt.show()


    return(ATA,ATx,ATy,ATz,nbPC)
    


def moindres_carres_contrainte(ATA,ATx,ATy,ATz,Bx,By,Bz,H,nb_noeudsT,nb_noeudsY):
    """
    approximation moindres carrés avec contraintes:
    Construction de la matrice des moindres carrés avec
    des contraintes linéaires
    Input : ATA,ATx,ATy,ATz (equations normales principales)
            Bx,By,Bz,H (matrices des contraintes)
            nb_noeudsT,nb_noeudsY (nombre de noeuds)
    Output : pcxx,pcyy,pczz (les points de controle, mais non correctement structurés...)
    """
    # matrice principale AHH
    A_0 = np.zeros((H.shape[0], H.shape[0]))
    ATx = np.array(ATx)
    ATy = np.array(ATy)
    ATz = np.array(ATz)
    A_1 = np.concatenate((ATA, np.transpose(H)), axis=1)
    A_2 = np.concatenate((H, A_0), axis=1)
    AHH = np.concatenate((A_1, A_2), axis=0)

    
    # deuxieme membre
    ATBx = np.concatenate([ATx, Bx])
    ATBy = np.concatenate([ATy, By])
    ATBz = np.concatenate([ATz, Bz])
    
    # Resolution directe (with linalg.solve)
    pcxx = np.linalg.solve(AHH, ATBx)
    pcyy = np.linalg.solve(AHH, ATBy)
    pczz = np.linalg.solve(AHH, ATBz)
    
    return(pcxx,pcyy,pczz)



def point_de_controle(pcxx,pcyy,pczz,nbPC,nb_noeudsY,nb_noeudsT):
    """
    Fabrication du Réseau des points de contrôle
    Input : pcxx,pcyy,pczz (les points)
            nbPC (nombre points de controle)
            nb_noeudsY,nb_noeudsT (nombres de noeuds)
    Output : PCX,PCY,PCZ (les points de controle structurés)
    """
    # on récupère des points de contrôles
    pcx = pcxx[:nbPC]
    pcy = pcyy[:nbPC]
    pcz = pczz[:nbPC]
    
    PCX = pcx.reshape(nb_noeudsY+2,nb_noeudsT+2)
    PCY = pcy.reshape(nb_noeudsY+2,nb_noeudsT+2)
    PCZ = pcz.reshape(nb_noeudsY+2,nb_noeudsT+2)
    PCX = PCX.T
    PCY = PCY.T
    PCZ = PCZ.T
    return(PCX,PCY,PCZ)
