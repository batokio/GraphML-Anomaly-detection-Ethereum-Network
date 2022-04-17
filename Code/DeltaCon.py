#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:54:16 2022

@author: Bryan
"""

from imports import *


# Function computing the similarity scores between two graphs
def DeltaCon(G1, G2):
    '''

    Parameters
    ----------
    G1 : TYPE: (Weighted) Directed Graph
    G2 : TYPE: (Weighted) Directed Graph
    Both Graphs should have the same node set.

    Returns
    -------
    sim : TYPE: float
        Similarity score.

    '''
    
    # Get the Adjacency matrix
    A1, A2 = GenAdjacencyMatrix(G1, G2)
  
    # Get the silmilarity score
    sim=Similarity(A1, A2)
    
    return sim
    

# Function that computing the adjacency matrix of two graphs
def GenAdjacencyMatrix(G1, G2):
    '''
    
    Parameters
    ----------
    G1 : (Weighted) Directed Graph
    G2 : (Weighted) Directed Graph

    Returns
    -------
    A1 : SciPy sparse matrix
        Adjacency matrix representation of G1.
    A2 : SciPy sparse matrix
        Adjacency matrix representation of G2.


	Use Fast Belief Propagation
	CITATION: Danai Koutra, Tai-You Ke, U. Kang, Duen Horng Chau, Hsing-Kuo
	Kenneth Pao, Christos Faloutsos
	Unifying Guilt-by-Association Approaches
	return [I+a*D-c*A]^-1
	'''


    # Get the nodelist to order the adjacency matrix
    nodelist = list(G1.nodes())
    
    # Get the adjacency matrices
    A1 = nx.adjacency_matrix(G1, nodelist=nodelist)
    A2 = nx.adjacency_matrix(G2, nodelist=nodelist)

    return A1, A2


# Function returning the inverse matrix of the adjacency matrix
def InverseMatrix(A):
    '''

    Parameters
    ----------
    A : SciPy sparse matrix
        Adjacency matrix representation.

    Returns
    -------
    TYPE
        DESCRIPTION.


	Use Fast Belief Propagation
	CITATION: Danai Koutra, Tai-You Ke, U. Kang, Duen Horng Chau, Hsing-Kuo
	Kenneth Pao, Christos Faloutsos
	Unifying Guilt-by-Association Approaches
	return [I+a*D-c*A]^-1
	'''
    
    I=identity(A.shape[0])		#identity matrix
    D=diags(sum(A).toarray(), [0])	#diagonal degree matrix

    c1=trace(D.toarray())+2
    c2=trace(square(D).toarray())-1
    h_h=sqrt((-c1+sqrt(c1*c1+4*c2))/(8*c2))

    a=4*h_h*h_h/(1-4*h_h*h_h)
    c=2*h_h/(1-4*h_h*h_h)
	
    '''
	compute the inverse of matrix [I+a*D-c*A]
	use the method propose in Unifying Guilt-by-Association equation 5
	'''	
	
    M=c*A-a*D
    S=I
    mat=M
    power=1
    while amax(M.toarray())>10**(-9) and power<7:
        S=S+mat
        mat=mat*M
        power+=1

    return S
  




# Function computing the similarity score based on the DeltaCon0 algorithm
def Similarity(A1, A2):
    '''
    

    Parameters
    ----------
    A1 : SciPy sparse matrix
        Adjacency matrix representation of G1.
    A2 : SciPy sparse matrix
        Adjacency matrix representation of G2.

    Returns
    -------
    Similarity : Float
    

    Use deltacon0 to compute similarity
    CITATION: Danai Koutra, Joshua T. Vogelstein, Christos Faloutsos
    DELTACON: A Principled Massive-Graph Similarity Function
    '''
    S1=InverseMatrix(A1)
    S2=InverseMatrix(A2)
    S1_temp = np.sqrt(S1)
    S2_temp = np.sqrt(S2)
    
    result_temp  = np.power(S1_temp - S2_temp, 2) 
    
    d = np.sum(result_temp, axis=1)
    d = np.sum(d, axis=0)
    
    d=np.sqrt(d)
    sim=1/(1+d)
    return sim.item()



