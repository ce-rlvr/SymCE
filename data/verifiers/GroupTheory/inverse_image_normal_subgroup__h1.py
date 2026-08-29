import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            M = witness['M']
        else:
            G, H, f, M = witness
    except Exception:
        return [False, False, False]

    # H_1: f is a group homomorphism from G to H
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        H_set = set(H_elements)
        
        h1_ok = True
        for g in G_elements:
            fg = f(g) if callable(f) else f[g]
            if fg not in H_set:
                h1_ok = False
                break
        if h1_ok:
            for g1 in G_elements:
                for g2 in G_elements:
                    fg1 = f(g1) if callable(f) else f[g1]
                    fg2 = f(g2) if callable(f) else f[g2]
                    fg12 = f(g1 * g2) if callable(f) else f[g1 * g2]
                    if fg12 != fg1 * fg2:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: M is a normal subgroup of H
    try:
        if hasattr(M, 'elements'):
            M_elements = list(M.elements)
        else:
            M_elements = list(M)
            
        M_set = set(M_elements)
        H_set = set(list(H.elements))
        
        h2_ok = True
        if not M_set.issubset(H_set):
            h2_ok = False
        elif H.identity not in M_set:
            h2_ok = False
        else:
            for m1 in M_set:
                if m1**-1 not in M_set:
                    h2_ok = False
                    break
                for m2 in M_set:
                    if m1 * m2 not in M_set:
                        h2_ok = False
                        break
                if not h2_ok:
                    break
            if h2_ok:
                for h in H_set:
                    for m in M_set:
                        if h * m * h**-1 not in M_set:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
    except Exception:
        h2_ok = False

    # neg_Q: f^{-1}(M) is not a normal subgroup of G
    try:
        G_elements = list(G.elements)
        if hasattr(M, 'elements'):
            M_elements = list(M.elements)
        else:
            M_elements = list(M)
        M_set = set(M_elements)

        preimage = set()
        for g in G_elements:
            fg = f(g) if callable(f) else f[g]
            if fg in M_set:
                preimage.add(g)
                
        is_normal = True
        if G.identity not in preimage:
            is_normal = False
        else:
            for p1 in preimage:
                if p1**-1 not in preimage:
                    is_normal = False
                    break
                for p2 in preimage:
                    if p1 * p2 not in preimage:
                        is_normal = False
                        break
                if not is_normal:
                    break
            if is_normal:
                for g in G_elements:
                    for p in preimage:
                        if g * p * g**-1 not in preimage:
                            is_normal = False
                            break
                    if not is_normal:
                        break
        neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: M is a normal subgroup of H",
    "¬Q: f^{-1}(M) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2