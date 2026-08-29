import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # 1. Check if witness is a custom object with explicit property methods
    # (Useful for infinite groups which cannot be computationally verified by enumeration)
    try:
        if hasattr(witness, 'is_subgroup') and hasattr(witness, 'is_proper') and hasattr(witness, 'union_of_conjugates_equals_group'):
            h1 = bool(witness.is_subgroup())
            h2 = bool(witness.is_proper())
            neg_q = bool(witness.union_of_conjugates_equals_group())
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a tuple (G, H)
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        elif hasattr(G, 'has_subgroup'):
            h1 = bool(G.has_subgroup(H))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: H is not equal to G
    try:
        if hasattr(H, 'is_proper'):
            h2 = bool(H.is_proper(G))
        elif hasattr(H, 'is_subgroup') and hasattr(G, 'is_subgroup'):
            h2 = not (H.is_subgroup(G) and G.is_subgroup(H))
        else:
            h2 = bool(H != G)
    except Exception:
        h2 = False

    # neg_Q: The union of gHg^{-1} over all g in G IS equal to G
    try:
        if hasattr(G, 'union_of_conjugates_equals'):
            neg_q = bool(G.union_of_conjugates_equals(H))
        elif hasattr(H, 'union_of_conjugates_equals_group'):
            neg_q = bool(H.union_of_conjugates_equals_group(G))
        else:
            # Finite group computation fallback
            if hasattr(G, 'order'):
                try:
                    if G.order() == sympy.oo:
                        return [h1, h2, False]
                except Exception:
                    pass
                    
            g_elements = list(G.elements)
            h_elements = list(H.elements)
            
            try:
                union_elements = set()
                for g in g_elements:
                    try:
                        g_inv = ~g
                    except Exception:
                        g_inv = g**-1
                    for h in h_elements:
                        union_elements.add(g * h * g_inv)
                neg_q = (len(union_elements) == len(g_elements))
            except TypeError:
                # Fallback for unhashable elements
                union_elements = []
                for g in g_elements:
                    try:
                        g_inv = ~g
                    except Exception:
                        g_inv = g**-1
                    for h in h_elements:
                        conj = g * h * g_inv
                        if conj not in union_elements:
                            union_elements.append(conj)
                neg_q = (len(union_elements) == len(g_elements))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: H is not equal to G",
    "¬Q: The union of gHg^{-1} over all g in G is equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2