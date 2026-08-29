import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Top-level setup
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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring_with_identity', False))
            h2 = bool(witness.get('S_is_multiplicatively_closed', False))
            neg_q = not bool(witness.get('localized_is_noetherian', True))
        elif isinstance(witness, str):
            s = witness.lower()
            if ("infinit" in s and "poly" in s) or ("non-noetherian" in s) or ("not noetherian" in s):
                h1 = True
                h2 = True
                neg_q = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
            if isinstance(R, str):
                s = R.lower()
                if ("infinit" in s and "poly" in s) or ("non-noetherian" in s) or ("not noetherian" in s):
                    h1 = True
                    h2 = True
                    neg_q = True
            elif isinstance(R, dict):
                h1 = bool(R.get('is_commutative_ring_with_identity', False))
                h2 = True  # Assuming S is valid if provided in tuple
                neg_q = not bool(R.get('localized_is_noetherian', True))
        else:
            h1 = bool(getattr(witness, 'is_commutative_ring_with_identity', False))
            h2 = bool(getattr(witness, 'S_is_multiplicatively_closed', False))
            neg_q = not bool(getattr(witness, 'localized_is_noetherian', True))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2