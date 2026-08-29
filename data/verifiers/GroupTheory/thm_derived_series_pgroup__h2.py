import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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
    # The witness can be a tuple (G, p) or just a group G.
    # If just G is provided, we default p to 2 to satisfy the hypothesis.
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = 2
    except Exception:
        G = witness
        p = 2

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # ¬Q: The derived series of G does NOT terminate in the trivial subgroup.
    # This is equivalent to saying G is NOT a solvable group.
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The derived series of G does not terminate (G is not solvable)"
]

N_HYP = 1
NEG_Q_INDEX = 1