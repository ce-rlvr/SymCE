import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, S = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = hasattr(G, 'elements') and hasattr(G, 'order') and G.order() > 0 and G.order() < float('inf')
    except Exception:
        h1_ok = False

    try:
        S_list = list(S)
        h2_ok = len(S_list) > G.order() / 2
    except Exception:
        h2_ok = False

    try:
        S_list = list(S)
        s_prods = []
        for x in S_list:
            for y in S_list:
                try:
                    s_prods.append(x * y)
                except Exception:
                    pass
        
        neg_q_ok = False
        for g in list(G.elements):
            if g not in s_prods:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The cardinality of S is strictly greater than |G| / 2",
    "¬Q: There exists g in G such that for all x, y in S, g != xy"
]

N_HYP = 2
NEG_Q_INDEX = 2