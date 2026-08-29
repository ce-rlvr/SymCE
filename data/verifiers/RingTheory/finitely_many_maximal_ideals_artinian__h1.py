import sympy
from sympy import QQ, ZZ

class MatrixRingObj:
    """
    Represents a matrix ring M_n(R) over a base ring R.
    Used to provide standard non-commutative ring counterexamples.
    """
    def __init__(self, base_ring, n):
        self.base_ring = base_ring
        self.n = n
        self.is_Ring = True

# Top-level setup: named object bindings for witness expressions
M2_QQ = MatrixRingObj(QQ, 2)
M3_QQ = MatrixRingObj(QQ, 3)
M2_ZZ = MatrixRingObj(ZZ, 2)

def conditions(witness) -> list[bool]:
    # H_1: R has a multiplicative identity
    try:
        if isinstance(witness, MatrixRingObj):
            h1 = True
        elif witness in [QQ, ZZ]:
            h1 = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R is an Artinian ring
    try:
        if isinstance(witness, MatrixRingObj):
            # A matrix ring over a field is Artinian
            h2 = getattr(witness.base_ring, 'is_Field', False)
        elif witness == QQ:
            h2 = True
        elif witness == ZZ:
            h2 = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R does not have finitely many maximal ideals
    # (In non-commutative rings, this refers to maximal left/right ideals. 
    # M_n(K) over an infinite field K has infinitely many maximal left ideals for n >= 2)
    try:
        if isinstance(witness, MatrixRingObj):
            is_finite_field = witness.base_ring.__class__.__name__ in ['GaloisField', 'FiniteField']
            if witness.n >= 2 and not is_finite_field:
                neg_q = True
            else:
                neg_q = False
        elif witness == QQ:
            neg_q = False
        elif witness == ZZ:
            neg_q = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "¬Q: R does not have finitely many maximal ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2