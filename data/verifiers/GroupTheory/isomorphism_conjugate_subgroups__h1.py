import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, g = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup') and hasattr(G, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            G_list = list(G)
            try:
                H_list = list(H.generate()) if hasattr(H, 'generate') else list(H)
            except Exception:
                H_list = list(H)
                
            h1 = all(x in G_list for x in H_list)
            if h1 and len(H_list) > 0:
                for x in H_list:
                    try:
                        inv = x**-1
                    except Exception:
                        inv = ~x
                    if inv not in H_list:
                        h1 = False
                        break
                    for y in H_list:
                        if (x * y) not in H_list:
                            h1 = False
                            break
            else:
                if len(H_list) == 0:
                    h1 = False
    except Exception:
        h1 = False
        
    # H_2: g is an element of G
    try:
        if hasattr(G, '__contains__') and not isinstance(G, list):
            h2 = bool(g in G)
        else:
            h2 = bool(g in list(G))
    except Exception:
        h2 = False
        
    # ¬Q: The conjugate subgroup gHg^{-1} is not isomorphic to H
    try:
        if hasattr(H, 'generators') and hasattr(H, 'is_isomorphic'):
            try:
                g_inv = g**-1
            except Exception:
                g_inv = ~g
            conj_gens = [g * h * g_inv for h in H.generators]
            gHg_inv = PermutationGroup(conj_gens)
            is_iso = bool(gHg_inv.is_isomorphic(H))
            neg_q = not is_iso
        else:
            try:
                H_list = list(H.generate()) if hasattr(H, 'generate') else list(H)
            except Exception:
                H_list = list(H)
                
            try:
                g_inv = g**-1
            except Exception:
                g_inv = ~g
                
            # Verify that conjugation is well-defined for all elements
            for h in H_list:
                _ = g * h * g_inv
                
            # If conjugation is well-defined, it is an inner automorphism of the ambient monoid's unit group,
            # so its restriction to H is an isomorphism onto its image.
            is_iso = True
            neg_q = not is_iso
    except Exception:
        # If g^-1 is undefined or multiplication fails, gHg^-1 cannot be formed,
        # meaning it is not isomorphic to H (the conclusion fails).
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: g is an element of G",
    "¬Q: The conjugate subgroup gHg^{-1} is not isomorphic to H"
]

N_HYP = 2
NEG_Q_INDEX = 2