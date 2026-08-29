import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (p, q, G) or just the group G.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            p, q, G = witness
        else:
            G = witness
            order = G.order() if callable(G.order) else G.order
            factors = factorint(order)
            keys = sorted(factors.keys())
            if len(keys) == 2 and factors[keys[0]] == 1 and factors[keys[1]] == 1:
                p, q = keys
            else:
                p, q = 0, 0
    except Exception:
        p, q, G = 0, 0, None

    # H_1: p and q are prime numbers such that p < q
    try:
        h1 = bool(isprime(p) and isprime(q) and p < q)
    except Exception:
        h1 = False

    # H_2: G is a group of order pq
    try:
        order = G.order() if callable(G.order) else G.order
        h2 = bool(order == p * q)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # The conclusion states:
    # 1. G is isomorphic to a semidirect product Z_q \rtimes Z_p
    # 2. There is exactly one non-abelian isomorphism class of groups of order pq
    #
    # Part 1 is always true for any group of order pq with p < q (the Sylow q-subgroup is normal).
    # Part 2 is true if and only if p divides q - 1.
    # Therefore, the conclusion holds iff p divides q - 1.
    # The negated conclusion holds iff p does NOT divide q - 1.
    try:
        if p > 0 and q > 0:
            neg_q = bool((q - 1) % p != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers such that p < q",
    "H_2: G is a group of order pq",
    "¬Q: G is not isomorphic to a semidirect product Z_q rtimes Z_p, or there is not exactly one non-abelian isomorphism class of groups of order pq"
]

N_HYP = 2
NEG_Q_INDEX = 2