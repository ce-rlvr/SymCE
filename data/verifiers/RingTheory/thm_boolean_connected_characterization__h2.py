import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

def make_Zn(n):
    """Creates the ring Zn represented as (n, add_table, mul_table)."""
    return (n, 
            [[(i + j) % n for j in range(n)] for i in range(n)],
            [[(i * j) % n for j in range(n)] for i in range(n)])

# Standard rings
Z1 = make_Zn(1)
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)

def is_boolean_ring(witness):
    n, add, mul = witness
    if not isinstance(n, int) or n <= 0: 
        return False
    if len(add) != n or any(len(row) != n for row in add): 
        return False
    if len(mul) != n or any(len(row) != n for row in mul): 
        return False
    
    # Check closure
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
            
    # Check associativity and distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                
    # Check commutativity of addition
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # Check existence of zero
    z = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)) and all(add[j][i] == j for j in range(n)):
            z = i
            break
    if z is None: 
        return False
    
    # Check existence of additive inverses
    for i in range(n):
        if not any(add[i][j] == z for j in range(n)): 
            return False
        
    # Check existence of multiplicative identity (one)
    one = None
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)) and all(mul[j][i] == j for j in range(n)):
            one = i
            break
    if one is None: 
        return False
    
    # Check Boolean property: x^2 = x for all x
    for i in range(n):
        if mul[i][i] != i: 
            return False
        
    return True

def only_idempotents_zero_one(witness):
    n, add, mul = witness
    z = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)) and all(add[j][i] == j for j in range(n)):
            z = i
            break
            
    one = None
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)) and all(mul[j][i] == j for j in range(n)):
            one = i
            break
            
    if z is None or one is None: 
        return False
    
    for i in range(n):
        if mul[i][i] == i:
            if i != z and i != one:
                return False
    return True

def is_isomorphic_to_Z2(witness):
    n, add, mul = witness
    if n != 2: 
        return False
        
    z = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)) and all(add[j][i] == j for j in range(n)):
            z = i
            break
    if z is None: 
        return False
        
    one = 1 - z
    if add[one][one] != z: return False
    if mul[one][one] != one: return False
    if mul[z][one] != z or mul[one][z] != z or mul[z][z] != z: return False
    
    return True

def conditions(witness):
    try:
        h1 = is_boolean_ring(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = only_idempotents_zero_one(witness)
    except Exception:
        h2 = False
        
    try:
        is_z2 = is_isomorphic_to_Z2(witness)
        neg_q = not is_z2
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: The only idempotent elements in R are 0 and 1",
    "¬Q: R is not isomorphic to the field of two elements, Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2