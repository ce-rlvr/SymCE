import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G is a simple group
    try:
        if not h1_ok:
            h2_ok = False
        else:
            # A group is simple if its only normal subgroups are the trivial group and itself.
            # SymPy's normal_subgroups() returns a list of all normal subgroups.
            ns = list(witness.normal_subgroups())
            h2_ok = (len(ns) == 2)
    except Exception:
        h2_ok = False

    # ¬Q: G is not a cyclic group of prime order
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # A finite group is cyclic of prime order if and only if its order is prime.
            neg_q_ok = not isprime(witness.order())
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a simple group",
    "¬Q: G is not a cyclic group of prime order"
]

N_HYP = 2
NEG_Q_INDEX = 2