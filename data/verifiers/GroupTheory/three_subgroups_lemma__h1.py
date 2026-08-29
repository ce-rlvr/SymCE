import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: X, Y, and Z are subgroups of G",
    "H_2: The mutual commutator subgroup of X, Y, and Z is the trivial subgroup",
    "H_3: The mutual commutator subgroup of Y, Z, and X is the trivial subgroup",
    "¬Q: The mutual commutator subgroup of Z, X, and Y is NOT the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    def to_group(H):
        if hasattr(H, 'generate'):
            return H
        return PermutationGroup(H)

    def mutual_commutator(A, B):
        A_elems = list(A.generate())
        B_elems = list(B.generate())
        if not A_elems or not B_elems:
            raise ValueError("Empty group")
        
        id_elem = A_elems[0] ** 0
        gens = []
        
        for a in A_elems:
            for b in B_elems:
                c = (a ** -1) * (b ** -1) * a * b
                if c != id_elem:
                    gens.append(c)
                    
        gens = list(set(gens))
        if not gens:
            return PermutationGroup([id_elem])
        return PermutationGroup(gens)

    def is_trivial(H):
        elems = list(H.generate())
        if not elems:
            return True
        id_elem = elems[0] ** 0
        for h in elems:
            if h != id_elem:
                return False
        return True

    X = Y = Z = None

    try:
        if len(witness) == 3:
            X, Y, Z = witness
            X = to_group(X)
            Y = to_group(Y)
            Z = to_group(Z)
            h1_ok = True
        elif len(witness) == 4:
            G, X, Y, Z = witness
            G = to_group(G)
            X = to_group(X)
            Y = to_group(Y)
            Z = to_group(Z)
            G_elems = list(G.generate())
            h1_ok = all(g in G_elems for g in X.generate()) and \
                    all(g in G_elems for g in Y.generate()) and \
                    all(g in G_elems for g in Z.generate())
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        XY = mutual_commutator(X, Y)
        XY_Z = mutual_commutator(XY, Z)
        h2_ok = is_trivial(XY_Z)
    except Exception:
        h2_ok = False

    try:
        YZ = mutual_commutator(Y, Z)
        YZ_X = mutual_commutator(YZ, X)
        h3_ok = is_trivial(YZ_X)
    except Exception:
        h3_ok = False

    try:
        ZX = mutual_commutator(Z, X)
        ZX_Y = mutual_commutator(ZX, Y)
        neg_q_ok = not is_trivial(ZX_Y)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]