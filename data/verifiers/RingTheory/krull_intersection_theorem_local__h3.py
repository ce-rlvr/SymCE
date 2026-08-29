import sympy
import math
import itertools
import functools

# Setup block
# The witness should ideally be a tuple (R, m) where R is a ring and m is an ideal.
# The following classes are provided to help construct a mathematically rigorous counterexample.

class Z_Ring:
    """The ring of integers."""
    is_commutative = True
    has_identity = True
    is_Noetherian = True

class Z_Ideal:
    """An ideal in the ring of integers."""
    def __init__(self, generator):
        self.generator = generator
    
    def intersection_powers_zero(self):
        # In Z, the intersection of I^n is {0} unless I = Z (generator 1 or -1)
        return self.generator not in (1, -1)

class ProductRing:
    """The product of two rings."""
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.is_commutative = R1.is_commutative and R2.is_commutative
        self.has_identity = R1.has_identity and R2.has_identity
        self.is_Noetherian = R1.is_Noetherian and R2.is_Noetherian

class ProductIdeal:
    """An ideal in a product ring."""
    def __init__(self, I1, I2):
        self.I1 = I1
        self.I2 = I2
    
    def intersection_powers_zero(self):
        # The intersection of powers in a product ring is zero iff it is zero in both components
        return self.I1.intersection_powers_zero() and self.I2.intersection_powers_zero()

def get_attr_or_key(obj, key, default=False):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def conditions(witness) -> list[bool]:
    try:
        # Unpack witness
        if isinstance(witness, tuple) and len(witness) == 2:
            R, m = witness
        else:
            R = witness
            m = get_attr_or_key(witness, 'm', witness)

        # H_1: R is a commutative ring with identity
        is_comm = get_attr_or_key(R, 'is_commutative', False)
        has_id = get_attr_or_key(R, 'has_identity', False)
        h1 = bool(is_comm and has_id)
        
        # H_2: R is a Noetherian ring
        h2 = bool(get_attr_or_key(R, 'is_Noetherian', False))

        # ¬Q: The intersection of m^n is not {0}
        int_zero_attr = get_attr_or_key(m, 'intersection_powers_zero', True)
        if callable(int_zero_attr):
            int_zero = int_zero_attr()
        else:
            int_zero = int_zero_attr

        neg_q = not bool(int_zero)

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: The intersection of m^n is not {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2