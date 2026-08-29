import sympy
from sympy import ZZ, QQ
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    # Extract R, K, M from the witness.
    # If the witness is just the module M, we implicitly assume R = ZZ and K = QQ.
    if isinstance(witness, tuple) and len(witness) == 3:
        R, K, M = witness
    else:
        R, K, M = ZZ, QQ, witness

    # H_1: R is an integral domain
    try:
        h1 = bool(getattr(R, 'is_domain', False))
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        h2 = bool(K == R.get_field())
    except Exception:
        h2 = False

    # ¬Q: The canonical R-module homomorphism from M to M \otimes_R K is not injective.
    # For R = ZZ and K = QQ, the map is injective iff M is torsion-free.
    # Thus, the map is NOT injective iff M has torsion.
    try:
        neg_q = False
        if R == ZZ and K == QQ:
            if hasattr(M, 'is_abelian') and M.is_abelian:
                # Finite abelian group has torsion iff it is non-trivial
                neg_q = bool(M.order() > 1)
            elif isinstance(M, (list, tuple)):
                # List of invariant factors (e.g., [0] for Z, [2] for Z/2Z)
                neg_q = any(x != 0 and x != 1 and x != -1 for x in M)
            elif isinstance(M, int):
                # Single invariant factor
                neg_q = (M != 0 and M != 1 and M != -1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "¬Q: The canonical R-module homomorphism from M to M \\otimes_R K is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2