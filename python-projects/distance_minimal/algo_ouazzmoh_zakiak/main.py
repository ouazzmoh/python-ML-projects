#!/usr/bin/env python3

from timeit import timeit
from sys import argv
from xml.etree.ElementPath import find
from geo.point import Point
from geo.tycat import tycat
from geo.segment import Segment
from time import time


def load_instance(filename):
    """
    loads .mnt file. 
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points


def recherche_brutforce(points):
    """Algorithme naif"""
    min_points = [points[0], points[1]]
    d_min = points[0].distance_to(points[1])
    for i in range(len(points)):
        for j in range(i+1, len(points)):       
            d_ij = points[i].distance_to(points[j])
            if d_ij < d_min and d_ij != 0:
                d_min = d_ij
                min_points = [points[i], points[j]]
    return min_points


def find_rec(points):
    """Diviser pour régner, retourne les deux points les plus proches"""
    
    #Condition d'arret
    if len(points) <= 3:
        return recherche_brutforce(points)
    
    #Diviser le plan
    X_left = points[:len(points)//2]
    X_right = points[len(points)//2:]
    pt_left = find_rec(X_left)
    pt_right = find_rec(X_right)
    d_left = pt_left[0].distance_to(pt_left[1])
    d_right = pt_right[0].distance_to(pt_right[1])
    
    #Determination de la distance minimale dans les deux parties du plan
    if d_left < d_right:    
        ptmin = pt_left
        d = d_left
    else:
        ptmin = pt_right
        d = d_right

    #Creation du bande
    xmid = points[len(points)//2].coordinates[0]
    bande = []
    for pt in points:
        if xmid - d <= pt.coordinates[0] <= xmid + d:
            bande.append(pt)
    bande.sort(key = lambda point : point.coordinates[1])

    #Calcule du dist du bande et comparaison avec la distance des deux parties du plan
    for i in range(len(points)):
        for j in range(i+1, min(i+7, len(bande))):
            if bande[i].distance_to(bande[j]) < d:
                d = bande[i].distance_to(bande[j])
                ptmin = [bande[i], bande[j]]
    return ptmin


def print_solution(points):
    """Diviser pour regner"""
    points.sort(key = lambda  point : point.coordinates[0])
    ptmin = find_rec(points)
    print(f"{ptmin[0].coordinates[0]}, {ptmin[0].coordinates[1]}; {ptmin[1].coordinates[0]}, {ptmin[1].coordinates[1]}")




def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """ 
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)

