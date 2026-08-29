import sympy
from sympy.combinatorics import PermutationGroup
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        p, q, G = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        p_val = int(p)
        q_val = int(q)
        h1 = (p_val == p) and (q_val == q) and (p_val < q_val)
    except Exception:
        h1 = False
        
    try:
        p_val = int(p)
        q_val = int(q)
        h2 = isinstance(G, PermutationGroup) and G.order() == p_val * q_val
    except Exception:
        h2 = False
        
    try:
        p_val = int(p)
        q_val = int(q)
        h3 = (p_val == p) and (q_val == q) and (p_val != 0) and ((q_val - 1) % p_val != 0)
    except Exception:
        h3 = False
        
    try:
        if hasattr(G, 'is_cyclic'):
            if callable(G.is_cyclic):
                is_cyc = bool(G.is_cyclic())
            else:
                is_cyc = bool(G.is_cyclic)
        else:
            order = G.order()
            is_cyc = False
            for g in G.elements:
                if g.order() == order:
                    is_cyc = True
                    break
        neg_q = not is_cyc
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p < q",
    "H_2: G is a group of order pq",
    "H_3: p does not divide q - 1",
    "¬Q: G is not cyclic"
]

N_HYP = 3
NEG_Q_INDEX = 3