import sympy
import math
import itertools
import functools

class MockRingModule:
    """
    Mock object to represent a ring-module pair (R, M) since SymPy lacks 
    native support for arbitrary modules and associated primes.
    """
    def __init__(self, is_commutative_ring, is_finitely_generated_module, is_zero_module, has_associated_primes):
        self.is_commutative_ring = is_commutative_ring
        self.is_finitely_generated_module = is_finitely_generated_module
        self.is_zero_module = is_zero_module
        self.has_associated_primes = has_associated_primes

# Named objects for the witness expression to reference
# Z_Z represents R=Z, M=Z (Noetherian, has associated primes)
Z_Z = MockRingModule(True, True, False, True)

# C_01_C_01 represents R=C([0,1]), M=C([0,1]) (Non-Noetherian, no associated primes)
C_01_C_01 = MockRingModule(True, True, False, False) 

# Z_0 represents R=Z, M=0 (Zero module)
Z_0 = MockRingModule(True, True, True, False)

def conditions(witness) -> list[bool]:
    def get_prop(name, default):
        if isinstance(witness, dict):
            return witness.get(name, default)
        return getattr(witness, name, default)

    try:
        h1 = bool(get_prop("is_commutative_ring", False))
    except Exception:
        h1 = False

    try:
        h2 = bool(get_prop("is_finitely_generated_module", False))
    except Exception:
        h2 = False

    try:
        h3 = not bool(get_prop("is_zero_module", True))
    except Exception:
        h3 = False

    try:
        neg_q = not bool(get_prop("has_associated_primes", True))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a finitely generated R-module",
    "H_3: M is not the zero module",
    "¬Q: Ass_R(M) is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3