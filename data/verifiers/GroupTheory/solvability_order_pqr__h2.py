import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup,
    AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for the witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # The witness could be just the group G, or a tuple (G, p, q, r)
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            G, p, q, r = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, pqr = witness
            p, q, r = pqr
        else:
            G = witness
            try:
                # If p, q, r are not provided, we can trivially satisfy |G| = p*q*r
                # by setting them to 1, 1, |G| since the "primes" hypothesis was dropped.
                p, q, r = 1, 1, G.order()
            except Exception:
                p, q, r = 1, 1, 1
    except Exception:
        G = witness
        p, q, r = 1, 1, 1

    # H_1: G is a finite group
    try:
        order = G.order()
        h1_ok = isinstance(order, (int, sympy.Integer)) and order > 0 and hasattr(G, 'is_solvable')
    except Exception:
        h1_ok = False

    # H_2: The order of G is pqr
    try:
        h2_ok = (G.order() == p * q * r)
    except Exception:
        h2_ok = False

    # ¬Q: G is not a solvable group (Conclusion fails)
    try:
        solvable = G.is_solvable() if callable(G.is_solvable) else G.is_solvable
        neg_q_ok = not solvable
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is pqr",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2