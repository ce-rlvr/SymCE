import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
    G, p, q = None, None, None
    if isinstance(witness, dict):
        G = witness.get('G', witness)
        p = witness.get('p', 2)
        q = witness.get('q', 3)
    elif isinstance(witness, (tuple, list)):
        G = witness[0] if len(witness) > 0 else witness
        p = witness[1] if len(witness) > 1 else 2
        q = witness[2] if len(witness) > 2 else 3
    else:
        G = witness
        p = 2
        q = 3

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are prime numbers
    try:
        h2 = bool(isprime(p) and isprime(q))
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are prime numbers",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2