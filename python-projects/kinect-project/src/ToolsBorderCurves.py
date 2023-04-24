# ToolsBorderCurves.py

"""========================================================================
Bibliothèque
    Detection and B-spline approximation of the 4 border curves 
    of the selected area

--> B-spline approximation of 2D-data
    def curve_approximation(xx,yy,zz,tt,nb_noeuds):

--> Detection and B-spline approximation of the border curves (method M4)
    BE CAREFUL : corner points are not necessary identical
    def BorderCurvesM4(x2,y2,z2,thetaMin,thetaMax,ym,yM,
                       err1,err2,nbLR,nbTB,disp):

--> Definition of the linear system of constraints 
    associated with the border curves of the B-spline surfaces
    def ConstraintsSystem(nb_noeudsT,nb_noeudsY,LC,RC,TC,BC):
========================================================================"""
from ToolsBsplines3D import *
from numpy import arctan, arccos

#-------------------------------------------------------------------
# B-spline approximation of 2D-data (in 3D space)
def curve_approximation(xx,yy,zz,tt,a,b,nb_noeuds):
    """
    Approximation of data (xx,yy,zz) according to parameters tt
    on the interval [a,b]
    by a uniform cubic Bspline curve with "nb_noeuds" knots 
    Output : pcx, pcy, pcz : Bspline control points coordinates
             xs, ys, zs : sampling of the Bspline solution
    """
    N = len(xx)
    # sequence of uniform Bspline knots :
    tk = np.linspace(a, b, nb_noeuds)
    # least squares approximation matrix :
    A = np.zeros((N,nb_noeuds+2))
    for ligne in range(N) :
        for i in range(nb_noeuds+2):
            A[ligne][i] = Bspline(tk, i , tt[ligne])
    
    #Making sure the passed arguments are arrays
    xx = np.array(xx)
    yy = np.array(yy)
    zz = np.array(zz)
    
    # Normal equations :
    
    ATA = np.dot(np.transpose(A), A)
    ATx = np.dot(np.transpose(A), xx)
    ATy = np.dot(np.transpose(A), yy)
    ATz = np.dot(np.transpose(A), zz)


    # resolution with numpy :
    pcx = np.linalg.solve(ATA, ATx)
    pcy = np.linalg.solve(ATA, ATy)
    pcz = np.linalg.solve(ATA, ATz)
    
    xs, ys, zs = Bspline3DCurveEvaluation(pcx,pcy,pcz,tk)
    return pcx, pcy, pcz, xs, ys, zs


#-------------------------------------------------------------------
# Detection and B-spline approximation of the border curves (method M4)
# BE CAREFUL : corner points are not necessary identical
def BorderCurvesM4(x2,y2,z2,thetaMin,thetaMax,ym,yM,err1,err2,nbLR,nbTB,disp):
    """
        Detection and B-spline approximation of the border curves 
        of the selected area
        --> for method M4
        (x2,y2,z2) : coordinates of all points
        thetaMin,thetaMax,ym,yM : parameters of the selected area
        err1 : angular error
        err2 : vertical error (according y-coordinates)
        nbLR : number of knots for Left & Right curves
        nbTB : number of knots for Top & Bottom curves
        disp = boolean : for display (or not) of the reconstructed curves
        Return control points of each border curve
            and the figure axes 'ax0'
        --> BE CAREFUL : corner points are not necessary identical !!!
    """

    # # Adapt the definition of theta that we have chosen to the one defined now

    #----------------------------------------------
    #graphic windows for display
    #----------------------------------------------
    if disp :
        fig = plt.figure()
        ax0 = plt.axes(projection='3d')
        ax0.set_xlabel('x axis')
        ax0.set_ylabel('y axis')
        ax0.set_zlabel('z axis')
        ax0.set_title('border curves')
    
    #------------------------------------
    # Cylindrical coordinates
    # on détermine la distance r et l'angle theta 
    # associé à chaque point (x2,y2,z2)
    #------------------------------------
    
    x2 = np.array(x2)
    y2 = np.array(y2)
    z2 = np.array(z2)


    r2 = (x2**2 + z2**2)**(1/2)
    th2 = -np.arctan(x2/z2)
    for k in range(len(x2)):
        if z2[k] < 0:
            th2[k] += np.pi

    """------------------------------------------------------------
    DETECTION of points close to the borders for approximation
    ------------------------------------------------------------"""  
    error1 = err1 # angular error
    n = len(x2)
    #--------------------------------------------------------------
    # LEFT CURVE (from observer) 
    #--------------------------------------------------------------
    # kept data for approximation
    xLC = []
    yLC = []
    zLC = []
    
    for i in range(n):
        if   ym < y2[i] < yM and thetaMin - err1 < th2[i] < thetaMin + err1:
            xLC.append(x2[i])
            yLC.append(y2[i])
            zLC.append(z2[i])
    
    if disp :
        ax0.scatter(xLC, yLC, zLC, color='b', marker='o', s=0.5) 
    
    #--------------------------------------------------------------
    # RIGHT CURVE (from observer) 
    #--------------------------------------------------------------
    # kept data for approximation
    xRC = []
    yRC = []
    zRC = []
    for i in range(n):
        if ym < y2[i] < yM and thetaMax - err1 < th2[i] < thetaMax + err1:
            xRC.append(x2[i])
            yRC.append(y2[i])
            zRC.append(z2[i])
    
    if disp :
        ax0.scatter(xRC, yRC, zRC, color='r', marker='o', s=0.5) 
        
    error2 = err2 # vertical error

    #--------------------------------------------------------------
    # TOP CURVE 
    #--------------------------------------------------------------
    # kept data for approximation
    xTC = []
    yTC = []
    zTC = []
    thTC = [] # we keep angle theta associated with each point for reconstruction
    
    for i in range(n):
        if thetaMin < th2[i] < thetaMax and yM- err2 < y2[i] < yM + err2:
            xTC.append(x2[i])
            yTC.append(y2[i])
            zTC.append(z2[i])
            thTC.append(th2[i])
    
    if disp :
        ax0.scatter(xTC, yTC, zTC, color='c', marker='o', s=0.5) 
        
    #--------------------------------------------------------------
    # BOTTOM CURVE 
    #--------------------------------------------------------------
    # kept data for approximation
    xBC = []
    yBC = []
    zBC = []
    thBC = [] # we keep angle theta associated with each point for reconstruction
    for i in range(n):
        if thetaMin < th2[i] < thetaMax and ym - err2 < y2[i] < ym + err2:
            xBC.append(x2[i])
            yBC.append(y2[i])
            zBC.append(z2[i])
            thBC.append(th2[i]) 
    
    if disp :
        ax0.scatter(xBC, yBC, zBC, color='g', marker='o', s=0.5) 
    

    #---------------------
    # Manging the control points
    #---------------------
    first_LC, last_LC = 0, 0

    



    """------------------------------------------------------------
    APPROXIMATION of Border curves
    ------------------------------------------------------------"""    
    #----------------------
    # Left curve
    #----------------------
    nb_noeudsG = nbLR
    a = ym
    b = yM
    pcxL, pcyL, pczL, xsL, ysL, zsL = curve_approximation(
        xLC, yLC, zLC, yLC, a, b, nb_noeudsG)
    LC = (pcxL, pcyL, pczL)
    if disp :
        # display of control polygon
        ax0.plot3D(pcxL,pcyL,pczL, 'bo--', lw=1, ms=5) 
        # B-spline
        ax0.plot3D(xsL,ysL,zsL,'b',lw=1)
    
    #----------------------
    # Right curve
    #----------------------
    nb_noeudsD = nbLR
    a = ym
    b = yM
    pcxR, pcyR, pczR, xsR, ysR, zsR = curve_approximation(
        xRC, yRC, zRC, yRC, a, b, nb_noeudsD)
    RC = (pcxR, pcyR, pczR)
    if disp :
        # display of control polygon
        ax0.plot3D(pcxR,pcyR,pczR, 'ro--', lw=1, ms=5) 
        # B-spline
        ax0.plot3D(xsR,ysR,zsR,'r',lw=1)
    
    #----------------------
    # Top curve
    #----------------------
    nb_noeudsH = nbTB
    a = thetaMin
    b = thetaMax
    pcxT, pcyT, pczT, xsT, ysT, zsT = curve_approximation(
        xTC, yTC, zTC, thTC, a, b, nb_noeudsH)
    TC = (pcxT, pcyT, pczT)
    if disp :
        # display of control polygon
        ax0.plot3D(pcxT,pcyT,pczT, 'co--', lw=1, ms=5) 
        # B-spline
        ax0.plot3D(xsT,ysT,zsT,'c',lw=1)
    
    #----------------------
    # Bottom curve
    #----------------------
    nb_noeudsB = nbTB
    a = thetaMin
    b = thetaMax
    pcxB, pcyB, pczB, xsB, ysB, zsB = curve_approximation(
        xBC, yBC, zBC, thBC, a, b, nb_noeudsB)
    BC = (pcxB, pcyB, pczB)
    if disp :
        # display of control polygon
        ax0.plot3D(pcxB,pcyB,pczB, 'go--', lw=1, ms=5) 
        # B-spline
        ax0.plot3D(xsB,ysB,zsB,'g',lw=1) 

    return LC, RC, TC, BC, ax0


#-------------------------------------------------------------------
# Definition of the linear system of constraints : 'couture'
# associated with the border curves of the B-spline surfaces
def ConstraintsSystem(nb_noeudsT,nb_noeudsY,LC,RC,TC,BC):
    """
        Definition of the linear system of constraints 
        associated with the border curves of the B-spline surfaces
        Input :
        nb_noeudsT,nb_noeudsY = number of knots (T for Theta)
        LC = control points of Left curve
        RC = control points of Right curve
        TC = control points of Top curve
        BC = control points of Bottom curve
        Output :
        the matrix H and second members according to x,y,z
    """
    #----------------------------------
    # number of control points
    ni = nb_noeudsT + 2
    nj = nb_noeudsY + 2
    # total number of constraints :
    # (constraints at corners are taken just once)
    nbConstraints = len(TC[0]) + len(LC[0]) - 2 + len(RC[0]) + len(BC[0]) - 2
    print(nbConstraints)
    print(nj)
    # number of variables (i.e., of control points)
    nbPC = ni*nj
    
    #----------------------------------
    # matrix H of constraints :
    #----------------------------------
    H = np.zeros((nbConstraints,nbPC)) 
    
    # # control points according to Bottom, Left, Right and Top curves
    # # (prise de tête...)

    #premier bloc
    for i in range(nj): 
        H[i][i] = 1

    #Dernier bloc
    i = nbConstraints - nj
    k = nbPC - nj
    while i < nbConstraints : 
        H[i][k] = 1
        i += 1
        k += 1

    #Bloc intermediaire
    i = nj
    for k in range(1, ni-1):
        H[i][k*nj] = 1
        H[i+1][(k+1)*nj-1] = 1
        i += 2


    
  
    #-------------------------------------------
    # second member :
    #----------------------------------
    # Corner points must be identical
    # so we consider the average value for each corner point
    (pcxL, pcyL, pczL) = LC # Left curve
    (pcxR, pcyR, pczR) = RC # Right curve
    (pcxT, pcyT, pczT) = TC # Top curve
    (pcxB, pcyB, pczB) = BC # Bottom curve
    
    # average at Bottom Left
    avBL_x, avBL_y, avBL_z = (pcxL[0] + pcxB[0])/2, (pcyL[0] + pcyB[0])/2, (pczL[0] + pczB[0])/2
        
    # average at Bottom Right
    avBR_x, avBR_y, avBR_z = (pcxR[0] + pcxB[-1])/2, (pcyR[0] + pcyB[-1])/2, (pczR[0] + pczB[-1])/2

    # average at Top Left
    avTL_x, avTL_y, avTL_z = (pcxL[-1] + pcxT[0])/2, (pcyL[-1] + pcyT[0])/2, (pczL[-1] + pczT[0])/2

    # average at Top Right
    avTR_x, avTR_y, avTR_z = (pcxR[-1] + pcxT[-1])/2, (pcyR[-1] + pcyT[-1])/2, (pczR[-1] + pczT[-1])/2
    # second member
    Bx, By, Bz = [],[],[]
    
    #-----SEWING-----
    Bx.append(avBL_x)
    By.append(avBL_y)
    Bz.append(avBL_z)
    Bx.extend(pcxL[1:-1])
    By.extend(pcyL[1:-1])
    Bz.extend(pczL[1:-1])
    Bx.append(avTL_x)
    By.append(avTL_y)
    Bz.append(avTL_z)
    for i in range(1, len(pcxB) - 1):
        Bx.append(pcxB[i])
        By.append(pcyB[i])
        Bz.append(pczB[i])
        Bx.append(pcxT[i])
        By.append(pcyT[i])
        Bz.append(pczT[i])
    Bx.append(avBR_x)
    By.append(avBR_y)
    Bz.append(avBR_z)
    Bx.extend(pcxR[1:-1])
    By.extend(pcyR[1:-1])
    Bz.extend(pczR[1:-1])
    Bx.append(avTR_x)
    By.append(avTR_y)
    Bz.append(avTR_z)
    Bx = np.array(Bx)
    By = np.array(By)
    Bz = np.array(Bz)
    return H, Bx, By, Bz




