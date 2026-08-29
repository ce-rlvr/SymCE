import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            p, q, G = witness
        else:
            G = witness
            order = G.order() if callable(G.order) else G.order
            factors = sympy.factorint(order)
            primes = sorted(factors.keys())
            if len(primes) == 2 and factors[primes[0]] == 1 and factors[primes[1]] == 1:
                p, q = primes[0], primes[1]
            else:
                p, q = 0, 0
    except Exception:
        return [False, False, False, False]

    # H_1: p and q are prime numbers
    try:
        h1 = sympy.isprime(p) and sympy.isprime(q)
    except Exception:
        h1 = False

    # H_2: p < q
    try:
        h2 = p < q
    except Exception:
        h2 = False

    # H_3: G is a group of order pq
    try:
        order = G.order() if callable(G.order) else G.order
        h3 = (order == p * q)
    except Exception:
        h3 = False

    # neg_Q: G is not a cyclic group
    try:
        is_cyclic = G.is_cyclic() if callable(G.is_cyclic) else G.is_cyclic
        neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: p < q",
    "H_3: G is a group of order pq",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3