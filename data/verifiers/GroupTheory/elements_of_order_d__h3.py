import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import totient

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, d = witness
    except Exception:
        return [False, False, False]
        
    try:
        is_cyc = getattr(G, 'is_cyclic', False)
        if callable(is_cyc):
            is_cyc = is_cyc()
        h1 = isinstance(G, PermutationGroup) and bool(is_cyc)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(d, (int, sympy.Integer)) and d > 0
    except Exception:
        h2 = False
        
    try:
        count = 0
        for g in G.generate():
            o = g.order() if callable(g.order) else g.order
            if o == d:
                count += 1
        neg_q = count != totient(d)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: d is a positive integer",
    "¬Q: G does not contain exactly phi(d) elements of order d"
]

N_HYP = 2
NEG_Q_INDEX = 2