import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from itertools import permutations

# Top-level setup
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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]
        
    # Remove duplicates from G to ensure it's a set of unique elements
    try:
        unique_G = []
        for g in G:
            if not any(g == ug for ug in unique_G):
                unique_G.append(g)
        G = unique_G
    except Exception:
        return [False, False, False]

    # H1: x and y are elements of G
    try:
        h1 = any(x == g for g in G) and any(y == g for g in G)
    except Exception:
        h1 = False

    # H2: x and y are conjugate in G
    # In a general semigroup, x and y are conjugate if there exist u, v in G 
    # such that x = uv and y = vu. This generalizes group conjugation (y = g x g^-1).
    try:
        h2 = False
        for u in G:
            for v in G:
                if (u * v == x and v * u == y) or (u * v == y and v * u == x):
                    h2 = True
                    break
            if h2:
                break
    except Exception:
        h2 = False

    # neg_Q: C_G(x) is not isomorphic to C_G(y)
    try:
        C_x = []
        for g in G:
            if g * x == x * g:
                C_x.append(g)
                
        C_y = []
        for g in G:
            if g * y == y * g:
                C_y.append(g)
                
        if len(C_x) != len(C_y):
            neg_q = True
        else:
            isomorphic = False
            if len(C_x) == 0:
                isomorphic = True
            else:
                # Check all possible bijections between C_x and C_y
                for p in permutations(C_y):
                    is_homo = True
                    for i, a in enumerate(C_x):
                        for j, b in enumerate(C_x):
                            ab = a * b
                            ab_idx = -1
                            for k, c in enumerate(C_x):
                                if ab == c:
                                    ab_idx = k
                                    break
                            
                            pa_pb = p[i] * p[j]
                            pa_pb_idx = -1
                            for k, c in enumerate(C_y):
                                if pa_pb == c:
                                    pa_pb_idx = k
                                    break
                            
                            # If the multiplication result's presence or index in the centralizer differs,
                            # then this bijection is not a valid magma isomorphism.
                            if ab_idx != pa_pb_idx:
                                is_homo = False
                                break
                        if not is_homo:
                            break
                    if is_homo:
                        isomorphic = True
                        break
            neg_q = not isomorphic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "¬Q: C_G(x) is not isomorphic to C_G(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2