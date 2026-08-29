import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, p), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]

    # H_1: p is the smallest prime number dividing the order of G
    try:
        order_G = G.order()
        primes = sympy.primefactors(order_G)
        h1_ok = (len(primes) > 0) and (p == min(primes)) and sympy.isprime(p)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G of index p
    try:
        is_subgroup = H.is_subgroup(G)
        index = G.order() / H.order()
        h2_ok = is_subgroup and (index == p)
    except Exception:
        h2_ok = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        neg_q_ok = not H.is_normal(G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is the smallest prime number dividing the order of G",
    "H_2: H is a subgroup of G of index p",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2