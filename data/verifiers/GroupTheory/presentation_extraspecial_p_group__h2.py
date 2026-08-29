import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'is_abelian') and not hasattr(witness[1], 'is_abelian'):
                G, p = witness
            else:
                p, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    try:
        if not hasattr(G, 'order') or not hasattr(G, 'is_abelian'):
            neg_q = True
        else:
            order = G.order
            if callable(order):
                order = order()
                
            is_ab = G.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
                
            if order != p**3:
                neg_q = True
            elif is_ab:
                neg_q = True
            else:
                admits = True
                for g in G.elements:
                    g_order = g.order
                    if callable(g_order):
                        g_order = g_order()
                    if g_order not in (1, p):
                        admits = False
                        break
                neg_q = not admits
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: p is an odd prime", "¬Q: G does not admit the presentation"]

N_HYP = 1
NEG_Q_INDEX = 1