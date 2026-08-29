import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, x = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = x in G.elements
    except Exception:
        h2 = False
        
    try:
        elements = list(G.elements)
        conj_class = set(g * x * ~g for g in elements)
        conj_size = len(conj_class)
        
        centralizer_size = sum(1 for g in elements if g * x == x * g)
        
        # The conclusion is that conj_size == len(elements) / centralizer_size.
        # We check if it fails (neg_Q).
        neg_q = (conj_size * centralizer_size) != len(elements)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2