import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, y = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(y in G)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            lcs = G.lower_central_series()
            c = len(lcs) - 1
            if c < 0:
                c = 0
            
            def commutator(a, b):
                return (~a) * (~b) * a * b
            
            neg_q = False
            for x in G.elements:
                val = x
                for _ in range(c):
                    val = commutator(val, y)
                if not val.is_Identity:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group of nilpotency class c",
    "H_2: y is an element of G",
    "¬Q: The c-fold left-normed commutator is not always the identity"
]

N_HYP = 2
NEG_Q_INDEX = 2