import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    """
    Given a witness (G, H, S, f), check if it is a valid counterexample.
    G, H: PermutationGroup
    S: iterable of Permutation objects
    f: dict or callable mapping Permutation to Permutation
    """
    try:
        G, H, S, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups, and f is a function from G to H
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            for g in G.elements:
                try:
                    val = f(g) if callable(f) else f[g]
                except Exception:
                    h1 = False
                    break
                if val not in H:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H_2: S is a subset of G that generates G
    try:
        if not all(s in G for s in S):
            h2 = False
        else:
            S_list = list(S)
            if not S_list:
                gen_S = PermutationGroup([G.identity])
            else:
                gen_S = PermutationGroup(S_list)
            h2 = (gen_S.order() == G.order())
    except Exception:
        h2 = False
        
    # ¬Q: The image f(S) does not generate the image set f(G)
    try:
        f_G = set()
        for g in G.elements:
            val = f(g) if callable(f) else f[g]
            f_G.add(val)
            
        f_S = []
        for s in S:
            val = f(s) if callable(f) else f[s]
            f_S.append(val)
            
        if not f_S:
            gen_f_S = PermutationGroup([H.identity])
        else:
            gen_f_S = PermutationGroup(f_S)
            
        gen_f_S_elements = set(gen_f_S.elements)
        neg_q = (gen_f_S_elements != f_G)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: S is a subset of G that generates G",
    "¬Q: <f(S)> != f(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2