import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        p, q, G = witness
    except Exception:
        return [False] * 5

    try:
        h1 = isprime(p) and isprime(q)
    except Exception:
        h1 = False

    try:
        h2 = p > q
    except Exception:
        h2 = False

    try:
        h3 = (p - 1) % q == 0
    except Exception:
        h3 = False

    try:
        h4 = hasattr(G, 'order') and G.order() == p * q
    except Exception:
        h4 = False

    try:
        # The Sylow p-subgroup has order p.
        # Since p > q, the Sylow p-subgroup is always unique.
        # Thus, G' is the unique Sylow p-subgroup iff its order is p.
        # The negated conclusion is that G' is NOT the unique Sylow p-subgroup.
        G_prime = G.derived_subgroup()
        neg_q = G_prime.order() != p
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: p > q",
    "H_3: q divides p - 1",
    "H_4: G is a group of order pq",
    "¬Q: G' is not the unique Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4