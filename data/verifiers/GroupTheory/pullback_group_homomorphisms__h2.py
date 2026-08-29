import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G_1, G_2, and H are groups",
    "H_2: f_2: G_2 -> H is a group homomorphism",
    "¬Q: The set {(x, y) in G_1 x G_2 | f_1(x) = f_2(y)} is not a subgroup of G_1 x G_2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G1, G2, H, f1, f2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G_1, G_2, and H are groups (and f1, f2 are well-defined maps to H)
    try:
        h1 = False
        if hasattr(G1, 'elements') and hasattr(G2, 'elements') and hasattr(H, 'elements'):
            h1 = True
            # Check if f1 maps G1 to H
            for g in G1.elements:
                val = f1(g) if callable(f1) else f1[g]
                if val not in H.elements:
                    h1 = False
                    break
            # Check if f2 maps G2 to H
            if h1:
                for g in G2.elements:
                    val = f2(g) if callable(f2) else f2[g]
                    if val not in H.elements:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: f_2 is a group homomorphism
    try:
        h2 = False
        if h1:
            h2 = True
            for x in G2.elements:
                for y in G2.elements:
                    val_x = f2(x) if callable(f2) else f2[x]
                    val_y = f2(y) if callable(f2) else f2[y]
                    val_xy = f2(x * y) if callable(f2) else f2[x * y]
                    if val_xy != val_x * val_y:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The set P is NOT a subgroup of G_1 x G_2
    try:
        neg_q = False
        if h1:
            P = []
            for x in G1.elements:
                for y in G2.elements:
                    val_x = f1(x) if callable(f1) else f1[x]
                    val_y = f2(y) if callable(f2) else f2[y]
                    if val_x == val_y:
                        P.append((x, y))
            
            is_subgroup = True
            if not P:
                is_subgroup = False
            else:
                e1 = G1.identity if hasattr(G1, 'identity') else list(G1.elements)[0]**0
                e2 = G2.identity if hasattr(G2, 'identity') else list(G2.elements)[0]**0
                if (e1, e2) not in P:
                    is_subgroup = False
                else:
                    # Check closure under group operation
                    for (x1, y1) in P:
                        for (x2, y2) in P:
                            if (x1 * x2, y1 * y2) not in P:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                    # Check closure under inverses
                    if is_subgroup:
                        for (x, y) in P:
                            if (x**-1, y**-1) not in P:
                                is_subgroup = False
                                break
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]