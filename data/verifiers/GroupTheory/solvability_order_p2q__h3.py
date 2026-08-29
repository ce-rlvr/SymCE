import sympy
from sympy.combinatorics import PermutationGroup
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
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            G = witness.get('G')
        elif hasattr(witness, 'p') and hasattr(witness, 'q') and hasattr(witness, 'G'):
            p = witness.p
            q = witness.q
            G = witness.G
        else:
            p, q, G = witness
    except Exception:
        return [False, False, False]

    # H_1: p and q are distinct prime numbers
    try:
        h1_ok = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1_ok = False

    # H_2: G is a finite group
    try:
        h2_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h2_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: G is a finite group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2