import sympy
from sympy import *
import itertools
import functools
import math

TrivialRing = ([0], [[0]], [[0]])
Z2Ring = ([0, 1], [[0, 1], [1, 0]], [[0, 0], [0, 1]])

def is_ring(elements, add_table, mul_table):
    try:
        n = len(elements)
        if n == 0: return False
        if len(add_table) != n or any(len(row) != n for row in add_table): return False
        if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
        
        for i in range(n):
            for j in range(n):
                if add_table[i][j] not in range(n): return False
                if mul_table[i][j] not in range(n): return False
                
        zeros = [i for i in range(n) if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n))]
        if not zeros: return False
        z = zeros[0]
        
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False
                    
        for i in range(n):
            if not any(add_table[i][j] == z for j in range(n)): return False
            
        has_id = False
        for i in range(n):
            if all(mul_table[i][j] == j for j in range(n)) and all(mul_table[j][i] == j for j in range(n)):
                has_id = True
                break
        if not has_id: return False
            
        return True
    except Exception:
        return False

def is_boolean_ring(elements, add_table, mul_table):
    try:
        if not is_ring(elements, add_table, mul_table): return False
        n = len(elements)
        for i in range(n):
            if mul_table[i][i] != i: return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'add_table') and hasattr(witness, 'mul_table'):
            elements = witness.elements
            add_table = witness.add_table
            mul_table = witness.mul_table
        else:
            elements, add_table, mul_table = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_boolean_ring(elements, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring(elements, add_table, mul_table)
    except Exception:
        h2 = False
        
    try:
        neg_q = h1 and len(elements) == 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R_x is the polynomial ring in one variable x over R",
    "¬Q: R_x is a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2