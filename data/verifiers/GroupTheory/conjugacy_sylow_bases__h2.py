import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
        G, B1, B2 = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a finite solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False
        
    # ¬Q: B_1 and B_2 are NOT conjugate in G
    try:
        def get_rep(x):
            if hasattr(x, 'elements'):
                return frozenset(x.elements)
            elif isinstance(x, (list, tuple, set)):
                return frozenset(get_rep(y) for y in x)
            return x

        def conj(x, g):
            if hasattr(x, 'elements'):
                return frozenset((g * y * ~g) for y in x.elements)
            elif isinstance(x, (list, tuple, set)):
                return frozenset(conj(y, g) for y in x)
            return g * x * ~g

        rep2 = get_rep(B2)
        are_conj = False
        for g in G.elements:
            if conj(B1, g) == rep2:
                are_conj = True
                break
        
        neg_q = not are_conj
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "¬Q: B_1 and B_2 are not conjugate in G"
]

N_HYP = 1
NEG_Q_INDEX = 1