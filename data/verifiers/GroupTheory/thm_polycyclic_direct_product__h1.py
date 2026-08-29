import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a polycyclic group
    # For finite groups, polycyclic is equivalent to solvable.
    try:
        if hasattr(H, 'is_polycyclic'):
            h1 = bool(H.is_polycyclic)
        else:
            h1 = bool(H.is_solvable)
    except Exception:
        h1 = False
        
    # neg_Q: G x H is NOT a polycyclic group
    try:
        gens = []
        degG = G.degree
        degH = H.degree
        
        # Embed G into the first degG points
        for g in G.generators:
            arr = list(g.array_form)
            if len(arr) < degG:
                arr += list(range(len(arr), degG))
            arr += list(range(degG, degG + degH))
            gens.append(Permutation(arr))
            
        # Embed H into the next degH points
        for h in H.generators:
            arr = list(range(degG))
            h_arr = list(h.array_form)
            if len(h_arr) < degH:
                h_arr += list(range(len(h_arr), degH))
            arr += [x + degG for x in h_arr]
            gens.append(Permutation(arr))
            
        if not gens:
            size = max(1, degG + degH)
            gens.append(Permutation(size - 1))
            
        GxH = PermutationGroup(gens)
        
        if hasattr(GxH, 'is_polycyclic'):
            neg_q = not bool(GxH.is_polycyclic)
        else:
            neg_q = not bool(GxH.is_solvable)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a polycyclic group",
    "¬Q: G x H is not a polycyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1
