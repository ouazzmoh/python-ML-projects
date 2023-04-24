# DeBoorCoxV0.py
"""========================================================================
DeBoorCox
- nombre de points de controle de deBoor-Cox = N+1
- nombre total de knots = N+d+2
  avec d+1 knots confondus au début et à la fin
========================================================================"""
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------
def PlotPolygon(ax,D,colorA):
    """ Plot polygon D of shape (N,2)
    """
    N,M  = np.shape(D)
    for k in range(N-1):
        ax.plot(D[k:k+2,0],D[k:k+2,1],colorA,ms=4)

#------------------------------------------------
def PlotPolygonBezier(ax,D,d,colorA,colorB):
    """ Plot polygon composite Bézier of shape (N,2)
    """
    N = len(D)
    for k in range(N-1):
        ax.plot(D[k:k+2,0],D[k:k+2,1],colorA,ms=4)
        plt.draw()
    NBez = int(N/(d+1))
    for k in range(NBez):
        k1 = k*(d+1)
        k2 = k1 + d
        ax.plot(D[k1,0],D[k1,1],colorB,ms=6)
        ax.plot(D[k2,0],D[k2,1],colorB,ms=6)
        plt.draw()

#########################
#  ACQUISITION FUNCTIONS
#########################

#------------------------------------------------
def PolygonAcquisition(ax,color1,color2) :
    """ Acquisition of a 2D polygon in the window with subplot "ax" 
        right click stop the acquisition
    """
    x = []  # x is an empty list
    y = []
    coord = 0
    while coord != []:
        coord = plt.ginput(1, mouse_add=1, mouse_stop=3, mouse_pop=2)
        # coord is a list of tuples : coord = [(x,y)]
        if coord != []:
            xx = coord[0][0]
            yy = coord[0][1]
            ax.plot(xx,yy,color1,ms=8)
            x.append(xx)
            y.append(yy)
            plt.draw()
            if len(x) > 1 :
                ax.plot([x[-2],x[-1]],[y[-2],y[-1]],color2)
    return x,y

#------------------------------------------------
def KnotsAcquisition(ax,n) :
    """ Acquisition of n distinct B-spline knots 
        on a segment in the axes "ax" 
        between xm and xM
        Then, we sort the knots in increasing order
        and add xm and xM as knots of multiplicity d+1
    """
    print("START OF KnotsAcquisition")
    print("--> insert ",n, "knots between ",xm,"and ",xM)

    # ax.plot([xm,xM],[y0,y0],'--g',lw=1)
    # ax.plot(xm,y0,'og',ms=8)
    # ax.plot(xM,y0,'og',ms=8)
    knots = []  # empty list

    k = 0
    while k < n :
        coord = plt.ginput(1, mouse_add=1, mouse_stop=3, mouse_pop=2)
        # coord is a list of tuples : coord = [(x,y)]
        if coord != []:
            xx = coord[0][0]
            if xx > xm and xx < xM:
                ax.plot(xx,y0,'sg',ms=6)
                knots.append(xx)
                plt.draw()
                k = k+1
        else:
            print("coord == []")
        
    knots.sort()
    for i in range(d+1):
        knots = np.hstack((xm,knots,xM))
    print("END OF KnotsAcquisition")
    return knots

#######################
#  B-SPLINE FUNCTIONS
#######################

#------------------------------------------------
def deBoorCox(Di,ti,d,t):
    """ deBoor-Cox algorithm for the evaluation of S(t)
        with B-spline control points Di : shape(Di) = (N+1,2)
        with knots ti : shape(ti) = (1,N+d+2)
        where t is a scalar value
        The B-spline S(t) is of degree d
        We assume that ti[d] <= t <= ti[N+1] =...= ti[N+1+d]
        Output = S(t)
    """

    # we localize t in [t_r, t_{r+1}[
    r = 0
    N = len(ti) - d -2
    for j in range(d, N+2):
        if ti[j] > t:
            r = j-1
            break
    # initialization
    Dzero = np.zeros((N+1, 2)) #shape (N+1,2) TODO with numpy
    D_steps = [] #to track triangulation steps, j
    for i in range(r-d, r+1):
        Dzero[i] = Di[i]
    D_steps.append(Dzero)
    # deBC algo
    for j in range(1, d+1):
        D = np.zeros((N+1, 2))
        for i in range(r-d+j, r+1):
            D[i] = ((t-ti[i])*D_steps[j-1][i] + (ti[i+d+1-j] - t) * D_steps[j-1][i-1])/(ti[i+d+1-j] - ti[i])
        D_steps.append(D)
    return D_steps[d][r]

#------------------------------------------------
def PlotPointsWithDeBoorCox(ax,Di,ti,d) :
    """ plot points of the B-spline curve S(t) 
        Values t are chosen by mouse clicking 
    """
    coord = 0
    print("START OF PlotPointsWithDeBoorCox")
    while coord != []:
        coord = plt.ginput(1, mouse_add=1, mouse_stop=3, mouse_pop=2)
        # coord is a list of tuples : coord = [(x,y)]
        if coord != []:
            xx = coord[0][0]
            if xx >= xm and xx <= xM:
                ax.plot(xx,y0,'or',ms=4)
                St = deBoorCox(Di,ti,d,xx)
                ax.plot(St[0],St[1],'or',ms=6)
                plt.draw()
        else:
            print("END OF PlotPointsWithDeBoorCox")


#------------------------------------------------
def WholeDisplayWithDeBoorCox(ax,Di,ti,d):
    """ display of the whole curve with deBoor-Cox algorithm
    """
    print("START of WholeDisplayWithDeBoorCox")
    N = len(Di) - 1
    for r in range(d,N+1):
        tvect = np.linspace(ti[r],ti[r+1],40)
        for t in tvect:
            St = deBoorCox(Di,ti,d,t)
            ax.plot(St[0],St[1],'.b',ms=2)
            plt.draw()
    print("END of WholeDisplayWithDeBoorCox")


#------------------------------------------------
def knotsInsertion(Di,ti,d,tn):
    """ Insertion of a new knot at position tn in ]tr, t_{r+1}[
        --> We assume that t_d < tn < t_{N+1}
        The B-spline S(t) is of degree d
        with B-spline points Di : shape(Di) = (N+1,2)
        with knots ti : shape(ti) = (1,N+d+2)
        we will get 
        - a new sequence of B-spline points Di2 (with one more point)
        - a new sequence of knots ti2 (with one more knot)
    """
    r = 0
    N = len(ti) - d -2
    for j in range(d, N+2):
        if ti[j] > tn:
            r = j-1
            break
    # new sequence of knots :
    ti2 = np.insert(ti, r+1, tn)
    # New B-spline points with deBoor-Cox algo
    # initialization
    Di2 = np.zeros((N+2, 2))
    for k in range(r-d+1):
        Di2[k] = Di[k]
    for k in range(r, N+1):
        Di2[k+1] = Di[k]
    # first step of deBoor-Cox : j=1
    for i in range(r-d+1, r+1):
        Di2[i] = ((tn-ti[i])*Di[i] + (ti[i+d] - tn) * Di[i-1])/(ti[i+d] - ti[i])
    return Di2, ti2


#------------------------------------------------
def MouseKnotsInsertion(ax,Di,ti,d) :
    """ We insert new hnots by mouse clicking 
        and, for each new knot, we evaluate the 
        - new sequence of B-spline points Di2 (with one more point)
          and plot it
        - new sequence of knots ti2 (with one more knot)
    """
    print("START OF MouseKnotsInsertion")
    coord = 0
    while coord != []:
        coord = plt.ginput(1, mouse_add=1, mouse_stop=3, mouse_pop=2)
        # coord is a list of tuples : coord = [(x,y)]
        if coord != []:
            xx = coord[0][0]
            if xx > xm and xx < xM:
                # we plot the new knot
                ax.plot(xx,y0,'vg',ms=6)
                plt.draw()
                # we determine the new B-spline control polygon Di2
                # and the new sequence of knots ti2
                Di2, ti2 = knotsInsertion(Di,ti,d,xx)
                # we plot Di2
                PlotPolygon(ax,Di2,'--sg')
                Di = Di2
                ti = ti2
        else:
            print("END OF MouseKnotsInsertion")
    return Di,ti


#------------------------------------------------
def Subdivision(Di,ti,d):
    """ One subdivision of the B-spline control polygon Di 
        by insertion of a knot at mid-point of each interval ]tr, t_{r+1}[
        The B-spline S(t) is of degree d
        with B-spline points Di : shape(Di) = (N+1,2)
        with knots ti : shape(ti) = (1,N+d+2)
        we will get 
        - a new sequence of B-spline points Di2
        - a new sequence of knots ti2
    """
    N = len(ti) - d -2
    Di2, ti2 = np.copy(Di), np.copy(ti)
    for i in range(d, N+1):
        Di2, ti2 = knotsInsertion(Di2, ti2, d, (ti[i]+ti[i+1])/2)
    return Di2,ti2


#------------------------------------------------
def BezierForm(Di,ti,d):
    """ Bézier form of the B-spline 
        with control polygon Di : shape(Di) = (N+1,2)
        with knots ti : shape(ti) = (1,N+d+2)
        and degree d
        by inserting d-1 times a knot on each knot t_r of multiplicity one, 
        ie for d+1 <= r <= N
        Finally, each knot will be of multiplicity d    # ---
    # ---
    
    # return Di2, ti2
        Output is a composite polygon Di2
        ie, a sequence of Bézier control polygon
    """
    N = len(ti) - d -2

    Di2 = np.zeros((N+1, 2))
    for k in range(len(Di)):
        Di2[k] = Di[k]

    ti2 = []
    for k in range(len(ti)):
        ti2.append(ti[k])

    for i in range(d, N+1):
        for k in range(d-1):
            Di2, ti2 = knotsInsertion(Di2, ti2, d, ti[i])
    return Di2,ti2





##############################################################
if __name__ == '__main__':
    
    # acquisition window
    minmax = 10
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.set_xlim((-minmax,minmax))
    ax.set_ylim((-minmax,minmax))
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_title("Acquisition window") 
    
    #==============================
    # knots bar 
    y0 = -9
    xm = -9.5
    xM = 9.5
    ax.plot([xm,xM],[y0,y0],'--g',lw=1)
    ax.plot(xm,y0,'og',ms=8)
    ax.plot(xM,y0,'og',ms=8)

    #==============================
    # B-spline of degree d
    d = 3

    #==============================
    # B-spline polygon acquisition
    xp1, yp1 = PolygonAcquisition(ax,'ob','b')
    N = len(xp1) - 1            # N+1 B-spline control points
    Di = np.vstack((xp1,yp1)).T # B-spline control points
    # BezierPlot(ax,xp1,yp1,'b')

    #==============================
    # knots mouse-acquisition
    #   nombre total de knots = N+d+2
    #   mais d+1 knots confondus au début et à la fin
    #   nombre de knots à insérer entre t_d et t_{N+1} = N-d
    #   indices r des knots disctincts : d <= r <= N+1
    ti = KnotsAcquisition(ax,N-d)
    print(ti)

    #==============================
    # display of B-spline points with deBoorCox algorithm
    PlotPointsWithDeBoorCox(ax,Di,ti,d)
    
    #==============================
    # display of the whole curve with deBoorCox algorithm
    
    WholeDisplayWithDeBoorCox(ax,Di,ti,d)
    # for r in range(d,N+1):
    #     tvect = np.linspace(ti[r],ti[r+1],40)
    #     #tvect = np.arange(ti[r],ti[r+1],0.04) # equal spacing
    #     for t in tvect:
    #         St = deBoorCox(Di,ti,d,t)
    #         ax.plot(St[0],St[1],'.b',ms=2)
    
    #==============================

    # Mouse knots insertion
    Di2, ti2 = MouseKnotsInsertion(ax,Di,ti,d)
    
    #==============================
    # Subdivision
    NbSubd = 4
    ti3 = np.copy(ti)
    Di3 = np.copy(Di)
    for j in range(NbSubd):        
        Di3,ti3 = Subdivision(Di3,ti3,d)
    PlotPolygon(ax,Di3,'-r')
    
    #==============================
    # Bézier form
    DB, tb = BezierForm(Di,ti,d)
    print("begin")
    PlotPolygonBezier(ax,DB,d,'-oc','sc')
    plt.show()
    print(">>>>>>>>>>")

 
 
