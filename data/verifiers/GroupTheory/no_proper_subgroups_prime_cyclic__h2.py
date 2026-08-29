import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G has no subgroups other than the trivial subgroup and G itself
    # For finite groups, this is mathematically equivalent to the order being 1 or prime.
    try:
        order = witness.order()
        h2 = bool(order == 1 or isprime(order))
    except Exception:
        h2 = False

    # ¬Q: G is not a finite cyclic group of prime order
    # A finite group is a cyclic group of prime order if and only if its order is prime.
    try:
        order = witness.order()
        neg_q = not isprime(order)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G has no subgroups other than the trivial subgroup and G itself",
    "¬Q: G is not a finite cyclic group of prime order"
]

N_HYP = 2
NEG_Q_INDEX = 2