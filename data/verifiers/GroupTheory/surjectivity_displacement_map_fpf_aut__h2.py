import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)
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
        G, phi = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group and phi maps G to G
    try:
        if not hasattr(G, 'elements'):
            h1 = False
        else:
            elements = list(G.elements)
            if len(elements) == 0:
                h1 = False
            else:
                identity = None
                for e in elements:
                    if all(e * g == g for g in elements):
                        identity = e
                        break
                if identity is None:
                    h1 = False
                else:
                    h1 = True
                    for g in elements:
                        val = phi[g] if isinstance(phi, dict) else phi(g)
                        if val not in elements:
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: For all g in G, phi(g) = g implies g = e
    try:
        elements = list(G.elements)
        identity = None
        for e in elements:
            if all(e * g == g for g in elements):
                identity = e
                break
        if identity is None:
            h2 = False
        else:
            h2 = True
            for g in elements:
                val = phi[g] if isinstance(phi, dict) else phi(g)
                if val == g and g != identity:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: f is not a bijection
    try:
        elements = list(G.elements)
        identity = None
        for e in elements:
            if all(e * g == g for g in elements):
                identity = e
                break
        
        if identity is None:
            neg_q = False
        else:
            f_values = []
            for g in elements:
                val = phi[g] if isinstance(phi, dict) else phi(g)
                g_inv = None
                for h in elements:
                    if g * h == identity and h * g == identity:
                        g_inv = h
                        break
                if g_inv is None:
                    raise ValueError("No inverse found")
                
                f_val = g_inv * val
                if f_val not in f_values:
                    f_values.append(f_val)
            
            is_bijection = len(f_values) == len(elements)
            neg_q = not is_bijection
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and phi maps G to G",
    "H_2: For all g in G, phi(g) = g implies g = e",
    "¬Q: The map f(x) = x^{-1}phi(x) is not a bijection"
]

N_HYP = 2
NEG_Q_INDEX = 2