import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        G, H, f, M = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(f, dict):
            f_eval = lambda x: f[x]
        elif callable(f):
            f_eval = f
        else:
            f_eval = None
    except Exception:
        f_eval = None

    # H1: G and H are groups, f is a map from G to H
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            h1 = False
        elif f_eval is None:
            h1 = False
        else:
            G_elems = list(G.generate_dimino())
            H_elems = list(H.generate_dimino())
            H_set = set(H_elems)
            if isinstance(f, dict):
                h1 = set(f.keys()) == set(G_elems) and all(v in H_set for v in f.values())
            else:
                h1 = all(f_eval(g) in H_set for g in G_elems)
    except Exception:
        h1 = False

    # H2: M is a normal subgroup of H
    try:
        if not isinstance(M, PermutationGroup):
            h2 = False
        else:
            M_elems = list(M.generate_dimino())
            H_elems = list(H.generate_dimino())
            M_set = set(M_elems)
            
            is_subgroup = all(m in H_elems for m in M_elems)
            
            is_normal = True
            if is_subgroup:
                for h in H_elems:
                    h_inv = h**-1
                    for m in M_elems:
                        if h * m * h_inv not in M_set:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            h2 = is_subgroup and is_normal
    except Exception:
        h2 = False

    # neg_Q: f^{-1}(M) is not a normal subgroup of G
    try:
        if f_eval is None:
            neg_q = False
        else:
            M_elems = list(M.generate_dimino())
            M_set = set(M_elems)
            G_elems = list(G.generate_dimino())
            
            identity = None
            for g in G_elems:
                if g * g == g:
                    identity = g
                    break
            
            preimage = []
            for g in G_elems:
                val = f_eval(g)
                if val in M_set:
                    preimage.append(g)
                    
            is_normal_subgroup = True
            if not preimage:
                is_normal_subgroup = False
            elif identity not in preimage:
                is_normal_subgroup = False
            else:
                preimage_set = set(preimage)
                for a in preimage:
                    if a**-1 not in preimage_set:
                        is_normal_subgroup = False
                        break
                    for b in preimage:
                        if a * b not in preimage_set:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                
                if is_normal_subgroup:
                    for g in G_elems:
                        g_inv = g**-1
                        for x in preimage:
                            if g * x * g_inv not in preimage_set:
                                is_normal_subgroup = False
                                break
                        if not is_normal_subgroup:
                            break
                            
            neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and f is a map from G to H",
    "H_2: M is a normal subgroup of H",
    "¬Q: The preimage f^{-1}(M) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2