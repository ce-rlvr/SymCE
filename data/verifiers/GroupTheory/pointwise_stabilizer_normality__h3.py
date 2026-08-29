import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def get_setwise_stabilizer(G, Y_set):
    if G.order() > 50000:
        raise ValueError("Group too large for naive setwise stabilizer computation")
    elements = []
    for g in G.generate():
        if {g(y) for y in Y_set} == Y_set:
            elements.append(g)
    return PermutationGroup(elements)

def get_pointwise_stabilizer(G, Y_set):
    H = G
    for y in Y_set:
        H = H.stabilizer(y)
    return H

def conditions(witness):
    try:
        if len(witness) == 2:
            G, Y = witness
        elif len(witness) == 3:
            G, X, Y = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        Y_set = set(Y)
        h2 = all(isinstance(y, int) and 0 <= y < G.degree for y in Y_set)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_Y = get_setwise_stabilizer(G, Y_set)
            G_pY = get_pointwise_stabilizer(G, Y_set)
            
            is_normal_subgroup = True
            
            # Check if G_pY is a subgroup of G_Y
            for h in G_pY.generators:
                if not G_Y.contains(h):
                    is_normal_subgroup = False
                    break
            
            if is_normal_subgroup:
                # Check normality: for all h in G_pY and k in G_Y, k*h*k^-1 must be in G_pY
                for h in G_pY.generators:
                    for k in G_Y.generators:
                        if not G_pY.contains(k * h * ~k):
                            is_normal_subgroup = False
                            break
                        if not G_pY.contains(~k * h * k):
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
            
            neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a set X",
    "H_2: Y is a subset of X",
    "¬Q: The pointwise stabilizer G_{(Y)} is not a normal subgroup of the setwise stabilizer G_{Y}"
]

N_HYP = 2
NEG_Q_INDEX = 2