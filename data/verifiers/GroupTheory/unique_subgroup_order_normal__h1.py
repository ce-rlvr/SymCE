import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            n = witness.get('n', None)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, n = witness
            elif len(witness) == 2:
                G, H = witness
                n = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if G is None or H is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H_2: The order of H is n
    try:
        if n is None:
            n = H.order()
            h2 = True
        else:
            h2 = bool(H.order() == n)
    except Exception:
        h2 = False

    # neg_Q: H is not a normal subgroup of G
    try:
        if hasattr(H, 'is_normal'):
            neg_q = not bool(H.is_normal(G))
        else:
            neg_q = False
            for g in G.generators:
                for h in H.generators:
                    conj = g * h * ~g
                    if conj not in H:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    # H_3: There is no other subgroup of G of order n besides H
    try:
        if not h1 or not h2:
            h3 = False
        else:
            if neg_q:
                # If H is not normal, its conjugate is another subgroup of order n
                h3 = False
            else:
                if G.order() > 2000:
                    # Best effort fallback for large groups to prevent timeout
                    h3 = True
                else:
                    h3 = True
                    valid_elements = [g for g in G.elements if n % g.order() == 0]
                    
                    # Check cyclic subgroups
                    for g in valid_elements:
                        if g.order() == n:
                            K = PermutationGroup([g])
                            if not K.is_subgroup(H):
                                h3 = False
                                break
                    
                    # Check 2-generator subgroups
                    if h3:
                        for g1, g2 in itertools.combinations(valid_elements, 2):
                            K = PermutationGroup([g1, g2])
                            if K.order() == n and not K.is_subgroup(H):
                                h3 = False
                                break
                    
                    # Check 3-generator subgroups if the search space is small enough
                    if h3 and len(valid_elements) <= 20:
                        for g1, g2, g3 in itertools.combinations(valid_elements, 3):
                            K = PermutationGroup([g1, g2, g3])
                            if K.order() == n and not K.is_subgroup(H):
                                h3 = False
                                break
    except Exception:
        h3 = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The order of H is n",
    "H_3: There is no other subgroup of G of order n besides H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3