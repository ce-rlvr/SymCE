import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Define custom ring objects to serve as potential witnesses,
# since SymPy's native domains are all integral domains (hence reduced and Noetherian)
# and cannot easily represent infinite products or non-Noetherian Boolean rings.

class _InfiniteBooleanRing:
    @property
    def is_reduced(self):
        return True
    @property
    def zero_ideal_has_primary_decomposition_of_primes(self):
        return False

class _InfiniteProductOfFields:
    @property
    def is_reduced(self):
        return True
    @property
    def zero_ideal_has_primary_decomposition_of_primes(self):
        return False

class _FiniteBooleanRing:
    @property
    def is_reduced(self):
        return True
    @property
    def zero_ideal_has_primary_decomposition_of_primes(self):
        return True

class _NonReducedRing:
    @property
    def is_reduced(self):
        return False
    @property
    def zero_ideal_has_primary_decomposition_of_primes(self):
        return False

# Bindings for the evaluation namespace
InfiniteBooleanRing = _InfiniteBooleanRing()
InfiniteProductOfFields = _InfiniteProductOfFields()
FiniteBooleanRing = _FiniteBooleanRing()
NonReducedRing = _NonReducedRing()

def _check_prop(obj, prop):
    if not hasattr(obj, prop):
        return None
    val = getattr(obj, prop)
    if callable(val):
        return val()
    return val

def conditions(witness) -> list[bool]:
    # H_1: R is a reduced ring
    try:
        h1_val = _check_prop(witness, 'is_reduced')
        if h1_val is not None:
            h1 = bool(h1_val)
        else:
            # Fallback for SymPy domains (which are integral domains, hence reduced)
            if hasattr(witness, 'is_Domain') and witness.is_Domain:
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # neg_Q: The zero ideal of R does NOT have a primary decomposition consisting entirely of prime ideals
    try:
        q_val = _check_prop(witness, 'zero_ideal_has_primary_decomposition_of_primes')
        if q_val is not None:
            neg_q = not bool(q_val)
        else:
            # Fallback for SymPy domains (integral domains have prime zero ideal, so it has a primary decomp of primes)
            if hasattr(witness, 'is_Domain') and witness.is_Domain:
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "¬Q: The zero ideal of R does not have a primary decomposition consisting entirely of prime ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1