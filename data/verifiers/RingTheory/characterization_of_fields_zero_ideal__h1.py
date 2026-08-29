import sympy
from sympy import QQ, ZZ, RR
from sympy.ntheory import isprime

# Top-level setup: Define standard counterexamples for rings where {0} is maximal but the ring is not a field.
# These include matrix rings over fields (simple rings) and prime-order rings with zero multiplication.

class MatrixRing:
    """Represents the ring of n x n matrices over a base ring."""
    def __init__(self, n, base_ring):
        self.n = n
        self.base_ring = base_ring

    def is_field(self):
        # M_n(R) is a field iff n=1 and R is a field.
        if self.n == 1:
            return getattr(self.base_ring, 'is_Field', False)
        return False

    def zero_is_maximal_ideal(self):
        # For a matrix ring over a field, the only two-sided ideals are {0} and M_n(F).
        # Thus, {0} is a maximal ideal.
        return getattr(self.base_ring, 'is_Field', False)

class ZeroMultiplicationRing:
    """Represents a commutative ring with zero multiplication (ab = 0 for all a, b)."""
    def __init__(self, order):
        self.order = order

    def is_field(self):
        # A field must have an identity 1 != 0, which is impossible if all products are 0.
        return False

    def zero_is_maximal_ideal(self):
        # Ideals are just additive subgroups. {0} is maximal iff the additive group has prime order.
        return isprime(self.order)

# Named objects for the witness expression to reference
M2_Q = MatrixRing(2, QQ)
M2_R = MatrixRing(2, RR)
M3_Q = MatrixRing(3, QQ)
Z2_zero = ZeroMultiplicationRing(2)
Z3_zero = ZeroMultiplicationRing(3)

def conditions(witness) -> list[bool]:
    try:
        # Resolve string names to objects if necessary
        if isinstance(witness, str):
            witness = globals().get(witness, witness)
            
        # Allow tuple representations like (QQ, 2) for M_2(Q)
        if isinstance(witness, tuple) and len(witness) == 2:
            base, n = witness
            if hasattr(base, 'is_Field') and isinstance(n, int):
                witness = MatrixRing(n, base)

        # Evaluate whether the ring is a field
        if hasattr(witness, 'is_field'):
            field_status = bool(witness.is_field() if callable(witness.is_field) else witness.is_field)
        elif hasattr(witness, 'is_Field'):
            field_status = bool(witness.is_Field)
        else:
            field_status = False

        # Evaluate whether {0} is a maximal ideal
        if hasattr(witness, 'zero_is_maximal_ideal'):
            zero_max_status = bool(witness.zero_is_maximal_ideal() if callable(witness.zero_is_maximal_ideal) else witness.zero_is_maximal_ideal)
        else:
            # Fallback for standard SymPy domains
            if field_status:
                zero_max_status = True
            elif witness == ZZ:
                zero_max_status = False
            else:
                zero_max_status = False

        # The conclusion is: R is a field iff {0} is a maximal ideal.
        # We want the negation of this conclusion.
        iff_holds = (field_status == zero_max_status)
        neg_q = not iff_holds

    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not true that R is a field iff {0} is a maximal ideal"
]

N_HYP = 0
NEG_Q_INDEX = 0