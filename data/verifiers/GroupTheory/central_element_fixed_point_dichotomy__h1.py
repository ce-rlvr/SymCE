import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: g is an element in the center of G, Z(G)",
    "¬Q: g fixes some points in X but not all points in X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                G, g = witness
                X = None
            elif len(witness) == 3:
                G, X, g = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not isinstance(g, Permutation):
            h1 = False
        elif g not in G:
            h1 = False
        else:
            h1 = all(g * h == h * g for h in G.generators)
    except Exception:
        h1 = False

    try:
        if X is None:
            if hasattr(G, 'degree'):
                X = list(range(G.degree))
            else:
                X = []
        else:
            X = list(X)
            
        def apply_perm(p, i):
            if isinstance(i, int) and i >= 0:
                if i < p.size:
                    return p(i)
                return i
            return i
            
        if len(X) == 0:
            neg_q = False
        else:
            fixed_count = sum(1 for x in X if apply_perm(g, x) == x)
            neg_q = (0 < fixed_count < len(X))
    except Exception:
        neg_q = False

    return [h1, neg_q]