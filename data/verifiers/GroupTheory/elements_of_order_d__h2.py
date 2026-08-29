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
        G, d = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            is_cyc = G.is_cyclic
            if callable(is_cyc):
                is_cyc = is_cyc()
            h1 = bool(is_cyc)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(d, (int, sympy.Integer)):
            h2 = False
        elif d == 0:
            h2 = False
        else:
            n = G.order
            if callable(n):
                n = n()
            h2 = (n % d == 0)
    except Exception:
        h2 = False
        
    try:
        if not isinstance(d, (int, sympy.Integer)):
            neg_q = False
        else:
            if hasattr(G, 'elements'):
                elements = G.elements
                if callable(elements):
                    elements = elements()
            else:
                elements = list(G.generate())
                
            count = 0
            for g in elements:
                o = g.order
                if callable(o):
                    o = o()
                if o == d:
                    count += 1
                    
            try:
                phi_d = totient(d)
                neg_q = bool(count != phi_d)
            except ValueError:
                # totient is undefined for d < 1, so the conclusion fails
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: d divides the order of G",
    "¬Q: The number of elements of order d in G is not equal to phi(d)"
]

N_HYP = 2
NEG_Q_INDEX = 2