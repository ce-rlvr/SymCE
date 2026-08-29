import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

A5 = AlternatingGroup(5)
S5 = SymmetricGroup(5)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 4:
                G, p, q, r = witness
            elif len(witness) >= 1:
                G = witness[0]
                p, q, r = 2, 3, 5
            else:
                G = None
                p, q, r = 2, 3, 5
        elif isinstance(witness, dict):
            G = witness.get('G', witness)
            p = witness.get('p', 2)
            q = witness.get('q', 3)
            r = witness.get('r', 5)
        else:
            G = witness
            p, q, r = 2, 3, 5
    except Exception:
        G = witness
        p, q, r = 2, 3, 5

    try:
        h1_ok = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isprime(p) and isprime(q) and isprime(r) and len({p, q, r}) == 3)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p, q, and r are distinct prime numbers",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2