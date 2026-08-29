import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

def is_normal_subgroup(G, N):
    for n in N.generators:
        if n not in G:
            return False
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
            if (~g * n * g) not in N:
                return False
    return True

def is_quotient_nilpotent(G, N):
    try:
        lcs = G.lower_central_series()
        stable_term = lcs[-1]
        for g in stable_term.generators:
            if g not in N:
                return False
        return True
    except Exception:
        pass

    current = G
    while True:
        is_sub = True
        for g in current.generators:
            if g not in N:
                is_sub = False
                break
        if is_sub:
            return True
        
        gens = []
        for a in current.generators:
            for b in G.generators:
                gens.append(a * b * ~a * ~b)
        
        if not gens:
            g = G.generators[0] if G.generators else None
            if g is not None:
                gens = [g * ~g]
            else:
                return True
        H = PermutationGroup(gens)
        
        while True:
            new_gens = list(H.generators)
            added = False
            for h in H.generators:
                for g in G.generators:
                    c1 = g * h * ~g
                    if c1 not in H:
                        new_gens.append(c1)
                        added = True
                    c2 = ~g * h * g
                    if c2 not in H:
                        new_gens.append(c2)
                        added = True
            if not added:
                break
            H = PermutationGroup(new_gens)
            
        if H.order() == current.order():
            return False
        current = H

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_normal_subgroup(G, N)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_quotient_nilpotent(G, N)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The quotient group G/N is not nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1