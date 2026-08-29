import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    G, p = None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p', 2)
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = 2  # Default prime if omitted, as p is disconnected from G in the remaining hypotheses
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        # In sympy, PermutationGroup instances are finite groups
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2