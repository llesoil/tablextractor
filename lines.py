#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:11:39 2020

@author: llesoil
"""

import networkx as nx
import numpy as np

from .points import *

def equalLine(line1, line2):
    # input : two lines line1 and line2
    # output : true if the line are the same (if they are closer than diff pixel from each other)
    xb1, yb1, xf1, yf1 = line1
    xb2, yb2, xf2, yf2 = line2
    lineEquals = False
    if equalPt(xb1, yb1, xb2, yb2) and equalPt(xf1, yf1, xf2, yf2):
        lineEquals = True
    return lineEquals


def supprDuplicateLine(lines):
    # input: a list of lines
    # ouput : the list of lines without the duplicates lines
    supprLine = []
    ind_lines = range(len(lines))
    for i in ind_lines:
        for j in ind_lines:
            if i!=j and equalLine(lines[i], lines[j]):
                supprLine.append(min(i,j))
    return [lines[k] for k in np.setdiff1d(ind_lines, np.unique(supprLine))]


def extractTypeLines(lines):
    # input : all the lines of the picture
    # output : one list of horizontal lines, anohter of vertical lines
    horizontal = []
    vertical = []
    for line in lines:
        for(xb, yb, xf, yf) in line:
            if typeLine(xb, yb, xf, yf) == 1:
                horizontal.append((xb, yb, xf, yf))
            if typeLine(xb, yb, xf, yf) == 2:
                vertical.append((xb, yb, xf, yf))
    return(supprDuplicateLine(horizontal), supprDuplicateLine(vertical))


def crossLines(line1, line2):
    # input : 2 lines, line1 horizontal and line2 vertical
    # output : True if the 2 lines crossed each other, False otherwise
    crossed = False
    (xb1, yb1, xf1, yf1) = line1
    (xb2, yb2, xf2, yf2) = line2
    if min(xb1, xf1) < min(xb2,xf2)+diff and max(xb1, xf1)+diff > max(xb2,xf2) and min(yb2,yf2) < min(yb1,yf1)+diff and max(yb2, yf2)+diff > max(yb1,yf1):
        crossed = True
    return crossed


def crossMatrix(lines):
    # input : one list of lines
    # output: the "cross matrix", C[h,v] = 1 if h cross v, 0 otherwise, where h are horizontal and v vertical lines
    
    # first we extract the horizontal and the vertical lines
    horizontal, vertical = extractTypeLines(lines)
    H = len(horizontal)
    V = len(vertical)
    
    # we create the final matrix
    C = np.zeros(H*V).reshape(H,V)
    
    for h in range(H):
        for v in range(V):
            if crossLines(horizontal[h],vertical[v]):
                C[h,v] = 1
    
    # keep the lines which cross other lines
    horizKeep = np.nonzero(np.sum(C, axis=1))[0]
    vertKeep = np.nonzero(np.sum(C, axis=0))[0]
    horizontal = [horizontal[k] for k in horizKeep]
    vertical = [vertical[k] for k in vertKeep]
    
    return (C[:,vertKeep][horizKeep, :], horizontal, vertical)


def findTables(lines):
    
    listTables = []
    
    C, horizontal, vertical = crossMatrix(lines)

    G = nx.Graph()

    H = len(horizontal)
    labelH = []
    for h in range(H):
        labelH.append('h'+str(h))

    V = len(vertical)
    labelV = []
    for v in range(V):
        labelV.append('v'+str(v))

    G.add_nodes_from(list(labelH), bipartite=0)
    G.add_nodes_from(list(labelV), bipartite=1)
    
    for h in range(H):
        for v in range(V):
            if C[h,v] == 1:
                G.add_edge(labelH[h],labelV[v])
                
    #connexComponents = list(nx.connected_component_subgraphs(G))
    connexComponents = [G.subgraph(c) for c in nx.connected_components(G)]

    for indexComp in range(len(connexComponents)):
        comp = connexComponents[indexComp]
        listIndexHLines = []
        listIndexVLines = []
        l, r = nx.bipartite.sets(comp)
        for _ , iteml in enumerate(l):
            if iteml[0]=='h':
                listIndexHLines.append(labelH.index(iteml))
            else:
                listIndexVLines.append(labelV.index(iteml))
        for _ , itemr in enumerate(r):
            if itemr[0]=='h':
                listIndexHLines.append(labelH.index(itemr))
            else:
                listIndexVLines.append(labelV.index(itemr))
        if len(listIndexHLines)>1 and len(listIndexVLines)>1:
            listTables.append(([horizontal[k] for k in listIndexHLines], [vertical[k] for k in listIndexVLines]))
        
    return listTables
