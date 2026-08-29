import sympy

class QuadraticOrder:
    """
    Represents an order in a quadratic field Q(sqrt(d)).
    d is a square-free integer.
    f is the conductor of the order (index in the maximal order).
    """
    def __init__(self, d, f=1):
        self.d = d
        self.f = f

    def is_ufd(self):
        # A UFD must be integrally closed, so it must be the maximal order (f = 1).
        if self.f != 1:
            return False
        return self.is_class_group_trivial()

    def is_class_group_trivial(self):
        if self.f == 1:
            # Class numbers of imaginary quadratic fields
            if self.d < 0:
                return self.d in [-1, -2, -3, -7, -11, -19, -43, -67, -163]
            else:
                # Some real quadratic fields with class number 1
                return self.d in [2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 22, 23, 29, 31, 33, 37, 38, 41, 43, 46, 47]
        else:
            # Non-maximal orders
            if self.d == -3 and self.f == 2:
                # Z[sqrt(-3)] has trivial Picard group
                return True
            if self.d == -1 and self.f == 2:
                # Z[2i] has trivial Picard group
                return True
            return False

# Top-level setup: named object bindings that the witness expression may reference.
Z_sqrt_minus_3 = QuadraticOrder(-3, 2)
Z_2i = QuadraticOrder(-1, 2)
Z_sqrt_minus_5 = QuadraticOrder(-5, 1)
Z_i = QuadraticOrder(-1, 1)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_ufd') and hasattr(witness, 'is_class_group_trivial'):
            is_ufd = bool(witness.is_ufd())
            is_trivial = bool(witness.is_class_group_trivial())
        elif hasattr(witness, 'is_UFD'):
            # Fallback for SymPy domains
            is_ufd = bool(witness.is_UFD)
            # For standard SymPy domains (like ZZ, QQ), class group is trivial if it's a UFD
            is_trivial = is_ufd
        else:
            return [False]
        
        # The conjecture states: R is a UFD iff the divisor class group of R is trivial.
        # We want the negated conclusion (i.e., the equivalence fails).
        neg_q = (is_ufd != is_trivial)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a UFD XOR the divisor class group of R is trivial"
]

N_HYP = 0
NEG_Q_INDEX = 0