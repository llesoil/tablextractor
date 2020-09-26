#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:11:38 2020

@author: llesoil
"""

# the difference of pixels between the beginning and the final points x/y to be considered as a vertical/horizontal line
# and between two points, to consider they are on the same position
diff = 10

def permute(tab, i, j):
    temp = tab[i]
    tab[i] = tab[j]
    tab[j] = temp
    return tab


def typeLine(xb, yb, xf, yf):
    # input : the four coordinates of a line
    # output : 0 if the line is diagonal,
    #          1 if the line if horizontal, 
    #          2 if the line is vertical
    if abs(yb-yf) < diff:
        return 1
    if abs(xb-xf) < diff:
        return 2
    else:
        return 0


def equalPt(x1, y1, x2, y2):
    # input : two points A1 (x1, y1) and A2 (x2,y2)
    # output : A1 == A2
    isEqual = False
    if abs(x1-x2) < diff and abs(y1-y2) < diff:
        isEqual = True
    return isEqual


def isBefore(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    isBefore = False
    if y1<y2 or (abs(y1-y2)<diff and x1 < x2):
        isBefore = True
    return isBefore


def getPermutations(centers):
    # get all the permutations to have a sorted list of tables
    orderIni = [k for k in range(len(centers))]
    nbCenters = len(centers)
    for i in range(nbCenters-1, 0, -1):
        for j in range(0, i):
            if isBefore(centers[j+1], centers[j]):
                centers = permute(centers, j+1, j)
                orderIni = permute(orderIni, j+1, j)
    return orderIni