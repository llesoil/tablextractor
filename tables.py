#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:13:15 2020

@author: llesoil
"""

import cv2
from lines import *

def sortTables(listTables):

    centers = []
    
    for table in listTables:
        horiz, vert = sorted(table[0], key = lambda x: x[1]), sorted(table[1], key = lambda x: x[0])
        centers.append(getCenterOfTable(horiz, vert))
    
    listSortTables = []
    for indexTable in getPermutations(centers):
        listSortTables.append(listTables[indexTable]) 
    return listSortTables


def sortLineTable(listTables):
    
    listSortedLines = []
    
    for table in listTables:
        horiz = sorted(table[0], key = lambda x: (x[1], x[0])), 
        vert = sorted(table[1], key = lambda x: (x[0], x[1]))
        listSortedLines.append((horiz, vert))

    return listSortedLines


def getCenterOfTable(horiz, vert):
    return (int((vert[0][0]+vert[len(vert)-1][0])/2), int((horiz[0][1]+horiz[len(horiz)-1][1])/2))


def crossMatrix2(horiz, vert):
    H = len(horiz)
    V = len(vert)
    
    C = np.zeros(H*V).reshape(H,V)
    
    for h in range(H):
        for v in range(V):
            if crossLines(horiz[h],vert[v]):
                C[h,v] = 1
    
    return C


def listPoints(horiz, vert):
    
    C = crossMatrix2(horiz, vert)
    listCol = []
    
    H = len(horiz)
    V = len(vert)
    for indexH1 in range(H-1):
        h = horiz[indexH1]
        if indexH1 == 0:
            listLine = []
        else:
            if h[1] != horiz[indexH1-1][1]:
                listCol.append(listLine)
                listLine = []
        indexV1 = 0
        while (indexV1 < V):
            if C[indexH1, indexV1] == 1:
                indexV2 = indexV1+1
                while (indexV2 <V):
                    if C[indexH1, indexV2] == 1 and indexH1 != H-1:
                        indexH2 = indexH1+1
                        while indexH2 < H:
                            if C[indexH1, indexV1]==1 and C[indexH1, indexV2]==1:
                                listLine.append(((h[1], vert[indexV1][0]),
                                                  (horiz[indexH2][1], vert[indexV2][0]),
                                                  (h[1], vert[indexV2][0]),
                                                  (horiz[indexH2][1], vert[indexV1][0])))
                                indexH2 = H
                                indexV1 = indexV2
                            indexH2+=1
                    indexV2+=1
            indexV1+=1
    return listCol



def findPoints(path):
    
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = 300, minLineLength = 100, maxLineGap = 5)
    
    listTables = sortLineTable(sortTables(findTables(lines)))
    
    listTablePts = []
    
    for i in range(len(listTables)):

        horiz, vert = listTables[i]
        print(vert[0])
        
        listTablePts.append(listPoints(horiz[0], vert))
        
    return listTablePts

#findPoints("/home/llesoil/Downloads/print_weburl.png")

