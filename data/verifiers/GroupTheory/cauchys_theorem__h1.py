import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_cayley_table(G, p):
    n = len(G)
    for row in G:
        if not isinstance(row, list) or len(row) != n:
            return False
            
    identity = None
    for i in range(n):
        is_id = True
        for j in range(n):
            if G[i][j] != j or G[j][i] != j:
                is_id = False
                break
        if is_id:
            identity = i
            break
            
    if identity is None:
        return False
        
    for i in range(n):
        curr = i
        for _ in range(p - 1):
            curr = G[curr][i]
        if curr == identity and i != identity:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        p_val = int(p)
        h1 = sympy.isprime(p_val)
    except Exception:
        h1 = False
        
    # H2: p divides the order of G
    try:
        if hasattr(G, 'order'):
            order_G = G.order() if callable(G.order) else G.order
        elif hasattr(G, '__len__'):
            order_G = len(G)
        else:
            order_G = None
            
        if order_G is not None:
            h2 = (int(order_G) % p_val == 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: G does NOT contain an element of order p
    try:
        has_element = False
        
        if isinstance(G, list) and len(G) > 0 and isinstance(G[0], list):
            has_element = check_cayley_table(G, p_val)
        else:
            if hasattr(G, 'elements'):
                elements = G.elements
            elif hasattr(G, 'generate'):
                elements = G.generate()
            elif hasattr(G, '__iter__'):
                elements = G
            else:
                elements = []
                
            for g in elements:
                if hasattr(g, 'order'):
                    try:
                        o = g.order() if callable(g.order) else g.order
                        if o is not None and int(o) == p_val:
                            has_element = True
                            break
                    except Exception:
                        pass
                
                if hasattr(g, 'is_Matrix') and g.is_Matrix:
                    try:
                        I_mat = eye(g.rows)
                        if (g**p_val) == I_mat and g != I_mat:
                            has_element = True
                            break
                    except Exception:
                        pass
                        
        neg_q = not has_element
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "¬Q: G does not contain an element of order p"
]

N_HYP = 2
NEG_Q_INDEX = 2