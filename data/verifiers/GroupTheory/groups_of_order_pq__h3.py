import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            ints = [x for x in witness if isinstance(x, (int, sympy.Integer))]
            non_ints = [x for x in witness if not isinstance(x, (int, sympy.Integer))]
            if len(ints) == 2 and len(non_ints) == 1:
                p, q = ints[0], ints[1]
                G = non_ints[0]
            else:
                G, p, q = witness
        else:
            G, p, q = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p) and isprime(q) and p < q)
    except Exception:
        h1 = False

    try:
        h2 = bool((q - 1) % p == 0)
    except Exception:
        h2 = False

    try:
        if hasattr(G, 'order') and callable(G.order):
            order = G.order()
        else:
            order = None
            
        if order != p * q:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers such that p < q",
    "H_2: p divides q-1",
    r"¬Q: G is not isomorphic to a semidirect product Z_q \rtimes Z_p, or there is not exactly one non-abelian isomorphism class"
]

N_HYP = 2
NEG_Q_INDEX = 2