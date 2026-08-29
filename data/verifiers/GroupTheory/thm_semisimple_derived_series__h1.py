import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        G, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1_ok = bool((isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0)
    except Exception:
        h1_ok = False
        
    try:
        H = G
        for _ in range(n):
            next_H = H.derived_subgroup()
            if next_H.order() == H.order():
                break
            H = next_H
        neg_q_ok = bool(H.order() != G.order())
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 0",
    "¬Q: The n-th derived subgroup G^{(n)} is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1