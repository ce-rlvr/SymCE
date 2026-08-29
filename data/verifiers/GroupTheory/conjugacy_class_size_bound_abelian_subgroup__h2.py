import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, A, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x is an element of A
    try:
        h2 = x in A
    except Exception:
        h2 = False
        
    # ¬Q: The size of the conjugacy class of x in G is strictly greater than the index of A in G
    try:
        # A must be a subgroup of G for the index to be well-defined
        if not all(g in G for g in A.generators):
            neg_q = False
        else:
            conj_class = set()
            for g in G.generate():
                conj_class.add(g * x * ~g)
            conj_size = len(conj_class)
            
            index = G.order() / A.order()
            neg_q = bool(conj_size > index)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of A",
    "¬Q: The size of the conjugacy class of x in G is strictly greater than the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2