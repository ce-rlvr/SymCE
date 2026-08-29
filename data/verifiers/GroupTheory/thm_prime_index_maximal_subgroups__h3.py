import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            M = witness.get('M')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, M = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            if hasattr(M, 'is_subgroup'):
                h1 = bool(M.is_subgroup(G))
            else:
                h1 = all(G.contains(g) for g in M.generators)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        h2_val = getattr(G, 'is_nilpotent', False)
        if callable(h2_val):
            h2_val = h2_val()
        h2 = bool(h2_val)
    except Exception:
        h2 = False
        
    try:
        g_order = G.order() if callable(G.order) else G.order
        m_order = M.order() if callable(M.order) else M.order
        
        if m_order == 0 or g_order % m_order != 0:
            neg_q = False
        else:
            index = g_order // m_order
            neg_q = not isprime(index)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a nilpotent group",
    "neg_Q: The index of M in G is not a prime number"
]

N_HYP = 2
NEG_Q_INDEX = 2