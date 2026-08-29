import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, Y = witness
            elif len(witness) == 3:
                G, X, Y = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Y is a subset of X
    action_type = None
    try:
        if h1:
            degree = G.degree
            if isinstance(Y, (set, list, tuple)):
                # Standard action on the domain points
                if all(isinstance(y, (int, sympy.Integer)) and 0 <= int(y) < degree for y in Y):
                    h2 = True
                    action_type = 'standard'
                # Conjugation action on group elements
                elif all(isinstance(y, Permutation) for y in Y):
                    h2 = True
                    action_type = 'conjugation'
                else:
                    h2 = False
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: G_{(Y)} is the pointwise stabilizer of Y in G
    # This is true by definition as we compute it directly below.
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # Conclusion: The pointwise stabilizer G_{(Y)} is a normal subgroup of the setwise stabilizer G_Y.
    # neg_q is True if it is NOT a normal subgroup.
    neg_q = False
    try:
        if h1 and h2:
            elements = list(G.elements)
            G_Y = []
            G_pY = []
            
            if action_type == 'standard':
                Y_set = set(int(y) for y in Y)
                for g in elements:
                    # Setwise stabilizer condition
                    mapped_Y = {g(y) for y in Y_set}
                    if mapped_Y == Y_set:
                        G_Y.append(g)
                    
                    # Pointwise stabilizer condition
                    if all(g(y) == y for y in Y_set):
                        G_pY.append(g)
                        
            elif action_type == 'conjugation':
                Y_set = set(Y)
                for g in elements:
                    # Setwise stabilizer condition (Normalizer)
                    mapped_Y = {g * y * ~g for y in Y_set}
                    if mapped_Y == Y_set:
                        G_Y.append(g)
                    
                    # Pointwise stabilizer condition (Centralizer)
                    if all(g * y * ~g == y for y in Y_set):
                        G_pY.append(g)
            
            G_pY_set = set(G_pY)
            is_normal = True
            
            # Check normality: for all h in G_{(Y)} and g in G_Y, g * h * g^-1 in G_{(Y)}
            for h in G_pY:
                for g in G_Y:
                    conj = g * h * ~g
                    if conj not in G_pY_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a subset of X",
    "H_3: G_{(Y)} is the pointwise stabilizer of Y in G",
    "¬Q: The pointwise stabilizer G_{(Y)} is NOT a normal subgroup of the setwise stabilizer G_Y"
]

N_HYP = 3
NEG_Q_INDEX = 3