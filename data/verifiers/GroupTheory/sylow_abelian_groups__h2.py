import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_order(G):
    order = G.order
    if callable(order):
        return order()
    return order

def conditions(witness):
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a finite abelian group
    try:
        h1 = bool(G.is_abelian)
        order = get_order(G)
        if order == 0 or order == float('inf'):
            h1 = False
    except Exception:
        h1 = False
        
    # H2: p divides the order of G
    try:
        order = get_order(G)
        h2 = (order % p == 0)
    except Exception:
        h2 = False
        
    # neg_Q: G does NOT have exactly one Sylow p-subgroup
    try:
        if not sympy.isprime(p):
            q = False
        else:
            S = G.sylow_subgroup(p)
            q = True
            for g in G.generators:
                for s in S.generators:
                    if (g * s * g**-1) not in S:
                        q = False
                        break
                if not q:
                    break
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: p divides the order of G",
    "¬Q: G does not have exactly one Sylow p-subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2