import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    G = None
    p = None
    q = None
    
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 1:
                G = witness[0]
            if len(witness) == 3:
                p = witness[1]
                q = witness[2]
        else:
            G = witness

        if p is not None and q is not None:
            try:
                h1 = bool(isprime(p) and isprime(q) and p != q)
            except Exception:
                h1 = False
            try:
                h2 = bool(G.order() == p**2 * q)
            except Exception:
                h2 = False
        else:
            try:
                order = G.order()
                factors = factorint(order)
                if len(factors) == 2:
                    p1, e1 = list(factors.items())[0]
                    p2, e2 = list(factors.items())[1]
                    if (e1 == 2 and e2 == 1) or (e1 == 1 and e2 == 2):
                        h1 = True
                        h2 = True
            except Exception:
                pass
    except Exception:
        pass

    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: The order of G is exactly p^2*q",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2