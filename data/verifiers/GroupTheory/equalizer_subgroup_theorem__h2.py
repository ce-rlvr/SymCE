import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, f, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups, and f, g are functions from G to H
    h1 = False
    try:
        if hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity'):
            G_els = set(G.elements)
            H_els = set(H.elements)
            
            def check_func(func):
                if isinstance(func, dict):
                    if set(func.keys()) != G_els: 
                        return False
                    if not all(v in H_els for v in func.values()): 
                        return False
                    return True
                elif callable(func):
                    if not all(func(x) in H_els for x in G_els): 
                        return False
                    return True
                return False
            
            if check_func(f) and check_func(g):
                h1 = True
    except Exception:
        h1 = False

    # H_2: g is a group homomorphism from G to H
    h2 = False
    try:
        if h1:
            g_func = (lambda x: g[x]) if isinstance(g, dict) else g
            h2 = True
            for x in G_els:
                for y in G_els:
                    if g_func(x * y) != g_func(x) * g_func(y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The set E = {x \in G | f(x) = g(x)} is NOT a subgroup of G
    neg_q = False
    try:
        if h1:
            f_func = (lambda x: f[x]) if isinstance(f, dict) else f
            g_func = (lambda x: g[x]) if isinstance(g, dict) else g
            
            E = set()
            for x in G_els:
                if f_func(x) == g_func(x):
                    E.add(x)
            
            is_subgroup = True
            if not E:
                is_subgroup = False
            elif G.identity not in E:
                is_subgroup = False
            else:
                for x in E:
                    for y in E:
                        if (x * y) not in E:
                            is_subgroup = False
                            break
                    if (x**-1) not in E:
                        is_subgroup = False
                        break
                    if not is_subgroup:
                        break
            
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups, and f, g are functions from G to H",
    "H_2: g is a group homomorphism from G to H",
    "¬Q: The set E = {x in G | f(x) = g(x)} is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2